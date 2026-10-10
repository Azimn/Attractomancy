"""E3-T2P3 plain source-copying strict string and missing marker tests."""
import unittest
from l1_plaintext_v3 import grade,MARKER

class PlainTextTests(unittest.TestCase):
    def test_present_exact(self):
        x={"expected":"A cautious judgment is not a weak judgment","arm":"isolated_field","other_field_value":"Other"}
        self.assertTrue(grade(x,x["expected"])["strict_exact"])

    def test_present_case_change_is_wrong(self):
        x={"expected":"The effect remained uncertain.","arm":"whole_record","other_field_value":"Other"}
        self.assertFalse(grade(x,"The effect remained Uncertain.")["strict_exact"])

    def test_extra_label_is_not_exact(self):
        x={"expected":"Exact archive phrase","arm":"whole_record","other_field_value":"Other"}
        y=grade(x,"BELIEF CHANGE: Exact archive phrase")
        self.assertFalse(y["strict_exact"])
        self.assertTrue(y["format_extra_text"])

    def test_explicit_absence_is_exact(self):
        x={"expected":None,"arm":"target_withheld","other_field_value":"Other"}
        self.assertTrue(grade(x,MARKER)["strict_exact"])

    def test_withheld_guesses_are_wrong(self):
        x={"expected":None,"arm":"target_withheld","other_field_value":"Other"}
        y=grade(x,"Inferred relationship")
        self.assertFalse(y["strict_exact"])
        self.assertTrue(y["unjustified_field_response"])

    def test_quoted_marker_is_not_exact(self):
        x={"expected":None,"arm":"target_withheld","other_field_value":"Other"}
        self.assertFalse(grade(x,'"'+MARKER+'"')["strict_exact"])

    def test_output_with_extra_prefix_is_not_exact(self):
        x={"expected":"A precise source fact","arm":"isolated_field","other_field_value":"Other"}
        self.assertFalse(grade(x,"Source: "+x["expected"])["strict_exact"])

    def test_wrong_other_field_diagnosed(self):
        x={"expected":"Correct belief","arm":"whole_record","other_field_value":"Other relationship"}
        self.assertTrue(grade(x,"Other relationship")["wrong_field_response"])

if __name__=="__main__":
    unittest.main()
