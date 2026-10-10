"""Synthetic unit tests for L1 semantic reviewer validity gate.

All judgments here are invented TEST FIXTURES ONLY, not independent research labels.
"""
import copy
import unittest
from l1_semantic_adjudicate import validate

def fixture():
    packet=[{"packet_case_id":"SYN-REVIEW-1",
             "source_excerpt":"The observer measured the millstream twice, then requested a third reading.",
             "candidate_interpretations":[
                {"candidate_id":"C_A","proposed_interpretation":"The observer wanted a third reading."},
                {"candidate_id":"C_B","proposed_interpretation":"The observer rejected measurement."},
                {"candidate_id":"C_C","proposed_interpretation":"A relationship changed."},
             ]}]
    answers=[]
    for i in range(3):
        answers.append({
            "packet_case_id":"SYN-REVIEW-1","reviewer_id":f"TEST-R{i}",
            "reviewer_disclosure":{"did_not_consult_original_corpus":True,
                                   "not_original_case_author":True},
            "candidate_assessments":[
                {"candidate_id":"C_A","label":"supported_by_narrative",
                 "exact_narrative_quote":"requested a third reading",
                 "rationale":"This literal clause supports the proposal.","confidence":0.9},
                {"candidate_id":"C_B","label":"contradicted_by_narrative",
                 "exact_narrative_quote":"measured the millstream twice",
                 "rationale":"Measurement did occur in the source.","confidence":0.8},
                {"candidate_id":"C_C","label":"underdetermined_by_narrative",
                 "exact_narrative_quote":None,
                 "rationale":"No interpersonal state is described here.","confidence":0.7},
            ]
        })
    return packet,answers

class ReviewTests(unittest.TestCase):
    def test_all_three_synthetic_reviewers_valid(self):
        p,a=fixture()
        x=validate(p,a)
        self.assertEqual(x["min_reviewers"],3)
        self.assertEqual(x["pairwise_exact_label_agreement"],1.0)
        self.assertTrue(x["no_main_e3_confirmatory_status"])

    def test_no_reviews_fail(self):
        p,a=fixture()
        with self.assertRaises(ValueError):
            validate(p,[])

    def test_two_reviews_fail(self):
        p,a=fixture()
        with self.assertRaisesRegex(ValueError,"Three"):
            validate(p,a[:2])

    def test_missing_evidence_quote_fail(self):
        p,a=fixture()
        a[0]["candidate_assessments"][0]["exact_narrative_quote"]="not in the source at all"
        with self.assertRaises(ValueError):
            validate(p,a)

    def test_duplicate_reviewer_fail(self):
        p,a=fixture()
        a[1]["reviewer_id"]=a[0]["reviewer_id"]
        with self.assertRaises(ValueError):
            validate(p,a)

    def test_blank_rationale_fail(self):
        p,a=fixture()
        a[0]["candidate_assessments"][0]["rationale"]=""
        with self.assertRaises(ValueError):
            validate(p,a)

    def test_absent_disclosure_fail(self):
        p,a=fixture()
        a[0]["reviewer_disclosure"]["did_not_consult_original_corpus"]=False
        with self.assertRaises(ValueError):
            validate(p,a)

    def test_missing_candidate_fail(self):
        p,a=fixture()
        a[0]["candidate_assessments"].pop()
        with self.assertRaises(ValueError):
            validate(p,a)

    def test_support_requires_literal_quote(self):
        p,a=fixture()
        a[0]["candidate_assessments"][2]["label"]="supported_by_narrative"
        with self.assertRaises(ValueError):
            validate(p,a)

    def test_confidence_out_of_range_fail(self):
        p,a=fixture()
        a[0]["candidate_assessments"][0]["confidence"]=1.4
        with self.assertRaises(ValueError):
            validate(p,a)

if __name__=="__main__":
    unittest.main()
