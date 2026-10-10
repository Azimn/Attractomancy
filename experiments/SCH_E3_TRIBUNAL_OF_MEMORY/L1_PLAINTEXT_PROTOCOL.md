# E3-T2P: The Bare Transcript — plain-text output ablation

**Frozen:** October 10, 2026. **Status:** Exploratory v3 *after inspection of v1/v2 output errors*, not independent confirmatory replication.

## Motivation

[E3-T2](L1_FIELD_PROTOCOL.md) tested strict JSON reproduction of two already-author-written fields, \`belief_changes\` and \`relationship_changes\`, in Pretorius's pinned reconstructed-fiction L1. The first response prompt accidentally included a literal \`"source text"\` example. The corrected v2 removed that example but many model outputs still violated the prescribed JSON schema while *containing the correct raw source value*. In a post hoc inspection, Qwen2.5-0.5B included the exact value in 19/24 isolated and 16/24 complete-event responses, while Qwen2.5-1.5B included it in 24/24 and 23/24 respectively. These exploratory text-match observations do **not** replace the primary strict JSON results.

The appropriate next mechanism question is **serialization versus content selection**. Ask for the literal field value as **plain text**, avoiding JSON entirely. Separate strict source-text copying from missing-field decisions. Even if copying succeeds, directly reading the original structured L1 metadata is still cheaper, deterministic and correct by construction.

## Frozen intervention and scoring

Reuse **exactly the same twelve events selected from twelve episodes**, their original fields, read-only source adapter, and three presentation conditions in v2. There are 12 events × two fields × three conditions = **72 contexts/model**, greedy decoding, max 112 new tokens. Conditions:

- \`isolated_field\`: source ID/title and exactly the requested explicit field.
- \`whole_record\`: actual narrative, expectations, observations, decisions, consequences, and both labeled fields.
- \`target_withheld\`: same narrative and other label but without the requested labeled field.

The prompt contains **no quoted correct-value demonstration** and no JSON serialization example. For a presented target field, instruction is to copy its exact contents *as one line* with no label, prefix, quoting, paraphrase or explanation. For an absent target field, output **\`FIELD_ABSENT\`** and no other text. The marker is a predeclared response-class symbol, not a retrieved autobiographical cue; it is visible in every condition.

Primary strict outcome: model's entire response after trimming surrounding whitespace equals the original structured source field (present conditions), or equals exactly \`FIELD_ABSENT\` (withheld). Preserve capitalization/punctuation and original raw output. Record how often a model falsely supplies a value when a field is absent. An ordinary software field lookup is the **non-model oracle** and expected to succeed by construction on 72/72 states. Do not claim an LLM outperforms direct source access.

**Paired diagnostic:** Compare the v2 original response-string post hoc "contained the exact target value" rate against the v3 new strict plain-text rate, using identical source cases. Differences are **prompt-sensitive**, not isolated statistical evidence of a serialization mechanism; both instruction phrasing and response medium change, and v3 was selected after looking at v2 outputs. Do not recompute v2 strict JSON scores or redefine its pass criterion.

## Provenance and safety

The L1 remains pinned at Pretorius-Connectome commit \`6d2768211f5c2184c8bbdb833c06e169b5137197\`. Confirm 450 reconstructed-only source events, the immutable shared-memory manifest, subject identity, two original author-written fields, twelve unique episode IDs, 72 unique case IDs, absent target value in withheld prompts, and SHA-256 for the admitted source excerpt. Reject wrong owner before inference as in v2. The model never sees the reference answer if the field is deliberately withheld. Outputs are separately named raw files and never blended into v1/v2 artifacts.

This study still tests **literal retrieval from already labeled source bytes**, not source-independent narrative comprehension, autobiographical reasoning, evidence sufficiency across multiple events, relationship commitment behavior, or consciousness. The independent three-reviewer narrative semantic packet and full E3 Tribunal remain unexecuted.
