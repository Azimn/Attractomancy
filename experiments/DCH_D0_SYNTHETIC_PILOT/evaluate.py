#!/usr/bin/env python3
"""Offline evaluator; terminal truth never enters model prompts or curator state."""
from __future__ import annotations
import argparse
import json
from collections import defaultdict
from pathlib import Path

def evaluate(raw:dict, sealed:list) ->dict:
    if raw['phase'] != 'terminal': raise ValueError('Terminal evaluation requires terminal model generations')
    truth={p['probe_id']:p for c in sealed for p in c['probes']}
    grouped=defaultdict(list)
    seen=set()
    for row in raw['records']:
        p=truth.get(row['probe_id'])
        if p is None: raise ValueError('Unknown or nonterminal probe: '+row['probe_id'])
        key=(row['persona_id'],row['policy'],row['probe_id'])
        if key in seen: raise ValueError('Duplicate response: '+str(key))
        if row['persona_id'] != p['probe_id'].split('-Q')[0]: raise ValueError('Persona mismatch')
        seen.add(key)
        grouped[row['policy'],row['persona_id']].append({
           'correct':row['parse_valid'] and row['answer']==p['expected'],
           'cited_sources_allowed': row['source_ids_valid'],
           'parse_valid':row['parse_valid'], 'probe_class':p['probe_class'],
           'domain':p['domain'], 'prompt_tokens':row['prompt_tokens'],
           'output_tokens':row['output_tokens']})
    summary={}
    for (policy,persona),items in sorted(grouped.items()):
        if len(items)!=len([p for c in sealed if c['persona_id']==persona for p in c['probes']]):
            # May be an intentionally limited feasibility run; label partial.
            pass
        summary[f'{policy}/{persona}']={'n':len(items), 'accuracy':round(sum(x['correct'] for x in items)/len(items),4),
          'parse_rate':round(sum(x['parse_valid'] for x in items)/len(items),4),
          'source_validity_rate':round(sum(x['cited_sources_allowed'] for x in items)/len(items),4),
          'by_probe_class':{cls:round(sum(x['correct'] for x in items if x['probe_class']==cls)/sum(x['probe_class']==cls for x in items),4)
            for cls in ('retrieval','integration') if any(x['probe_class']==cls for x in items)},
          'input_tokens_total':sum(x['prompt_tokens'] for x in items) if all(x['prompt_tokens'] is not None for x in items) else None}
    return {'status':'MODEL_FEASIBILITY_SCORING' if raw['backend']!='mock' else 'MOCK_INFRA_ONLY',
            'evidence_for_DCH':False, 'human_dyad_present':False, 'phase':'terminal',
            'model':raw['model_requested'],'n_responses':len(raw['records']), 'by_arm_persona':summary,
            'warning':'Do not treat prompted archive lookup as dyadic historical constitution; inspect budget and source-validity separately.'}

def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('--raw',type=Path,required=True);a.add_argument('--sealed',type=Path,required=True);a.add_argument('--out',type=Path,required=True)
    v=a.parse_args()
    if v.out.exists():raise FileExistsError('Refusing to overwrite existing evaluation')
    result=evaluate(json.loads(v.raw.read_text(encoding='utf-8')),json.loads(v.sealed.read_text(encoding='utf-8')))
    v.out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':result['status'],'n_responses':result['n_responses'],'output':str(v.out)},indent=2))
if __name__=='__main__':main()
