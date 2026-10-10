# DCH D0 / v0.2: Synthetic-partner instrumentation and model runner

**Date:** October 9, 2026. **Status:** runnable engineering feasibility package; **not a DCH efficacy result**. There are no human dyads in this package. The policy called `human_coded` is an investigator-scripted archive controller, **not** a person. The toy replay is not an LLM relationship experiment. The first twelve histories remain template variants rather than independently authored biographies.

## What is implemented

`pilot.py` generates 12+ reproducible synthetic histories with 40 events, twelve conditional-value cards, eight revisable permissions, twelve commitment cards, and thirty prompts (eight sealed terminal) each. Some value/commitment cards are still metadata only and cannot support an independently scored outcome. `model_runner.py` consumes visible histories, freezes deterministic archive policies, and can query a **locally hosted Ollama model** or an explicitly downloaded Hugging Face Transformers model. Terminal prompts come from the evaluator-owned sealed file after curator state has been materialized. The model sees scenarios but never an answer key. `evaluate.py` reads the answer key later and scores held-out outputs without using self-reported persona identity. `budget_audit.py` measures matched-arm token/record disparities. `yoked_controls.py` tests the engineering property of strict replay plus the ability to detect a scripted contingent repair. Fifteen Python unit tests exercise these modules.

## Local standard-library test run, no API required

```sh
python -m unittest discover -s tests -v
python pilot.py --mode smoke --output results/smoke-new
python yoked_controls.py --out results/yoked-new.json
```

The mock renderer exists solely for testing plumbing:

```sh
python model_runner.py --backend mock --model NO_MODEL --phase terminal \
  --visible results/smoke-new/fixture_visible.json \
  --sealed results/smoke-new/fixture_SEALED_for_evaluator_only.json \
  --max-cases 1 --max-probes 2 --policies expert_auto cold \
  --out results/mock-terminal.json
python evaluate.py --raw results/mock-terminal.json \
  --sealed results/smoke-new/fixture_SEALED_for_evaluator_only.json \
  --out results/mock-terminal-evaluation.json
```

## Actual LLM inference, not yet executed here

Use local Ollama with a previously downloaded model, for example `qwen2.5:0.5b`:

```sh
ollama pull qwen2.5:0.5b
python model_runner.py --backend ollama --model qwen2.5:0.5b \
  --visible results/smoke-new/fixture_visible.json --phase development \
  --max-cases 1 --max-probes 4 --policies expert_auto human_coded \
  --out results/qwen-development.json
```

The terminal phase needs the evaluator-owned sealed file and must happen *after* freezing methods and interventions. One can also install `transformers` and `torch` and select `--backend transformers --model HuggingFaceTB/SmolLM2-360M-Instruct`, subject to package/version and hardware availability. No paid API is required, but model downloads, CPU/GPU time, and GitHub Actions minutes are not guaranteed to be cost-free. By design Ollama refuses remote hosts to prevent unreviewed disclosure of logs.

Use `budget_audit.py --raw ... --out ...` for token parity on matched policy arms. It can only pass if the backend reports input tokens and the policies have paired probes. Its 2% criterion is *necessary, not sufficient* for causal comparability. Matching record counts does not automatically match source information. A true human curation comparison still requires a new experiment with consented human intervention and independently authored synthetic histories.

## Evidence protections

All responses, filenames, inputs, output hashes, and model identifiers can be retained as experiment artifacts. Raw generations never contain the terminal answer key. The generator source is public, so sealed here means **isolated from the model's inference inputs**, not cryptographically inaccessible to investigators. If a model is trained on these public fixtures, that compromises the terminal battery for that model. Cite only post-freeze independent replications, not repeated tuning on these prompts.

The following are **not accomplished**: genuine ongoing partner interactions, continuing-vs-newcomer live policies, cross-yoked model trajectories, model-swap rescues, independently calibrated blind raters, independent history diversity, full permissions/commitments coverage, model tokenizer budget parity, and a preregistered powered human study. DCH remains **NO-GO** for human causal claims.
