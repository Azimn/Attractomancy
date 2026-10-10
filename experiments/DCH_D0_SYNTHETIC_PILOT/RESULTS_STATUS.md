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
