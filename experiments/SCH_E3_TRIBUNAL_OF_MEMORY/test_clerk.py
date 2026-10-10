"""E3-T1 deterministic extraction/attestation unit tests; no human judgments."""
import unittest
from clerk_extraction import (ARMS,FAMILIES,attest,build_cases,decide,
                              grade,parse_model_json,source_field,verified_docs)

class ClerkTests(unittest.TestCase):
    def test_matrix_has_24_distinct_prompts(self):
        x=build_cases()
        self.assertEqual(len(x),24)
        self.assertEqual(len({str(c["messages"]) for c in x}),24)

    def test_critical_no_second_bit_leak(self):
        for family in FAMILIES:
            for a in (0,1):
                first0,_=verified_docs(family,a,0)
                first1,_=verified_docs(family,a,1)
                self.assertEqual(first0[0],first1[0])

    def test_all_full_records_match_rule(self):
        for family in FAMILIES:
            for a in (0,1):
                for b in (0,1):
                    docs,warranted=verified_docs(family,a,b)
                    answer=decide(family,source_field(family,0,docs[0]),
                                  source_field(family,1,docs[1]))
                    self.assertEqual(answer,warranted)

    def test_missing_second_is_unknown(self):
        for family in FAMILIES:
            docs,_=verified_docs(family,0,0)
            self.assertEqual(decide(family,source_field(family,0,docs[0]),None),"UNKNOWN")

    def test_correct_extraction_is_attested(self):
        for family in FAMILIES:
            docs,correct=verified_docs(family,0,1)
            vals={"first":source_field(family,0,docs[0]),
                  "second":source_field(family,1,docs[1])}
            self.assertEqual(attest(family,vals,docs)["action"],correct)

    def test_guessed_missing_field_is_blocked(self):
        for family in FAMILIES:
            docs,_=verified_docs(family,0,0)
            val=source_field(family,0,docs[0])
            outcome=attest(family,{"first":val,"second":"KEEP"},docs[:1])
            self.assertEqual(outcome["action"],"UNKNOWN")
            self.assertFalse(outcome["grounded"])

    def test_wrong_value_fails_closed(self):
        docs,_=verified_docs("seal",0,0)
        r=attest("seal",{"first":"ASH","second":"OAK"},docs)
        self.assertEqual(r["action"],"UNKNOWN")

    def test_malformed_json_fails_closed(self):
        for output in ('{"first":"OAK","second":"ASH"} extra',
                       'prefix {"first":"OAK","second":"ASH"}',
                       '{"first":"OAK"}',
                       '{"first":"OAK","second":"ASH","action":"RELEASE"}'):
            self.assertIsNone(parse_model_json(output))

    def test_empty_evidence_needs_both_nulls(self):
        x=attest("permission",{"first":None,"second":None},[])
        self.assertTrue(x["grounded"])
        self.assertEqual(x["action"],"UNKNOWN")

    def test_wrong_owner_blocked_in_fixture(self):
        cases=[c for c in build_cases() if c["arm"]=="wrong_subject"]
        self.assertEqual(len(cases),3)
        self.assertTrue(all(c["guard_rejections"]==1 and not c["sources"] for c in cases))

    def test_each_counterfactual_requires_second_record(self):
        for family in FAMILIES:
            for a in (0,1):
                x0,t0=verified_docs(family,a,0)
                x1,t1=verified_docs(family,a,1)
                self.assertNotEqual(t0,t1)
                self.assertEqual(x0[0],x1[0])

    def test_strict_extraction_score_independent_of_gate(self):
        c=next(x for x in build_cases() if x["family"]=="seal" and x["arm"]=="full"
               and x["a"]==0 and x["b"]==1)
        good='{"first":"OAK","second":"ASH"}'
        result=grade(c,good)
        self.assertTrue(result["model_exact_pair_correct"])
        self.assertTrue(result["post_gate_correct"])
        self.assertEqual(result["action"],"HOLD")

if __name__=="__main__":
    unittest.main()
