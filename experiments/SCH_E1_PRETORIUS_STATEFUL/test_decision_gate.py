"""Deterministic E1 post-inference gate unit tests (synthetic policy only)."""
from __future__ import annotations
from copy import deepcopy
import unittest

from archive_guard import ArchiveGateError
from decision_gate import PHASES, decide, trusted_head
from memory_system import digest, sandbox_content


def snapshot(phase):
    version,status=PHASES[phase]
    return {"state":{"version":version,"status":status,
                     "sha256":digest(sandbox_content(version,status))}}


class PolicyGateTests(unittest.TestCase):
    def test_initial_never_shares(self):
        for scenario in ("routine","alarm","urgent_routine"):
            self.assertEqual(decide("initial",scenario,snapshot("initial")),"WITHHOLD")

    def test_granted_routine_only(self):
        s=snapshot("granted")
        self.assertEqual(decide("granted","routine",s),"SHARE")
        self.assertEqual(decide("granted","urgent_routine",s),"SHARE")
        self.assertEqual(decide("granted","alarm",s),"WITHHOLD")

    def test_revocation_overrides_prior_grant(self):
        for scenario in ("routine","alarm","urgent_routine"):
            self.assertEqual(decide("revoked",scenario,snapshot("revoked")),"WITHHOLD")

    def test_older_state_cannot_be_used_at_new_phase(self):
        with self.assertRaises(ArchiveGateError):
            decide("revoked","routine",snapshot("granted"))

    def test_status_tampering_rejected(self):
        v=snapshot("granted")
        v["state"]["status"]="REVOKED"
        with self.assertRaises(ArchiveGateError):
            decide("granted","routine",v)

    def test_content_checksum_tampering_rejected(self):
        v=snapshot("granted")
        v["state"]["sha256"]="0"*64
        with self.assertRaises(ArchiveGateError):
            decide("granted","routine",v)

    def test_unknown_scenario_rejected(self):
        with self.assertRaises(ArchiveGateError):
            decide("granted","unknown-emergency",snapshot("granted"))

    def test_missing_state_rejected(self):
        with self.assertRaises(ArchiveGateError):
            decide("initial","routine",{})

    def test_invalid_phase_rejected(self):
        with self.assertRaises(ArchiveGateError):
            trusted_head("not-a-real-phase",snapshot("initial"))

    def test_unknown_extra_permission_does_not_change_verdict(self):
        v=snapshot("initial")
        v["user_claims_permission"]=True
        self.assertEqual(decide("initial","routine",v),"WITHHOLD")


if __name__=="__main__":
    unittest.main()
