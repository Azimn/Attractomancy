# E2G: Source-Authored Association Graph Versus Lexical Recall

**Predeclared:** October 9, 2026 (America/Chicago), before first E2G execution.  
**Source:** Frozen Pretorius-Connectome 450-event reconstructed fictional L1 (commit \`6d2768211f5c2184c8bbdb833c06e169b5137197\`).  
**Question:** Can explicit source-authored links between autobiographical events help retrieve **both** relevant memories from a novel dilemma, beyond a conventional word/bigram lexical retrieval baseline?

The original 450-record L1 contains source-authored \`links_to_prior_events\` event-ID edges. They are editorial reconstruction metadata, **not** neural synapses, biological connectivity, learning observations, or subjectively experienced associations. They are allowed as optional retrieval-side evidence; they cannot be recast as a connectome, and the protected L1 must not be rewritten.

## Fixed comparison

1. Use the owner-provided \`pretorius_connectome.associative.AssociativeMemory\` \`mode="lexical"\` score vector as the *identical* baseline for every arm. Its TF-IDF vectorizer fits 450 original narratives using the existing library behavior. It has no access to gold event IDs, scenario decisions, or evaluation labels.
2. Construct an undirected adjacency solely from each source record's \`links_to_prior_events\`. Ignore no valid links and reject unknown references. Include a self-loop on every memory to avoid isolated-node failure. Normalize each row by its total degree.
3. For a query, normalize nonnegative lexical scores so the maximum is one. Perform **three diffusion updates** using \(z_{t+1}=0.75x+0.25P^\top z_t\), with \`z_0=x\`, where \`P\` is the row-normalized source event adjacency. The restart component retains lexical evidence. Rank each output by decreasing score, then event ID ascending to break ties. Candidate budgets remain exactly 2, 5 and 10 across all methods; no extra model-visible records are granted to graph arms.
4. Compare a **shuffled-link negative control** using fixed seeds 11, 19 and 37. The control preserves each source event's number of outgoing \`links_to_prior_events\` but randomly reassigns valid target event IDs before symmetrization. It does *not* preserve both in- and out-degree distributions, episode geometry or source-link semantics; state this limitation.
5. Score whether **both** original, researcher-selected source events appear in top 2, 5 or 10. Report individual source hits, positions and the full ranked top-ten event IDs. The six E2 dilemmas are not independently blinded; all source pairs are author-selected after examining the archive. Do not evaluate correctness of model decisions in E2G.

## Prospective prediction and interpretation

The directional engineering prediction is that source-authored association diffusion improves pair recall@10 relative to pure lexical retrieval, and outperforms shuffled-link diffusion under the *same* top-ten budget. A null, negative, or shuffled-control advantage must be retained.

This experiment does not manipulate symbolic cues; it tests a candidate associative memory-selection mechanism in the architecture that might matter more than cue invocation. It offers no proof of representational learning, subjective identity or provenance authenticity. All six evaluation tasks, source entries and graph edges come from the same authored fictional corpus, and alternate relevant memories have not been reviewed. Any apparent improvement is exploratory and requires future held-out, independently annotated query/graph evaluation.

**Implementation:** [graph_retrieval.py](graph_retrieval.py). **Workflow:** [sch-e2g-graph.yml](../../.github/workflows/sch-e2g-graph.yml). Results must be saved to a run-specific directory before interpretation.
