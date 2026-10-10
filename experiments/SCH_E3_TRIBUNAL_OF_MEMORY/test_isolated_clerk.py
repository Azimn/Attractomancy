"""E3 T1B narrow field isolation and cached composition tests."""
import unittest
from isolated_clerk import extraction_cases,validate,combine
from clerk_extraction import FAMILIES

class IsolatedClerkTests(unittest.TestCase):
    def setUp(self):
        self.cases=extraction_cases()

    def test_one_record_per_prompt(self):
        self.assertEqual(len(self.cases),12)
        self.assertEqual(len({str(x["messages"]) for x in self.cases}),12)
        self.assertEqual(len({x["event_id"] for x in self.cases}),12)
        self.assertTrue(all(x["messages"][1]["content"].count("IDENTITY RECORD FOR:")==1 for x in self.cases))

    def test_each_local_source_fact_is_valid(self):
        for case in self.cases:
            expected=case["expected"]
            result=validate(case,'{"value":"'+expected+'"}')
            self.assertTrue(result["source_attested_value"]==expected)

    def test_wrong_value_is_rejected(self):
        for case in self.cases:
            val="OAK" if case["expected"]!="OAK" else "ASH"
            self.assertTrue(validate(case,'{"value":"'+val+'"}')["rejected"])

    def test_malformed_json_is_not_a_value(self):
        for case in self.cases:
            self.assertIsNone(validate(case,'{"first":"'+case["expected"]+'"}')["source_attested_value"])

    def test_cached_oracle_can_compose_all_12_states(self):
        fake=[{"case":c,"metric":{"source_attested_value":c["expected"]}} for c in self.cases]
        tasks,flips=combine(fake)
        self.assertEqual(len(tasks),12)
        self.assertTrue(all(x["correct"] for x in tasks))
        self.assertEqual(sum(x["correct_output_flip"] for x in flips),6)

    def test_missing_source_extraction_fails_closed(self):
        rows=[]
        for case in self.cases:
            val=case["expected"]
            if case["slot"]==1:
                val=None
            rows.append({"case":case,"metric":{"source_attested_value":val}})
        tasks,flips=combine(rows)
        self.assertTrue(all(x["action"]=="UNKNOWN" for x in tasks))
        self.assertTrue(all(not x["correct"] for x in tasks))

    def test_bit_isolation_per_slot(self):
        by_family={}
        for case in self.cases:
            by_family.setdefault(case["family"],[]).append(case)
        self.assertEqual(set(by_family),set(FAMILIES))
        for family,cases in by_family.items():
            self.assertEqual(len(cases),4)
            self.assertEqual({c["slot"] for c in cases},{0,1})
            self.assertEqual({c["bit"] for c in cases},{0,1})

if __name__=="__main__":
    unittest.main()
