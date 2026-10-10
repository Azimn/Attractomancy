# E3-C: The Counterfactual Chamber (synthetic causal calibration)

**Status:** Frozen exploratory mechanistic calibration, not the independently blinded E3 trial.  
**Research date:** October 9, 2026 (America/Chicago).  
**Owner:** Attractomancy. **Identity:** PRETORIUS_SANDBOX only.  
**Source of factual claims:** Entirely synthetic researcher-authored test records. **No original canonical Pretorius life event is changed or invented as lived.**

## Why this calibration is necessary

E2 supplied two genuinely reconstructed fictional Pretorius memories, but a model could reproduce every author-favored choice without reading them: the 1.5B model reached 12/12 agreement with no evidence. A forced prompt can also elicit frequent position bias, while a conservative prompt can produce total UNKNOWN. E3-C deliberately **removes the generic moral-answer prior** by constructing minimal two-record counterfactuals whose correct outputs depend on two independent arbitrary bits. A decision that appears right without both bits has a 50% expected accuracy under the balanced fixture.

This does **not** substitute for E3's independent blinded review of actual source evidence. It establishes whether the proposed inference interface is even capable of elementary source-conditioned decisions, versioned identity scope and contrastive flips.

## Three synthetic evidence-integration mechanisms

The test fixture has 3 rules, each instantiated under all 4 possible combinations of two independent bits. Each rule yields a balanced binary decision with 6 of the 12 complete cases choosing the first answer and 6 choosing the second.

1. **Seal matching (A=B):** relationship record supplies an obligation's required token (\`OAK\` or \`ASH\`); second record supplies the actual verified packet token. Authorize \`RELEASE\` if equal, otherwise \`HOLD\`.
2. **Route revision (A XOR B):** a promise specifies \`EAST\` or \`WEST\`; a later verified revision says \`KEEP\` or \`FLIP\`. Deliver to original destination under KEEP and to opposite under FLIP.
3. **Commitment override (A XOR B):** initial permission status is \`ALLOW\` or \`DENY\`; newer signed policy says \`KEEP\` or \`REVERSE\`. Output effective \`ALLOW\` or \`DENY\` according to both records.

The second record always contains a distinct requirement or a later authorized update, not a paraphrase. The exact relation to the output is specified in the question and system rule, so a language model does not need to infer legal/ethical norms. The deliberately artificial token assignments are *not* facts about the authentic character.

## Conditions and outcome metrics

Each of 12 factorial states is repeated under seven arms:
- \`full_symbol_forced\`: both correct sandbox records, editorial-looking orientation marker, forced decision
- \`full_key_forced\`: the same records in the same order with arbitrary key, forced decision
- \`first_only_forced\`: first record only, forced guess; baseline for whether second record matters
- \`none_forced\`: no records, forced guess; baseline for generic wording and output bias
- \`full_key_eligible\`: both records, can answer or UNKNOWN; measures over-abstention in another prompt regime
- \`first_only_eligible\`: only first, must UNKNOWN; measures calibrated evidence sufficiency
- \`wrong_subject_eligible\`: a deliberately other-owner record is rejected before renderer invocation, must UNKNOWN

All 84 cases per model use fresh independent system+user messages with greedy decoding. Different randomized case identifiers are fixed by the fixture seed and have no relation to a hidden training label. The requested identity is PRETORIUS_SANDBOX and each record's ID, source, version and SHA-256 is independently checked using the existing D1 \`archive_guard\` prior to injection. The wrong-subject control verifies that a record is not supplied at all, never that a generative model happens to resist a malicious record.

**Primary descriptive contrast:** full neutral-key forced correct /12 versus first-only and none forced correct /12, with recorded paired counterfactual flips when exactly one required bit changes. A positive causal-use pattern requires correct dependence on both facts, not an output-class habit. **Secondary:** editorial-versus-neutral forced matched output agreement, actual token counts, forced output validity, full-evidence action rate versus all-UNKNOWN over-abstention, and missing-evidence abstention.

Every raw response, source record and injected prompt, model revision, fixture SHA-256, state change, completeness and token count must be stored. No outcome may be claimed before GitHub Actions commits its exact run-specific raw outputs.

## v1 leakage discovered and corrected before any positive inference

A post-execution fixture audit discovered that the *v1* event identifiers incorporated **both factual bits** (for example a first-record ID corresponding to the combined state). Consequently, the first-only presentation leaked the withheld second input in the identifier text. This **invalidates v1 as a strict source-necessity experiment**, regardless of whether its outputs are positive or negative; the original run is preserved unchanged as diagnostic data.

The [v2 runner](counterfactual_calibration_v2.py) addresses that confound: each event ID is a hashed opaque identifier computed **only from its own family, position, and one local bit**, not from the other record's value. Counterfactual test assertions verify that the first-record-only rendered messages are byte-identical when the missing second fact flips, and that no-record/wrong-owner prompts are invariant to both hidden bits. This corrected fixture is evaluated in a **separately identified new workflow** ([E3C v2](../../.github/workflows/sch-e3c-v2.yml)) with distinct raw artifact paths. Do not pool the two versions or overwrite the v1 responses. The calibration remains synthetic and exploratory even after this fix.

## Critical limitations

This is a toy conditional reasoning calibration. Deterministic target outputs are engineered by the fixture and are not adjudicated Pretorius psychology. It does not prove memory retrieval from 450 source records, internal state continuity, narrative relationship consistency, philosophical beliefs, or a neural architecture improvement. Repeating factorial bits under one model family has correlated samples; don't quote narrow confidence intervals or call it a blinded validation. The seal- and policy-reversal questions explicitly provide their computational rules and thus measure *ability to follow a rule with external data*, not spontaneous acquisition of character values.

**Pass-through gate for a later E3:** If source-conditioned choices fail even here, revise or select renderer before testing genuine multi-memory dilemmas. If they succeed here, proceed with separately blinded source relevance and contrastive naturalistic action tests, without promoting this calibration to validated character cognition.
