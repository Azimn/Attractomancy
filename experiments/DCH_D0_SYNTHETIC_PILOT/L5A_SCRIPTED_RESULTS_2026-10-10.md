# DCH L5a results: programmed live-versus-own-yoke sensitivity

**Executed:** October 10, 2026. **Evidence class:** deterministic simulation, not a human-dyad study or DCH efficacy test. **CI:** [run 38060883230](https://github.com/Azimn/Attractomancy/actions/runs/38060883230), completed successfully. **Sources:** [l5_policy_pilot.py](l5_policy_pilot.py), [L5a protocol](L5A_SCRIPTED_REPLAY_PROTOCOL.md), [ten L5a tests](tests/test_l5_policy_pilot.py). **Raw artifacts:** [results/l5a-scripted-38060883230/](results/l5a-scripted-38060883230/).

## Verified numeric observations

Twelve authored synthetic episodes share a common four-key state machine and are **not twelve independently authored biographies**. The counterfactual schedule has 11 simulator-authorized updates (three permission revocations, three commitment cancellations, three deadline changes and two priority revisions) plus one unsigned adversarial decoy. There are four *scripted* curator roles, hence 48 actor/episode trajectory sets. Each includes an unperturbed baseline, a strict identical-input own-tape replay, a live post-perturbation policy and a perturbed own-tape replay.

| Scripted role | Live accuracy | Perturbed own-tape replay accuracy | Live-minus-yoke | Live authorized writes |
| --- | ---: | ---: | ---: | ---: |
| incumbent_proxy | 12/12 | 1/12 | 11/12 | 11 |
| briefed_replacement_proxy | 12/12 | 1/12 | 11/12 | 11 |
| expert_automatic | 12/12 | 1/12 | 11/12 | 11 |
| lesioned_control | 7/12 | 1/12 | 6/12 | 6 |

All 48 baseline exact-tape equivalence checks passed. All roles saw hash-identical new observations and initial authorized archives per scenario, with one decision opportunity, one permitted authorized write and a five-record storage cap. The four decision labels span privacy, commitment termination, rescheduling and changed value priority. Raw trace fields include proposal/action origin, applied source IDs, action-status, model-independent gate decisions and source evidence certificates. No real language model or human participant made any of the choices.

The lesioned controller was **coded to ignore** permission and priority updates, accounting for its five failures. The three competent controllers were **coded to implement equivalent update rules**, explaining their tie and 11/12 positive own-replay deltas. These data validate replay/repair sensitivity and reject neither a human-specific nor an automated-archive-sufficiency hypothesis. A fixed tape that cannot respond to a newly introduced event is not a well-informed adaptive replacement partner. Its worse counterfactual performance is expected by construction.

## Limitations and next gate

The source provenance label `signed_by_simulator` is an engineered Boolean fixture annotation, not a cryptographically authenticated external event; it should not be exposed as authority in a real participant system without a trusted server-side source ledger. The action budgets are identical, but deliberation time, model tokens, and participant training expenditure are not measured. Each case contains one intervention opportunity, not the long-term interactive histories required by DCH. All four roles are algorithms, not living partners; even `incumbent_proxy` is only an instrumentation label.

**Advancement:** L5a passes its narrow engineering checks. The overall DCH G1–G6 remain NO-GO, and no human-specific claim has been tested. L5b should introduce an independently held trusted-event registry, actor action-only interface, nontrivial multi-event histories, independently authored biographies, a trainable or experimentally interacting policy, a strong information-equivalent automated curator, and real matched-budget/live-yoked comparisons before approaching volunteer human participants.

No claims about subjectivity, consciousness, or unique metaphysical continuity follow from these observations.
