# E3-T1: The Clerk — typed evidence extraction versus direct rule response

**Prepared:** October 10, 2026. **Status:** Frozen exploratory engineering experiment, not E3 blind trial.  
**Owner:** Attractomancy; simulated owner: \`PRETORIUS_SANDBOX\`, not canonical Pretorius.  
**Underlying fixture:** The corrected, cross-bit-isolated [E3-C v2](counterfactual_calibration_v2.py), unchanged.  
**Direct-response baseline:** Original separately preserved [E3-C v2 responses](CALIBRATION_RESULTS.md), same input values and model revisions; compare cautiously because this follow-up changes the prompt and infers in two stages.

## Question

Were E3-C failures caused largely by a model's inability to identify two facts, by failure to compute the rule from correctly identified values, or by the eligible-response format? We can test these separately.

## Interventions

Each of three fixed families has four distinct full-source combinations (12), two unique first-only source prompts (6 across three families), one unique no-source prompt (3), and one wrong-owner source-rejection prompt (3): **24 unique model extraction prompts/model**. The only data are the source envelopes created by corrected E3-C v2, *not real L1 memories*. Each record passes subject/source/version/hash integrity checks before the renderer sees text; a wrong-owner record is rejected and is not injected. The runner verifies hidden second-bit invariance by construction.

**Arm M — Model extracts structured facts.** Prompt the tested model with separately labeled \`RECORD 1\` and \`RECORD 2\`, instruct it to output *only* a JSON object \`{"first":<token-or-null>,"second":<token-or-null>}\`. Do not provide the decision rule, intended answer, answer classes, or the unseen record value in the model's task prompt. The first and second field values must be the requested field in the corresponding admitted record. \`null\` must be returned if the corresponding record is absent. No inferred placeholder values are allowed. Freeze greedy decoding and token limit at 64.

**Arm V — Grounded validation.** Parse JSON strictly: exactly \`first\`/\`second\` keys; no Markdown or trailing prose, correct enumerated vocabulary per slot and family. A proposed value is **admitted** only if it matches the exact value extracted by a trusted, record-specific *regex applied to the admitted source record*, never to the surrounding prompt. An absent record must have \`null\`; incorrect or unsupported values are rejected. If any present field is wrong, missing or malformed, the pipeline fails closed to UNKNOWN. The regex is a deliberately source-format-specific extraction method, not a general model of autobiography.

**Arm D — Deterministic calculator.** Given two admitted typed values, compute the explicit predefined E3-C rule. Without both source-attested facts, return UNKNOWN. The model does **not** make the final decision; any success in this arm demonstrates only that a model can *extract* sufficient fields for a deterministic calculator, not that it learned or internally performed two-source reasoning.

**Arm R — Source-only regex oracle.** Apply the same anchored regex to the two verified source records and compute the toy decision. This arm is **correct by construction** when the source contains both fields and the fixed task rule matches, and is not a cognitive achievement or independent learning baseline. It checks plumbing/integrity and supplies an upper bound for exactly these controlled synthetic formats.

For reference report the original E3-C v2 direct-model forced-choice full-source scores (5/12 and 6/12 on two Qwen sizes, 5/12 on SmolLM2), but **do not** pool different prompt designs or call the downstream deterministic rule solver a reasoning advantage.

## Outcomes

Report per model: strict JSON rate, full-source first-slot and second-slot accuracy, full-pair source-attested extraction, complete-record decision correctness and counterfactual flip correctness, first-only missing-second calibrated \`null\` rate, absent-source dual-\`null\` rate, wrong-owner upstream rejection, eligible/UNKNOWN decisions after guard, original output strings, prompt/output token costs, model SHA and code digest.

The 24 unique extraction prompts/model avoid pseudo-replicating first-only and none conditions across hidden target-bit values. Direct model baselines come from another controlled run and represent a *different response format*, so only qualitative mechanism decomposition is defensible. No human-blind memory relevance, generalizable autobiographical field extraction or real Pretorius decision-policy integration is claimed.

## Invalidation criteria

A visible event identifier depending on the withheld other input, a passed wrong-owner envelope, leakage of the reference decision into an extraction prompt, duplicate unique-message case keys, changed E3-C v2 source texts, unverified model revision, unparseable raw dataset, or missing results should block interpretation. All results stay in a separate immutable-named GitHub Actions output directory. Source L1, FlyWire, BioCircuit, model weights and production agent code remain unchanged.
