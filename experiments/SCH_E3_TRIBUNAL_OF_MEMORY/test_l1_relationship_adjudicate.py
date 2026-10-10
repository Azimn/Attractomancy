"""Only synthetic reviewer unit fixtures; zero actual human labels."""
import copy
import unittest
from l1_relationship_adjudicate import FLAGS,validate

def fixture():
    old="The earlier visitor promised a letter every month and sealed it before sunset."
    new="The later visitor wrote another letter and continued the arrangement."
    packet=[{"pair_id":"SYN-ONE","earlier_excerpt":old,"later_excerpt":new}]
    data=[]
    for i in range(3):
        data.append({
            "pair_id":"SYN-ONE","reviewer_id":f"TEST{i}",
            "reviewer_disclosure":{"not_original_case_author":True,"did_not_consult_organizer_mapping":True},
            "candidate_relation_flags":{k:k=="reinforces_prior_context" for k in FLAGS},
            "reviewer_rationale":"The later event continues the earlier explicit written arrangement.",
            "confidence":0.85,
            "earlier_exact_quote":"promised a letter every month",
            "later_exact_quote":"continued the arrangement",
            "explicit_prior_commitment":None,"explicit_superseding_statement":None,
        })
    return packet,data

class RelationshipReviewTests(unittest.TestCase):
    def test_valid_synthetic_reviewers(self):
        p,r=fixture()
        x=validate(p,r)
        self.assertEqual(x["cases"],1)
        self.assertEqual(x["min_distinct_reviewers"],3)
        self.assertEqual(x["mean_pairwise_flag_agreement"],1.0)

    def test_not_enough_reviewers(self):
        p,r=fixture()
        with self.assertRaisesRegex(ValueError,"three"):
            validate(p,r[:2])

    def test_no_annotation_not_complete(self):
        p,r=fixture()
        with self.assertRaises(ValueError):
            validate(p,[])

    def test_duplicate_reviewer(self):
        p,r=fixture()
        r[1]["reviewer_id"]=r[0]["reviewer_id"]
        with self.assertRaises(ValueError):
            validate(p,r)

    def test_bare_recency_not_revocation(self):
        p,r=fixture()
        r[0]["candidate_relation_flags"]["supersedes_specific_commitment"]=True
        with self.assertRaisesRegex(ValueError,"Revocation"):
            validate(p,r)

    def test_uncited_later_quote_fails(self):
        p,r=fixture()
        r[0]["later_exact_quote"]="an entirely different scene"
        with self.assertRaisesRegex(ValueError,"Later"):
            validate(p,r)

    def test_fake_disclosure_fails(self):
        p,r=fixture()
        r[0]["reviewer_disclosure"]["did_not_consult_organizer_mapping"]=False
        with self.assertRaisesRegex(ValueError,"disclosure"):
            validate(p,r)

    def test_ambiguous_exclusive(self):
        p,r=fixture()
        r[0]["candidate_relation_flags"]["insufficient_to_reconcile"]=True
        with self.assertRaisesRegex(ValueError,"Insufficient"):
            validate(p,r)

    def test_negative_without_quotes_passes(self):
        p,r=fixture()
        r[0]["candidate_relation_flags"]={k:k=="insufficient_to_reconcile" for k in FLAGS}
        r[0]["earlier_exact_quote"]=None
        r[0]["later_exact_quote"]=None
        x=validate(p,r)
        self.assertEqual(x["reviewer_case_submissions"],3)

    def test_flag_typing_required(self):
        p,r=fixture()
        r[0]["candidate_relation_flags"]["reinforces_prior_context"]="true"
        with self.assertRaises(ValueError):
            validate(p,r)

if __name__=="__main__":
    unittest.main()
