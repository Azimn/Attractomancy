# Tribunal of Memory: staged architectural recommendation, not deployed character code

**Date:** October 9, 2026. **Decision status:** Experimental architecture candidate.  
**Source corpus:** Pretorius-Connectome 450-record L1 stays immutable and source-owned.  
**Evidence basis:** Verified [D1](../SCH_D1_EXTERNAL_RECONSTRUCTION/RESULTS.md), [E1](../SCH_E1_PRETORIUS_STATEFUL/RESULTS.md), [E2](../SCH_E2_MULTIMEMORY_DECISIONS/RESULTS.md), and [corrected E3-C](CALIBRATION_RESULTS.md). Synthetic results are *not* canonical persona episodes.

## Working architecture

The Tribunal metaphor refers to an inspectable **evidence-to-action pipeline**, not an autonomous judge or an imputed machine conscience. Every theatrical name maps to a typed engineering contract:

1. **The Gatekeeper (identity and provenance):** Required \`subject_id\`, \`source_type\`, \`event_id\`, \`source_version\`, \`trust_assertion\` and trusted manifest hash. Reject wrong-subject records and invalid version chains before any model sees their text. The D1/E1 tests demonstrated the difference between software-rejected foreign records and an LLM that would copy them if given access. Checksums are tamper-consistency, not independent authentication.
2. **The Witness Summons (candidate discovery):** Lexical, local semantic, explicit source-link and relational lookups produce **one candidate pool**, without privileged evaluator gold IDs. The E2 six-dilemma pilot failed complete source-pair recall at top ten for lexical and MiniLM; association diffusion helped one case only. Retrieval must score independently blinded *sufficient evidence sets*, not single favorite memory IDs.
3. **Cross-Examination (source comparison):** Maintain a case-local evidence table of \`event_id\`, author/source, chronological order, claim, certainty, relationship target, candidate contradictions, and record-version supersession. Never infer the absence of a contradicting record from a small top-k cache. Mark contradictory or missing components rather than smoothing them into agreeable prose.
4. **The Clerk (typed state extraction):** Extract **explicit typed operands** from each admitted record with evidence spans, rejecting absent or unverified fields. Compare the model's extracted fields with controlled fixture ground truth *before* crediting its subsequent decisions. This is a testable next candidate, not yet validated. A typed extractor should not silently invent values to complete an appealing story.
5. **The Magistrate (action eligibility):** Compute hard authorization from a trusted state ledger and explicit policy where a genuine nonnegotiable boundary exists, with reason codes. E1's deterministic post-gate corrected toy disclosure decisions without changing model cognition. Preserve that difference: software policy compliance is a safety property, not an emergent psychological trait.
6. **The Voice (character renderer):** Given admitted witnesses, contradictions, authorized action scope and self-model context, render in Pretorius's characteristic style. Record what was actually said and done as a separately versioned post-instantiation event only if it truly happened. Do not rewrite the preawakening reconstructed L1 or mix synthetic experiment data into the lived archive.

## Why the components remain separate

D1 restored arbitrary facts almost perfectly from valid records while models often ignored identity mismatches or relationship rules. E1 preserved synthetic relationship state across restarts but the renderer still violated its policy. E2 found that presenting preselected original memories could worsen author-choice agreement versus giving no memories. Corrected E3-C v2 showed that both small Qwen models failed every fully correct counterfactual flip under two simple source-bit rules, despite properly admitted records. Together these imply that \`memory present\` does not entail \`memory selected\`, \`memory used\`, or \`action permissible\`.

These results do **not** justify replacing Pretorius's motivational systems with a deterministic state machine. Motivations, values, relationship histories, and conflicting wants can remain graded, probabilistic or learned; hard limits on source identity and authorization should nevertheless have separately verified contracts. A renderer can voice ambivalence while the action gate still refuses an unpermitted disclosure.

## T1 results: typed extraction is useful but model-dependent

The executed [joint Clerk experiment](CLERK_RESULTS.md) and [source-isolated Private Clerk](ISOLATED_RESULTS.md) separated source-token extraction from a deterministic action calculator. All three tested models (Qwen2.5-0.5B, Qwen2.5-1.5B, SmolLM2-1.7B) produced run-pinned raw data under the original corrected synthetic E3-C v2 source contracts.

| Model | Direct forced action | Joint typed two-record extraction + software | Isolated one-record extraction + cached software |
| --- | ---: | ---: | ---: |
| Qwen2.5-0.5B | 5/12 | 3/12 | **10/12** |
| Qwen2.5-1.5B | 6/12 | **9/12** | 6/12 |
| SmolLM2-1.7B | 5/12 | 4/12 | **8/12** |

These are different prompt tasks and output pathways over twelve synthetic states, and the final rule is **software-computed** in the two staged paths. Their results do not establish an across-model gain from splitting memories: **the better extraction layout depends on the renderer**. T1B generated only twelve distinct model outputs per model and reused each verified record across two counterfactual combinations, so its twelve composed decisions are not twelve independent two-source model inferences.

The newly tested [source-attested SQLite cache](verified_fact_cache.py) scopes a derived field by subject, source, event ID, source revision, content digest, extractor revision and field schema. Its [unit-tested revision drill](../../.github/workflows/sch-e3-fact-cache.yml) begins with a synthetic permission ALLOW, then advances to a new signed source clause requiring DENY. Prior cached fields are invalidated, and a new validated extraction is required. This is a useful integrity and replay **software guarantee**, not cryptographic proof of origin or autonomously learned model updating. No original Pretorius relationship or autobiographical record was mutated.

**Design choice:** Keep the Clerk abstraction but do not hardwire isolated or joint prompts. Choose a renderer-specific extraction strategy only after held-out validation and with record-level provenance checks. Whether a real event demands one field, competing memories or relational narrative synthesis remains an independently labeled problem. Eligibility rules should not be inferred from model output alone.

## Implementation gates

**Gate T0 (complete):** Existing independently versioned source archive, D1 subject guard, E1 durable state/alias controls, E2 error baselines and E3-C synthetic strict model calibration are present. The synthetic test is diagnostic and **not** a reason to claim persona emergence.

**Gate T1 (partial exploratory completion):** Typed synthetic-source extraction and software verification were executed on three local models, with strict source-attested output and missing-operand fail-closed behavior. A synthetic SQLite version and digest invalidation drill passed. This does **not** satisfy the stronger requirement for per-field evidence spans, independent source relevance adjudication, real-L1 data, or a production-integrated extractor. The staged calculator's correct answers are software-enforced, not independently reasoned by the renderer.

**Gate T2 (not satisfied):** Independent blinded relevance annotations for at least 36 newly authored questions and a sufficient-set adjudication. Six E2 source-informed calibration questions do not count. At least three independent raters and multiple acceptable event sets are required.

**Gate T3 (not satisfied):** Full real-L1 retrieval + temporal-state update + counterfactual action inference tested under different renderer families, with neutral-key and no-memory controls, calibrated abstention versus productive action, measured token/CPU costs, source admission security and grounded action logging.

**Gate T4 (not authorized):** Production Pretorius integration, continuous subjective claims, self-model updates as lived experiences, or research efficacy assertions. Requires audit and a separately scoped implementation decision, not just a synthetic green CI check.

This staged approach preserves the verified data and reusable shared-memory interfaces while isolating the exact failure point. It also avoids presenting mystical symbolism or a strong SCH form as a prerequisite for functional autobiographical memory.
