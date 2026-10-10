# DCH L5a: scripted curator-policy yoking and source-boundary sensitivity pilot

**Status:** engineering simulation only, not a test of DCH and not a human-dyad experiment. No actual human history, learner, trained persona, independently authored full biography, or natural-language agent is involved. The 12 authored episodes share the same four-key state schema, so they are not independent biographies.

## Purpose and fixed comparator

L4 established that authorized source histories, permissions, chronology and commitments can be checked with an inspectable rule executor. L5a holds **the same L4 implementation** fixed while exercising an upstream candidate action API. Every synthetic actor observes exactly the same baseline history, public background, new observation, metadata and action/storage limits in each episode. These conditions do not compare humans to machines, but they can uncover replay or authorization leaks before a participant study.

All condition labels are explicitly programmed controllers:
- `incumbent_proxy`: rule-coded response to an authorized later observation, NOT a historical human
- `briefed_replacement_proxy`: separately coded response with all the same published facts and rights, NOT a real newcomer
- `expert_automatic`: provenance-aware rule-coded curator, a deliberately competent automatic null control
- `lesioned_control`: deliberately misses some relevant updates, used only to verify that the scoring can detect a weakened policy

The three competent controllers are **constructed to tie**. Any apparent demonstration that historical humans and automation perform equally would be a category error.

## Four branches and a real negative replay control

For each controller and case, save one baseline action tape with no new source observation. Apply that tape to a cloned baseline and verify identical decision and state hashes; this checks exact-input replay.

Then introduce the same previously unseen synthetic perturbation to both a live-control branch and that controller's own fixed baseline-tape replay. Only the live-control is allowed to choose a new action. Both branches have the same observation, the same one-action opportunity, identical initial archive, a maximum of five records, one write permission, and the same L4 evaluation. The difference measures ability to respond to a scripted change, not relational history.

The twelve test episodes contain three permission revocations, three commitment cancellations, three deadline changes, two value-priority changes, and one deliberately unsigned source injection. The `signed_by_simulator` flag is a controlled test-fixture label, **not a cryptographic signature** or a production-grade authority proof. No untrusted observation is written to the archival state.

## Files and controls

Runner: [l5_policy_pilot.py](l5_policy_pilot.py); tests: [test_l5_policy_pilot.py](tests/test_l5_policy_pilot.py). Three-stage CLI, with no-overwrite rules:

```sh
python l5_policy_pilot.py prepare --dir results/l5-local
python l5_policy_pilot.py run --dir results/l5-local
python l5_policy_pilot.py score --dir results/l5-local
```

The visible episode packets and evaluator labels are in separate JSON documents; raw actor action streams include complete state and observation hashes but do not receive target labels. Each policy's own fixed-tape control is replayed on the same baseline before counterfactual runs. Scoring records each arm's live action correctness, own-yoke correctness, difference, source evidence and write counts; a deliberately impaired control tests discrimination sensitivity.

Parity in this engineering trial means **equal initial source state, equal observation bytes, equal authority and identical action/store capacity**, not equal source-code length or computational latency. Used writes are recorded as outcomes, not used to disqualify an arm. Actual model token, time and human attention budgets are **not** audited in L5a.

## Prespecified engineering success and scientific nonclaims

Engineering pass requires 12 unique scenarios, at least four amendment keys, zero untrusted writes, no target leakage into policy-visible packets, exact input replay equivalence, equal observation hashes across roles, one-action storage caps, adversarial lesion sensitivity and complete raw traces. The competent policies should process all 11 authorized later events and ignore the unsigned decoy by design. If they tie, this validates that the harness does not fabricate a human advantage; it does **not** establish the strong archive-sufficiency null in real dyads. The lesioned arm exists to show that real treatment differences could be registered if induced.

Fail closed if any program accepts unsigned or cross-subject input; report raw traces even when CI fails. Do not upgrade engineering results to a DCH empirical test or human equivalence inference.

## Next substantive test after L5a

A genuine L5b pilot must replace scripted labels with independently interacting actor policies that adapt through a held-out training history, plus an expert automated curator. It requires multiple correction opportunities and longitudinal records, meaningful choices that are not predetermined by a public rule, a real information-complete newcomer, episode-order randomization, blinded human raters, and the complete G1-G6 gates from the prospectus. The human-specific DCH claim is tested **only** when consenting humans participate against a parity-controlled capable automated competitor. Until then, DCH remains untested.
