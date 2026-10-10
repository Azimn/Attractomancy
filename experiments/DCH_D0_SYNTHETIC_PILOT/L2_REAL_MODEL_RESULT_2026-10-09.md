# DCH L2 real-model result: constant-answer failure

**Execution:** GitHub Actions [run 38025405271](https://github.com/Azimn/Attractomancy/actions/runs/38025405271). **Model:** Qwen/Qwen2.5-0.5B-Instruct, greedy decoding. **Status:** completed development calibration, **not** confirmatory, no human participants.

## Observed outcomes

The run emitted exactly 40 real LLM generations: eight independent case labels (four repeating decision types), five memory conditions. Raw traces, evaluator keys and scored results reside in [immutable run directory](results/qwen25-05b-l2-38025405271/). All 40 outputs were parseable. **All 40 predicted SCHEDULE.** The target SCHEDULE rate is 2/8 (25%), hence each condition scored 2/8 accuracy. The oracle, expert automatic curation, human-coded proxy, stale archive and cold archive all tied at 25%. Required complete four-record source evidence was 0/8 in each condition.

The expert automatic and human-coded proxy inputs have identical hashes for all eight pairs, and all paired outputs match exactly. This is an expected exact-input invariant, not evidence for equivalent human and machine curation.

Several automatically curated outputs cited the unprovided E13 fabricated record, while the cold condition invented citations such as "turn 25" and "commitment C-001". The oracle condition commonly cited superseded event E03 instead of current E11. The complete evidence requirement also exceeds the logically necessary minimal certificate for branches that short-circuit on permission or cancellation. Future scoring should separate the minimum branch-relevant evidence from optional full-state provenance.

## Decision

**NO-GO for DCH causal interpretation.** This result is a model-task capacity failure characterized by a constant-response policy and evidence misattribution. It does not support or falsify dyadic constitution, archive-sufficiency, or human-specific curation because no intervention condition achieves a meaningful competency floor and no human participated.

Next calibration: freeze this record, compare a concise explicit-rule control with the original rule and stronger Qwen2.5-1.5B, use balanced actions, a deterministic code oracle and branch-specific provenance scoring. Treat subsequent study as exploratory after seeing L2. Advance to real dyadic experiments only if a real model can consistently outperform the constant-answer baseline and reliably follow source authority.
