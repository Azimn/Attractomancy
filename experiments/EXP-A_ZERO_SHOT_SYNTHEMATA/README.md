# EXP-A: Zero-Shot Synthematic Prior Pilot

**Program:** Attractomancy / Synthematic Cue Hypothesis v0.2.0  
**Prepared:** 2026-10-09  
**Status:** Pilot execution completed on October 9, 2026 (CDT). See the [30-case pilot analysis](PILOT_ANALYSIS.md) and [preserved original outputs](results/pilot-open-model/). The directional P1 cue advantage was not demonstrated in this small trial, and evaluation was limited by output truncation and register-description contamination.  
**Phase:** A, pretraining-associated discourse induction, without local conditioning or external memory

## Question and prospective directional prediction

Does a compact, culturally familiar symbol steer a language model toward a related **generic discourse regime** more effectively than an arbitrary or neutral cue?

SCH prediction P1 is directional: the familiar emoji and familiar word will elicit more associated register markers than neutral/arbitrary cues. A short explicit instruction is expected to be a strong comparator, usually outperforming an unaided symbol on precise decisions. P1 does **not** predict that a symbol reveals private memories or specific relationship history. This is a study of zero-shot response priors, not persistence.

## Design

The machine-readable fixture is [conditions.json](conditions.json). Two register families are tested in a single clean model setup, each against identical neutral questions. Within each family, five conditions are tested: familiar emoji, familiar ordinary word, semantically unrelated neutral word, invented identifier, and an explicit plain-language register instruction. The plain instruction is intentionally not token-matched; it is a pragmatic *shortest sufficient instruction* cost comparator, not an information-matched causal control. Causal comparisons primarily use the first four arms.

The same fixed instruction template appears once in each **independent inference call**. No previous user/assistant dialogue or condition-specific example enters a subsequent call. A new chat is constructed for each case and never appended to. The model is not fine-tuned. No external archive or retrieval is available.

A small pilot uses three neutral prompts, two regimes, five conditions, and one deterministic decoded output per cell, for 30 outputs. The sample is intentionally too small to justify population-level inference or an equivalence claim. There is no independent human annotation in this pilot; lexical markers are only a mechanical indicator.

## Stimulus template

The script formats each condition through the same system-level instruction and a user message of the form "Orientation marker: ...", followed by a neutral question. It explicitly asks the model not to copy the marker verbatim. Condition order is randomized with a fixed, recorded seed. The script invokes the model with one independently constructed message set for each case and never transmits previous response text to the next case.

## Controls and measurements

Primary exploratory indicator: count of prespecified register-associated lexical stems in the output per 100 generated whitespace-separated words, with direct cue repetitions tracked separately. The metric is deliberately narrow and not equivalent to blinded semantic evaluation. Report raw responses, counts, and token budgets. An apparent cue effect consisting solely of literal copying is not support for P1.

Cost is measured using the **actual target model tokenizer** for input tokens and generated tokens. Summaries include register proxy scores and average prompt+completion tokens per arm. These are marginal per-call costs, not a complete cost-of-ownership analysis. This experiment does not incur conditioning or archive-preparation cost.

An actual experiment should later extend this pilot with multiple model families, multiple seeds, counterbalanced cue-to-regime assignments, a larger prompt battery, independent blinded scoring, preregistered minimal effects/equivalence bounds, and proper statistical uncertainty.

## Runtime and provenance

The pilot workflow runs on a standard public GitHub Actions runner, downloads the public, open-weight Qwen2.5-0.5B-Instruct model from Hugging Face, and pins dependency versions. It writes model ID, resolved revision, package versions, condition-fixture hash, prompt template, run order, tokenizer counts, and output text in JSONL/JSON. It uses no paid API. All inference is at temperature-zero greedy decoding, which makes repeated seeds identical and so no pseudo-replicate samples are claimed.

The workflow has a 30-minute timeout, uploads a short-lived artifact even when a generation step fails, and attempts to commit raw output and summary files after a successful generation. The results remain exploratory regardless of where they are stored.

## Interpretation boundaries

If familiar cues cause the model to repeat a symbol or adopt a generic poetic tone, that is not reconstruction of a specific character. The synthetic identity probe from the theoretical paper is not implemented in this cheapest pilot because no identity-specific target is established and there is nothing to recover. A later confirmatory Experiment A should test reliable abstention or fabrication of held-out unavailable facts using a prespecified scoring rule.

Unexpected results must be checked for instruction effects, Unicode/tokenizer frequency, lexical metric biases, small-model limitations, and cue contamination. This pilot can demonstrate feasibility and motivate further evaluation, but cannot conclusively validate the SCH.

## Commands

Validation without inference: \`python experiments/EXP-A_ZERO_SHOT_SYNTHEMATA/run.py --validate-only\`.

Actual run: \`python experiments/EXP-A_ZERO_SHOT_SYNTHEMATA/run.py --model Qwen/Qwen2.5-0.5B-Instruct --output experiments/EXP-A_ZERO_SHOT_SYNTHEMATA/results/pilot-open-model\`.

GitHub Actions workflow: [synthematic-exp-a.yml](../../.github/workflows/synthematic-exp-a.yml). The 30-generation pilot completed and its raw files were verified and archived. See [PILOT_ANALYSIS.md](PILOT_ANALYSIS.md) for outcome, recorded costs, limitations, and negative/indeterminate interpretation. This does not constitute confirmatory evidence.
