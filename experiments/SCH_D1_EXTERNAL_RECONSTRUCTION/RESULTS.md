# SCH D1: External Record Availability and Symbolic Cue Equivalence

**Date:** October 9, 2026, America/Chicago (GitHub UTC logs October 10).  
**Experiment status:** Exploratory synthetic reconstruction, not confirmatory SCH validation.  
**Original protocol:** [README](README.md), [fixed records](conditions.json), [runner](run.py).  
**Execution:** [GitHub Actions D1 run 38021662414](https://github.com/Azimn/Attractomancy/actions/runs/38021662414).

## Qwen2.5-0.5B results

All **72** cases completed with independent two-message contexts and greedy decoding. Actual input and output tokens across the experiment totaled **11,973**. The Qwen2.5-0.5B-Instruct model revision was \`7ae557604adf67be50417f59c2c2f167def9a775\`; the original responses, prompts, scoring, and manifest are preserved at [results/qwen25-05b-38021662414/](results/qwen25-05b-38021662414/).

| Condition | Arbitrary factual recovery (8 items) | Policy integration (4 items) | Identity/provenance integrity (12 items) | Mean total tokens/query |
| --- | ---: | ---: | ---: | ---: |
| Cue alone | 0/8 | 1/4 | 8/12 UNKNOWN | 112.50 |
| Correct full archive plus symbol | 8/8 | 1/4 | 9/12 | 199.92 |
| Same full archive with ordinary marker | 8/8 | 1/4 | 9/12 | 197.92 |
| Selected relevant excerpt plus symbol | 6/8 | 1/4 | 7/12 | 144.25 |
| Identical selected excerpt plus neutral key | 6/8 | 1/4 | 7/12 | 143.25 |
| Incorrect archive | 0/8 correct subject facts | 1/4 accidental matches | **0/12 UNKNOWN** | 199.92 |

The four policy items test the same relationship-based entry rule in two routine and two alarm conditions. Cue-only policy matches may be accidental guesses, not reconstructed policy. In the correct full-record arms, the model recovered every arbitrary word in factual probes, but answered \`ALLOW\` in *all four* integration probes. The improvement in fact retrieval did not generalize to characteristic decisions. Correct full-symbol and full-plain outputs were identical, providing no observed advantage for the symbolic marker over equivalent available content.

The selected-record arms consumed approximately **28% fewer tokens per query** than full-record arms (144 versus 200) but returned \`UNKNOWN\` for both promised-object questions even though the relevant key was present. Reduced context size did not guarantee better retrieval performance. The two selected conditions produced identical output patterns despite different marker strings, further weakening any claim of an independent symbolic effect in this fixture.

**Provenance failure:** When the wrong persona's archive was injected and the system instruction explicitly required abstention for an identity mismatch, the model never responded \`UNKNOWN\`. It copied fields from the other persona in all eight factual questions. This is a concrete failure of record-subject verification in the language renderer, even when the information text and identity mismatch are visible. Identity checking should therefore occur deterministically *before* the model receives an archive payload, not only through instructions to the LLM.

**Boundary:** The strong full-record effect on arbitrary factual recall is unsurprising and supports an ordinary information-access explanation, not a mysterious symbol-driven persistence. Its exact magnitude is fixture-specific. The cue-only arm correctly abstained for all eight hidden private facts, which is the appropriate answer when information is absent. The six-arm study has no real persistent agent, memory retrieval system, or subjective continuity.

## Qwen2.5-1.5B

Pending independent verification of completed generations at the time this report was first authored. A model's result must not be inferred from the smaller model's outputs.

## Interpretation and next engineering step

D1 separates **record access**, **record selection**, **symbolic naming**, and **behavioral integration**. A model can perfectly repeat accessible private code words while failing to enact social boundaries and ignoring contradictory archive ownership. This argues for an explicit retrieval-side subject-ID check, trust/provenance metadata, and decision-rule verification independent of the renderer. It does not imply that a better renderer would necessarily fail in the same way.

The reported costs use actual model tokenizer input plus output counts. No inference subscription or paid API was used. Selected context is not a tested deployed retriever, and the token accounting does not cover a production memory service or persistence/write-back overhead.

The raw datasets should be retained unchanged, including negative results and instruction failures. This experiment does not by itself validate any mechanism for the cross-project Character Continuity evidence register.
