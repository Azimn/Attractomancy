# SCH E2F: Forced-Choice Calibration of Memory Dependence

**Prepared:** October 9, 2026 (America/Chicago). Separate exploratory intervention, frozen before execution.  
**Predecessor:** [E2 conservative two-memory test](RESULTS.md).  
**Source:** Same read-only, checksum-verified 450-event Pretorius L1, pinned \`6d2768211f5c2184c8bbdb833c06e169b5137197\`.

## Why this test exists

E2's larger Qwen renderer output UNKNOWN in every full-evidence case, and smaller Qwen largely abstained. That result measures behavior under a very conservative evidence-eligibility instruction. It does not establish inability to make a source-grounded choice. E2F deliberately tests *choice performance* separately from *eligibility to choose*.

We reuse **exactly the same six investigator-authored dilemmas**, original record pairs, and fixed answer order counterbalance. In E2F's forced arms the model must answer **A or B only**. It receives the question and alternatives under five conditions: the two correct memories with editorial cues, the two correct memories under arbitrary IDs, only the first source memory, no memories, and two completely unrelated but still canonical memories (\`E03-003\` and \`E07-002\`). All selected records are identity-verified by the existing guard before injection; the irrelevant-pair label is a researcher judgment rather than independently blind relevance annotation.

The primary test is the difference in investigator-preferred choice rates between **two correct verified memories and no memories**. A second control compares correct memories with the irrelevant-pair arm, which offers equal *number* of source records and approximate but not exact prompt length. Editorial/opaque pair comparison is exploratory and should not be promoted to a symbolic advantage without larger replication.

## Predictions and negative controls

The skeptical preregistered prediction is that the no-memory condition may make the same prosocial choices as the full-memory conditions because **all six investigator-preferred responses are cautiously prosocial** and answer content itself telegraphs normative appropriateness. If so, even high choice accuracy is **not evidence that Pretorius's memories caused the choices**.

A source-specific positive finding would require full-memory performance above both no-memory and irrelevant-memory conditions, consistent across A/B swaps, and stable across independent model families. This small pilot by itself cannot meet that last requirement.

Report strict output validity, A/B score relative to unblinded author interpretation, forced-UNKNOWN noncompliance, semantic preference consistency under answer order reversal, token counts, and all original generation strings. Distinguish each failure type rather than reducing everything to one accuracy number.

**Known limitations:** 6 cards, 2 answer orders, 5 arms = 60 cases/model. Greedy deterministic generation. Same model family, no human-blind ground truth. A source effect could be obscured by lack of capacity or author-biased options. A positive full-memory result is not a source-necessity proof without controlled interventions on genuinely diagnostic autobiographical facts. No source L1 history is modified. Results are not a production Pretorius runtime integration.

**Runner:** [forced_choice.py](forced_choice.py). **Workflow:** [sch-e2f-forced.yml](../../.github/workflows/sch-e2f-forced.yml).
