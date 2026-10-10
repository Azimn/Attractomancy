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

## Qwen2.5-1.5B results

The second model completed all **72** independent-context cases. Its [raw dataset and provenance](results/qwen25-15b-38021662414/) report model revision \`989aa7980e4cf806f80c7fef2b1adb7bc71aa306\` and **11,996** total input and output tokens. The data were preserved in \`main\` after a completed successful workflow.

| Condition | Arbitrary factual recovery (8 items) | Policy integration (4 items) | Correct integrity handling (12 items) | Mean total tokens/query |
| --- | ---: | ---: | ---: | ---: |
| Cue only, no record | 0/8 | 3/4 accidental matches | 8/12 UNKNOWN | 112.83 |
| Correct full record plus symbol | 8/8 | 3/4 | 11/12 | 200.08 |
| Identical full record, ordinary marker | 8/8 | 4/4 | 12/12 | 198.17 |
| Selected correct record plus symbol | 8/8 | 4/4 | 12/12 | 144.75 |
| Identical selected record, neutral key | 8/8 | 4/4 | 12/12 | 143.75 |
| Incorrect full archive | 0/8 correct identity facts | 2/4 accidental matches | **1/12 UNKNOWN** | 200.08 |

The symbol-bearing full-record arm made one additional integration error (\`SEMAR\`, alarm without pass, responded ALLOW rather than REFUSE). By contrast, both selected-record arms, one carrying the original symbol and the other a neutral index key, generated the same correct answers to all twelve questions. This is **no observed evidence for an independent symbol advantage** with equivalent accessible records. The 12/12 selected-record accuracy is a small-sample exploratory observation, not a statistically established population effect.

At approximately 144 tokens per query rather than 199, the selected-record conditions saved **about 28% of input-plus-output tokens** without an observed quality loss on this model and fixture. The additional symbol-bearing token did not provide accuracy benefit. It is therefore *record selection*, not ceremonial cue semantics, that currently offers the more plausible engineering opportunity.

**Serious provenance failure persists at the higher capacity:** In 11 of 12 wrong-archive prompts the model produced an answer instead of the required UNKNOWN despite an explicit subject-ID mismatch. For the eight arbitrary-fact questions it often provided factual material from the *other* character. This behavior is the practical equivalent of an identity-memory contamination event and strongly motivates a deterministic subject-identity check before archive injection.

## Cross-model interpretation

The joint observations favor the ordinary external-information account of arbitrary autobiographical-fact recovery. Neither model recovered any of the eight concealed private facts from a bare cue, while both recovered all eight with the correct full archive. The original symbol did not outperform a plain full-record marker on either model. Likewise, selected-symbol and selected-neutral arms were identical within each model's output pattern, even when the 0.5B model failed two selected fact questions. The proposed **cue-specific residual benefit is not supported in these two runs**.

The small model's rule-integration accuracy stayed at 1/4 despite correct full or selected records; the larger model reached 3/4 to 4/4 with those records. This illustrates a separation between *data availability* and *the model's capacity to use that data for characteristic decisions*.

The provenance integrity controls were especially poor in both models: zero correct abstentions for the smaller model and one correct abstention for the larger model when deliberately given the wrong subject's record. The system's symbolic marker was not an effective integrity check. The strongest actionable architectural conclusion is to enforce identity, record-version, and trust-source agreement deterministically upstream of the language renderer.

**Causal limitations:** This is deterministic textual record injection, not a live retriever. There are only two synthetic profiles, six questions each, and one greedy response per model-case. The information-matched cue-versus-neutral observations are compatible with P5 but are far too small to establish practical equivalence universally. External records explain reconstruction in these test contexts, not persistence of model activations or a subjective self.


## Interpretation and next engineering step

D1 separates **record access**, **record selection**, **symbolic naming**, and **behavioral integration**. A model can perfectly repeat accessible private code words while failing to enact social boundaries and ignoring contradictory archive ownership. This argues for an explicit retrieval-side subject-ID check, trust/provenance metadata, and decision-rule verification independent of the renderer. It does not imply that a better renderer would necessarily fail in the same way.

The reported costs use actual model tokenizer input plus output counts. No inference subscription or paid API was used. Selected context is not a tested deployed retriever, and the token accounting does not cover a production memory service or persistence/write-back overhead.

The raw datasets should be retained unchanged, including negative results and instruction failures. This experiment does not by itself validate any mechanism for the cross-project Character Continuity evidence register.


## Deterministic record gate implementation

The [archive guard](archive_guard.py) and [tests](test_archive_guard.py) are committed as a reference integrity boundary. [GitHub Actions run 38021996965](https://github.com/Azimn/Attractomancy/actions/runs/38021996965) completed successfully with **10/10 unit tests passing**. The gate refuses records when a requested subject does not match indexed subject metadata or the record header, the source is not in a trusted allowlist, a revision is malformed, or recorded content differs from its SHA-256 digest. A deliberately forged record with a freshly computed matching checksum is accepted, demonstrating that this is an integrity and routing check rather than authenticated provenance. Production systems still need trusted source assertions or cryptographic signatures, authorization, versioning, and auditing.
