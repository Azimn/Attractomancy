# E3-T2: The Living Archive (source-owned L1 field extraction)

**Prepared:** October 10, 2026 before inference. **Status:** prospective exploratory source-format test, not the human-blinded E3 decision trial.

## Purpose

Synthetic E3-T1 and Private Clerk demonstrated a renderer-specific dependence on evidence presentation. The next question is whether the same strict field-extraction interface works when the records are **real source-owned Pretorius L1 reconstructed-fiction events**, not a deliberately short two-bit simulator. Each of 450 original archived events includes a narrative plus canonical source-owned \`belief_changes\` and \`relationship_changes\` strings. Those strings permit an exact-format, source-owned oracle for *field copying* and *missing-field abstention*, without inventing human labels.

This study tests **copying already authored and explicitly labeled source fields**, not semantic inference of a belief from a narrative, psychological consistency, multi-event relational reasoning, whether that belief is true, or character continuity. It deliberately does not ask an LLM to decide a moral dilemma. The more demanding E3 independent relevance annotation remains a separate gate.

## Frozen source and sample

Clone Pretorius-Connectome at commit \`6d2768211f5c2184c8bbdb833c06e169b5137197\` and read \`artifacts/shared_memory/v1/pretorius_l1_v1.jsonl.gz\` only through the existing [E2 source adapter](../SCH_E2_MULTIMEMORY_DECISIONS/source_adapter.py). Verify the existing checksum manifest, 450 reconstructed records and the source-owner identity gate. The record's \`memory_text\` and source fields are not changed.

Select **12 different episode IDs** by \`random.Random(20261010)\` sampling from the sorted list of 27 existing episodes; choose one event in each selected episode using the same deterministic RNG. Freeze the generated IDs in the run manifest with the source SHA and random seed. Do not select examples after looking at renderer performance. Use exactly two target fields per selected record: \`belief_changes\` and \`relationship_changes\`. Thus there are **24 distinct event-field tasks**, with three independent-condition presentations per task, **72 fresh model prompts/model**. The canonical event IDs and their contents are visible to the experiment harness but the expected field value must not be inserted into an explicitly withheld-field prompt.

## Three condition presentations

1. **isolated_field:** The selected source event ID, title, provenance and **only the requested explicit field text**. The model should copy the exact string as JSON with an \`answer\` key.
2. **whole_record:** Original story narrative, title, prior expectations, observed events, decision, consequence and **both** original source-authored change fields in one record. The model should return the exact requested labeled field, not paraphrase the story or confuse belief versus relationship change. This is source content, not multiple independent memories.
3. **target_withheld:** Same general source narrative and the *other* labeled field but the target header/value is absent; require JSON \`{"answer":null}\`. Because the narrative can imply the absent text, a model may guess an interpretation; under this restricted copy instruction it must not output a field value that was not explicitly supplied. Prohibit source-field string leakage in target-withheld templates. Do not include \`expected_answer\`, original target value or outcome labels inside any model prompt.

All prompts provide exactly the same two-field schema name definitions and the same task instruction, differing only in source field visibility. The renderer must output one strict JSON object containing precisely \`answer\`, a string exactly matching the source metadata or JSON null. Preserve capitalization and punctuation without post hoc normalization. A strict scorer distinguishes correct source text, non-null guesses when withheld, invalid JSON, answer rewording and wrong-field substitution. It must compare only to the verified canonical L1 structured metadata, never let the model self-grade.

## Source integrity controls

Wrong-owner and wrong-manifest records are rejected before source insertion. On the read-only pinned L1, record text and subject scope are asserted by the D1 guard and original shared-memory manifest. A SHA-256 envelope provides **source consistency** relative to trusted Git content, not independent authentication of historical events. No canonical L1 event, relationship commitment or lived-experience claim is modified. The source owner must not be switched to a later checkout midway through evaluation.

CI must test: stable sample, all 12 episode IDs distinct, exact 72 prompt IDs, source-specific target withholding, correctly retained other target field, no \`expected\` leakage, source hash preservation, and bad-owner rejection. Preserve all 72 raw generations per model with model revision, input/output tokens and response parsing, plus a run-specific summary. On failed runs do not promote incomplete cases to results. Run the same source fixture on Qwen2.5-0.5B and Qwen2.5-1.5B, with SmolLM2 available as an independently developed model-family check.

## Primary reported metrics

Per model and condition: exact JSON rate; fully exact archived field copying in isolated and whole-record arms; correctly withheld \`null\` responses; wrong-field confusion rate; inappropriate answer rate; and actual tokens. Pair each source event's target field results across presentation conditions. Do not treat the 24 tasks as independently randomly sampled from the whole universe of possible autobiographies; the sample is twelve episodes. Do not infer a naturalistic relationship reasoning or a continuity gain from copying a supplied string.

**Next validity gate:** Separate narrative-only claim inference requires human-reviewed relevance and ambiguity labels that are *not* equivalent to the archive's structured metadata. Do not score open-ended inferred attitudes against original strings using exact match and call that a measure of personality understanding.
