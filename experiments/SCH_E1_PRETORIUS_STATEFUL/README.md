# SCH E1: Pretorius Stateful Memory, Provenance Gate, and Cue-Selection Control

**Study:** exploratory architecture integration, October 9, 2026 (America/Chicago)  
**Canonical source owner:** [Pretorius-Connectome](https://github.com/Azimn/Pretorius-Connectome), pinned checkout \`6d2768211f5c2184c8bbdb833c06e169b5137197\`.  
**Source data:** its existing checksum-verified [L1 archive](https://github.com/Azimn/Pretorius-Connectome/tree/main/artifacts/shared_memory/v1), 450 reconstructed memories / 27 episodes.  
**Research owner:** [Attractomancy](https://github.com/Azimn/Attractomancy); no canonical source or Pretorius production runtime is modified.  
**Status:** frozen prospective exploratory implementation. Check workflows and committed artifacts for actual results before attributing findings.

## Narrow question and predictions

Can an editorial symbolic or sensory *recall cue* add selection quality or cost benefit beyond a neutral key that points to the same canonical Pretorius memory, **after** enforcing a deterministic subject/provenance gate?

The core head-to-head test is **exact alias equivalence**. Each chosen memory has one genuine editorial \`recall_cues\` string and one deterministic opaque ID indexing the *same* immutable L1 record. If both routes use identical alias indexes and a guard, they should return the same memory event. Any higher-level differences in an optional renderer would measure *response framing*, not retrieval superiority. This is intended as a negative control and can falsify residual symbol-specific claims.

A second **unindexed retrieval diagnostic** queries SQLite FTS5 over the source narrative and title with the editorial cue as an ordinary phrase, **without** consulting the alias table. This measures how much the naturally meaningful cue overlaps with narrative text, and cannot be fairly interpreted as an intrinsic advantage over an arbitrary ID unless information budgets and indexing are made equivalent. Neither exact alias access nor raw lexical matching is evidence of semantic understanding.

The benchmark samples two records per episode from 27 source episodes, using a deterministic seed and a recall cue with one unique lowercase string across all 450 records. A separate shadowed-state test uses a *synthetic* and explicitly noncanonical memory stream to exercise a simulated relationship permission, a grant, and a revocation, across separate Python process invocations sharing one on-disk SQLite file. This tests whether session-to-session restoration and latest-state selection work, not whether Pretorius has acquired a real personal experience.

## Trust and provenance architecture

The pinned source checkout supplies the original L1 normalization, SHA-256 and Git blob checks. This study imports the source owner’s \`pretorius_connectome.shared_memory.read_l1\` rather than rebuilding or rewriting original records. The SQLite store records canonical event IDs, source provenance, per-record hashes, and two alias types. The canonical identity is PRETORIUS; the separate test overlay identity is PRETORIUS_SANDBOX. Records must pass the previously developed [D1 record guard](../SCH_D1_EXTERNAL_RECONSTRUCTION/archive_guard.py) before their content is presented to a language model. The guard checks requested identity, authorized source, embedded identity header, and SHA-256. This is consistency and integrity checking **within a trusted source boundary**, not authenticated provenance or an anti-forgery signature.

No synthetic overlay event may be committed to the canonical Pretorius corpus, recast as reconstructed biography, or described as an experienced memory. The test ledger is strictly separate and its entries are visibly marked SIMULATED_EXPERIMENT. The source L1 and FlyWire/BioCircuit caches are read-only and unaffected. Prior evidence about limited semantic robustness remains intact.

## Stateful experimental steps

1. In a new Python process, validate the pinned source L1 and populate a persistent SQLite store from **exactly 450** reconstructed records. Build a deterministic alias index with one unique editorial recall cue and one opaque lookup key per benchmark event. Include an independent FTS5 index over the actual narrative and title, with no editorial cue in the indexed text.
2. In a *separate* process, probe all 54 benchmark events through both alias types; assert equal event IDs, source hash, and delivered record content; measure JSON payload size, lookup latency, and exact source retrieval. Record unindexed lexical FTS5 ranks separately. Exercise deliberate wrong-identity and tampered-content guard rejections.
3. In additional isolated Python processes, write the simulation-only ledger updates GRANT and REVOKE. At each version, reopen the on-disk store, verify owner and stream separation, and produce an independently reconstructible active relationship state. No previous model conversation is reused.
4. Optionally run a local Qwen renderer over identical guarded memories plus the retrieved synthetic state after each phase. Compare editorial cue versus opaque key with information-identical records on fixed relationship decisions. Measure actual model tokenizer input/output, exact action accuracy, and paired output agreement. This is an **integration probe**, not real Pretorius agency.
5. Commit complete raw source identifiers, output strings, source manifest hashes, model revision, token counts, guard rejection cases, SQLite state-head checksums and summary. Do not commit the entire redundant 450-event archive or disclose any student data.

## Interpretation

A 100% alias lookup for both cue and opaque key is an *implementation correctness test*. The engineering value, if any, must arise from retrieval robustness to imperfect natural queries, smaller context budgets, or behavior that a neutral key cannot achieve at matched information cost. A renderer that makes the same decision under both aliases provides no symbol-specific evidence even if both correctly enact the relationship rule.

A verified process restart is evidence of durable external state, **not** of model parameter persistence or continuous consciousness. Success on synthetic interaction constraints cannot retroactively validate canonical historical self-representation. An improved retrieval mechanism should be integrated into the actual character architecture only after a stronger, blind, cross-model study.

## Reproduction

Harness: [memory_system.py](memory_system.py), renderer: [render.py](render.py), aggregation: [summarize.py](summarize.py), CI: [sch-e1-pretorius.yml](../../.github/workflows/sch-e1-pretorius.yml). The CI workflow checks out source \`6d2768211f5c2184c8bbdb833c06e169b5137197\` under \`pretorius_source\` and stages a private SQLite file under the runner's working directory. Model- and run-specific artifacts are retained separately; the frozen L1 repository is never written.
