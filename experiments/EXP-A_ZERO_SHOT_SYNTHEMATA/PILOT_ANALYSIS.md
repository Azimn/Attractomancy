# EXP-A Pilot 001: Zero-shot cue-associated discourse, Qwen2.5-0.5B-Instruct

**Completed:** October 9, 2026 (CDT); execution logs dated October 10, 2026 (UTC)  
**Run:** [GitHub Actions generation run 38013536840](https://github.com/Azimn/Attractomancy/actions/runs/38013536840)  
**Artifact recovery:** [Preservation run 38013884084](https://github.com/Azimn/Attractomancy/actions/runs/38013884084)  
**Status:** Completed exploratory **pilot**, not confirmatory experimental evidence  
**Interpretation:** P1's proposed familiar-cue advantage is **not demonstrated** in this small pilot. No claim is made that P1 has been statistically falsified.

## Primary result

The run generated **30 independent responses** from Qwen2.5-0.5B-Instruct at model commit \`7ae557604adf67be50417f59c2c2f167def9a775\`. There were two discourse-regime targets, five cue/control arms each, and three neutral questions per arm. A fresh two-message context was constructed for each deterministic, greedy-decoded generation. No prior messages, persona archive, retrieval tool, fine-tuning, or private identity material was available to the model. Fixture validation and all 30 generations completed successfully. A separate GitHub Actions job verified and archived the original JSONL response file, manifest, and numerical summary after the generation job's final Git push was rejected because the repository had moved.

The original *mechanical lexical proxy*, counting preregistered register-related stems per 100 output words, was:

| Discourse target | Arbitrary name | Neutral word | Familiar emoji | Familiar word | Explicit plain instruction |
| --- | ---: | ---: | ---: | ---: | ---: |
| Recursive-reflective | 0.000 | 0.000 | 0.000 | 0.000 | 3.865 |
| Mythic-ceremonial | 1.990 | 0.813 | 0.995 | 1.235 | 3.384 |

Each cell has **n = 3 prompts**, with only one deterministic generation per prompt. These are descriptive means of a narrow lexical measure, not unbiased estimates of stylistic fidelity.

The *directional P1 prediction* was that familiar cues would outperform arbitrary and neutral markers on associated generic register features. In this pilot, they **did not reliably do so**. The familiar cues produced no marker hits in the recursive-reflective regime. In the mythic-ceremonial regime, the arbitrary name scored higher than either familiar cue. The explicit prose instruction received the largest original lexical score in both regimes, but this result is vulnerable to instruction-word copying and metalinguistic description rather than actual adoption of the requested style.

## Execution provenance and cost

The recorded model is \`Qwen/Qwen2.5-0.5B-Instruct\`, revision \`7ae557604adf67be50417f59c2c2f167def9a775\`, with Transformers 4.51.3, PyTorch 2.5.1+cpu, Python 3.11.17, and greedy decoding. Fixture SHA-256: \`1ee2adcf4378fb8065d68aae14ec7aa5ad049b2c8429c65f6f9d500f35d1d8f2\`. Total generated tokens were **2,635**, total prompt tokens **2,384**, and total marginal input/output tokens **5,019** over 30 cases. Model-run elapsed time was **226.73 seconds**, including initialization. No paid inference API was used; the run used a standard runner in a public GitHub repository.

Average *total tokens per response* ranged from about 164 to 172 across arms. In the recursive-reflective regime, the explicit instruction consumed approximately 171.67 input-plus-generated tokens, versus 166.67 for the familiar emoji. In the mythic-ceremonial regime the same means occurred. These small differences do **not** establish a cost-quality advantage because the lexical proxy does not yet validate actual regime adherence. There was no archive and no upfront cue-conditioning cost in this experiment.

## Important measurement failures

**Output-length censoring.** **29 of 30 outputs hit the 88-token maximum**. Many responses ended mid-explanation. The apparent difference between arms could reflect which parts of an answer were emitted before truncation, and the corpus is unsuitable for strong register or quality comparisons.

**Metalinguistic contamination.** Several outputs described the assigned orientation marker or instructed the imaginary archivist to use a named register rather than actually speaking in that register. A post-run heuristic scan found **8 of 30** responses potentially referring metalinguistically to an orientation marker, register, or explicit approach. This heuristic is not a validated human coding instrument. At least **4** non-instruction cases reproduced the cue text despite a request not to. Exact copies must not be awarded semantic-induction credit.

**Lexical proxy and direct cue wording.** The original proxy cannot distinguish stylistic enactment from mentioning a word such as "recursive" or "ceremonial." It may undercount legitimate semantic analogues and reward copied instruction language. A transparent *post hoc sensitivity check*, excluding lexical marker words present in the input cue or explicit instruction from output hits, reduces the plain-instruction means to approximately **0.97** for recursive-reflective and **1.28** for mythic-ceremonial. The mythic arbitrary-name mean remains approximately **1.96**. This post hoc calculation is diagnostic only, not a substitute confirmatory endpoint. It does not establish an alternative ranking, especially with n = 3 per cell.

**No target-specific identity measure.** This phase deliberately tests generic discourse induction. There was no fictional autobiographical dossier to retrieve, so the pilot neither supports nor refutes SCH predictions about recovery of private character information after a reset.

**Model and design dependence.** One small, instruction-tuned model was tested with one question template, three tasks, one generation per cell, and an arguably ambiguous concept of "orientation marker." Symbol familiarity and intrinsic semantic relevance were not independently rated. Familiar and arbitrary cue lengths were measured but not matched for tokenizer segmentation. The explicit-instruction arm differs in informational content by design and is a practical engineering comparator, not a causal effect-isolation control.

## Decision

The correct initial reading is a **negative or indeterminate feasibility result** for simple zero-shot synthematic steering in this tested setup. Do not cite this as confirmation that compact cultural symbols recruit a stable hidden identity structure. The theoretical P1 expectation should remain a *prospective claim*, explicitly challenged by this pilot rather than rewritten to make the result appear positive.

Before a confirmatory Experiment A, freeze a revised protocol that uses meaningfully shorter output requests with a larger completion cap, prohibits and separately scores explanation of the marker, and replaces the lexical proxy with blinded ratings of enacted discourse rather than words about discourse. Counterbalance symbols among target regimes, include a truly matched neutral/nonce cue, and introduce a shortest sufficient instruction optimized on development prompts. Conduct several independent stochastic or paraphrase repetitions, then scale to more than one renderer. Predefine the minimum effect, quality threshold, token-cost frontier, and how a null or opposite-direction result will be classified. Preserve the original fixture and results unchanged.

The next experiment should use a new versioned fixture and result directory. **Do not edit or overwrite the 30 original responses, manifest, or summary.**

## Immutable study artifacts within the repository

Original pre-run fixture: [conditions.json](conditions.json)  
Original generation script: [run.py](run.py)  
Raw outputs: [responses.jsonl](results/pilot-open-model/responses.jsonl)  
Model and fixture provenance: [manifest.json](results/pilot-open-model/manifest.json)  
Numerical aggregate: [summary.json](results/pilot-open-model/summary.json)  
Original experimental procedure: [README.md](README.md)

**Evidence boundary:** This record reports directly generated model text and calculations on that text. It makes no claim of machine consciousness, durable hidden state, spiritual efficacy, or successful persona reconstruction.
