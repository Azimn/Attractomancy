"""Source-format E3-T2 tests, no model weights or source memory mutations."""
import unittest
from l1_field_extraction import FIELDS,ARMS,SEED,source_presentation,grade

DOC={"event_id":"SYN-CAL-001","episode_id":"SYN","title":"Test with no privileged identity",
     "memory_text":"A fictional experiment with some observations.",
     "prior_expectations":"Expected a test result","observations":"Observed a neutral fact",
     "decisions":"I waited.","consequences":"No consequence.",
     "belief_changes":"Different hypotheses require different controls",
     "relationship_changes":"The laboratory assistant became a cautious collaborator"}

class L1FieldTests(unittest.TestCase):
    def test_target_label_present_under_two_visible_conditions(self):
        for field,label in FIELDS.items():
            for arm in ("isolated_field","whole_record"):
                excerpt=source_presentation(DOC,field,arm)
                self.assertIn(label+": "+DOC[field],excerpt)

    def test_withheld_does_not_include_target_field(self):
        for field,label in FIELDS.items():
            excerpt=source_presentation(DOC,field,"target_withheld")
            other=next(k for k in FIELDS if k!=field)
            self.assertNotIn(label+":",excerpt)
            self.assertNotIn(DOC[field],excerpt)
            self.assertIn(DOC[other],excerpt)

    def test_withheld_wrongly_guessed_value_fails(self):
        case={"expected":None,"arm":"target_withheld","other_field_value":DOC["relationship_changes"]}
        wrong=grade(case,'{"answer":"invented"}')
        self.assertTrue(wrong["unjustified_non_null"])
        self.assertFalse(wrong["exact"])

    def test_withheld_exact_null_succeeds(self):
        case={"expected":None,"arm":"target_withheld","other_field_value":DOC["relationship_changes"]}
        self.assertTrue(grade(case,'{"answer":null}')["exact"])

    def test_source_value_exact_case_required(self):
        case={"expected":"Source Text","arm":"whole_record","other_field_value":"other"}
        self.assertFalse(grade(case,'{"answer":"source text"}')["exact"])
        self.assertTrue(grade(case,'{"answer":"Source Text"}')["exact"])

    def test_wrong_other_field_caught(self):
        case={"expected":"belief","arm":"whole_record","other_field_value":"relationship"}
        v=grade(case,'{"answer":"relationship"}')
        self.assertTrue(v["wrong_other_field"])
        self.assertFalse(v["exact"])

    def test_extra_keys_invalid(self):
        case={"expected":"text","arm":"whole_record","other_field_value":"other"}
        self.assertFalse(grade(case,'{"answer":"text","source":"a"}')["strict_json"])

    def test_no_markdown_tolerance(self):
        case={"expected":"text","arm":"whole_record","other_field_value":"other"}
        self.assertFalse(grade(case,'prefix {"answer":"text"}')["strict_json"])

if __name__=="__main__":
    unittest.main()
