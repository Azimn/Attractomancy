#!/usr/bin/env python3
"""Development-only DCH four-record integration. No human-dyad evidence."""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from model_runner import backend_instance,parse_response

POLICIES=('expert_auto','human_coded','stale','cold','oracle')
RULE=('Synthetic operational rule: use the latest authorized record for each key. '
'If permission is revoked return WITHHOLD; otherwise, if commitment_status is cancelled '
'return DECLINE; otherwise, if current_turn is before due_turn return SCHEDULE; '
'otherwise return FULFILL_ followed by uppercase current priority. '
'If any required key is missing, return UNKNOWN. '
'Reply as JSON with answer (string) and source_event_ids (list of strings). '
'Cite one valid event for each of permission, commitment_status, due_turn and priority '
'when resolving a non-UNKNOWN action; never invent ids. This is a synthetic task.')

def digest(x):
    return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False).encode()).hexdigest()

def build_cases(count=12):
    if count<8:raise ValueError('At least eight balanced trajectories required')
    cases,answers=[],[]
    for i in range(count):
        pid=f'L2-{i+1:03d}'
        permission='revoked' if i%4==0 else 'allowed'
        status='cancelled' if i%4==1 else 'pending'
        due=20 if i%4 in (0,1,2) else 28
        priority=('accuracy','repair','speed')[i%3]
        now=25
        originals={'permission':'allowed' if permission=='revoked' else 'revoked',
                   'commitment_status':'pending' if status=='cancelled' else 'cancelled',
                   'due_turn':35 if due==20 else 15,
                   'priority':'repair' if priority!='repair' else 'accuracy'}
        current={'permission':permission,'commitment_status':status,'due_turn':due,'priority':priority}
        ev=[]
        for t,(key,val) in enumerate(originals.items(),start=1):
            ev.append({'event_id':f'{pid}-E{t:02d}','turn':t,'key':key,'value':val,'authorized':True})
        for t,(key,val) in enumerate(current.items(),start=9):
            ev.append({'event_id':f'{pid}-E{t:02d}','turn':t,'key':key,'value':val,'authorized':True})
        ev.append({'event_id':f'{pid}-E13','turn':13,'key':'priority',
                   'value':'speed' if priority!='speed' else 'repair','authorized':False})
        expected=('WITHHOLD' if permission=='revoked' else 'DECLINE' if status=='cancelled'
                  else 'SCHEDULE' if now<due else 'FULFILL_'+priority.upper())
        cases.append({'persona_id':pid,'current_turn':now,'events':ev,
                      'prompt':f'At turn {now}, a requester asks the persona to fulfill commitment C-{i+1:03d}. '
                      'Determine the authorized next action using all four current records.'})
        answers.append({'persona_id':pid,'expected':expected,
                        'necessary_source_ids':[f'{pid}-E{t:02d}' for t in range(9,13)],
                        'probe_class':'four_record_integration'})
    return cases,answers

def prepare(folder:Path,count:int=12):
    cases,answers=build_cases(count)
    folder.mkdir(parents=True,exist_ok=True)
    for name,value in [('dev_visible.json',cases),('dev_EVALUATOR_ONLY.json',answers)]:
        (folder/name).write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
    return {'cases':count,'visible_sha256':digest(cases),'answer_sha256':digest(answers)}

def records_for_policy(events,policy):
    allowed=[e for e in events if e['authorized']]
    if policy=='cold':return []
    if policy=='stale':return allowed[:4]
    if policy=='oracle':return allowed
    if policy in ('human_coded','expert_auto'):
        latest={}
        for e in allowed:latest[e['key']]=e
        return sorted(latest.values(),key=lambda x:x['turn'])
    raise ValueError(policy)

def run(visible:Path,out:Path,backend_kind:str,model:str,policies:list[str],max_cases=None):
    if out.exists():raise FileExistsError(out)
    cases=json.loads(visible.read_text(encoding='utf-8'))
    if max_cases is not None:cases=cases[:max_cases]
    backend=backend_instance(backend_kind,model,'http://127.0.0.1:11434')
    rows=[]
    for case in cases:
        for policy in policies:
            if policy not in POLICIES:raise ValueError(policy)
            records=records_for_policy(case['events'],policy)
            archive=[{k:e[k] for k in ('event_id','turn','key','value')} for e in records]
            messages=[{'role':'system','content':RULE},
                      {'role':'user','content':'Authorized archive: '+
                       json.dumps(archive,sort_keys=True,separators=(',',':'))+'\n'+case['prompt']}]
            result=backend.respond(messages)
            parsed=parse_response(result['text'])
            ids={e['event_id'] for e in records}
            rows.append({'persona_id':case['persona_id'],'policy':policy,
                         'prompt_sha256':digest(messages),'archive_sha256':digest(archive),
                         'archive_record_count':len(archive),
                         'prompt_chars':sum(len(m['content']) for m in messages),
                         'raw_text':result['text'],**parsed,
                         'source_ids_valid':all(s in ids for s in parsed['source_event_ids']),
                         'prompt_tokens':result['prompt_tokens'],'output_tokens':result['output_tokens'],
                         'model_reported':result['model_reported'],'done_reason':result['done_reason']})
    payload={'status':'DEVELOPMENT_LLM' if backend_kind!='mock' else 'MOCK_ONLY',
             'backend':backend_kind,'model_requested':model,
             'visible_sha256':hashlib.sha256(visible.read_bytes()).hexdigest(),
             'evidence_for_DCH':False,'human_partner_present':False,'records':rows}
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8')
    return {'responses':len(rows),'status':payload['status']}

def evaluate(raw:Path,answers:Path,out:Path):
    rows=json.loads(raw.read_text(encoding='utf-8'))['records']
    targets={x['persona_id']:x for x in json.loads(answers.read_text(encoding='utf-8'))}
    by={}
    for row in rows:
        target=targets[row['persona_id']]
        correct=bool(row['answer']==target['expected'] and row['parse_valid'])
        sufficient=bool(set(target['necessary_source_ids']).issubset(set(row['source_event_ids'])))
        by.setdefault(row['policy'],[]).append({'correct':correct,
             'evidence_sufficient':sufficient and row['source_ids_valid'],
             'parse_valid':row['parse_valid'],'persona_id':row['persona_id'],
             'expected':target['expected'],'actual':row['answer']})
    summaries={k:{'n':len(v),'accuracy':sum(x['correct'] for x in v)/len(v),
                  'provenance_complete':sum(x['evidence_sufficient'] for x in v)/len(v),
                  'parse_rate':sum(x['parse_valid'] for x in v)/len(v)} for k,v in by.items()}
    pairs={}
    for r in rows:pairs.setdefault(r['persona_id'],{})[r['policy']]=r
    matched=[]
    for pair in pairs.values():
        if 'expert_auto' in pair and 'human_coded' in pair:
            a,b=pair['expert_auto'],pair['human_coded']
            matched.append({'identical_input':a['prompt_sha256']==b['prompt_sha256'],
                            'identical_output':a['raw_text']==b['raw_text']})
    result={'status':'DEVELOPMENT_NOT_CONFIRMATORY','policy_summary':summaries,
            'matched_expert_human_n':len(matched),
            'matched_inputs_identical':all(p['identical_input'] for p in matched),
            'matched_outputs_identical':all(p['identical_output'] for p in matched),
            'matched_rows':matched,'rows':by,'DCH_claim':'NONE'}
    out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    return {k:v for k,v in result.items() if k!='rows'}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('mode',choices=('prepare','run','evaluate'))
    ap.add_argument('--folder',type=Path,required=True)
    ap.add_argument('--backend',choices=('transformers','ollama','mock'),default='mock')
    ap.add_argument('--model',default='Qwen/Qwen2.5-0.5B-Instruct')
    ap.add_argument('--count',type=int,default=12)
    ap.add_argument('--max-cases',type=int)
    ap.add_argument('--policies',nargs='+',choices=POLICIES,
                    default=['expert_auto','human_coded','stale','cold','oracle'])
    args=ap.parse_args(); p=args.folder
    if args.mode=='prepare':output=prepare(p,args.count)
    elif args.mode=='run':output=run(p/'dev_visible.json',p/'dev_raw.json',
                                   args.backend,args.model,args.policies,args.max_cases)
    else:output=evaluate(p/'dev_raw.json',p/'dev_EVALUATOR_ONLY.json',p/'dev_eval.json')
    print(json.dumps(output,indent=2))
if __name__=='__main__':main()
