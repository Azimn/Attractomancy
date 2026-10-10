#!/usr/bin/env python3
"""Post-hoc descriptive token and storage parity auditing for paired model arms."""
from __future__ import annotations
import argparse
import json
from collections import defaultdict
from pathlib import Path

def audit(raw: dict, a='expert_auto', b='human_coded', tolerance=0.02)->dict:
    rows=defaultdict(dict)
    for r in raw['records']:
        k=(r['persona_id'],r['probe_id'])
        if r['policy'] in (a,b):
            if r['policy'] in rows[k]: raise ValueError('Duplicate arm/probe')
            rows[k][r['policy']] = r
    measured=[]; unavailable=0
    for k,v in sorted(rows.items()):
        if set(v)!={a,b}:
            unavailable+=1
            continue
        x,y=v[a],v[b]
        t1,t2=x['prompt_tokens'],y['prompt_tokens']
        if t1 is None or t2 is None:
            unavailable+=1
            continue
        denom=max(t1,t2,1)
        measured.append({'persona_id':k[0],'probe_id':k[1],
                         'token_disparity':abs(t1-t2)/denom,
                         'record_count_disparity':abs(x['archive_record_count']-y['archive_record_count'])/max(x['archive_record_count'],y['archive_record_count'],1)})
    return {'status':'BUDGET_PARITY_AUDIT','arms':[a,b], 'tolerance':tolerance,
      'n_measured_pairs':len(measured),'n_unmeasured_pairs':unavailable,
      'within_tolerance': bool(measured and not unavailable and all(x['token_disparity']<=tolerance and x['record_count_disparity']<=tolerance for x in measured)),
      'max_token_disparity':max((x['token_disparity'] for x in measured),default=None),
      'max_record_disparity':max((x['record_count_disparity'] for x in measured),default=None),
      'note':'Matching count/token budgets does not imply equivalent information or human-vs-algorithm policy fidelity.'}

def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('--raw',type=Path,required=True)
    a.add_argument('--out',type=Path,required=True)
    v=a.parse_args()
    if v.out.exists():raise FileExistsError('Refusing overwrite')
    s=audit(json.loads(v.raw.read_text(encoding='utf-8')))
    v.out.write_text(json.dumps(s,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(s,indent=2))
if __name__=='__main__':main()
