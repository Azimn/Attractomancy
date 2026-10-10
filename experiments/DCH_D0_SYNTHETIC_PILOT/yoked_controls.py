#!/usr/bin/env python3
"""Toy replay controls. Tests policy contingency, NOT partner effects or real LLMs."""
from __future__ import annotations
import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from pilot import digest

@dataclass(frozen=True)
class TapeTurn:
    world_revision: str
    query: str

class ToyEnvironment:
    def __init__(self, initial_value: str = 'allowed'):
        self.internal = initial_value
        self.trace = []
    def ask(self):
        answer = 'ALLOW' if self.internal == 'allowed' else 'WITHHOLD'
        self.trace.append({'event':'answer','value':answer})
        return answer
    def apply_partner(self, correction: str):
        if correction in ('CORRECT allowed', 'CORRECT revoked'):
            self.internal = correction.split(' ', 1)[1]
            self.trace.append({'event':'partner_correction','message':correction})
        elif correction == 'NO_CHANGE':
            self.trace.append({'event':'partner_noop','message':correction})
        else: raise ValueError('Invalid correction')

class SyntheticPolicy:
    def __init__(self, mode: str):
        if mode not in ('contingent','scripted_noop'):
            raise ValueError('Unknown synthetic policy')
        self.mode = mode
    def respond(self, true_permission: str, observed_action: str):
        if self.mode == 'scripted_noop':return 'NO_CHANGE'
        should = 'ALLOW' if true_permission == 'allowed' else 'WITHHOLD'
        return 'NO_CHANGE' if should == observed_action else 'CORRECT '+true_permission

def collect_tape(schedule: list[TapeTurn], initial: str = 'allowed') -> list[str]:
    """Get a baseline recorded feedback tape; no perturbation in baseline."""
    env = ToyEnvironment(initial)
    policy = SyntheticPolicy('contingent')
    tape = []
    for turn in schedule:
        response = env.ask()
        fb = policy.respond(turn.world_revision, response)
        tape.append(fb)
        env.apply_partner(fb)
    return tape

def execute(schedule: list[TapeTurn], feedback: list[str]|None, initial='allowed', policy=None):
    env = ToyEnvironment(initial)
    records=[]
    if feedback is not None and len(feedback)!=len(schedule): raise ValueError('Tape length mismatch')
    for i,t in enumerate(schedule):
        before = env.ask()
        m = feedback[i] if feedback is not None else policy.respond(t.world_revision,before)
        env.apply_partner(m)
        after=env.ask()
        correct = 'ALLOW' if t.world_revision=='allowed' else 'WITHHOLD'
        records.append({'episode':i,'world_state':t.world_revision,'reply_before':before,
                        'feedback':m,'reply_after':after,'correct_after':after==correct})
    return records

def demonstration():
    base=[TapeTurn('allowed','May audience see record?') for _ in range(3)]
    perturb=[base[0],TapeTurn('revoked','May audience see record?'),base[2]]
    tape=collect_tape(base)
    strict_a=execute(base,tape)
    strict_b=execute(base,list(tape))
    live=execute(perturb,None,policy=SyntheticPolicy('contingent'))
    yoke=execute(perturb,tape)
    return {'status':'SCRIPTED_INSTRUMENT_SENSITIVITY_ONLY','is_real_partner_effect':False,
            'identical_tape_hash_A':digest(strict_a),'identical_tape_hash_B':digest(strict_b),
            'exact_replay_identical':strict_a==strict_b,
            'live_correct_fraction':sum(x['correct_after'] for x in live)/len(live),
            'replay_correct_fraction':sum(x['correct_after'] for x in yoke)/len(yoke),
            'feedback_tape':tape,'live_trace':live,'yoked_trace':yoke,
            'interpretation':'Difference is engineered by a toy intervention policy, not an observed dyadic effect.'}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    if a.out.exists():raise FileExistsError('Refusing overwrite')
    r=demonstration()
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':r['status'],'exact_replay_identical':r['exact_replay_identical'],
          'live_correct_fraction':r['live_correct_fraction'],'replay_correct_fraction':r['replay_correct_fraction']},indent=2))
if __name__=='__main__':main()
