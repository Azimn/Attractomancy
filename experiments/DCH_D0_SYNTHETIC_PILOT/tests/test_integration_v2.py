import json
import tempfile
import unittest
from pathlib import Path
from integration_v2 import build_cases, prepare, records_for_policy, run, evaluate

class IntegrationV2Tests(unittest.TestCase):
    def test_balanced_composite_actions(self):
        cases,answers=build_cases(12)
        self.assertEqual(len(cases),12)
        self.assertGreaterEqual(len({r['expected'] for r in answers}),4)
        self.assertTrue(all(len(x['necessary_source_ids'])==4 for x in answers))

    def test_current_curators_equivalent_but_stale_differs(self):
        cases,_=build_cases(8)
        self.assertTrue(all(records_for_policy(c['events'],'expert_auto')==records_for_policy(c['events'],'human_coded') for c in cases))
        self.assertTrue(all(records_for_policy(c['events'],'expert_auto')!=records_for_policy(c['events'],'stale') for c in cases))
        self.assertTrue(all(len(records_for_policy(c['events'],'expert_auto'))==4 for c in cases))
        self.assertTrue(all(e['authorized'] for c in cases for e in records_for_policy(c['events'],'oracle')))

    def test_separate_evaluator_and_provenance(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);prepare(p,12)
            self.assertNotIn('expected',(p/'dev_visible.json').read_text())
            r=run(p/'dev_visible.json',p/'dev_raw.json','mock','NO_MODEL',['expert_auto','human_coded','stale','cold','oracle'],8)
            self.assertEqual(r['responses'],40)
            evaluated=evaluate(p/'dev_raw.json',p/'dev_EVALUATOR_ONLY.json',p/'dev_eval.json')
            self.assertTrue(evaluated['matched_inputs_identical'])
            self.assertTrue(evaluated['matched_outputs_identical'])
            self.assertEqual(evaluated['policy_summary']['expert_auto']['accuracy'],0)
            self.assertNotIn('necessary_source_ids',(p/'dev_raw.json').read_text())

if __name__=='__main__':unittest.main()
