#!/usr/bin/env python3
"""EXP-A zero-shot synthematic cue pilot. No API keys or persistent model memory."""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import platform
import random
import re
import statistics
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIXTURE = HERE / "conditions.json"
WORDS = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def fixture() -> tuple[dict, str]:
    raw = FIXTURE.read_bytes()
    obj = json.loads(raw)
    assert obj["schema_version"] == "EXP-A-0.1"
    assert len(obj["regimes"]) == 2
    assert len(obj["questions"]) == 3
    assert len({q["id"] for q in obj["questions"]}) == 3
    for regime in obj["regimes"]:
        kinds = [c["kind"] for c in regime["conditions"]]
        assert kinds == [
            "familiar_emoji", "familiar_word", "neutral_word",
            "arbitrary_name", "plain_instruction",
        ], kinds
        assert len(set(kinds)) == 5
        assert len(regime["expected_stems"]) == len(set(regime["expected_stems"]))
        assert all("cue" in c for c in regime["conditions"])
    return obj, sha256(raw)

def build_cases(obj: dict) -> list[dict]:
    cases = []
    for regime in obj["regimes"]:
        for condition in regime["conditions"]:
            for question in obj["questions"]:
                cases.append({
                    "id": f'{regime["id"]}/{condition["id"]}/{question["id"]}',
                    "regime": regime["id"],
                    "label": regime["label"],
                    "stems": regime["expected_stems"],
                    "arm": condition["id"],
                    "cue": condition["cue"],
                    "question_id": question["id"],
                    "question": question["text"],
                })
    random.Random(obj["seed"]).shuffle(cases)
    assert len(cases) == 30
    assert len({c["id"] for c in cases}) == len(cases)
    return cases

def prompt_for(obj: dict, case: dict) -> list[dict]:
    return [
        {"role": "system", "content": obj["instruction"]},
        {"role": "user", "content": obj["user_template"].format(
            cue=case["cue"], question=case["question"]
        )},
    ]

def lexical_score(output: str, case: dict) -> dict:
    words = [w.lower() for w in WORDS.findall(output)]
    exclusion = case["cue"].lower() if case["arm"] == "familiar_word" else ""
    hits = [
        w for w in words
        if w != exclusion and any(w.startswith(stem) for stem in case["stems"])
    ]
    return {
        "word_count": len(words),
        "register_marker_words": len(hits),
        "register_marker_rate_per_100_words": round(100 * len(hits) / max(1, len(words)), 4),
        "register_marker_examples": hits,
        "exact_cue_echo_count": (
            output.casefold().count(case["cue"].casefold())
            if case["arm"] != "plain_instruction" else None
        ),
    }

def aggregates(rows: list[dict]) -> list[dict]:
    groups: dict[tuple[str, str], list[dict]] = collections.defaultdict(list)
    for row in rows:
        groups[(row["regime"], row["arm"])].append(row)
    out = []
    for (regime, arm), group in sorted(groups.items()):
        out.append({
            "regime": regime,
            "arm": arm,
            "n": len(group),
            "mean_register_proxy_per_100_words": round(
                statistics.mean(r["metrics"]["register_marker_rate_per_100_words"] for r in group), 4
            ),
            "mean_prompt_tokens": round(statistics.mean(r["prompt_tokens"] for r in group), 2),
            "mean_output_tokens": round(statistics.mean(r["generated_tokens"] for r in group), 2),
            "mean_total_tokens": round(statistics.mean(
                r["prompt_tokens"] + r["generated_tokens"] for r in group
            ), 2),
            "cue_echoed_cases": sum(
                (r["metrics"]["exact_cue_echo_count"] or 0) > 0 for r in group
            ),
        })
    return out

def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--validate-only", action="store_true")
    p.add_argument("--model", default="Qwen/Qwen2.5-0.5B-Instruct")
    p.add_argument("--output", type=Path, default=HERE / "results" / "pilot-open-model")
    p.add_argument("--max-cases", type=int, default=30)
    args = p.parse_args()
    obj, digest = fixture()
    cases = build_cases(obj)
    assert 1 <= args.max_cases <= len(cases)
    print(f"FIXTURE_SHA256={digest}; CASES={len(cases)}", flush=True)
    if args.validate_only:
        for c in cases:
            assert len(prompt_for(obj, c)) == 2
            assert c["cue"] in prompt_for(obj, c)[1]["content"]
        print("VALIDATION PASS: fixture, balance, unique IDs, and isolation templates", flush=True)
        return 0

    import torch
    import transformers
    from transformers import AutoModelForCausalLM, AutoTokenizer

    torch.set_num_threads(min(4, torch.get_num_threads()))
    start = time.monotonic()
    print(f"LOAD_MODEL={args.model}", flush=True)
    tokenizer = AutoTokenizer.from_pretrained(args.model, trust_remote_code=False)
    model = AutoModelForCausalLM.from_pretrained(
        args.model, torch_dtype=torch.float32, trust_remote_code=False
    )
    model.eval()
    resolved_revision = getattr(model.config, "_commit_hash", None)
    args.output.mkdir(parents=True, exist_ok=True)

    meta = {
        "study": "EXP-A zero-shot synthematic cue pilot",
        "status": "exploratory_pilot_not_confirmatory",
        "model": args.model,
        "model_resolved_commit": resolved_revision,
        "tokenizer_name": getattr(tokenizer, "name_or_path", None),
        "fixture_sha256": digest,
        "fixture_version": obj["schema_version"],
        "case_order_seed": obj["seed"],
        "greedy_decoding": True,
        "max_new_tokens": obj["max_new_tokens"],
        "python": platform.python_version(),
        "torch": torch.__version__,
        "transformers": transformers.__version__,
        "cases_planned": len(cases),
        "cases_attempted": min(args.max_cases, len(cases)),
        "run_scope": "full_30_case_pilot" if args.max_cases == 30 else "partial_smoke",
        "conditioning": "none",
        "archive_access": "none",
        "independent_context_per_generation": True,
    }
    write_json(args.output / "manifest.json", meta)
    rows: list[dict] = []
    raw_path = args.output / "responses.jsonl"
    with raw_path.open("w", encoding="utf-8") as handle:
        for idx, case in enumerate(cases[:args.max_cases], start=1):
            messages = prompt_for(obj, case)
            inputs = tokenizer.apply_chat_template(
                messages, add_generation_prompt=True,
                tokenize=True, return_tensors="pt",
            )
            attention_mask = torch.ones_like(inputs)
            with torch.inference_mode():
                generated = model.generate(
                    input_ids=inputs,
                    attention_mask=attention_mask,
                    max_new_tokens=obj["max_new_tokens"],
                    do_sample=False,
                    pad_token_id=tokenizer.eos_token_id,
                )
            output_ids = generated[0, inputs.shape[1]:]
            output_text = tokenizer.decode(output_ids, skip_special_tokens=True)
            row = {
                "case_id": case["id"],
                "regime": case["regime"],
                "arm": case["arm"],
                "cue": case["cue"],
                "question": case["question"],
                "messages": messages,
                "output": output_text,
                "prompt_tokens": int(inputs.shape[1]),
                "generated_tokens": int(output_ids.shape[0]),
                "metrics": lexical_score(output_text, case),
            }
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            handle.flush()
            rows.append(row)
            print(f"CASE={idx}/{args.max_cases}; id={case['id']}; "
                  f"tokens={row['prompt_tokens']}+{row['generated_tokens']}; "
                  f"proxy={row['metrics']['register_marker_rate_per_100_words']}", flush=True)

    summary = {
        **meta,
        "elapsed_seconds": round(time.monotonic() - start, 2),
        "cases_completed": len(rows),
        "actual_generated_tokens": sum(x["generated_tokens"] for x in rows),
        "actual_prompt_tokens": sum(x["prompt_tokens"] for x in rows),
        "aggregate_by_regime_arm": aggregates(rows),
        "interpretation": (
            "Mechanical lexical proxy only. No blinded judgment, confirmatory "
            "effect estimate, personal-memory recovery, or persistence inference."
        ),
    }
    write_json(args.output / "summary.json", summary)
    print("SUMMARY_JSON_BEGIN", flush=True)
    print(json.dumps({
        "model": args.model, "revision": resolved_revision,
        "cases_completed": len(rows),
        "tokens": summary["actual_prompt_tokens"] + summary["actual_generated_tokens"],
        "aggregate_by_regime_arm": summary["aggregate_by_regime_arm"],
    }, ensure_ascii=False), flush=True)
    print("SUMMARY_JSON_END", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())
