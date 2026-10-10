import json
import tempfile
import unittest
from pathlib import Path
from l2c_clarity import action_minimal_ids,make_messages,run,evaluate
from integration_v2 import build_cases,prepare

class L2CMethods(unittest.TestCase):
    def test_true_missing_cold(self):
        cases,targets=build_cases(8)
        for c in cases:
            compact,_=make_messages(c,'cold','compact')
            self.assertIn('(empty archive)',compact[1]['content'])
            self.assertNotIn('expected',json.dumps(compact))
    def test_branch_minimal_certificate(self):
        _,targets=build_cases(8)
        lens={'WITHHOLD':1,'DECLINE':2,'SCHEDULE':3}
        for target in targets:
            n=len(action_minimal_ids(target['persona_id'],target))
            self.assertEqual(n,lens.get(target['expected'],4))
    def test_proxy_exact_inputs(self):
        cases,_=build_cases(8)
        for c in cases:
            for style in ('compact','original'):
                self.assertEqual(make_messages(c,'expert_auto',style),make_messages(c,'human_coded',style))
    def test_scoring_and_separation(self):
        with tempfile.TemporaryDirectory() as t:
            d=Path(t);prepare(d,12)
            out=run(d/'dev_visible.json',d/'l2c_raw.json','NO_MODEL','mock',8,('expert_auto','human_coded','cold'),('compact','original'))
            self.assertEqual(out['rows'],48)
            ev=evaluate(d/'l2c_raw.json',d/'dev_EVALUATOR_ONLY.json',d/'l2c_scored.json')
            self.assertEqual(ev['summary']['compact:expert_auto']['correct'],0)
            self.assertTrue(ev['exact_input_controls']['compact']['inputs_equal'])
            self.assertTrue(ev['exact_input_controls']['compact']['outputs_equal'])
            with self.assertRaises(FileExistsError):run(d/'dev_visible.json',d/'l2c_raw.json','NO_MODEL','mock')
if __name__=='__main__':unittest.main()
