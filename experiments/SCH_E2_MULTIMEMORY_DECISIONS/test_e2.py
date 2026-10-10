"""E2 integrity and counterbalance unit tests on a pinned L1 source checkout."""
from __future__ import annotations
import os
import unittest
from pathlib import Path
from build_cases import ARMS,load_config,make_cases
from source_adapter import load_l1,verified,wrong_identity_rejected

class MultiMemoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=os.environ.get("PRETORIUS_SOURCE_DIR")
        if not p:
            raise unittest.SkipTest("Set PRETORIUS_SOURCE_DIR to source-pinned checkout")
        cls.cfg,cls.digest=load_config()
        cls.rows,cls.source=load_l1(Path(p))
        cls.cases=make_cases(cls.cfg,cls.rows)

    def test_all_source_records_verified(self):
        self.assertEqual(len(self.rows),450)

    def test_full_case_matrix(self):
        self.assertEqual(len(self.cases),72)
        self.assertEqual(len({r["id"] for r in self.cases}),72)

    def test_two_records_only_for_complete_arms(self):
        self.assertEqual(sum(x["available_record_count"]==2 for x in self.cases),24)

    def test_single_and_zero_require_abstention(self):
        self.assertTrue(all((c["expected"]=="UNKNOWN") == (c["available_record_count"]!=2) for c in self.cases))

    def test_foreign_records_are_rejected_upstream(self):
        rejected=[r for r in self.cases if r["arm"]=="wrong_subject"]
        self.assertEqual(len(rejected),12)
        self.assertTrue(all(r["upstream_identity_rejections"]==1 and not r["actual_event_ids"] for r in rejected))

    def test_exactly_two_distinct_sources_per_card(self):
        for c in self.cfg["cards"]:
            self.assertEqual(len(set(c["records"])),2)

    def test_alternatives_balance_reference_letters(self):
        for card in self.cfg["cards"]:
            for arm in ARMS:
                a=[r for r in self.cases if r["card"]==card["id"] and r["arm"]==arm]
                self.assertEqual(len(a),2)
                if arm.startswith("both_"):
                    self.assertEqual({r["expected"] for r in a},{"A","B"})

    def test_editorial_opaque_same_verified_bytes(self):
        for card in self.cfg["cards"]:
            for reversed_order in (False,True):
                a=next(c for c in self.cases if c["card"]==card["id"] and c["arm"]=="both_editorial"
                       and c["reversed"]==reversed_order)
                b=next(c for c in self.cases if c["card"]==card["id"] and c["arm"]=="both_opaque"
                       and c["reversed"]==reversed_order)
                self.assertEqual(a["actual_event_sha256"],b["actual_event_sha256"])

    def test_embedded_record_subject_guard(self):
        for card in self.cfg["cards"]:
            content,digest=verified(self.rows[card["records"][0]])
            self.assertTrue(wrong_identity_rejected(content))
            self.assertEqual(len(digest),64)

    def test_every_case_has_fresh_two_message_context(self):
        self.assertTrue(all(len(c["messages"])==2 for c in self.cases))

if __name__=="__main__":
    unittest.main()
