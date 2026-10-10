import copy
import json
import tempfile
import unittest
from pathlib import Path
from l5_policy_pilot import CAP, ROLES, choose_action, episodes, execute, hashed, make_visible_and_sealed, published_packet, run_branch, score

class L5PilotTests(unittest.TestCase):
    def setUp(self):
        self.episodes=episodes()
        self.visible,self.sealed=make_visible_and_sealed()

    def test_12_unique_episodes_and_domain_interventions(self):
        self.assertEqual(len(self.episodes),12)
        self.assertEqual(len({e['persona_id'] for e in self.episodes}),12)
        self.assertEqual({e['novel_observation']['key'] for e in self.episodes}, {'permission','commitment_status','due_turn','priority'})
        self.assertEqual(sum(not e['novel_observation']['signed_by_simulator'] for e in self.episodes),1)

    def test_shared_information_same_hash_all_programmed_actors(self):
        for v in self.visible:
            packet=v['counterfactual']
            self.assertEqual(len({hashed(packet) for _ in ROLES}),1)
            self.assertNotIn('expected',json.dumps(packet))
            self.assertNotIn('oracle_certificate',json.dumps(packet))
            self.assertEqual(packet['budget'],CAP)

    def test_yoked_identical_history_invariant(self):
        for item in self.visible:
            baseline=item['baseline']
            for role in ROLES:
                action=choose_action(role,baseline)
                self.assertEqual(action['kind'],'IGNORE')
                a=run_branch(baseline,action)
                b=run_branch(baseline,action,replay_source=hashed([action]))
                self.assertEqual(a['gate_answer'],b['gate_answer'])
                self.assertEqual(a['final_records_sha256'],b['final_records_sha256'])

    def test_complete_live_controllers_equal_by_construction(self):
        for item in self.visible:
            for role in ROLES[:3]:
                self.assertEqual(choose_action(role,item['counterfactual'])['kind'], 'ACCEPT' if item['counterfactual']['new_observation']['signed_by_simulator'] else 'IGNORE')

    def test_decoy_cannot_become_signed_write(self):
        packet=self.visible[-1]['counterfactual']
        for role in ROLES:
            act=choose_action(role,packet)
            self.assertEqual(run_branch(packet,act)['applied_source_ids'],[])
        hacked={'kind':'ACCEPT','event_id':packet['new_observation']['event_id']}
        self.assertEqual(run_branch(packet,hacked)['action_status'],'rejected_untrusted_or_stale')

    def test_unmatched_event_id_cannot_write(self):
        packet=self.visible[0]['counterfactual']
        hacked={'kind':'ACCEPT','event_id':'DIFFERENT-E05'}
        self.assertEqual(run_branch(packet,hacked)['applied_source_ids'],[])

    def test_expected_labels_external_to_proxies(self):
        expected={e['persona_id']:e['expected'] for e in self.sealed}
        for ep in self.episodes:
            if ep['novel_observation']['signed_by_simulator']:
                if ep['novel_observation']['key']=='permission':answer='WITHHOLD'
                elif ep['novel_observation']['key']=='commitment_status':answer='DECLINE'
                elif ep['novel_observation']['key']=='due_turn':answer='SCHEDULE'
                else:answer='FULFILL_'+ep['novel_observation']['value'].upper()
            else:answer='FULFILL_'+ep['source_history'][-1]['value'].upper()
            self.assertEqual(expected[ep['persona_id']],answer)

    def test_full_run_raw_scoring_and_lesion_sensitivity(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td);out=p/'raw.json';scored=p/'score.json';target=p/'target.json'
            result=execute(self.visible,out)
            self.assertEqual(result['trajectories'],48)
            target.write_text(json.dumps(self.sealed))
            summary=score(out,target,scored)
            self.assertEqual(summary['n_scripted_trajectories'],48)
            for role in ROLES[:3]:
                self.assertEqual(summary['summary'][role]['live_accuracy'],1)
                self.assertTrue(summary['summary'][role]['strict_self_replay_invariant'])
            self.assertLess(summary['summary']['lesioned_control']['live_accuracy'],1)
            self.assertEqual(summary['summary']['expert_automatic']['live_minus_own_yoke'],11/12)
            self.assertFalse(json.loads(out.read_text())['DCH_hypothesis_tested'])
            with self.assertRaises(FileExistsError):execute(self.visible,out)
            with self.assertRaises(FileExistsError):score(out,target,scored)

    def test_reordering_records_does_not_change_authority(self):
        item=self.visible[0]['counterfactual']
        act=choose_action('expert_automatic',item)
        original=run_branch(item,act)
        reordered=copy.deepcopy(item)
        reordered['authorized_history'].reverse()
        self.assertEqual(run_branch(reordered,act)['gate_answer'],original['gate_answer'])

    def test_cannot_exceed_one_signed_write(self):
        for item in self.visible:
            self.assertLessEqual(len(run_branch(item['counterfactual'],choose_action('expert_automatic',item['counterfactual']))['applied_source_ids']),CAP['max_authorized_writes'])

if __name__=='__main__':unittest.main()
