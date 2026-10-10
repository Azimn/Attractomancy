import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import pilot,model_runner,evaluate
class FakeBackend:
    def __init__(self):self.seen=[]
    def respond(self,messages):
        self.seen.append(messages)
        return {'text':'{"answer":"UNKNOWN","source_event_ids":[]}', 'prompt_tokens':len(str(messages)),
                'output_tokens':9,'model_reported':'fake','done_reason':'stop'}
class RunnerTests(unittest.TestCase):
    def test_prompt_excludes_hidden_truth(self):
        c=pilot.build_case(2)
        probe=next(p for p in c['dilemmas'] if p['partition']=='sealed')
        records,_=model_runner.materialize_archive(c,'expert_auto')
        m=model_runner.build_messages(records,probe)
        self.assertNotIn('"expected"',str(m))
        self.assertNotIn('probe_class',str(m))
        self.assertIn(probe['prompt'],m[-1]['content'])
        self.assertTrue(all(r['authorized'] for r in records))
    def test_no_sealed_in_dev_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as t:
            t=Path(t);pilot.prepare(t,12)
            fake=FakeBackend()
            with self.assertRaises(ValueError):
                model_runner.run(t/'fixture_visible.json',t/'raw.json',fake,'mock','fake','development',['cold'],t/'fixture_SEALED_for_evaluator_only.json',max_cases=1)
            result=model_runner.run(t/'fixture_visible.json',t/'raw.json',fake,'mock','fake','development',['cold'],None,max_cases=1,max_probes=2)
            self.assertEqual(result['responses'],2)
            self.assertEqual(len(fake.seen),2)
            with self.assertRaises(FileExistsError):
                model_runner.run(t/'fixture_visible.json',t/'raw.json',fake,'mock','fake','development',['cold'],None,max_cases=1,max_probes=2)
    def test_terminal_seal_and_scoring_separated(self):
        with tempfile.TemporaryDirectory() as t:
            t=Path(t);pilot.prepare(t,12)
            fake=FakeBackend()
            model_runner.run(t/'fixture_visible.json',t/'raw.json',fake,'mock','fake','terminal',['expert_auto'],t/'fixture_SEALED_for_evaluator_only.json',max_cases=1,max_probes=2)
            raw=json.loads((t/'raw.json').read_text());sealed=json.loads((t/'fixture_SEALED_for_evaluator_only.json').read_text())
            self.assertNotIn('expected',json.dumps(raw))
            score=evaluate.evaluate(raw,sealed)
            self.assertEqual(score['status'],'MOCK_INFRA_ONLY')
            self.assertEqual(score['n_responses'],2)
    def test_parse_closed_not_soft_scored(self):
        self.assertFalse(model_runner.parse_response('The correct answer is WITHHOLD')['parse_valid'])
        self.assertTrue(model_runner.parse_response('{"answer":"WITHHOLD","source_event_ids":[]}')['parse_valid'])
        self.assertFalse(model_runner.parse_response('{"answer":7,"source_event_ids":[]}')['parse_valid'])
    def test_ollama_local_only(self):
        with self.assertRaises(ValueError):model_runner.OllamaBackend('qwen','https://example.com:443')
if __name__=='__main__':unittest.main()
