# DCH D0/v0.2: Evidence register

**Run date:** October 9, 2026 (America/Chicago). All values below are locally executed engineering observations. No actual language model was loaded because no compatible local weights or Ollama server were available. Do not infer dyadic effects.

## Existing deterministic lookup smoke

Twelve seeded synthetic histories, 480 events, 144 conditional-value cards (partially metadata only), 96 permission cards, 144 commitments (partially metadata only), 360 dilemmas, 96 sealed terminal probes. Of those 96, 48 are simple retrieval and 48 require combining a current persona value and a revocable permission. The seeded histories still share a template. Five v0.1 tests pass. The toy oracle and cold-start score 100% and 0%; human-coded and expert auto both 100%; passive-append 50%; ceremonial no-new-update 25%. **These are programmed reference values, not empirical measurements.**

## New v0.2 instrumentation

Fifteen unit tests pass, including a terminal run that proves the fake model was never handed an `expected` field, a development-phase test that rejects any sealed-file input, and a strict no-overwrite rule for raw outputs. Four mocked terminal generations pass through the model-runner/evaluator boundary (two per simulated arm). Their fake model scores 0% on the two test prompts; this is a deliberately hard-coded UNKNOWN output, not an LLM null.

The three-turn scripted yoked control produces exactly matching replay hashes in the strict same-tape condition. When a synthetic permission revocation is introduced, its coded adaptive policy correctly repairs 3/3 trials, whereas a nonadaptive baseline tape remains correct 2/3. The 1/3 difference is **mechanically produced by the test script**. It demonstrates detection sensitivity for contingency, not constitution, human specificity, or a real-language-model repair mechanism.

The budget audit correctly **fails closed** when compared arms lack token measurements. G1 and G2 apply only to the toy oracle, G5 is a partial engineering check, and the G6 strict mock-control passes. G3, G4 and actual model/partner runs have not occurred. **Overall status: NO-GO for inferential or human work.**

## Next gates

The next actual execution is an LLM feasibility comparison on development data, with model hash/version, inference/token counts and full raw generations recorded. Verify a realistic automatic archive controller, independently written dilemmas, and fixed-budget parity before touching the sealed terminal suite. Only afterward should continuing-partner and newcomer live trajectories be collected under the locked yoked-replay protocol. Refusing to claim a positive effect from a deterministic toy is a requirement of the study, not a failure.

## First real-model calibration: L2, completed

**Measured run:** [Qwen2.5-0.5B GitHub Actions 38025405271](https://github.com/Azimn/Attractomancy/actions/runs/38025405271). Raw generations and evaluator results are in `results/qwen25-05b-l2-38025405271/`. All 40 model responses were parseable but all 40 chose SCHEDULE, independent of correct answer and whether the archive was expert curated, a human-coded proxy, stale, cold, or full-oracle. The correct SCHEDULE prevalence is 25%, therefore all conditions scored 2/8 action accuracy and 0/8 full-four-record provenance. Exact-input expert/human-proxy hashes and outputs matched 8/8. Source hallucinations include unprovided E13. This is a model-capacity or task-interface failure, **not evidence against DCH**. See [full result](L2_REAL_MODEL_RESULT_2026-10-09.md).

**Instrument verification:** The separate deterministic `reference_solver.py` validates all 12 generated answer keys and rejects unauthorized E13 when constructing decisions. Branch-minimal evidence and full-four-record evidence are now separate measurements in exploratory L2C. The complete local test suite currently passes 24 tests.

**Follow-up status at this snapshot:** [Qwen2.5-1.5B frozen-fixture capacity replication](https://github.com/Azimn/Attractomancy/actions/runs/38025720757) and [Qwen0.5B compact-vs-original record-format calibration](https://github.com/Azimn/Attractomancy/actions/runs/38025854993) entered model inference. They have no verified scores at this snapshot; do not reinterpret queued/in-progress work as a positive result.

**Current advancement decision remains NO-GO** for confirmatory or human dyadic trials. The original smoke numbers above remain historical engineering observations, not current proof of an efficacy hypothesis.
