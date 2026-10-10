# E3-T2: Original Pretorius L1 field access, example contamination and source witnesses

**Status:** Original small-model run complete but prompt-confounded; corrected v2 inference currently executing. **This is not the independently blinded E3 trial.**  
**Source:** Pretorius-Connectome commit \`6d2768211f5c2184c8bbdb833c06e169b5137197\`, canonical L1 manifest SHA-256 \`ce23717b3950a772cc25e4bf60107eaddf4a0375122b6893c15417669ae033bb\`, 450 reconstructed-fiction records. No source changes or learned model weights.  
**Protocol:** [L1_FIELD_PROTOCOL.md](L1_FIELD_PROTOCOL.md).

## Source selection and original metadata

The existing source adapter selected **12 events in 12 different episodes** under fixed seed 20261010:

\`E12-007\`, \`E08-015\`, \`E22-001\`, \`E02-019\`, \`E09-009\`, \`E11-005\`, \`E13-011\`, \`E25-015\`, \`E27-020\`, \`E23-006\`, \`E06-007\`, \`E17-003\`.

Each event has **two original author-written L1 string fields**, \`belief_changes\` and \`relationship_changes\`. The exact target text is a field value already present in the pinned source archive; it is not a validated interpretation inferred from a narrative. An exact-copy model comparison comprises 24 event-field pairs under three conditions: requested field alone, full source context with both changes, and target field withheld (expected JSON \`null\`). That yields 72 independent prompts/model.

## v1: Full 0.5B data, invalidated as an ability measure

[GitHub workflow](https://github.com/Azimn/Attractomancy/actions/runs/38057942612) · [original Qwen2.5-0.5B response rows](results/l1-fields-qwen25-05b-38057942612/)

The v1 system message explicitly supplied the dummy JSON pattern \`{"answer":"source text"}\`. Qwen2.5-0.5B returned this exact pattern in **70/72** original generations. The other two generations returned \`{"answer":"Source text"}\` and a copied non-target source claim. All 72 outputs were strict JSON, but every required exact value or null check failed:

| Original v1 prompt condition | Correct source value or null | Strict JSON | Spurious non-null answer despite target withheld |
| --- | ---: | ---: | ---: |
| Isolated explicit source field | **0/24** | 24/24 | N/A |
| Whole source event with both fields | **0/24** | 24/24 | N/A |
| Requested field withheld | **0/24** | 24/24 | **24/24** |

The 0.5B pilot used model revision \`7ae557604adf67be50417f59c2c2f167def9a775\` and **30,930** actual input/output tokens. It demonstrates how easily an overly concrete output exemplar can dominate a small renderer; **it does not demonstrate inability to access the requested original L1 fields**, since the repeated exemplar is a confound. Raw data and v1 code remain unchanged.

The separately versioned [v2 runner](l1_field_extraction_v2.py) removes the literal example and asserts that the previous placeholder does not occur in any generated prompt. It keeps original source, selected events, target strings and presentation arms fixed. This is an exploratory, informed correction; do not pool its outputs with v1, retroactively score v1 as valid evidence, or call the rerun independent preregistered replication. Numerical v2 findings are **pending run-specific raw output verification**.

## Direct source-owned witness baseline

A [read-only typed L1 witness adapter](l1_witness_adapter.py) and [passing CI run](https://github.com/Azimn/Attractomancy/actions/runs/38058594338) recovered both fields from all twelve selected events directly through the trusted original L1, with **24/24 exact source field values** and **zero language model calls**, *by software construction*. Each witness records the unchanged record's original canonical character span, event ID, episode ID, source revision, source-manifest digest, canonical full content hash and exact field value hash. Tampered witness content and a forged claimed source row were both rejected. This establishes a source-access/integrity interface, **not** psychological truth, learned model reasoning, or cryptographic proof of who authored the original narrative.

Because these 24 metadata values are already structured, using a renderer to copy them can only be justified as an *interface/comprehension stress test*. Direct typed source access should be the engineering default for those existing fields. The serious cognitive research question is whether source narrative and competing relationship history justify or revise those fields.

## Independent semantic review pending

The [unlabeled L1 narrative packet](packets/l1-semantic-calibration/review_packet.jsonl) contains **24 evaluation cases and 72 candidate belief/relationship interpretations**. Within-episode and out-of-episode candidate claims are *comparators*, not presumed false answers: a source excerpt might support more than one. Reviewers must quote exact narrative evidence and choose support, contradiction, underdetermination or unrelated, with confidence and rationale. The [semantic adjudication validator](l1_semantic_adjudicate.py) and ten synthetic unit tests passed [CI](https://github.com/Azimn/Attractomancy/actions/runs/38058310805), but **no actual human reviewer judgments exist**. Existing author-supplied sidecar descriptions are not independently validated semantics.

The packet is a source-informed calibration artifact, not the independently authored 36+ dilemma set, multi-record evidence sufficiency pool or three-reviewer decision benchmark required by the full E3 Tribunal.

## Interpretation boundary

A character can have perfect structured source-field lookup and still fail to select the right field, adjudicate contradictions, enact relationship obligations, or distinguish current updates from obsolete commitments. D1/E1/E2/E3-C already showed those separate failure modes on earlier interventions. The next validation step should target *narrative support and temporal source conflicts* with independent labels, not improving an artificial exact-copy score by more prompting.

**Live Pretorius and source-owner artifacts:** untouched.
