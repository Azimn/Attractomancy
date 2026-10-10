# E3-T1B: The Private Clerk — per-record typed extraction and compositional reuse

**Prepared:** October 10, 2026, before results. **Study:** exploratory synthetic capacity ablation, not main E3.  
**Fixture:** Original corrected E3-C v2, source-isolated record IDs and subject guard. **No new canonical Pretorius memory or lived experience.**

## Hypothesis

The first [joint two-record Clerk](CLERK_RESULTS.md) allowed Qwen2.5-0.5B to produce valid JSON on 12/12 full-source cases, but only 3/12 contained both correct source-attested values. It frequently confused which record contained the *original* fact versus the *later update*. Rather than adding a larger model or a neural subsystem, isolate the extraction operation by verified source record and allow software to combine the results.

## Intervention

Enumerate 3 test families × 2 possible first-record source values × 2 slots = **12 distinct verified source documents**. Each document has one local bit, with an opaque identifier independent of other state bits. A model receives **one record at a time**, no decision question, no second record, no correct action label, and a fixed instruction to return exactly \`{"value":"TOKEN"}\`. Slot/family labels describe the field to extract but do not disclose its value; e.g. "extract the signed original EAST/WEST route" or "extract the newer KEEP/FLIP amendment."

Each model generates just 12 independent isolated field extractions, with identical greedy decoding settings and a maximum of 32 generated tokens. Validate strict JSON shape, token vocabulary, the source-specific anchored factual clause, source owner, explicit version and content hash. Unsupported, malformed or missing fields cause a closed UNKNOWN result. An exact-format deterministic regex oracle supplies the same field without model generation and is correct by construction for these synthetic clauses.

For each of the original twelve complete E3-C factorial states, combine the two **independently cached model-produced source fields**. Apply the same deterministic two-bit decision rule only if both validated values are present; otherwise UNKNOWN. Score 12 complete outcomes, six paired counterfactual flips, and per-source first and second slot accuracy. Record total 12-call model token cost, average per-field cost, implied *cold* two-record lookup cost and reuse cost for all 12 full-state evaluations. This reuse is an **amortization of repeated source facts**, not a measured persistent character-memory benefit.

A software-only exact regex on synthetic clauses should always recover 12/12 original target decisions. This is plumbing, not an empirical claim about a model. The model-field ablation must be credited only for values that its original strict JSON response extracted correctly. Do not silently replace bad model fields with oracle fields when computing model-dependent outcomes.

**Primary comparison:** model joint full-source exact extraction, direct one-step output and per-record isolated extraction under the same fixed factorial inputs, but different prompt formats and number of inference calls. Therefore any gain is an *architecture ablation* with prompt-engineering confounds, not a controlled identification of independent cognitive capacity.

**Controls and gates:** No source text or event ID depends on the other record's bit; isolated prompts for each bit are identical regardless of eventual counterpart state. The original v2 provenance guard must reject wrong owner before passing any text. The real main E3 is still blocked by the absence of independently authored naturalistic questions and source-relevance reviewers. No production Pretorius runtime modification is allowed.

**Implementation:** [isolated_clerk.py](isolated_clerk.py), run-specific model artifacts, and [sch-e3-t1b-isolated.yml](../../.github/workflows/sch-e3-t1b-isolated.yml). Keep original outputs, model revision, prompt strings, source record hashes, strict score, and token accounting.
