# E3 external research links: multi-hop memory, temporal updates, and causal influence

**Review date:** October 9, 2026.  
**Status:** Source-grounded design leads, not E3 outcomes or independent replication. The work below informs test construction and must not be presented as validation of Pretorius or SCH.

## 1. Wu et al., LongMemEval (2024/ICLR 2025)

[LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory](https://arxiv.org/abs/2410.10813) distinguishes information extraction, multi-session reasoning, temporal reasoning, knowledge updating and abstention. Its evaluation and retrieval/indexing discussions suggest testing **five axes separately**, instead of a single memory-correctness aggregate. For E3, separate candidate-event recall, evidence sufficiency, later-version precedence, missing-evidence abstention and actual decision correctness.

Relevance: E2 showed accurate source verification did not guarantee decisions, and either universal abstention or universal forced guesses can make a crude aggregate misleading.

## 2. Hu et al., EverMemBench (2026)

[EverMemBench: Benchmarking Long-Term Interactive Memory in Large Language Models](https://arxiv.org/abs/2602.01313) reports challenges in multi-party, interleaved, temporally evolving conversation memories, including a disconnect between implicit relevance and similarity search. It motivates a **subject-scoped multi-relationship candidate pool**, not simply a corpus of fact-label matches. Require versioned relationships, false-owner exclusion, and joint sufficiency judgments, ideally with genuinely interleaved events.

Relevance: E2R/E2S retrieval lost at least one of both author-selected evidence records in every natural-query top-ten set, while D1 showed wrong-owner facts readily contaminate language output when they are admitted to context.

## 3. Han, Lee, and Do, RFEval (2026)

[RFEval: Benchmarking Reasoning Faithfulness under Counterfactual Reasoning Intervention in Large Reasoning Models](https://arxiv.org/abs/2602.17053) separately examines answer correctness and causal influence through counterfactual interventions. The E3 decision evaluation should similarly require **counterfactual source-state flips** rather than counting agreement with researcher-authored answers as use of memory. A model can produce a plausible rationale and correct decision without relying on supplied evidence.

Relevance: In E2F, a larger model matched the investigator's intended six counterbalanced decisions *more often without records* than with the authentic source pairs. This is prior-driven convergence and demands explicit causal controls. The E3-C synthetic calibration implements a very narrow, controlled two-bit version, not RFEval's full design.

## 4. Li et al., TiMem (2026)

[TiMem: Temporal-Hierarchical Memory Consolidation for Long-Horizon Conversational Agents](https://arxiv.org/abs/2601.02845) proposes temporally hierarchical memory organization and complexity-aware recall, with evaluation on conversational memory tasks. This is a candidate *comparison hypothesis* for selecting autobiographical evidence at different levels of detail. It does not justify transplanting its memory tree into Pretorius without controlled cost-quality ablations against the source-owned L1 and learned/multimodal caches.

Relevance: E1 showed a shorter *selected* record could save tokens while keeping correctness on the larger model; E2 failed to select correct paired records. A complexity-aware selector might address both selection and retrieval costs, but E3's labeled evidence judgments must be constructed before this is tested.

## Research boundary

These papers support the *design of separable tests*, not an empirical claim that symbolic cue encoding enhances memory or that externally reconstructed source records make an AI character self-aware. Keep paper effects and benchmark setups distinct: LoCoMo/LongMemEval and multi-party conversation data are not the Pretorius 450-event fictional historical archive. Citations to these works should preserve actual publication dates, author lists, and benchmark-specific claims; do not copy externally reported model scores into Pretorius score tables.

**Priority for E3:** provenance-scoped joint source relevance, temporal state revisions, tested ability to abstain *selectively*, counterfactual response dependence, and amortized end-to-end token/latency cost.
