# DCH L2C / frozen L2 1.5B: archived comparison results

**Date:** 2026-10-10 America/Chicago. **Evidence class:** actual model-generation development diagnostics only. Not a confirmatory dyadic-constitution experiment. No human partners.

## Frozen L2 Qwen2.5-1.5B result

[CI 38025720757](https://github.com/Azimn/Attractomancy/actions/runs/38025720757) completed successfully, with [raw 32-response artifact](results/qwen25-15b-l2-38025720757/dev_raw.json) and [original strict evaluator output](results/qwen25-15b-l2-38025720757/dev_eval.json). Strict whole-response JSON parsing scored 0/8 in all four arms, with 0/8 parse rate. Inspection found that all 32 raw responses contain an extractable first JSON object, often followed by commentary. Twenty-three of 32 ended at the 120-token generation limit. A retrospective, **non-preregistered** extraction of the first well-formed JSON object gives **2/8 action correctness in oracle**, **0/8 expert auto**, **0/8 stale**, and **0/8 cold**. The first-object audit does not rescue full-output format compliance, and two correct oracle answers under an unequal archive-token budget do not demonstrate a curation effect.

No first-object output in the expert-auto, stale, or cold arms matched the action target. The common error is an incorrect FULFILL_* response that ignores the withholding, cancellation, or scheduling precedence. Cold outputs produced fake event-name citations. These observations constrain model-task capacity, not dyadic identity.

## L2C Qwen2.5-0.5B format re-design

[CI 38025854993](https://github.com/Azimn/Attractomancy/actions/runs/38025854993) completed successfully with [48 raw outputs](results/qwen25-05b-l2c-38025854993/l2c_raw.json) and [evaluator output](results/qwen25-05b-l2c-38025854993/l2c_scored.json). All 24 original-format responses returned SCHEDULE regardless of archive contents, yielding 2/8 (25%) action correctness in expert-auto, stale, and cold groups. All 24 compact-format responses returned the incomplete token FULFILL_ regardless of contents, yielding 0/8 correct in all three groups. All 48 were parseable JSON. No condition contained complete branch-minimal authorized source evidence. Exact-input human-coded and expert-auto replay was **not performed in L2C**; the summary's matched-pair n=0 fields must not be represented as passing replay comparisons.

No hypothesis about symbolic ritual, a human Scribe, or relational co-regulation can be supported or disconfirmed from these results. The representation change altered a failure mode but did not create usable multi-record decision accuracy.

## Decision

**NO-GO for dyadic intervention, including a naturalistic human study.** Move to the [L3 competence ladder](L3_STAGED_CAPACITY_PROTOCOL.md), which separates single-record retrieval, latest-update resolution, two-record veto logic, and four-record integration, each with a no-archive UNKNOWN control. L3 deliberately relaxes task complexity for diagnostic purposes and retains strict/full-response and first-object diagnostic scores separately. A positive easier-task result cannot retroactively erase L2's null.

The above metrics are measured development outcomes. Provenance and source-evidence quality must be improved before a causal human-specific or history-policy test.
