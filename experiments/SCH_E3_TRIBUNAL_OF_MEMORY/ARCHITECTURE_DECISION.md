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

## Implementation gates

**Gate T0 (complete):** Existing independently versioned source archive, D1 subject guard, E1 durable state/alias controls, E2 error baselines and E3-C synthetic strict model calibration are present. The synthetic test is diagnostic and **not** a reason to claim persona emergence.

**Gate T1 (next possible code):** Typed source-field extractor with per-field evidence span, missing-operand rejection, correct reference ID, and a fixed counterfactual rule evaluator. Compare direct prompt, evidence-extract-then-compute, and deterministic source-side extraction on exactly the same corrected fixture and costs. A model that can only succeed when software does all reasoning has not demonstrated cognitive integration.

**Gate T2 (not satisfied):** Independent blinded relevance annotations for at least 36 newly authored questions and a sufficient-set adjudication. Six E2 source-informed calibration questions do not count. At least three independent raters and multiple acceptable event sets are required.

**Gate T3 (not satisfied):** Full real-L1 retrieval + temporal-state update + counterfactual action inference tested under different renderer families, with neutral-key and no-memory controls, calibrated abstention versus productive action, measured token/CPU costs, source admission security and grounded action logging.

**Gate T4 (not authorized):** Production Pretorius integration, continuous subjective claims, self-model updates as lived experiences, or research efficacy assertions. Requires audit and a separately scoped implementation decision, not just a synthetic green CI check.

This staged approach preserves the verified data and reusable shared-memory interfaces while isolating the exact failure point. It also avoids presenting mystical symbolism or a strong SCH form as a prerequisite for functional autobiographical memory.
