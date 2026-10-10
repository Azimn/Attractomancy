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

## Qwen2.5-1.5B

This section is pending verification of the independent larger-model artifact. Until verified, no accuracy, token, or cue-effect result is claimed for it.

## Methodological limits and engineering implication

This experiment is **not** Pretorius's deployed production character, real-world relationship memory, a semantic recall benchmark, or a comparison to a complete alternative neural representation. The 450-event archive is source-pinned, but its narratives are deliberately reconstructed. The permission, grant, and revocation are visibly artificial fixtures. The model gets the correct memory and latest synthetic state through deterministic retrieval; the cue and neutral key share the exact same database index and should be equivalent by construction. The experiment is a strong check that cue semantics do not unexpectedly change these results, but it is not a surprising empirical finding that two keys resolve to one record.

A separate lexical FTS5 cue lookup is only a diagnostic: because the query phrases and indexed text are not information-matched with opaque keys, its performance does not identify a unique causal benefit of symbolic cues. No statistical significance, cross-model generalization, subject continuity, or naturalistic agent utility is claimed.

The prospective next test is to use a stronger persona renderer and tasks requiring two or more verified original memories or relationship records, with candidate retrieval and provenance checking fixed and blinded semantic integration scoring. The correct architecture should enforce source ownership, stream separation, and nonnegotiable constraints before trusting prose-generating behavior.
