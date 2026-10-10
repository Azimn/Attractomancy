#!/usr/bin/env python3
"""DCH L2C exploratory representation-capacity study.
Post-L2 prompt redesign, not preregistered or human-dyad evidence."""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from model_runner import backend_instance,parse_response
from integration_v2 import build_cases,records_for_policy,digest,POLICIES

COMPACT_RULE=(
 'Use ONLY the supplied authorized state records. Each record is one key=value at a turn with a source ID. '
 'The latest turn for a key replaces its earlier values. '
 'If any of permission, commitment_status, due_turn, priority is unknown: UNKNOWN. '
 'Otherwise do this in ORDER: permission=revoked => WITHHOLD; '
 'commitment_status=cancelled => DECLINE; current_turn<due_turn => SCHEDULE; '
 'otherwise FULFILL_ followed by uppercase priority. '
 'Return exactly one JSON object: {"answer":"...","source_event_ids":["..."]}. '
 'Cite ids for values used in your decision, never invent ids.')

def make_messages(case,policy,style):
    records=records_for_policy(case['events'],policy)
    archive=[{k:e[k] for k in ('event_id','turn','key','value')} for e in records]
    if style=='compact':
        tab='\n'.join(f"{e['turn']} | {e['event_id']} | {e['key']} = {e['value']}" for e in archive)
        if not tab:tab='(empty archive)'
        body='AUTHORIZED STATE RECORDS:\n'+tab+'\nCURRENT TURN: '+str(case['current_turn'])+'\nDetermine authorized next action.'
        rule=COMPACT_RULE
    elif style=='original':
        from integration_v2 import RULE
        rule=RULE
        body='Authorized archive: '+json.dumps(archive,sort_keys=True,separators=(',',':'))+'\n'+case['prompt']
    else:raise ValueError(style)
    return ([{'role':'system','content':rule},{'role':'user','content':body}],archive)

def run(visible,path,model,backend_kind='mock',count=8,policies=('expert_auto','stale','cold'),styles=('compact','original')):
    if path.exists():raise FileExistsError(path)
    cases=json.loads(visible.read_text(encoding='utf-8'))[:count]
    backend=backend_instance(backend_kind,model,'http://127.0.0.1:11434')
    rows=[]
    for case in cases:
        for style in styles:
            for policy in policies:
                messages,records=make_messages(case,policy,style)
                result=backend.respond(messages)
                parsed=parse_response(result['text'])
                rows.append({'persona_id':case['persona_id'],'style':style,'policy':policy,
                  'prompt_sha256':digest(messages),'archive_sha256':digest(records),
                  'record_count':len(records),'raw_text':result['text'],**parsed,
                  'source_ids_valid':all(x in {e['event_id'] for e in records} for x in parsed['source_event_ids']),
                  'prompt_tokens':result['prompt_tokens'],'output_tokens':result['output_tokens'],
                  'model_reported':result['model_reported'],'done_reason':result['done_reason']})
    data={'status':'REAL_MODEL_DEVELOPMENT' if backend_kind!='mock' else 'MOCK_ONLY',
      'model':model,'backend':backend_kind,'visible_sha256':hashlib.sha256(visible.read_bytes()).hexdigest(),
      'human_partner_present':False,'evidence_for_DCH':False,'rows':rows}
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    return {'rows':len(rows),'status':data['status']}

def action_minimal_ids(case,target):
    ordered=[f"{case}-E09",f"{case}-E10",f"{case}-E11",f"{case}-E12"]
    action=target['expected']
    count=1 if action=='WITHHOLD' else 2 if action=='DECLINE' else 3 if action=='SCHEDULE' else 4
    return ordered[:count]

def evaluate(raw,answers,output):
    obj=json.loads(raw.read_text(encoding='utf-8'))
    expected={x['persona_id']:x for x in json.loads(answers.read_text(encoding='utf-8'))}
    by={}
    for row in obj['rows']:
        target=expected[row['persona_id']]
        necessary=action_minimal_ids(row['persona_id'],target)
        cited=set(row['source_event_ids'])
        k=row['style']+':'+row['policy']
        by.setdefault(k,[]).append({'id':row['persona_id'],'correct':row['parse_valid'] and row['answer']==target['expected'],
            'branch_min_source':row['source_ids_valid'] and set(necessary).issubset(cited),
            'all_four_sources':row['source_ids_valid'] and set(target['necessary_source_ids']).issubset(cited),
            'source_valid':row['source_ids_valid'],'parse_valid':row['parse_valid'],
            'target':target['expected'],'actual':row['answer'],'prompt_tokens':row['prompt_tokens'],'output_tokens':row['output_tokens']})
    summary={k:{'n':len(items),**{name:sum(bool(r[name]) for r in items)/len(items) for name in
      ('correct','branch_min_source','all_four_sources','source_valid','parse_valid')},
      'mean_prompt_tokens':(sum(r['prompt_tokens'] for r in items)/len(items)
         if all(r['prompt_tokens'] is not None for r in items) else None)} for k,items in by.items()}
    controls={}
    for style in ('original','compact'):
        match={}
        for r in obj['rows']:
            if r['style']==style and r['policy'] in ('human_coded','expert_auto'):
                match.setdefault(r['persona_id'],{})[r['policy']]=r
        pair=[x for x in match.values() if len(x)==2]
        controls[style]={'n':len(pair),
                         'inputs_equal':(all(p['human_coded']['prompt_sha256']==p['expert_auto']['prompt_sha256'] for p in pair) if pair else None),
                         'outputs_equal':(all(p['human_coded']['raw_text']==p['expert_auto']['raw_text'] for p in pair) if pair else None)}
    result={'status':'EXPLORATORY_POST_L2_REDESIGN','model':obj['model'],'summary':summary,
            'exact_input_controls':controls,'rows':by,'DCH_claim':'NONE'}
    if output.exists():raise FileExistsError(output)
    output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    return {k:v for k,v in result.items() if k!='rows'}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('mode',choices=('prepare','run','evaluate'))
    p.add_argument('--folder',required=True,type=Path)
    p.add_argument('--model',default='Qwen/Qwen2.5-0.5B-Instruct')
    p.add_argument('--backend',default='mock',choices=('mock','transformers','ollama'))
    p.add_argument('--count',type=int,default=8)
    p.add_argument('--styles',nargs='+',default=['compact','original'],choices=('compact','original'))
    p.add_argument('--policies',nargs='+',default=['expert_auto','stale','cold'],choices=POLICIES)
    args=p.parse_args();d=args.folder
    if args.mode=='prepare':
        from integration_v2 import prepare
        v=prepare(d,12)
    elif args.mode=='run':v=run(d/'dev_visible.json',d/'l2c_raw.json',args.model,args.backend,args.count,args.policies,args.styles)
    else:v=evaluate(d/'l2c_raw.json',d/'dev_EVALUATOR_ONLY.json',d/'l2c_scored.json')
    print(json.dumps(v,indent=2))
if __name__=='__main__':main()
