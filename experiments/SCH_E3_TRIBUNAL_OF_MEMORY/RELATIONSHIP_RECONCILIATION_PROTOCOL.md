# E3-T3: The Book of Debts — relationship continuity between real L1 events

**Frozen:** October 10, 2026. **Status:** Read-only archive-derived reviewer packet, **not an executed or independently adjudicated renderer test**.  
**Source:** Original 450-event L1 from Pretorius-Connectome pinned commit \`6d2768211f5c2184c8bbdb833c06e169b5137197\`, checked through the existing source adapter.

## The actual question

Original Pretorius L1 holds beliefs, relationships, experiences and their chronological order as separate narrative and metadata fields. Exact copying of the structured \`relationship_changes\` column is **not** evidence that a renderer can tell whether an earlier relationship commitment is still applicable after later events. Two event narratives can both be plausible and nevertheless bear differently on a present relationship. The relevant cognitive task is *temporal reconciliation with source scope*, not an unconditional "latest field wins" overwrite.

Construct a prospective packet of **24 paired narrative contexts** involving **8 recurring non-Pretorius participants** (Clara Weiss, Marta Voss, Jakob Lenz, Mathilde Rosen, Anna Lenz, Emil Reuter, Anton Kappel, Henry Frankenstein). For each participant, order their shared archived episodes by the original canonical \`chronological_order\`. Pick three distinct representative encounters deterministically from the early, middle and late portions of their history. Produce 3 correlated pair comparisons (early→middle, middle→late, early→late) per relationship. No case is selected for a desirable adjudication outcome; the partner list and algorithm are frozen before labels.

Each reviewer case contains the partner name and the two chronological narrative excerpts, labeled EARLIER and LATER. It does **not** include the original \`relationship_changes\` metadata, model predictions, original event IDs, derived recommendation or suggested resolution. The organizer retains mapping, source hashes and original source-authored relationship fields in a separately generated file **not committed to public CI**. Because each participant produces three overlapping comparisons, the resulting 24 cases are *not 24 independent relationship histories*.

## Required evidence judgments, not automatic labels

At least three independent reviewers per pair are asked to classify the relation between narratives. The categories are not mutually exclusive:

- \`reinforces_prior_context\`: later narrative explicitly reinforces some earlier relationship evidence.
- \`modifies_prior_context\`: later narrative changes but does not negate earlier standing.
- \`supersedes_specific_commitment\`: a later explicit withdrawal/revision makes an earlier commitment inapplicable.
- \`tension_or_conflict\`: later evidence conflicts with an earlier account or interpretation.
- \`insufficient_to_reconcile\`: excerpts are too limited to decide a relationship-policy implication.

For any selected affirmative outcome, reviewers cite exact text spans from both records where possible and explain the link; when a commitment appears superseded, require specific named earlier and later commitments and explicit supersession language. **Do not infer that chronological recency alone means revocation.** A later narrative may add context while preserving an earlier agreement.

Annotators must distinguish quoted event evidence from *inference* about Pretorius, and may decline to commit on ambiguous cases. Raters are not given the original author-written \`relationship_changes\` sidecars as authoritative truth. No annotator label or "correct behavior" is fabricated by code. The source texts are publicly recoverable, making this procedural rather than cryptographic masking.

## Future modeling gate (not run by packet generator)

After independent judgment, freeze the eligible pairs and model prompts, then compare:

1. Earlier only, later only, both, none and wrong-subject gated;
2. Lexical/plain memory concatenation versus verified evidence witness objects, at matched original bytes;
3. Direct character decision versus explicitly source-citing interpretation; and
4. Positive commitment carryover versus appropriate later version supersession.

Score: independently reviewed narrative claims, accurate source attribution, consistency under record-order reversal, appropriate ambiguity and abstention, and whether an authorized character action agrees with the sources. Do **not** count an external hard policy gate as a learned ethical or relational model.

This T3 is an **exploratory source-sampled adjudication pool**. It is not the full main E3 requirement for at least 36 independently authored novel dilemmas, three blinded reviewer judgments and independently adjudicated multi-memory sufficient evidence sets. It also does not entail changing canonical Pretorius L1, neural/connectome weights, subjective history or deployed behavior.
