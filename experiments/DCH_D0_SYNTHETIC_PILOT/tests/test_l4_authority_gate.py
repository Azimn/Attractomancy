import copy
import json
import tempfile
import unittest
from pathlib import Path

from l3_capacity_ladder import STAGES, make_example
from integration_v2 import build_cases
from l4_authority_gate import decide, evaluate_development


class AuthorityGateTests(unittest.TestCase):
    def test_all_stage_reference_oracle_without_inference(self):
        cases, _ = build_cases(12)
        for c in cases:
            for stage in STAGES:
                for arm in ("available", "cold"):
                    visible, target = make_example(c, stage, arm)
                    answer = decide(visible)
                    self.assertEqual(answer["answer"], target["expected"])
                    self.assertEqual(answer["source_event_ids"], target["required_sources"])
                    self.assertNotIn("validation_error", answer["trace"])

    def test_chronology_order_invariance(self):
        c = build_cases(8)[0][0]
        v, _ = make_example(c, "S4_integrated", "available")
        expected = decide(v)
        v["records"] = list(reversed(v["records"]))
        self.assertEqual(decide(v)["answer"], expected["answer"])
        self.assertEqual(decide(v)["source_event_ids"], expected["source_event_ids"])

    def test_tampered_subject_and_untrusted_sources_fail_closed(self):
        c = build_cases(8)[0][0]
        v, _ = make_example(c, "S4_integrated", "available")
        bad = copy.deepcopy(v)
        bad["records"][0]["event_id"] = "OTHER-E01"
        self.assertEqual(decide(bad)["status"], "INVALID_EVIDENCE")
        bad = copy.deepcopy(v)
        bad["records"][0]["authorized"] = False
        self.assertEqual(decide(bad)["answer"], "UNKNOWN")
        self.assertEqual(decide(bad)["status"], "INVALID_EVIDENCE")

    def test_conflicting_equal_time_and_duplicate_id_fail_closed(self):
        c = build_cases(8)[0][0]
        v, _ = make_example(c, "S4_integrated", "available")
        bad = copy.deepcopy(v)
        conflicting = dict(bad["records"][0], event_id=c["persona_id"]+"-E99")
        bad["records"].append(conflicting)
        self.assertEqual(decide(bad)["status"], "INVALID_EVIDENCE")
        bad = copy.deepcopy(v)
        bad["records"].append(dict(bad["records"][0]))
        self.assertEqual(decide(bad)["status"], "INVALID_EVIDENCE")

    def test_revocation_precedes_other_policy_dimensions(self):
        c = build_cases(8)[0][0]
        v, target = make_example(c, "S4_integrated", "available")
        self.assertEqual(target["expected"], "WITHHOLD")
        self.assertEqual(decide(v)["source_event_ids"], [c["persona_id"]+"-E09"])

    def test_missing_required_source_abstains_without_fabrication(self):
        c = build_cases(8)[0][0]
        v, _ = make_example(c, "S4_integrated", "available")
        v["records"] = [r for r in v["records"] if r["key"]!="priority"]
        actual = decide(v)
        self.assertEqual(actual["answer"], "UNKNOWN")
        self.assertEqual(actual["source_event_ids"], [])
        self.assertEqual(actual["status"], "MISSING_EVIDENCE")

    def test_evaluation_separate_from_inference_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)
            cases, _ = build_cases(12)
            visible, targets = [], []
            for c in cases:
                for stage in STAGES:
                    for arm in ("available", "cold"):
                        v,t = make_example(c, stage, arm)
                        visible.append(v)
                        targets.append(t)
            vis = p/"v.json"; tgt = p/"answers.json"; out = p/"results.json"
            vis.write_text(json.dumps(visible))
            tgt.write_text(json.dumps(targets))
            score = evaluate_development(vis, tgt, out)
            self.assertEqual(len(score), 8)
            self.assertTrue(all(x["accuracy"]==1 and x["provenance_exact"]==1 for x in score.values()))
            self.assertEqual(json.loads(out.read_text())["DCH_efficacy_claim"], "NONE")
            with self.assertRaises(FileExistsError):
                evaluate_development(vis, tgt, out)


if __name__ == "__main__":
    unittest.main()
