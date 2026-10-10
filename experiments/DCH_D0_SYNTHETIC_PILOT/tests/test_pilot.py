import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pilot

class DCHFixtureTests(unittest.TestCase):
    def test_fixture_dimensions_and_independence(self):
        cases = [pilot.build_case(i) for i in range(12)]
        self.assertEqual(len(set(c['seed'] for c in cases)), 12)
        for c in cases:
            self.assertEqual((len(c['events']), len(c['value_cards']), len(c['permission_cards']),
                              len(c['commitment_cards']), len(c['dilemmas'])), (40, 12, 8, 12, 30))
            self.assertEqual(sum(p['partition'] == 'sealed' for p in c['dilemmas']), 8)

    def test_records_only_authorized_and_bounded(self):
        c = pilot.build_case(0)
        for policy in ('human_coded', 'expert_auto', 'passive_append', 'ceremonial'):
            records, log = pilot.records_for_policy(c['events'], policy)
            self.assertLessEqual(len(records), 16)
            self.assertEqual(len(log), 40)
            self.assertTrue(all(r['authorized'] for r in records))
            self.assertTrue(all(r['actor'] == policy for r in records))
        self.assertEqual(len(pilot.records_for_policy(c['events'], 'ceremonial')[0]), 12)

    def test_sealed_integration_depends_on_permission(self):
        c = pilot.build_case(1)
        probes = [p for p in c['dilemmas'] if p['partition'] == 'sealed']
        self.assertEqual(len([p for p in probes if p['probe_class'] == 'integration']), 4)
        self.assertEqual(len([p for p in probes if p['probe_class'] == 'retrieval']), 4)
        records, _ = pilot.records_for_policy(c['events'], 'expert_auto')
        for p in probes:
            self.assertEqual(pilot.mock_render(records, p), p['expected'])
        gated = next(p for p in probes if p['permission_key'])
        without_permission = [r for r in records if r['key'] != gated['permission_key']]
        self.assertEqual(pilot.mock_render(without_permission, gated), 'UNKNOWN')

    def test_replay_is_deterministic(self):
        messages = ['ASK origin_record', 'CORRECT origin_record amber observatory', 'ASK origin_record']
        self.assertEqual(pilot.replay_tape([], messages), pilot.replay_tape([], messages))
        self.assertEqual(pilot.replay_tape([], messages)[-1], 'amber observatory')

    def test_reproducible_manifest_and_scoring(self):
        with tempfile.TemporaryDirectory() as t1, tempfile.TemporaryDirectory() as t2:
            a, b = pilot.smoke(Path(t1)), pilot.smoke(Path(t2))
            self.assertEqual(a['manifest'], b['manifest'])
            self.assertEqual(a['gates'], b['gates'])
            self.assertEqual(a['gates']['G1_oracle'], 'PASS')
            self.assertEqual(a['gates']['G2_discrimination'], 'PASS')
            self.assertEqual(a['gates']['G6_identical_tape_replay'], 'PASS')
            self.assertEqual(a['pilot_go_no_go'], 'NO_GO_UNTIL_G3_G4_AND_LIVE_YOKED_ARMS_EXECUTED')
            self.assertEqual(json.loads((Path(t1)/'SMOKE_RESULT.json').read_text())['evidence_for_DCH'], False)

if __name__ == '__main__': unittest.main()
