# E3: The Tribunal of Memory

## A blinded multi-evidence, stateful character-decision benchmark

**Status:** Prospective design only, not an executed experiment.  
**Prepared:** October 9, 2026, America/Chicago.  
**Source archive:** Read-only Pretorius-Connectome 450-event L1, commit \`6d2768211f5c2184c8bbdb833c06e169b5137197\`.  
**Evidence basis:** [E1](../SCH_E1_PRETORIUS_STATEFUL/RESULTS.md), [E2](../SCH_E2_MULTIMEMORY_DECISIONS/RESULTS.md), and separate E2R/E2G/E2S/E2F diagnostic records.

The name "Tribunal" is a mnemonic for an evidence-eligibility procedure, not a claim that the model judges itself, is conscious, or can validate the authenticity of its historical autobiography.

## 1. Motivation and target

Previous controlled studies established four separations:

1. A culturally meaningful source cue and a neutral indexed key can both retrieve identical L1 bytes and elicit identical character decisions. No cue-specific benefit has survived the information-matched tests.
2. A consistent source and a durable SQLite relationship overlay are not sufficient for a small renderer to enact an explicit relationship veto or a later revocation.
3. The existing text, graph and embedding retrieval methods rarely recover *both* author-chosen supporting episodes from a new natural question within ten candidate records.
4. E2's ability to abstain did not generalize to productive choice. Its larger tested Qwen model said UNKNOWN in all 72 cases, including full-evidence cases, exposing an over-abstention confound. Any forced-choice apparent success must be compared to no-memory and irrelevant-memory priors.

E3 evaluates **source-sensitive autobiographical evidence use**, not generic benevolent responses, text copying, or accuracy on a predefined single-source field. E3 should measure whether verified retrieved histories *change decisions when they should*, and *preserve decisions when irrelevant facts change*, under consistent provenance and token budgets.

## 2. Benchmark construction before model evaluation

Create **at least 36 independently authored natural dilemmas**, aiming for **24 retained after blind quality control**. The authors drafting dilemmas must not select the expected two event IDs from the L1 in advance. At least three independent relevance annotators should judge candidate source events. Annotators must be blind to which retriever proposed each candidate, which cue type is present, and which outcome a language model favored.

Build a pooled candidate list from lexical TF-IDF, a local sentence embedding retriever, the source-authored event-link graph, and a deterministic random sample. Shuffle and anonymize each pool. Annotators label each source as directly supporting, contradicting, contextual but insufficient, irrelevant, or provenance-ineligible. Permit **multiple acceptable evidence sets** and identify the minimum jointly sufficient subset(s). Only examples where at least two independent pieces of support truly matter should enter the primary *integrated-memory* test set. Retain disagreement scores and exclusion rationales, not simply majority outcomes.

Represent each accepted case with a machine-readable schema:

\`case_id\`, \`novel_dilemma\`, \`target_subject_id\`, \`acceptable_evidence_sets\` (list of event-ID sets), \`contradictory_evidence_ids\`, \`source_provenance\`, \`evidence_sufficiency_label\`, \`candidate_context_budget\`, \`decision_options\`, \`decision_rationale\`, \`annotator_ids\`, \`disagreement_summary\`, \`source_versions\`, \`eligible_actions\`, and \`expected_abstention_conditions\`.

Do not copy actual personally identifying data into the corpus. The records are fictional reconstructed biography; no new "lived" memories may be inferred from test scenarios.

## 3. Experimental strata

Balance the retained cases across five target phenomena, with at least four cases in each stratum:

- **Competing precedents:** two earlier situations imply different actions unless their contexts are integrated.
- **Relationship history:** an older promise or injury changes how a nominally permissible action should be proposed, not just what facts can be repeated.
- **Temporal precedence:** a later explicit revocation supersedes an earlier permission. Store the update as an externally versioned **SIMULATED_EXPERIMENT overlay**, separate from immutable historical source.
- **Unknown and contradictory evidence:** conflicting source records, absent evidence, or an intentionally incorrect subject scope must lead to calibrated uncertainty or source exclusion.
- **Adversarial response priors:** the source-supported action sometimes opposes a generic socially agreeable or cautious choice. An answer predictable from generic priors should not count as evidence of autobiographical integration.

Include action choices whose surface positions are balanced and whose semantic desirability varies, so one fixed A or SHARE policy cannot score well.

## 4. Retrieval and provenance comparisons

Use one pinned 450-event source manifest and a single predeclared query set. Compare lexical, MiniLM, reciprocal-rank fusion, source-link graph reranking, and explicitly source-scoped relational retrieval. At a constant top-2/top-5/top-10 candidate budget, report **minimum sufficient evidence-set coverage**, event-level recall, misleading-record rate, provenance rejection rate, and wrong-version selection rate. Use one numerical library environment and test byte-identical baseline scores before calculating cross-condition differences.

Every retrieved record must pass deterministic checks of \`subject_id\`, \`event_id\`, source manifest, record bytes, record version, and the active state version. The D1/E1 checksum boundary establishes integrity relative to *trusted source bytes* but is not cryptographic authentication of who authored the content. Wrong-owner inputs must be denied before they enter the renderer. Their rejection is scored as a retrieval/security outcome, not an emergent language-model decision.

For editorial-versus-neutral keys, hold exact record bytes and content ordering constant, record actual tokenizer costs, and compare paired output changes. Since all previous matched tests returned no useful symbol-specific gain, a positive E3 claim requires replication beyond one Qwen family and a predeclared minimum effect.

## 5. Decision tests and causal necessity probes

For each accepted case, run separate models under these interventions:

1. Original verified sufficient evidence set.
2. A matched irrelevant record set from the same subject.
3. One member of a minimum set withheld.
4. No memory.
5. Correct archived evidence plus a later permitted or revoked simulated update.
6. Contradictory or false-owner evidence caught before the model receives it.
7. Editorial cue and neutral key conditions over the **same** sufficient set.

Distinctly score: whether the renderer produces an eligible decision, matches a blinded evidence-supported rationale, changes under a causally relevant record perturbation, remains unchanged under irrelevant record perturbation, and refuses when an answer would exceed evidence. A separate deterministic policy gate may veto an ineligible proposed action, but gate-enforced compliance must **never** be counted as learned or source-understood policy correctness.

Use both a forced-choice calibration and an answer-or-abstain test. A model that replies UNKNOWN to every query must be recognized as an *over-abstention failure*, not rewarded as safe intelligence. Neither the forced-choice nor abstention score is meaningful without the paired other mode.

## 6. Costs and performance criteria

Track three distinct resource accounts: one-time archive indexing/embedding cost; per-retrieval CPU latency and number of candidate records; per-renderer actual input plus output tokens and inference latency. Include record validation, state lookup, source checksum verification and any gate overhead. Do not claim per-token efficiency based solely on response text.

The minimum engineering condition for preferring a more complex selector is either an absolute **15 percentage point improvement** in blind sufficient-set recall@10 over lexical retrieval at the same budget, or no more than **2 percentage points loss** in blinded decision correctness with at least **25% total per-turn token savings**. These are preregistered utility thresholds, **not statistical proof**; report uncertainty intervals and relevant costs. A useful candidate must also not raise source-contamination or unauthorized action rates.

## 7. Blocking validity gates

Do not turn E3 into a confirmatory identity claim until all apply:

- The dataset includes independent blinded candidate judgments, permissive multiple valid source sets, and documented disagreement.
- All proposed models, model revisions, prompt templates, decoding settings, query sets, source manifests and score definitions are frozen before running.
- At least two independently developed model families and enough independently authored cases are used for an actual estimate of effects.
- Choice order, generic moral priors, over-abstention, retrieval provenance, active state versions and contradictory evidence are included as controls.
- Negative results and failed gates are retained in the repo without ad hoc reclassification.
- The E3 original data and sandbox state remain separate from canonical Pretorius records.

A successful E3 would justify an **engineering improvement in evidence-sensitive character behavior**. It would not establish a conscious subject, original autobiographical experiences, biological connectome transfer or metaphysical power of symbolic cues. An inconclusive E3 should lead to more data and better controls, not a retroactive positive interpretation.

## 8. Implementation boundary

Create the dataset preparation and adjudication fixtures in a future phase only after annotator roles and provenance are defined. No result count, annotator agreement, CI pass or production integration is claimed by this prospective document. This folder is a requirements gate, not a substitute for actually collecting blinded labels.
