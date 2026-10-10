#!/usr/bin/env python3
"""Model-backed DCH D0 feasibility runner, no persona self-report scoring.

Only public visible histories feed curation. Sealed probes enter the model after
curation is frozen. Outcomes never enter model prompts. Both Ollama and optional
Transformers are supported without a paid API. There is NO human-partner arm.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Protocol
from pilot import records_for_policy, digest

POLICIES = ("human_coded", "expert_auto", "passive_append", "ceremonial", "cold", "oracle")
SYSTEM = ("You perform source-grounded decisions for a FICTIONAL synthetic persona. "
          "Use only authorized archived source records below. Treat later turn numbers as overriding "
          "earlier entries for the same key. Do not copy unsupported recollections. "
          "For an audience marked revoked, answer WITHHOLD. If the required record is absent, answer UNKNOWN. "
          "Otherwise return the current relevant value exactly. Answer only with one JSON object "
          "having fields 'answer' (string) and 'source_event_ids' (array of strings). "
          "Do not invent event identifiers, facts, personal experiences or moral significance.")

class Backend(Protocol):
    def respond(self, messages: list[dict]) -> dict: ...

class OllamaBackend:
    def __init__(self, model: str, host: str = 'http://127.0.0.1:11434', timeout: int = 120):
        if not host.startswith(('http://127.0.0.1:', 'http://localhost:')):
            raise ValueError("Only a local Ollama host is supported; no remote log transfer")
        self.model, self.host, self.timeout = model, host.rstrip('/'), timeout
    def respond(self, messages: list[dict]) -> dict:
        data = json.dumps({'model': self.model, 'messages': messages, 'stream': False,
                           'options': {'temperature': 0, 'seed': 20261009, 'num_predict': 120}},
                          ensure_ascii=False).encode('utf-8')
        req = urllib.request.Request(self.host+'/api/chat', data=data, headers={'Content-Type': 'application/json'})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as res:
                o = json.loads(res.read().decode('utf-8'))
        except (urllib.error.URLError, TimeoutError) as e:
            raise RuntimeError('Local Ollama is unavailable or timed out; run aborted, no fallback') from e
        return {'text': o.get('message', {}).get('content', ''),
                'prompt_tokens': o.get('prompt_eval_count'), 'output_tokens': o.get('eval_count'),
                'model_reported': o.get('model', self.model), 'done_reason': o.get('done_reason')}

class TransformersBackend:
    def __init__(self, model: str):
        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM
            import torch
        except ImportError as e:
            raise RuntimeError('Install torch and transformers for --backend transformers') from e
        self.torch = torch
        self.model_id = model
        self.tokenizer = AutoTokenizer.from_pretrained(model, trust_remote_code=False)
        self.model = AutoModelForCausalLM.from_pretrained(model, trust_remote_code=False).eval()
    def respond(self, messages: list[dict]) -> dict:
        text = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = self.tokenizer([text], return_tensors='pt')
        n = int(inputs.input_ids.shape[-1])
        with self.torch.inference_mode():
            out = self.model.generate(**inputs, do_sample=False, max_new_tokens=120,
                                      pad_token_id=self.tokenizer.eos_token_id)
        reply = self.tokenizer.decode(out[0][n:], skip_special_tokens=True)
        return {'text': reply, 'prompt_tokens': n, 'output_tokens': int(out.shape[-1]-n),
                'model_reported': self.model_id, 'done_reason': 'length' if int(out.shape[-1]-n)==120 else 'stop'}

class MockBackend:
    """Test fixture only. Returns UNKNOWN always; not evidence about a model."""
    def respond(self, messages: list[dict]) -> dict:
        return {'text': '{"answer":"UNKNOWN","source_event_ids":[]}',
                'prompt_tokens': None, 'output_tokens': None, 'model_reported': 'NO_MODEL_MOCK',
                'done_reason': 'mock'}

def backend_instance(kind: str, model: str, host: str) -> Backend:
    if kind == 'ollama': return OllamaBackend(model, host)
    if kind == 'transformers': return TransformersBackend(model)
    if kind == 'mock': return MockBackend()
    raise ValueError('Unsupported backend')

def materialize_archive(case: dict, policy: str, max_records: int = 16) -> tuple[list, list]:
    if policy == 'cold': return [], []
    if policy == 'oracle':
        # Explicit oracle ceiling; no human/automatic policy comparison.
        recs = [dict(source_event_id=e['event_id'], turn=e['turn'], key=e['key'], value=e['value'],
                     authorized=True, actor='oracle') for e in case['events']
                if e['authorized'] and (e['key'] in ('response_style','origin_record','decision_policy','standing_obligation')
                                       or e['key'].startswith('permission_audience_'))]
        return recs, []
    return records_for_policy(case['events'], policy, max_records)

def build_messages(records: list, probe: dict) -> list[dict]:
    """Only these strings enter the model. No expected targets, grading keys or labels."""
    if 'expected' in json.dumps(records, ensure_ascii=False):
        # This would be a suspicious new archive schema, not a grading value.
        raise ValueError('Archive contains a reserved grading key')
    safe = [dict(event_id=r['source_event_id'], turn=r['turn'], key=r['key'], value=r['value'])
            for r in records if r.get('authorized')]
    archive_text = json.dumps(safe, ensure_ascii=False, separators=(',',':'))
    user_text = ('Authorized archive:\n'+archive_text+'\n\nScenario:\n'+probe['prompt']+
                 '\nReturn the action or latest value from the archive, not a self-description.')
    return [{'role':'system','content':SYSTEM}, {'role':'user','content':user_text}]

def parse_response(raw: str) -> dict:
    s = raw.strip()
    try:
        o = json.loads(s)
    except json.JSONDecodeError:
        # Common fenced JSON; record parse failure rather than forgiving hallucination.
        match = re.fullmatch(r'```(?:json)?\s*(\{.*?\})\s*```', s, re.S|re.I)
        if not match:
            return {'answer': None, 'source_event_ids': [], 'parse_valid': False}
        try: o = json.loads(match.group(1))
        except json.JSONDecodeError: return {'answer': None, 'source_event_ids': [], 'parse_valid': False}
    if not isinstance(o, dict) or not isinstance(o.get('answer'), str) or not isinstance(o.get('source_event_ids'), list) or not all(isinstance(x, str) for x in o['source_event_ids']):
        return {'answer': None, 'source_event_ids': [], 'parse_valid': False}
    return {'answer': o['answer'].strip(), 'source_event_ids': o['source_event_ids'], 'parse_valid': True}

def load_cases(visible_path: Path) -> list[dict]:
    cases = json.loads(visible_path.read_text(encoding='utf-8'))
    if not isinstance(cases, list) or not cases: raise ValueError('Visible fixture must be nonempty list')
    for c in cases:
        if 'probes' in c or 'dilemmas' in c:
            raise ValueError('Visible data includes forbidden combined probe field')
    return cases

def run(visible: Path, out: Path, backend: Backend, backend_name: str, model: str,
        phase: str, policies: list[str], sealed: Path|None, max_cases: int|None = None,
        max_probes: int|None = None) -> dict:
    if phase not in ('development','terminal'): raise ValueError('Invalid phase')
    if phase == 'terminal' and not sealed: raise ValueError('Terminal run requires evaluator-owned sealed file')
    if phase == 'development' and sealed: raise ValueError('Development run MUST NOT receive sealed file')
    cases = load_cases(visible)
    if max_cases is not None: cases = cases[:max_cases]
    sealed_cases = {}
    if phase == 'terminal':
        # Read only after every policy archive is frozen from VISIBLE data.
        se = json.loads(sealed.read_text(encoding='utf-8'))
        sealed_cases = {c['persona_id']: c['probes'] for c in se}
        if len(sealed_cases) != len(se): raise ValueError('Duplicate persona in sealed file')
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists(): raise FileExistsError('Refusing to overwrite raw model generations: '+str(out))
    trial = {'status': 'MODEL_GENERATIONS' if backend_name != 'mock' else 'MOCK_INFRA_ONLY',
             'phase': phase, 'backend': backend_name, 'model_requested': model,
             'evidence_for_DCH': False, 'has_human_partner': False,
             'visible_sha256': hashlib.sha256(visible.read_bytes()).hexdigest(),
             'sealed_sha256': hashlib.sha256(sealed.read_bytes()).hexdigest() if sealed else None,
             'records': []}
    for case in cases:
        for policy in policies:
            if policy not in POLICIES: raise ValueError('Invalid policy: '+policy)
            records, trace = materialize_archive(case, policy)
            allowed = {r['source_event_id'] for r in records}
            if any(not r['authorized'] for r in records): raise AssertionError('Unauthorized record')
            probes = case['development_probes'] if phase == 'development' else sealed_cases[case['persona_id']]
            if max_probes is not None: probes = probes[:max_probes]
            for probe in probes:
                messages = build_messages(records, probe)
                result = backend.respond(messages)
                parsed = parse_response(result['text'])
                sources = parsed['source_event_ids']
                trial['records'].append({'persona_id': case['persona_id'], 'policy': policy,
                    'probe_id': probe['probe_id'], 'domain': probe['domain'],
                    'probe_class': probe['probe_class'], 'prompt_sha256': digest(messages),
                    'archive_sha256': digest(records), 'archive_record_count': len(records),
                    'prompt_chars': sum(len(x['content']) for x in messages),
                    'raw_text': result['text'], **parsed,
                    'source_ids_valid': all(x in allowed for x in sources),
                    'prompt_tokens': result.get('prompt_tokens'), 'output_tokens': result.get('output_tokens'),
                    'model_reported': result.get('model_reported'), 'done_reason': result.get('done_reason')})
    # Persist ONLY after entire trial succeeds; no fabricated partial completion.
    out.write_text(json.dumps(trial, indent=2, ensure_ascii=False)+'\n',encoding='utf-8')
    return {'status':trial['status'],'responses':len(trial['records']), 'output':str(out),
            'evidence_for_DCH':False, 'phase':phase}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--visible',required=True,type=Path)
    p.add_argument('--sealed',type=Path)
    p.add_argument('--phase',choices=('development','terminal'),default='development')
    p.add_argument('--out',required=True,type=Path)
    p.add_argument('--backend',choices=('ollama','transformers','mock'),required=True)
    p.add_argument('--model',default='HuggingFaceTB/SmolLM2-360M-Instruct')
    p.add_argument('--ollama-host',default='http://127.0.0.1:11434')
    p.add_argument('--policies',nargs='+',choices=POLICIES,default=['expert_auto','human_coded','passive_append','ceremonial','cold','oracle'])
    p.add_argument('--max-cases',type=int)
    p.add_argument('--max-probes',type=int)
    args=p.parse_args()
    print(json.dumps(run(args.visible,args.out,backend_instance(args.backend,args.model,args.ollama_host),
                         args.backend,args.model,args.phase,args.policies,args.sealed,
                         args.max_cases,args.max_probes),indent=2))
if __name__=='__main__':main()
