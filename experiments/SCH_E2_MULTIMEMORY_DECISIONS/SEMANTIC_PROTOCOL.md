# SCH E2S: Local Semantic Retrieval Against Source-Owned Lexical Baseline

**Status:** Exploratory, fixed protocol before first run.  
**Date:** October 9, 2026 (America/Chicago).  
**Source snapshot:** Pretorius-Connectome \`6d2768211f5c2184c8bbdb833c06e169b5137197\`.  
**Probe set:** The six previously fixed E2 novel dilemmas and their twelve author-chosen source-event IDs. **No new labels or queries were devised in response to E2R or E2G outcomes.**

## Hypothesis and conditions

Previous E2R/E2G results found poor lexical two-source assembly and only a narrow improvement from source-authored graph diffusion. The prospective E2S engineering hypothesis is that **local sentence embeddings** on the *canonical original memory narratives* may surface more of the fixed two-source evidence than lexical TF-IDF alone. These outcomes are not guaranteed, and exact pair recall at a fixed top-ten budget remains the primary metric.

The independent encoder is \`sentence-transformers/all-MiniLM-L6-v2\` (384-dimensional, English, sentence/paragraph similarity, Apache-2.0). Its pretrained parameters are held fixed; there is **no model fine-tuning**. Model repository revision and runtime package versions must be recorded. The implementation directly uses the model's attention-mask-weighted mean pooling and unit vector normalization with Transformers, avoiding an external API or subscription. To limit truncation confounds, inputs are clipped to 256 word pieces and the number of truncated source documents is counted. Both lexical and dense encoders process all 450 original L1 \`memory_text\` contents; neither receives selected event IDs, questions' intended action labels, editorial recall cues, knowledge graph links, or alternate author-written source summaries.

Five conditions share identical six natural-dilemma queries and source corpus:
1. Source-owned lexical TF-IDF baseline (\`AssociativeMemory.score(mode="lexical")\`).
2. MiniLM cosine similarity alone.
3. Unweighted reciprocal rank fusion of MiniLM and lexical rank positions, \`1/(60+r_lexical)+1/(60+r_dense)\`; no performance-tuned interpolation.
4. Dense embeddings permuted across event IDs under seed 11, with queries unchanged (negative association null).
5. Dense embeddings permuted under seed 37 (second negative association null).

Report source IDs at top ten, each of the twelve exact gold ranks, pair recall@2, @5 and @10, and individual event recall@10. Do not infer that nonselected relevant records are irrelevant. Record model revision, document/token truncation count, input doc count, full implementation hash or commit, elapsed times and machine dependency versions. No selected memory should be injected into a language renderer in this step.

## Constraints and interpretation

E2 gold pairs are retrospective, investigator-selected, and unblinded, with all six author-preferred decisions on the cautious/prosocial side. The benchmark tests *agreement with those exact pairs*, **not** broad semantic relevance, worldview continuity, or proof of a behaviorally integrated memory system. A top-ten gain is evidence of better retrieval of *these selected records* only. A near-zero score does not rule out other useful records. The two permutation nulls should perform poorly if the embedding index carries source-specific information, but winning against weak nulls does not establish semantic understanding.

MiniLM weights are not derived from a fly connectome. The L1 projected lexical cache is not modified, the existing pretrained source-owned TF-IDF baseline is not refitted on privileged gold IDs, and the original canon and all source hash contracts remain unchanged. Per-query encoder cost and one-time corpus encoding cost should be separated, because precomputed embeddings change the economics of repeated retrieval.

**Model source:** [Hugging Face MiniLM](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2).  
**Execution:** [semantic_retrieval.py](semantic_retrieval.py) via [sch-e2s-semantic.yml](../../.github/workflows/sch-e2s-semantic.yml).  
**Additional required validation:** once outputs are available, compare the top-10 candidate sets with E2R and E2G, preserve all negative and inconclusive outcomes, and propose a larger *blinded independently annotated* multi-evidence benchmark before any promotion to Pretorius.
