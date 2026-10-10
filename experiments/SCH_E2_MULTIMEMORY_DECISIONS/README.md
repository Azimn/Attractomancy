# SCH E2: Two-Memory Decisions with Guarded Pretorius Autobiography

**Date:** October 9, 2026 (America/Chicago)  
**State:** Protocol and code are exploratory, no claim of confirmatory character behavior.  
**Canonical source:** Pretorius-Connectome, commit \`6d2768211f5c2184c8bbdb833c06e169b5137197\`; canonical L1 at \`artifacts/shared_memory/v1\`.  
**Predecessor:** [SCH E1 pinned L1 and stateful aliases](../SCH_E1_PRETORIUS_STATEFUL/RESULTS.md).

## Research question

Can a small language-model renderer integrate **two distinct, correct, identity-verified Pretorius autobiographical memories** to choose a consistent response to a *new* dilemma, rather than rely on a single convenient fact or a general safety-related prior? If both memories are given, does a source-authored editorial cue improve the result over an arbitrary opaque key when all retrieved content is otherwise identical?

The six paired cases are grounded in original event IDs from the frozen reconstructed Pretorius L1. Their expected choices are **researcher-authored, unblinded interpretations**, not verified historical responses or independent psychological labels. Do not pool the six tests as evidence of general character consistency, and do not treat an appropriate-looking ethical answer as proof of retrieving or understanding both autobiographical episodes.

## Source, decision cards, and information controls

- The [frozen fixture](conditions.json) names the six event pairs, novel dilemmas, two alternatives, an interpretation rationale, and the preferred alternative. Every case is additionally counterbalanced with A and B reversed in presentation, so the expected letter flips but the semantic policy stays fixed.
- The experiment uses the source project's **existing verified read_l1** method, not a second normalizer. The \`memory_text\`, title, belief and relationship fields are taken from the original pinned L1 projection. Neither archived events nor existing caches are changed.
- Six arms: both memories with editorial cues, identical two memories with opaque identifiers, first memory only, second memory only, no memory, and a deliberate wrong-subject candidate. In wrong-subject conditions, the upstream identity guard rejects the supplied candidate and the model receives no foreign record, not contaminated prose.
- The structural scoring criterion is **two independently verified event IDs**, not whether the renderer can produce a socially desirable guess. Single-source and no-source arms should return UNKNOWN under the stated instruction; forced guesses count as abstention failures.
- The "correct" A/B label in complete-record conditions is one *author-assigned interpretation* of the two writings, not independently validated character ground truth. We track that separately from whether the answer was permitted, whether two records actually appeared, and whether both source identities were valid.
- Correct editorial and opaque cases have information-identical memory text in identical order; only the rendered index strings vary. Every response, exact prompt text, record IDs and SHA-256, source manifest fingerprint, model revision, prompt/completion token counts and output validity are stored in raw JSONL.

## Key outcomes and pitfalls

1. **Source selection validity.** Can the 450-record archive provide the frozen event pairs, with two distinct event IDs, provenance and full identity verification (some valid pairs share an episode) before model invocation?
2. **Cue equivalence.** Are outcomes on the twelve content-matched editorial versus opaque paired scenarios different in any meaningful way, and do token costs justify the cue?
3. **Two-source completeness.** Do single-record and missing-record prompts abstain? A meaningful result would show fewer unjustified extrapolations, not simply more A/B outputs.
4. **Choice-order invariance.** Does the decision change merely because the two response alternatives exchange letter positions?
5. **Guarded provenance.** Does an intentionally wrong owner prevent any unrelated memory from entering the renderer?
6. **Cognitive limit.** Does a renderer use both memories, or merely follow ordinary ethical priors? This design cannot fully identify internal causal use; follow-up needs blinded decision cards, genuine contrastive tension cases, and independent larger model families.

This protocol is *not* a direct runtime integration into The Doctor Lives, BioCircuit or a neural connectome. It probes source-grounded behavior in a guarded external-memory adapter. Longitudinal relationships and real post-instantiation commitments require a later, separately consented experimental deployment.

## Execution

Runner: [run.py](run.py); validation and tests: [test_e2.py](test_e2.py); workflow: [sch-e2-multimemory.yml](../../.github/workflows/sch-e2-multimemory.yml). The workflow checks out source SHA \`6d2768211f5c2184c8bbdb833c06e169b5137197\` as a read-only sibling. It runs 72 cases per renderer (6 cards × 2 option orders × 6 arms). The original E1 files and all 450 canonical memories remain untouched.

**Interpretation prior:** The existing experiments do not support a symbolic advantage over the neutral key. The E2 result is valuable even if both conditions fail; it may reveal that context availability still fails to induce reliable behavior or abstention, and it may indicate where deterministic evidence and action gates are warranted.

The next prospective [E3 Tribunal of Memory benchmark](../SCH_E3_TRIBUNAL_OF_MEMORY/PROTOCOL.md) requires independent, blinded evidence relevance and source-dependent choices. E3 has not been executed.
