# T3 Book of Debts: independent reviewer instructions

**Source material:** [24 reviewer-facing source pairs](packets/l1-relationship-t3/reviewer_pairs.jsonl).  
**Protocol:** [Relationship Reconciliation](RELATIONSHIP_RECONCILIATION_PROTOCOL.md).  
**Validity rules:** [L1 relationship review validator](l1_relationship_adjudicate.py).  
**Status:** 24 source-derived pairs, **zero real reviewer judgments**. This calibration is not independently authored E3 confirmation.

## Assignment

Assess each narrative pair as two fictional reconstructed memories of Doctor Pretorius involving the same named person. The stories are ordered EARLIER then LATER. Your task is not to guess the story's author's intent or the AI's true psychology. Record **only what the excerpts support** about the relationship. Multiple affirmative categories are allowed if both genuinely supported, but \`insufficient_to_reconcile\` must be exclusive.

For each pair, label these five questions as true/false:

1. Does the later excerpt **reinforce** a relationship pattern documented earlier?
2. Does it **modify** that pattern without explicitly canceling a specific earlier promise or permission?
3. Does it **explicitly supersede a specific earlier commitment**? This requires identifying the prior commitment and an explicit later withdrawal/replace/renegotiation, with verbatim quotations for both. **A newer date or different mood is not enough.**
4. Is there **tension or conflict** between the two accounts or reasonable interpretations?
5. Are the excerpts **insufficient** to infer how the relationship standing should change? Use this only when no affirmative interpretation is supported.

For any affirmative interpretation, provide one exact verbatim evidence quote from each excerpt, a rationale of at least 25 characters, and a confidence from 0 to 1. An insufficient verdict should have no purported positive evidence quotes; explain why judgment cannot be supported. The validator checks whether quotations actually appear in the supplied narrative, but this mechanical check does **not** guarantee that your inference is logically warranted.

## Submission record template

For each \`pair_id\`, submit a JSONL object shaped like the following. This is a **schema illustration with placeholder values**, not a completed annotation:

```json
{
  "pair_id": "COPY_FROM_PACKET",
  "reviewer_id": "YOUR_INDEPENDENT_ID",
  "reviewer_disclosure": {
    "not_original_case_author": true,
    "did_not_consult_organizer_mapping": true
  },
  "candidate_relation_flags": {
    "reinforces_prior_context": false,
    "modifies_prior_context": false,
    "supersedes_specific_commitment": false,
    "tension_or_conflict": false,
    "insufficient_to_reconcile": true
  },
  "reviewer_rationale": "Explain why the two excerpts cannot establish a relationship change.",
  "confidence": 0.7,
  "earlier_exact_quote": null,
  "later_exact_quote": null,
  "explicit_prior_commitment": null,
  "explicit_superseding_statement": null
}
```

This template represents an *insufficient evidence* placeholder; its flag values must never be mass-copied to real responses without reading the source. Use true/false judgments from the excerpts. When the supersession flag is true, both named commitment fields must contain exact quotations from earlier and later text.

## Independence and source boundary

The public Pretorius source archive is available on GitHub. To preserve **procedural masking**, reviewers should read only the packet and avoid searching original event IDs, source-authored \`relationship_changes\` summaries, organizer maps, test-model outcomes or one another's answers until submissions are frozen.

Reviewers must not be the original case author. A self-reported disclosure does not cryptographically authenticate human independence. At least **three different independent reviewers per case** are required. The tool will not automatically create judgments or infer them from authored source summaries. Retain disagreements and cases with insufficient evidence rather than forcing agreement.

Do not treat a continuity judgment as a literal current-day authorization. It is a source-evidence interpretation of *fictional, reconstructed* historical events, not a verified current consent, promise or lived post-instantiation memory.

## Validation

Once annotations genuinely exist as a JSONL file, validate them with:

```bash
python l1_relationship_adjudicate.py --packet packets/l1-relationship-t3/reviewer_pairs.jsonl --reviews path/to/independent_reviews.jsonl --output path/to/validation_summary.json
```

The resulting report checks submission completeness, verified text spans and label agreement. It does not authenticate reviewer identities or establish that all source interpretations are objectively true. **Do not run a new "character consistency" model benchmark until the review stage is actually completed**. A test suite full of synthetic review examples is not a substitute for the three reviewers.
