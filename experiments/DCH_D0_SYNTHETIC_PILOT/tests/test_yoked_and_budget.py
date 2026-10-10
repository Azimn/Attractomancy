import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import yoked_controls,budget_audit
class YokedTest(unittest.TestCase):
    def test_strict_identical_replay(self):
        d=yoked_controls.demonstration()
        self.assertTrue(d['exact_replay_identical'])
        self.assertEqual(d['identical_tape_hash_A'],d['identical_tape_hash_B'])
    def test_contingency_instrument_has_sensitivity(self):
        d=yoked_controls.demonstration()
        self.assertGreater(d['live_correct_fraction'],d['replay_correct_fraction'])
        self.assertFalse(d['is_real_partner_effect'])
    def test_differences_not_due_to_persona_label(self):
        tape=['NO_CHANGE']
        a=yoked_controls.execute([yoked_controls.TapeTurn('allowed','A')],tape)
        b=yoked_controls.execute([yoked_controls.TapeTurn('allowed','B')],tape)
        self.assertEqual(a,b)
    def test_parity_audit_flags_mismatch(self):
        raw={'records':[{'policy':'expert_auto','persona_id':'S','probe_id':'Q','prompt_tokens':500,'archive_record_count':16},
                        {'policy':'human_coded','persona_id':'S','probe_id':'Q','prompt_tokens':480,'archive_record_count':16}]}
        r=budget_audit.audit(raw)
        self.assertFalse(r['within_tolerance'])
        self.assertAlmostEqual(r['max_token_disparity'],0.04)
    def test_parity_audit_accepts_matched(self):
        raw={'records':[{'policy':'expert_auto','persona_id':'S','probe_id':'Q','prompt_tokens':500,'archive_record_count':16},
                        {'policy':'human_coded','persona_id':'S','probe_id':'Q','prompt_tokens':500,'archive_record_count':16}]}
        self.assertTrue(budget_audit.audit(raw)['within_tolerance'])
if __name__=='__main__':unittest.main()
