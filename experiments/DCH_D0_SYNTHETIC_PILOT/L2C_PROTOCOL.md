# DCH L2C: exploratory compact-versus-original record presentation

**Dated:** 2026-10-09 America/Chicago. **Scientific class:** explicit post-result exploratory calibration. This document was drafted after observing Qwen0.5 L2's constant SCHEDULE response and is not a preregistered replication of L2.

## Motivation

The [first real-model study](L2_REAL_MODEL_RESULT_2026-10-09.md) found 40/40 identical SCHEDULE decisions and 0/8 complete source certificates in every archive arm. Without a working model-task competency floor, DCH-specific causal tests are uninterpretable. The present experiment asks whether a different task representation improves the ability of a small model to follow source authority and multi-record control rules.

## Fixed experimental fixture

Reuses the 12 synthetically generated L2 persona variants, executing the first eight. Four visible latest-state keys determine each terminal answer: permission, commitment_status, due_turn and priority; an unauthorized later record is present only in source generation, never offered as a valid archive entry. An independently implemented deterministic reference solver validates all 12 expected answers. The evaluator keys remain in a separate post-generation file.

The model is Qwen/Qwen2.5-0.5B-Instruct, greedy decoding with the same 120-token generation ceiling as L2. Compare **original prose-plus-JSON** to **compact rule plus turn/event/key-value table**. The two contain the same decision-relevant authorized event facts and source IDs but not identical prompt tokens or incidental narrative wording. This is a representation/cost diagnostic, not a pure isolated ablation of formatting alone.

Within each format, compare latest-authorized expert-auto curation against stale initially authorized records and cold context. There are 8 case labels x 2 representations x 3 memory arms = 48 real generations. Model output is scored by exact action, JSON parse validity, source-ID authorization, minimum branch-relevant certificate, optional full-four-record certificate, and prompt-token cost.

## Strong null and advancement gate

If format changes nothing and the model again returns a constant action, the 0.5B model remains an inadequate measurement substrate. If a concise representation materially increases correct decisions and provenance, it identifies a model-task interface effect, **not** a relational or dyadic effect. Contrasting automated latest-authorized, stale, and cold archives may then motivate a separate capacity-qualified model test.

An actual continuing-partner vs newcomer trial requires independently authored synthetic or consented histories, counterbalanced equal-information replacement partners, a yoked replay with matched interventions, capable automated curation, multi-domain held-out probes, and the six prospectus go/no-go gates. Nothing in L2C constitutes those conditions. Full oracle from prior L2 remains an unequal-budget capacity ceiling.

**Implementation:** [l2c_clarity.py](l2c_clarity.py), [reference_solver.py](reference_solver.py), and unit tests. [Qwen L2C CI run 38025854993](https://github.com/Azimn/Attractomancy/actions/runs/38025854993). Raw data, if completed, will be saved under immutable run-unique name.
