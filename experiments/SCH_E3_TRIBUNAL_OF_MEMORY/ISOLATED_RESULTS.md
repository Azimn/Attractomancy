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

## Complete three-model isolated-extraction comparison

The [T1B GitHub Actions workflow](https://github.com/Azimn/Attractomancy/actions/runs/38028491759) completed successfully on **all three models**, preserving 12 original, independent source-only prompts for each model (**36 new model generations**) and the 12 software-composed synthetic state decisions per model. The synthetic source, fixed document IDs, local-bit isolation checks, original model revisions and scoring rules are shared across the three runs.

| Strict measure | Qwen2.5-0.5B | Qwen2.5-1.5B | SmolLM2-1.7B |
| --- | ---: | ---: | ---: |
| Model extracts exact, source-attested single-record value | **11/12** | 8/12 | **10/12** |
| First-slot record values correct | 5/6 | 4/6 | 5/6 |
| Second-slot record values correct | 6/6 | 4/6 | 5/6 |
| Strict single-value JSON | 11/12 | 12/12 | 12/12 |
| Source-attested software-composed decisions correct | **10/12** | 6/12 | 8/12 |
| Correct paired counterfactual reversals | **5/6** | 2/6 | 3/6 |
| Total model tokens for 12 extraction calls | **3,625** | 3,609 | 4,163 |
| Model calls at software-composition time | 0 | 0 | 0 |
| Fixed-format oracle software correctness | 12/12 | 12/12 | 12/12 |

[Qwen2.5-0.5B original data](results/isolated-qwen25-05b-38028491759/) · [Qwen2.5-1.5B original data](results/isolated-qwen25-15b-38028491759/) · [SmolLM2-1.7B original data](results/isolated-smollm2-17b-38028491759/)

**Crucial model-specific interaction:** The Qwen2.5-0.5B renderer improved from **3/12** correct software-validated joint extraction decisions to **10/12** with source-isolated extraction. SmolLM2-1.7B improved from **4/12 to 8/12**. But Qwen2.5-1.5B **declined from 9/12 joint to 6/12 isolated**. This overturns any claim that isolation is generally superior across model sizes or independent families. The intervention alters prompts, model access to surrounding context and reuse, so these scores are **exploratory architecture diagnostics**, not a controlled estimate of gains from memory splitting.

The *reason* the 0.5B isolated run scored only 11/12 exact source values is a lowercase \`ash\` response in place of \`ASH\`. No original output was changed; if a future preregistered case-normalization policy accepts that token, it may recover the missing value, but counting it retroactively as a pass would violate the current strict criterion. Qwen2.5-1.5B had four substantive source-value mistakes, and SmolLM2 had two. The full raw responses and per-record accepted source digests are included.

**Causal boundary:** In all conditions, the language model was only asked to extract an arbitrary token. The counterfactual and source-eligibility rule was *programmed in ordinary Python*. Correct reversal after source-attested extraction indicates a useful pipeline for toy source-grounded actions, **not** an LLM independently integrating autobiographical beliefs or deciding character values. All twelve memory scenarios share just twelve distinct local source documents; each record appears in two scenarios and the cached results are reused. The effective sample for extraction is twelve source prompts/model, not twelve independent multi-memory inferences.

**Cost boundary:** First-use source-isolated extraction requires **two** separate model invocations (roughly 600-700 tokens from these examples), more than the roughly 330 tokens for a one-step Qwen direct neutral-key decision. Only when source-field values are **reused, provenance-validated and version-invalidated** might precomputed extraction amortize the inference cost. The 3,625/3,609/4,163-token totals for twelve unique stored values compared with twelve reused decision contexts demonstrate a fixture-specific caching scenario, not an actual longitudinal production benchmark. The software calculator's CPU latency and cache maintenance costs were not measured.

### Mechanistic conclusion

Joint and isolated prompting should be **replaceable renderer-specific strategies**. The principal engineering invariant is not that each synthetic source must receive one model call; it is that a value can contribute to an authorized action **only when it is supported by its own trusted source** and that a changed/withdrawn source version invalidates the corresponding derived value. A policy can prefer the joint or isolated extraction path after *held-out* calibration with a real intended renderer. Selecting whichever arm scored best on these twelve exploratory source states and then calling it independently validated would overfit the test set.

The next meaningful engineering task is a **versioned source-attested fact cache** with strict invalidation on record and relationship-state changes, followed by real-L1 source-fact extraction with independently reviewed labels. It is premature to integrate one of these extraction modes into Pretorius's production cognition.


## Next real benchmark gate

The full E3 Tribunal still needs 36 newly authored naturalistic questions (not source-informed E2 rewordings), at least three independent relevance reviewers, potentially *multiple* sufficient evidence sets, realistic contradictory source updates, independently developed model families, and an audited state/provenance/latency ledger. No T1B result meets these conditions or authorizes merging into Pretorius production.
