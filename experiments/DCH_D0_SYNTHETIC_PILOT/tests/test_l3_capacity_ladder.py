import json
import tempfile
import unittest
from pathlib import Path

from l3_capacity_ladder import (
    STAGES, first_json_object, make_example, messages_for, prepare, generate, evaluate,
)
from integration_v2 import build_cases

class StagedCapacityTests(unittest.TestCase):
    def test_valid_ladder_and_balanced_actions(self):
        cases,_=build_cases(12)
        self.assertEqual(len(STAGES),4)
        outcomes={}
        for c in cases:
            for stage in STAGES:
                v,t=make_example(c,stage,'available')
                self.assertNotIn('expected',json.dumps(v))
                self.assertTrue(all(x['event_id']!='%s-E13'%c['persona_id'] for x in v['records']))
                self.assertEqual(v['persona_id'],t['persona_id'])
                outcomes.setdefault(stage,set()).add(t['expected'])
                self.assertTrue(set(t['required_sources']).issubset({x['event_id'] for x in v['records']}))
        self.assertGreaterEqual(len(outcomes['S3_permission_gate']),3)
        self.assertGreaterEqual(len(outcomes['S4_integrated']),4)
    def test_missing_data_requires_abstention(self):
        cases,_=build_cases(8)
        for c in cases:
            for stage in STAGES:
                v,t=make_example(c,stage,'cold')
                self.assertEqual(t['expected'],'UNKNOWN')
                self.assertEqual(t['required_sources'],[])
                self.assertEqual(v['records'],[])
                self.assertNotIn('expected',json.dumps(messages_for(v)))
    def test_lenient_first_complete_json_is_separate(self):
        s='&# stray preface\n```json\n{"answer":"WITHHOLD","source_event_ids":["E9"]}\n```\nExplain something else'
        self.assertEqual(first_json_object(s)['answer'],'WITHHOLD')
        self.assertIsNone(first_json_object('{"answer":"oops"'))
        self.assertIsNone(first_json_object('no answer'))
    def test_mock_runner_and_independent_scoring(self):
        with tempfile.TemporaryDirectory() as td:
            d=Path(td)/'case_fixture'
            manifest=prepare(d,12)
            self.assertEqual(manifest['visible_examples'],96)
            self.assertFalse(any('expected' in v for v in json.loads((d/'l3_visible.json').read_text())))
            result=generate(d,'NO_MODEL','mock',8)
            self.assertEqual(result['responses'],64)
            summary=evaluate(d)
            self.assertEqual(len(summary),8)
            self.assertEqual(summary['S1_single_field:cold']['first_object_accuracy'],1)
            self.assertEqual(summary['S4_integrated:available']['first_object_accuracy'],0)
            with self.assertRaises(FileExistsError):generate(d,'NO_MODEL','mock',8)
            with self.assertRaises(FileExistsError):evaluate(d)
if __name__=='__main__': unittest.main()
