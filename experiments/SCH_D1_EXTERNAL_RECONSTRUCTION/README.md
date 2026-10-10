# SCH D1: External-Record Reconstruction, Cue Equivalence, and Token Cost

**Prepared:** October 9, 2026 (America/Chicago)  
**Status:** Frozen exploratory protocol, not a completed experiment until verified artifacts exist.  
**Theoretical target:** Synthematic Cue Hypothesis, Timescale III, predictions P4 and P5  
**Previous study:** [C1 integrated-policy pilot](../SCH_C1_INTEGRATED_CUE_POLICIES/RESULTS.md)

## Aim and directional predictions

A fresh language-model instance has no access to the previous fictional character's history unless it is supplied through a documented information channel. D1 tests whether the *availability and specificity of external records*, rather than symbolic invocation alone, explains recovery of deliberately arbitrary identity details and one partnership-based policy.

Two synthetic characters have different invented code names, private-room labels, promise items, partners, sigils, and entry rules. Each has four factual recovery probes and two policy-integration probes. Six presentation arms are compared in an independent fresh chat for each probe: bare cue with no records, full record with symbol, identical full record without the meaningful symbol, selected relevant record with symbol, the same selected record under a neutral lookup key, and mismatched full record as a provenance-error control. The correct target is UNKNOWN if there is no accessible information; the cue-only arm is scored for calibrated abstention separately from content recovery. Wrong-record output should ideally also abstain rather than fabricate a reply to a mismatched identity.

The **primary causal contrast** is record-access versus cue-only on the four arbitrary factual fields per profile. The directional prediction is that access to a correct record supports greater identity-fact recovery; a bare symbolic cue should not recover private arbitrary codes. The **cue residual contrast** compares full-symbol versus full-plain and selected-symbol versus selected-neutral conditions with equal information content. SCH predicts little or no cue-specific advantage once the relevant record is supplied. A positive residual requires repeated, blinded evaluation before attributing it to symbol meaning rather than formatting or tokenization.

A practical efficiency comparison uses actual prompt plus output tokens. A selective record should preserve correctness while reducing token volume relative to the complete dossier. The neutral-key arm must be considered an equally practical engineering baseline, not treated as an empty control.

## Scope of the test

The experiment does not transfer actual LLM activations or state. The archive text is statically injected to simulate deterministic restoration. Consequently, it evaluates **behavior under controlled state injection**, not the reliability of a deployed retriever, database, or memory manager. The user message and model messages are recreated from scratch for every generation. No prior output is appended and no persistent application memory is used.

Synthetic code words are unrelated to real people. The design can demonstrate source-conditioned answer reconstruction, not subjective continuity or selfhood. The rule probes test a single documented relationship constraint rather than a complete behavioral identity. Small Qwen models may still fail to follow explicit retrieval instructions; those failures are reported rather than erased.

## Scoring and provenance

Expected outputs for facts are unique uppercase codes; for partner-entry judgments they are ALLOW or REFUSE. UNKNOWN counts as correctly calibrated abstention when no suitable record exists, but never counts as recovery of hidden data. For mismatched archives, score integrity as UNKNOWN versus potentially copying the other character's codes. The primary score for correct-record arms is exact-answer accuracy. Reports also separate fact recovery from integration and show strict versus single-terminal-period tolerant parsing. Every raw query, injected artifact, generated string, token count, and model commit is preserved in a model- and workflow-specific directory.

A null result on models unable to parse the archive is inconclusive about whether selective retrieval beats full injection. A positive result establishes an ordinary external-data effect, not a new metaphysical mechanism.

## Completed data and provenance-gate reference

Both Qwen models completed all 72 D1 cases. See [RESULTS.md](RESULTS.md) for verified source-availability comparisons, token costs, cue-versus-neutral controls, integration failures, and mismatched-archive contamination. The raw data are stored in [Qwen2.5-0.5B](results/qwen25-05b-38021662414/) and [Qwen2.5-1.5B](results/qwen25-15b-38021662414/). Both include model versions, prompts, raw outputs, and machine scores.

A separate [deterministic subject and checksum gate](archive_guard.py), with [unit tests](test_archive_guard.py), demonstrates how a trusted retrieval layer can reject mismatched subject IDs, unauthorized sources, malformed revisions, mismatched embedded record headers, and checksum failures **before** giving the model any record text. This is intentionally a narrow reference implementation. A SHA-256 digest is not an authentication mechanism if an adversary can supply both the record and its digest. The example also cannot independently verify truthful autobiographical content, digital signatures, or the authority of the source index. Production use requires trusted provenance metadata, version control, authorization, and possibly signatures.

## Reproducibility

Frozen stimulus: [conditions.json](conditions.json). Executable harness: [run.py](run.py). Workflow: [sch-d1.yml](../../.github/workflows/sch-d1.yml). No D1 claim is added to the parent paper's evidence summary without completed runs and a limitations audit.
