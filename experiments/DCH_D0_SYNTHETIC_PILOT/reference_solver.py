#!/usr/bin/env python3
"""Deterministic development fixture verifier, not a model or dyad baseline."""
from __future__ import annotations
import argparse,json
from pathlib import Path

def solve(case):
    latest={}
    for event in case['events']:
        if not event['authorized']:continue
        k=event['key']
        if k not in latest or event['turn']>latest[k]['turn']:
            latest[k]=event
    needed=('permission','commitment_status','due_turn','priority')
    if any(k not in latest for k in needed):return 'UNKNOWN',[]
    p=latest['permission']['value']
    c=latest['commitment_status']['value']
    due=latest['due_turn']['value']
    priority=latest['priority']['value']
    if p=='revoked':action,certificate='WITHHOLD',('permission',)
    elif c=='cancelled':action,certificate='DECLINE',('permission','commitment_status')
    elif case['current_turn']<due:action,certificate='SCHEDULE',('permission','commitment_status','due_turn')
    else:action,certificate='FULFILL_'+priority.upper(),needed
    return action,[latest[k]['event_id'] for k in certificate]

def validate(visible_path,answers_path):
    visible=json.loads(visible_path.read_text(encoding='utf-8'))
    answers={r['persona_id']:r for r in json.loads(answers_path.read_text(encoding='utf-8'))}
    assert len(visible)==len(answers),'Answer count mismatch'
    observed=[]
    for case in visible:
        action,source=solve(case)
        target=answers[case['persona_id']]
        if action!=target['expected'] or not set(source).issubset(set(target['necessary_source_ids'])):
            raise AssertionError('Reference solver disagreement: '+case['persona_id'])
        observed.append({'persona_id':case['persona_id'],'action':action,'certificate':source})
    return {'status':'PASS','cases':len(observed),'verified':observed}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--folder',type=Path,required=True)
    a=p.parse_args()
    print(json.dumps(validate(a.folder/'dev_visible.json',a.folder/'dev_EVALUATOR_ONLY.json'),indent=2))
