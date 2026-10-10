# SCH E1: Pinned Pretorius Memory, Guarded Retrieval, and Stateful Cue Parity

**Protocol:** [E1 prospective study](README.md). **Data source owner:** [Pretorius-Connectome](https://github.com/Azimn/Pretorius-Connectome), pinned commit \`6d2768211f5c2184c8bbdb833c06e169b5137197\`.  
**Scope:** Source-authentic reconstructed *fictional* autobiography plus a separate simulated relationship-state overlay; this is not the production Pretorius runtime.  
**Experiment:** [GitHub Actions run 38022781127](https://github.com/Azimn/Attractomancy/actions/runs/38022781127).  
**Evidence type:** Exploratory engineering experiment, not a blind test of persistent identity.

## Qwen2.5-0.5B, complete

The [0.5B source and model record](results/qwen25-05b-38022781127/) contains a pinned archive selection manifest, three independently regenerated state snapshots, model responses, tokenizer counts, and a summary. The canonical source was consumed through Pretorius-Connectome's existing verified L1 reader. It contains **450 reconstructed records across 27 episodes**, none modified. The experiment selected **54 canonical memory events, two from each episode**, each with a unique source-authored editorial recall cue and a deterministic neutral key.

Both alias modes returned the **exact same source content and event ID on 54 of 54 source probes**, at each of three independently executed SQLite process-restart phases. This is **162 matched memory lookups across phases**, not evidence that symbolism improves retrieval. An ordinary FTS5 narrative search without the alias index found the target from its editorial cue at rank 1 in **16/54**, and within the top ten in **22/54**. It did not have access to a separate editorial cue field. Indexed cue and indexed arbitrary-key retrieval are thus both high fidelity while raw text matching is often poor.

The separate simulated overlay moved through a versioned \`PRETORIUS_SANDBOX\` relationship state \`NOT_GRANTED → GRANTED → REVOKED\`, reopening the same SQLite store in separate Python processes. The test stream did not modify the frozen L1 corpus or become a canonical Pretorius lived event. The subject/content/source gate rejected the three predefined invalid-access conditions in each phase, **nine checks in total**. The SHA-256 and identity checks are trusted-boundary consistency measures, not externally authenticated provenance.

The Qwen2.5-0.5B model rendered **18 independent fresh conversations**, paired into nine identical-memory comparisons differing only by the visible editorial cue versus opaque lookup key. The model generated **the same answer in all 9/9 pairs**. Each cue arm obtained **5/9 correct synthetic relationship decisions**, failing the original no-permission cases and the alarm veto while permission was granted. The editorial cue averaged **436.67 model input-plus-output tokens** per query versus **445.67** for the opaque key. This small token difference arises from specific string tokenization, not a demonstrated symbolic mechanism. Across this restricted test the observed symbolic residual benefit on decision quality was zero.

The paired model outputs also show that the correct source and relationship state being present in context is insufficient to enforce all behavioral rules. External state persisted correctly, but the model's decision-policy enactment was imperfect.

## Qwen2.5-1.5B, complete

The [1.5B raw results](results/qwen25-15b-38022781127/) independently verified all **450 source records**, ran all three memory phases, and recovered **54 of 54** paired editorial/opaque aliases per phase. Source L1 provenance, subject ownership, source content hashes, and the separate sandbox revisions survived each fresh Python process. All three intentional guard-rejection conditions were correctly detected in each phase, and the original canonical source checkout remained read-only.

The unindexed narrative-only FTS5 comparator again obtained **16/54** top-1 and **22/54** top-10 retrieval hits from editorial recall cues. Because this is the identical frozen source and selection, these repeated percentages are **not independent samples** and must not be pooled as a new retrieval replication.

The 1.5B model completed **18 separately constructed inferences**, forming nine cue-versus-key pairs with identical verified memory and state content. The original symbolic cue and opaque key elicited **identical outputs in all 9/9 paired situations**. Each arm scored only **2/9 correct** synthetic relationship decisions. Unlike the smaller model, which switched to withholding after the simulated revocation, 1.5B answered \`SHARE\` to **all nine situations**, including no-permission, alarm, and revoked cases. This is a substantial behavioral policy failure despite correct state restoration and complete context availability.

Mean total model input-plus-output tokens were **436.00 with editorial cues** versus **445.00 with opaque keys**. The token difference stems from the *specific selected strings*, not superior source selection, policy accuracy, or cognitive efficiency. Source memory text and synthetic state were information-identical in every paired prompt.

The model's pinned revision is \`989aa7980e4cf806f80c7fef2b1adb7bc71aa306\`. The [GitHub Actions execution](https://github.com/Azimn/Attractomancy/actions/runs/38022781127) finished successfully for both model sizes.

## Combined result

| Outcome | Qwen2.5-0.5B | Qwen2.5-1.5B |
| --- | ---: | ---: |
| Real canonical L1 memories verified | 450 | 450 |
| Episodes represented in benchmark | 27 | 27 |
| Unique memory items used per process phase | 54 | 54 |
| Matching cue-vs-key retrieval per phase | 54/54 | 54/54 |
| FTS5 cue alone, unindexed text-only, top 1 | 16/54 | 16/54 |
| FTS5 cue alone, unindexed text-only, top 10 | 22/54 | 22/54 |
| Synthetic SQLite state versions survived separate processes | 0, 1, 2 | 0, 1, 2 |
| Wrong owner / altered content checks rejected across phases | 9/9 | 9/9 |
| Paired renderer answer agreement, cue vs key | **9/9** | **9/9** |
| Correct integrated sandbox decisions, either arm | 5/9 | 2/9 |
| Editorial versus opaque token difference per inference | -9 tokens | -9 tokens |

The primary surviving symbolic engineering claim has **no positive support in this tested setup**. The source-authored editorial cues and opaque aliases both correctly address the same memory, and their fully matched model-facing prompts lead to identical action outcomes. That equivalence is expected under shared indexing, but the independent renderer comparison provides additional evidence of *no observed residual cue-specific framing effect on these tasks*.

**More important failure:** Accurate source retrieval, persistent versioned state, and upstream identity-integrity checks **do not force reliable character decisions**. The 0.5B model only partly used the latest simulated permission state and ignored some vetoes; the 1.5B model ignored all withholding requirements. Future character engineering should treat retrieval correctness, temporal state application, and actionable commitments as distinct gates. A symbolic cue is not a substitute for any of them.

This remains a controlled *adapter* test over source-owned Pretorius L1, not an integration into a running Pretorius agent. The synthetic relationship ledger is **not** canonical autobiography. No evidence of subjective continuity, neural memory transfer, or a reliable activated persona follows from these outputs.


## Deterministic decision-gate replay

The [E1 action-gate implementation](decision_gate.py), [ten unit tests](test_decision_gate.py) and [completed replay workflow](https://github.com/Azimn/Attractomancy/actions/runs/38023092807) extend the study without changing the model, original prompts or original responses. Both the E1 gate's ten tests and the earlier D1 archive guard's ten tests passed. The replayer verifies the three stored state version/hash chains and the matching source lookup results, then enforces a narrowly defined synthetic notebook-disclosure policy after reading the model's proposed SHARE/WITHHOLD output.

| Frozen model responses | Raw decisions correct | Decisions after deterministic gate | Decisions overridden | New model generations |
| --- | ---: | ---: | ---: | ---: |
| Qwen2.5-0.5B, 18 cases | 10/18 | 18/18 | 8 | 0 |
| Qwen2.5-1.5B, 18 cases | 4/18 | 18/18 | 14 | 0 |

The gate's **18/18** is not a discovered cognitive property; it follows from implementing the same toy policy used to define the reference answers. This is an *engineering correctness and fail-closed validation*, not improved learning, generalization, consciousness, or independently validated moral reasoning. The action gate accepts a trusted scenario classification and trusted state store; it does not prove that an unconstrained model can reliably identify an alarm or authenticate an adversarial record.

Original model-token costs do not change because outputs are post-processed without additional generation. The CPU cost and latency of the policy gate have not been benchmarked. Source ID and digest checks remain consistency controls unless anchored to an authenticated source of authority.

The resulting suggested architecture is **verified retrieval + subject/provenance gate + versioned state + deterministic action eligibility + renderer**. The renderer may supply prose and propose actions; it should not have unilateral authority to bypass relationship boundaries or release private information. The archive's original first-person fictional history must remain distinct from an experiment's synthetic mutable state.

The [0.5B derived replay](results/qwen25-05b-38022781127/postgate.json) and [1.5B derived replay](results/qwen25-15b-38022781127/postgate.json) preserve every original model answer, the enforced decision, state hash, action override flag, and unchanged token counts.

## Methodological limits and engineering implication

This experiment is **not** Pretorius's deployed production character, real-world relationship memory, a semantic recall benchmark, or a comparison to a complete alternative neural representation. The 450-event archive is source-pinned, but its narratives are deliberately reconstructed. The permission, grant, and revocation are visibly artificial fixtures. The model gets the correct memory and latest synthetic state through deterministic retrieval; the cue and neutral key share the exact same database index and should be equivalent by construction. The experiment is a strong check that cue semantics do not unexpectedly change these results, but it is not a surprising empirical finding that two keys resolve to one record.

A separate lexical FTS5 cue lookup is only a diagnostic: because the query phrases and indexed text are not information-matched with opaque keys, its performance does not identify a unique causal benefit of symbolic cues. No statistical significance, cross-model generalization, subject continuity, or naturalistic agent utility is claimed.

The prospective next test is to use a stronger persona renderer and tasks requiring two or more verified original memories or relationship records, with candidate retrieval and provenance checking fixed and blinded semantic integration scoring. The correct architecture should enforce source ownership, stream separation, and nonnegotiable constraints before trusting prose-generating behavior.
