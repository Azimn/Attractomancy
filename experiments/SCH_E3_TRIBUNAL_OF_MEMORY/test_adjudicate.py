"""Synthetic unit tests for E3 reviewer schema, never research adjudications."""
import copy
import unittest
from adjudicate import validate

def synthetic_fixture():
    candidates=[
        {"candidate_id":"C1","source_excerpt":"Synthetic alpha", "title":"Alpha"},
        {"candidate_id":"C2","source_excerpt":"Synthetic beta", "title":"Beta"},
        {"candidate_id":"C3","source_excerpt":"Synthetic noise", "title":"Noise"},
    ]
    packet=[{"case_id":"SYN-001","candidates":candidates,
             "example_not_blind_ground_truth":False}]
    labels=[
        {"candidate_id":"C1","label":"direct_support","rationale":"First required fact."},
        {"candidate_id":"C2","label":"direct_support","rationale":"Second required fact."},
        {"candidate_id":"C3","label":"irrelevant","rationale":"Unrelated."},
    ]
    judgments=[{"reviewer_id":f"R{i:02d}","case_id":"SYN-001",
                "candidate_labels":copy.deepcopy(labels),
                "case_sufficiency":"sufficient",
                "sufficient_sets":[["C1","C2"]],
                "case_rationale":"Combined source facts are jointly sufficient."}
               for i in range(1,4)]
    return packet,judgments

class E3AdjudicationTests(unittest.TestCase):
    def test_three_complete_reviewers_pass(self):
        packet,judgments=synthetic_fixture()
        result=validate(packet,judgments)
        self.assertEqual(result["n_judgments"],3)
        self.assertEqual(result["average_pairwise_candidate_label_agreement"],1.0)

    def test_two_reviewers_rejected(self):
        p,j=synthetic_fixture()
        with self.assertRaisesRegex(ValueError,"three"):
            validate(p,j[:2])

    def test_calibration_packet_cannot_promote(self):
        p,j=synthetic_fixture()
        p[0]["example_not_blind_ground_truth"]=True
        with self.assertRaisesRegex(ValueError,"Calibration"):
            validate(p,j)

    def test_missing_candidate_label_rejected(self):
        p,j=synthetic_fixture()
        j[0]["candidate_labels"].pop()
        with self.assertRaises(ValueError):
            validate(p,j)

    def test_duplicate_review_case_rejected(self):
        p,j=synthetic_fixture()
        j[1]["reviewer_id"]=j[0]["reviewer_id"]
        with self.assertRaises(ValueError):
            validate(p,j)

    def test_sufficiency_requires_two_distinct_passages(self):
        p,j=synthetic_fixture()
        j[0]["sufficient_sets"]=[["C1"]]
        with self.assertRaises(ValueError):
            validate(p,j)

    def test_unlabeled_irrelevant_passage_cannot_support(self):
        p,j=synthetic_fixture()
        j[0]["sufficient_sets"]=[["C1","C3"]]
        with self.assertRaises(ValueError):
            validate(p,j)

    def test_unknown_status_rejected(self):
        p,j=synthetic_fixture()
        j[0]["case_sufficiency"]="guess"
        with self.assertRaises(ValueError):
            validate(p,j)

    def test_insufficient_cannot_assert_sufficient_set(self):
        p,j=synthetic_fixture()
        j[0]["case_sufficiency"]="insufficient"
        with self.assertRaises(ValueError):
            validate(p,j)

    def test_no_fabricated_reviews_allowed(self):
        p,j=synthetic_fixture()
        with self.assertRaises(ValueError):
            validate(p,[])

if __name__=="__main__":
    unittest.main()
