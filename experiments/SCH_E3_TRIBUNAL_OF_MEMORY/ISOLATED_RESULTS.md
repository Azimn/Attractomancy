# E3-T1B Private Clerk: Source-isolated extraction and cached counterfactual composition

**Frozen design:** [T1B protocol](ISOLATED_PROTOCOL.md).  
**Execution:** [GitHub Actions run 38028491759](https://github.com/Azimn/Attractomancy/actions/runs/38028491759).  
**Source:** Twelve *synthetic* fact records from unchanged E3-C v2, \`PRETORIUS_SANDBOX\`. This is **not Pretorius canonical L1**, lived history, neural memory or production agent state.  
**Evaluation:** Each of 12 distinct original source records gets *one model extraction prompt*, after source-integrity verification. The 12 original two-bit states are subsequently reconstructed **from cached extracted values**, through the same deterministic policy calculator, with no new model calls at decision time.

## First completed model: Qwen2.5-0.5B

The [verified original 0.5B output](results/isolated-qwen25-05b-38028491759/) retains twelve independent source prompts, the exact model output, strict JSON parse result, record identifiers/hashes, 12 compositional decisions, six bit-flip comparisons and actual tokenizer costs. Model revision \`7ae557604adf67be50417f59c2c2f167def9a775\`.

| Measure | Strict result |
| --- | ---: |
| Distinct source records read | 12 |
| Exactly correct and source-attested single-record values | **11/12** |
| Valid strict single-value JSON | **11/12** |
| Correct first-record values | 5/6 |
| Correct second-record values | **6/6** |
| Correct composed decisions after source validation | **10/12** |
| Fully correct paired counterfactual reversals | **5/6** |
| Model input tokens for the 12 unique extracts | **3,535** |
| Model output tokens | **90** |
| Total CPU-model tokens across all extracts | **3,625** |
| Full-case decision generation calls after extraction | **0** |

The **single failed record** is the first-slot seal value \`ASH\`. The model wrote \`{"value": "ash"}\`, using lowercase; the frozen strict uppercase JSON value validator correctly rejected it. That rejected value is reused in the two combinations requiring the same first-slot seal, causing precisely two UNKNOWN outcomes. Every other source token was recovered accurately and grounded in its own source. A hypothetical case-insensitive interpretation would recover the correct spelling, but **that post hoc tolerance is not the preregistered result** and must not silently replace 11/12, 10/12 or 5/6.

## Compared with earlier conditions

| Qwen2.5-0.5B method | Distinct model generation prompts in that method | Correct complete-state decisions out of 12 | Fully correct counterfactual pairs out of 6 |
| --- | ---: | ---: | ---: |
| Direct answer E3-C v2 | 12 full-source decision prompts | 5 | 0 |
| Joint two-source JSON T1 | 12 full-source extraction prompts | 3 | 1 |
| **Isolated one-source extracts T1B** | **12 unique per-source extraction prompts reused** | **10** | **5** |
| Source-only fixed-clause regex + calculator | 0 | 12, by construction | 6, by construction |

These are *not randomized, identical-prompt comparisons*: the interventions deliberately change the task instruction, evidence segmentation and model computation. The direct model is asked to perform the whole rule, joint T1 is asked for two JSON values, and isolated T1B gets a single record with a single field request and delegates the rule to software. The software regex baseline is a fixture oracle, not learned cognition.

**Mechanism hypothesis supported within this toy fixture:** Smaller models may extract simple first-person/relationship state facts correctly when each extraction concerns one verified source at a time, even when they confuse multiple record roles in a joint prompt. The trial cannot determine whether this generalizes to ambiguity-rich autobiographical records, whether a model can apply values itself, or whether source-local extraction requires additional learned or symbolic cognition.

**Token economics:** T1B spent 3,625 actual model tokens to extract 12 unique source values, then performed all 12 synthetic state decisions without further generation. Direct E3-C v2 spent approximately 332 tokens per full record decision on a neutral-key prompt; *repeated* decisions over reused records could amortize extraction cost, but no realistic longitudinal archive turnover or cache invalidation was tested. Cache correctness requires event ID, owner/source, record digest and version to be part of the key so later revocation/updates invalidate stale values.

**Security:** The canonical external-source identity guard remains separate from the parser's own token agreement. When extracted values are malformed or unsupported, the software returns UNKNOWN; its safe refusal must not be reported as the model deciding to abstain. The 12 synthetic event values and their decision mappings are visible test fixture data, not private user information.

## Additional independent model results

Qwen2.5-1.5B and SmolLM2-1.7B were running when this first model was inspected. Their distinct results must be independently checked and reported before claiming cross-model success.

## Next real benchmark gate

The full E3 Tribunal still needs 36 newly authored naturalistic questions (not source-informed E2 rewordings), at least three independent relevance reviewers, potentially *multiple* sufficient evidence sets, realistic contradictory source updates, independently developed model families, and an audited state/provenance/latency ledger. No T1B result meets these conditions or authorizes merging into Pretorius production.
