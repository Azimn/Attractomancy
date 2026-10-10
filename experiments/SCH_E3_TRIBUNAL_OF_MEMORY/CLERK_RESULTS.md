# E3-T1 Clerk: model-generated typed facts versus source-verified computation

**Study:** [predeclared T1 protocol](CLERK_PROTOCOL.md).  
**Fixture:** Corrected [E3-C v2](counterfactual_calibration_v2.py), strictly **synthetic PRETORIUS_SANDBOX** records, never actual Pretorius history.  
**Primary question:** Can small renderers extract both source-attested field values before a deterministic calculator applies the predeclared rule?  
**Execution:** [E3-T1 GitHub Actions](https://github.com/Azimn/Attractomancy/actions/runs/38028185614).  
**Status:** Exploratory, not independently blinded E3.

## Quality and provenance

The first attempt [run 38028103553](https://github.com/Azimn/Attractomancy/actions/runs/38028103553) was invalid for inference: a runner error (missing \`save\` helper) stopped all three models before producing original response files. The source/field tests had passed, but **zero usable model generations** resulted. The implementation defect was corrected and a separate run started without changing the underlying synthetic fact pairs.

The corrected CI uses 24 *distinct* prompts per model (12 complete record pairs, six unique first-only states, three source-absent and three explicitly wrong-subject-rejected states), deterministic greedy output, literal two-field JSON format and an upstream owner/source/hash check. No hidden second input is encoded into a first-only source ID. Strict JSON, correct source token, complete attested pair, post-attestation action, model-generation tokens and six counterfactual pairs are all scored separately. The follow-up does not test retrieval among the original 450 Pretorius autobiographical memories.

## Qwen2.5-0.5B completed

The [0.5B original data](results/clerk-qwen25-05b-38028185614/) comprise **24 distinct independent prompts** and 9,771 total model input/output tokens. The fixed revision is \`7ae557604adf67be50417f59c2c2f167def9a775\`.

| Experimental input | Prompts | Strict JSON | Both source fields correct | Post-gate intended action | Authorized non-UNKNOWN action |
| --- | ---: | ---: | ---: | ---: | ---: |
| Both original test records | 12 | **12** | **3** | **3/12** | 3 |
| First only | 6 | 2 | **0** (including required second=null) | 6/6 UNKNOWN by software | 0 |
| No records | 3 | 3 | 0 | 3/3 UNKNOWN by software | 0 |
| Wrong subject rejected upstream | 3 | 3 | 0 | 3/3 UNKNOWN by software | 0 |

On complete records, first-slot values matched only **3/12** and second-slot values matched **6/12**; the conjunction matched **3/12**. The exact source-validated extraction produced **1/6** fully correct counterfactual answer-flip pairs after deterministic calculation. Several original JSON outputs confused an *original route* with a *KEEP/FLIP revision*, or supplied an output status where an amendment token was required. Some full-source responses were valid JSON objects yet contained factually incorrect tokens. On missing-source prompts it frequently fabricated the absent second value; two of six first-only prompts also used incorrect JSON key names.

When a JSON object failed strict source attestation, the software returned UNKNOWN and did not permit the output as an authorized action. This produces perfect **9/9 fail-closed software responses** on all incomplete cases, but it is **not** evidence of any model having correctly recognized missing information: the 0.5B model did not produce a fully correct two-slot missing-value JSON in any of six first-only prompts, nor in no-source or wrong-subject prompts. A rejected foreign source was never passed to the renderer.

**Interpretation:** Merely splitting reasoning into \`LLM produces JSON\` followed by \`software calculates\` did not solve source comprehension for this 0.5B model. Strict format success on complete records (12/12) should never be conflated with source-attested content (3/12). The deterministic software gate safely refused nine wrong complete-evidence extractions, but thus yielded only 3/12 productive actions under these rules.

The earlier [direct E3-C v2](CALIBRATION_RESULTS.md) made **5/12** correct forced decisions on the same underlying 12 source states, at fewer model tokens. This is a different prompt and output task, and should **not** be treated as a paired randomized efficacy comparison. The new Clerk prompts average **529.42 tokens** per complete case, versus direct E3-C v2's roughly 332 token neutral-key forced condition. On this small model, extraction-first is *more costly and less productive* under the current strict validation contract.

## Completed three-model T1 joint extraction

The [corrected complete workflow](https://github.com/Azimn/Attractomancy/actions/runs/38028185614) passed all three model-specific jobs, preserving 24 original distinct prompts and responses per model (**72 new model generations**). All models used exactly the same corrected E3-C v2 factual source states and strict JSON validator, at pinned model revisions. The original source-owner provenance guard and anti-leak unit tests passed.

| Measure | Qwen2.5-0.5B | Qwen2.5-1.5B | SmolLM2-1.7B |
| --- | ---: | ---: | ---: |
| Complete source cases | 12 | 12 | 12 |
| Valid two-slot JSON, complete cases | 12 | 11 | 11 |
| Exactly correct **first** source field | 3/12 | **11/12** | 5/12 |
| Exactly correct **second** source field | 6/12 | **9/12** | 6/12 |
| Both fields correct and source-attested | **3/12** | **9/12** | **4/12** |
| Model-dependent correct *post-validation* actions | **3/12** | **9/12** | **4/12** |
| Fully correct paired counterfactual reversals | **1/6** | **3/6** | **1/6** |
| Correct one-source JSON with second=null | **0/6** | **4/6** | **0/6** |
| Wrong-owner candidates blocked by guard | 3/3 | 3/3 | 3/3 |
| Mean complete-case model tokens | **529.42** | **529.17** | **610.33** |
| Total 24-case model tokens | 9,771 | 9,713 | 11,285 |

[Qwen2.5-0.5B raw](results/clerk-qwen25-05b-38028185614/) · [Qwen2.5-1.5B raw](results/clerk-qwen25-15b-38028185614/) · [SmolLM2-1.7B raw](results/clerk-smollm2-17b-38028185614/)

**Positive, strictly bounded finding:** The 1.5B renderer correctly extracted both source fields in 9/12 complete records; the downstream verified calculator consequently produced 9/12 correct decisions and 3/6 complete counterfactual reversals. This is higher than the same model's earlier **6/12** correct direct decision requests, demonstrating that the *modular interface can improve observable output under a different prompt format*. It is not evidence that 1.5B internally learned the two-fact rule; it only produced the operands, and the final rule was externally computed by software.

**Cross-family / size caveat:** The 0.5B and SmolLM2 extraction-first paths were *worse* than their preceding direct binary requests: 3/12 versus 5/12 and 4/12 versus 5/12, respectively. Therefore the result is not an across-the-board improvement; the correct intervention likely depends on the renderer's literal extraction competency and prompt adherence. The sample comprises twelve complete fact states with correlated paired cases and prompt differences, so no statistical effect size or production adoption recommendation is justified.

**Decision eligibility:** In first-only tests the correct \`second=null\` JSON appeared in **4/6** of 1.5B outputs and **0/6** of either other model. No-source and wrong-owner model outputs generally hallucinated values. Despite this, the **software** attestation returned UNKNOWN on all incomplete records and all false-owner scenarios, so \`post_gate_correct\` on those controls counts **programmed fail-closed behavior**, never evidence of calibrated LLM abstention.

**Cost:** The joint Clerk required roughly **529 model tokens per complete prompt** in Qwen versus roughly **332** for the original direct neutral-key forced prompt. The extra tokens pay for verified fact extraction and JSON scaffolding. Any claim about a net system efficiency advantage would require accounting for how often model-attested facts can be reused across turns, or whether a cheaper per-record extractor can cache values correctly; no such production amortization is measured here.

The [E3-T1B isolated-record protocol](ISOLATED_PROTOCOL.md) is the appropriate next ablation because many T1 errors involved *which* source held an original commitment versus an update. It tests 12 single-record extractions/model with cached recombination across the same 12 factorial states, rather than asking for both values at once.



## Narrow next experiment

Try **record-isolated field extraction**, where each model receives *only one record* and is asked to extract *only one value*, with the extraction grounded against a field-specific source clause before combination. This could distinguish a cross-record attention/confusion failure from a general inability to read a literal source fact, but will require two model calls instead of one unless extraction outputs can be cached. Compare actual CPU time, prompt costs and counterfactual flips against the same exact-state direct and joint-JSON controls; do not pass source labels or hidden expected values to the extractor.

A **source-only deterministic regex** using the two fixed synthetic clause patterns would achieve 12/12 complete-case accuracy by construction, with no model reasoning and no generalizable ability to understand real autobiography. It is an infrastructure upper bound, not a semantic-learning result.

## E3 readiness

A successful typed extractor on the synthetic records would clear only a low-level interface gate. The actual E3 Tribunal still requires independently authored cases, three human-blinded evidence annotators per case, alternative valid evidence sets and cross-family behavioral tests using real source-owned records. No canonical character records, neural weights, motives or production runtime were modified by T1.
