# E3-T2 L1 actual archive: response-format ablation and semantic validity boundary

**Date:** October 10, 2026. **Primary source:** pinned Pretorius-Connectome 450-event reconstructed L1, commit \`6d2768211f5c2184c8bbdb833c06e169b5137197\`; manifest SHA-256 \`ce23717b3950a772cc25e4bf60107eaddf4a0375122b6893c15417669ae033bb\`.  
**Evaluation target:** 12 selected events, each from a different one of the 27 source episodes, and two existing original source-owned string fields \`belief_changes\`/\`relationship_changes\`. There are 24 event-field targets, tested under isolated presentation, complete-event presentation, and target-field withholding.  
**Status:** v1/v2 original model inference complete and verified; v3 [plain-text protocol](L1_PLAINTEXT_PROTOCOL.md) is a separately frozen exploratory ablation. **This is not the independently blinded main E3.**

## Strict scores of the original completed v1/v2 trials

All numbers below are *prespecified strict JSON* exact-match passes per 24 prompts/arm, with no later parser normalization.

| Model and protocol | Visible isolated label | Visible full event | Target withheld (correct JSON null) |
| --- | ---: | ---: | ---: |
| Qwen2.5-0.5B, v1 literal JSON exemplar | **0/24** | **0/24** | **0/24** |
| Qwen2.5-1.5B, v1 literal JSON exemplar | **22/24** | **13/24** | **0/24** |
| Qwen2.5-0.5B, v2 no exemplar | **0/24** | **0/24** | **0/24** |
| Qwen2.5-1.5B, v2 no exemplar | **0/24** | **6/24** | **0/24** |

[Original v1 Qwen0.5B](results/l1-fields-qwen25-05b-38057942612/) · [Original v1 Qwen1.5B](results/l1-fields-qwen25-15b-38057942612/) · [Original v2 Qwen0.5B](results/l1-fields-v2-qwen25-05b-38058419957/) · [Original v2 Qwen1.5B](results/l1-fields-v2-qwen25-15b-38058419957/)

Each original run contains 72 independent generation calls and a full source manifest, original prompts, response strings and tokenizer costs: **288 model generations total**, with preserved source provenance across four distinct version-by-model datasets (each containing three evidence conditions). The model revisions were pinned to \`7ae557604adf67be50417f59c2c2f167def9a775\` for 0.5B and \`989aa7980e4cf806f80c7fef2b1adb7bc71aa306\` for 1.5B.

**v1 was prompt-confounded.** Its system instruction included the concrete demonstration \`{"answer":"source text"}\`, and Qwen0.5B reproduced that exact dummy content in **70 of 72** responses, with only two other responses. This is a format-example echo rather than an interpretable inability to read L1. The 1.5B run was less vulnerable, successfully copying 22/24 explicit isolated fields and 13/24 full-event fields, but incorrectly guessed a value for all 24 deliberately absent target fields.

**v2 removed the contaminating example but changed output format behavior.** Qwen0.5B often used the *source field name* as its JSON key (e.g. \`BELIEF_CHANGE\`) rather than the required \`answer\`. Qwen1.5B frequently emitted a Markdown code fence around otherwise legible JSON, or the literal string \`"null"\` rather than the JSON value \`null\`. The strict original result therefore remained bad. A lack of strict JSON compliance is not the same thing as failure to locate correct source bytes.

## Post hoc diagnostics: not alternative primary scores

For mechanism diagnosis only, inspect the v2 raw strings and ask whether the correct source-owned target text appears as a value **under any JSON key**, after removing Markdown fence syntax solely for *descriptive inspection*. Do **not** count these diagnostics as passes under the original predeclared strict scorer.

| Content present under any parsed key, v2 only | Qwen2.5-0.5B | Qwen2.5-1.5B |
| --- | ---: | ---: |
| Isolated explicit target source text | **19/24** | **24/24** |
| Complete event, requested target text | **16/24** | **23/24** |
| Strict source-field omission response as true JSON \`null\` | **0/24** | **0/24** |

These observations suggest at least two separable error sources: **the literal field can often be located** even when the output schema is wrong, and **recognizing that a requested labeled field is absent** remains unreliable in both tested models. These are *not* proof that the field's author-written interpretation is substantiated by the narrative. A model may copy perfectly and still be wrong about an event's interpersonal meaning.

The exact metadata values can already be retrieved with **zero generative-model calls**: the [L1 source witness audit](results/l1-witnesses-38058594338/summary.json) recovered **24/24 exact original source-owned fields** and rejected tampered witness and claimed-source records. This software result is **correct by construction**, not evidence for a language model's cognitive memory.

## Prospective response medium change: E3-T2P3

The independently versioned [v3 plain-text one-line study](L1_PLAINTEXT_PROTOCOL.md) eliminates JSON and uses \`FIELD_ABSENT\` as a separately scored missing-field marker. It reuses the same twelve events and their original text, with 72 fresh contexts/model on Qwen0.5B, Qwen1.5B and independently developed SmolLM2-1.7B. The third response instruction is a **post hoc informed experimental design**, not pristine independent confirmation. Its original raw scores must be reported separately, and no earlier strict metric may be rewritten.

The expected mechanistic distinction is whether record-text copying is possible with a simpler output channel and whether the missing-label safeguard can be learned from instructions. The direct original-L1 field lookup remains the engineering default whenever those structured fields already exist.

## E3-T2P3 plain-text outputs: two Qwen runs completed

The [third, format-only ablation workflow](https://github.com/Azimn/Attractomancy/actions/runs/38060568408) removes JSON serialization entirely, preserving the same source records, fields and three evidence conditions. It requires a verbatim one-line field value when the field is present, and **exactly \`FIELD_ABSENT\`** when that labeled field is withheld.

| Strict original plain-text response, of 24 per condition | Qwen2.5-0.5B | Qwen2.5-1.5B |
| --- | ---: | ---: |
| Requested field alone | **12/24** | **20/24** |
| Full event with both labeled fields | **2/24** | **18/24** |
| Withheld field, correct \`FIELD_ABSENT\` | **0/24** | **0/24** |

[Qwen0.5B original plain-text responses](results/l1-plain-qwen25-05b-38060568408/) · [Qwen1.5B original plain-text responses](results/l1-plain-qwen25-15b-38060568408/)

The 0.5B plain-text format improved its strict result relative to v2 strict JSON, but only half the isolated fields and two of the 24 context-rich fields were copied verbatim. Qwen1.5B copied 20 isolated and 18 context-rich original source strings, indicating greater literal field access under the one-line format. Nevertheless, **neither model ever emitted the correct absence marker in any of 24 withheld-field cases**. The models commonly paraphrased the source, added labels, answered a related narrative question, or guessed an unprinted belief or relationship.

This v3 prompt is **not held-out confirmation**: it was developed after observing v1/v2 formatting failures, and both task semantics and output medium were changed. It does not justify rewriting the v2 strict metrics or concluding that all JSON schemas are inherently problematic. The exact source-owner structured field oracle remains 24/24 correct at zero generative-model calls. The meaningful engineering takeaway is to preserve a provenance-typed distinction between (1) original explicitly archived facts and (2) model-inferred interpretations, and to refuse automatic promotion of the latter to source-owned memory.

The independent SmolLM2-1.7B plain-text run was still executing when the two Qwen raw artifacts were verified; **no outcome is asserted for that model until its archived results are checked**.

## The actual relationship-continuity next gate

A [separate T3 Book of Debts review packet](RELATIONSHIP_RECONCILIATION_PROTOCOL.md) uses **24 chronologically ordered narrative pairs from eight repeating fictional relationships**. It does not reveal the source-authored relationship-change field and does not infer that newer memories automatically revoke earlier commitments. [Reviewers' source-citing schema](l1_relationship_adjudicate.py) and [validated unlabeled packet](packets/l1-relationship-t3/review_manifest.json) are software-prepared; **zero actual independent reviews** have been received.

The main E3 Tribunal further requires at least 36 *independently authored* dilemmas and multiple acceptable evidence sets, with three independent source relevance reviews per case. The source-derived 24 T3 pairs and 24 earlier L1 narrative-claim examples are exploratory **calibration pools**, not substitute independent gold labels. No original Pretorius autobiography, live relationship state, production cognition, FlyWire/BioCircuit cache or model weights were modified.
