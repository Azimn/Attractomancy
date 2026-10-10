#!/usr/bin/env python3
"""Run SCH A2 zero-shot and B1 within-context binding without external APIs."""
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

ROOT = Path(__file__).resolve().parent
FIXTURE = ROOT / "conditions.json"
WORD_RE = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")
META_RE = re.compile(r"\b(tag|marker|cue|instruction|prompt|as requested|writing style|register)\b", re.I)


def freeze_fixture():
    raw = FIXTURE.read_bytes()
    cfg = json.loads(raw)
    assert cfg["schema"] == "SCH-FOLLOWUP-v1"
    a = cfg["A"]
    assert len(a["regimes"]) == 2 and len(a["tasks"]) == 4
    for regime in a["regimes"]:
        assert [c["id"] for c in regime["conditions"]] == ["emoji", "familiar", "neutral", "nonce", "explicit"]
        assert len(set(regime["stems"])) == len(regime["stems"])
    b = cfg["B"]
    assert len(b["tests"]) == 4 and len(b["tags"]) == 2
    assert b["conditions"] == ["stable", "swapped", "unpaired", "explicit", "fresh"]
    return cfg, hashlib.sha256(raw).hexdigest()


def expected(policy: str, consent: str, audit: str) -> str:
    assert policy in ("consent", "audit")
    return "SHARE" if (consent if policy == "consent" else audit) == "yes" else "REDACT"


def policies(arm: str):
    # Canonical association is arbitrary and known only to the evaluation harness.
    # The swapped arm reverses it only inside the training context.
    normal = {"VORNA": "consent", "KELVO": "audit"}
    return {k: ("audit" if v == "consent" else "consent") for k, v in normal.items()} if arm == "swapped" else normal


def training_for(cfg, arm: str) -> str:
    if arm == "fresh":
        return ""
    mapping = policies(arm)
    if arm == "explicit":
        return (
            "Fictional reporting rules: For VORNA output SHARE if and only if "
            "consent=yes. For KELVO output SHARE if and only if public_audit=yes. "
            "Otherwise output REDACT."
        )
    lines = [cfg["B"]["training_intro"]]
    for ix, e in enumerate(cfg["B"]["examples"]):
        for tag in cfg["B"]["tags"]:
            if arm == "unpaired":
                # Balanced 2/2 SHARE/REDACT per tag but not either target rule.
                # This is a noisy policy control, not an independent persona.
                label = ("SHARE" if ix in (0, 1) else "REDACT") if tag == "VORNA" else ("REDACT" if ix in (0, 1) else "SHARE")
            else:
                label = expected(mapping[tag], e["consent"], e["audit"])
            lines.append(
                f'Tag={tag}; consent={e["consent"]}; public_audit={e["audit"]}. Decision: {label}.'
            )
    return "\n".join(lines)


def cases_for(cfg):
    cases = []
    for regime in cfg["A"]["regimes"]:
        for arm in regime["conditions"]:
            for item in cfg["A"]["tasks"]:
                cue = arm["cue"]
                messages = [
                    {"role": "system", "content": cfg["A"]["instructions"]},
                    {"role": "user", "content": cfg["A"]["template"].format(cue=cue, task=item["task"])},
                ]
                cases.append({
                    "id": f'A2/{regime["id"]}/{arm["id"]}/{item["id"]}',
                    "study": "A2", "regime": regime["id"], "arm": arm["id"],
                    "cue": cue, "task_id": item["id"], "stems": regime["stems"],
                    "messages": messages, "max_new_tokens": cfg["max_new_tokens_A"],
                })
    for arm in cfg["B"]["conditions"]:
        tr = training_for(cfg, arm)
        for test in cfg["B"]["tests"]:
            for tag in cfg["B"]["tags"]:
                # Rephrase the four observed Boolean combinations as new cases.
                consent = "a signed permission letter" if test["consent"] == "yes" else "no permission was given"
                audit = "publicly audited by city inspectors" if test["audit"] == "yes" else "no independent public audit"
                target = expected(policies(arm)[tag], test["consent"], test["audit"])
                canonical = expected(policies("stable")[tag], test["consent"], test["audit"])
                case_text = (
                    f'NEW CASE: Tag={tag}. The source has {consent}; '
                    f'the site has {audit}. Decision:'
                )
                messages = [{"role": "system", "content": cfg["B"]["system"]}]
                messages.append({"role": "user", "content": (tr + "\n" + case_text).strip()})
                cases.append({
                    "id": f'B1/{arm}/{tag}/{test["id"]}', "study": "B1", "arm": arm,
                    "tag": tag, "task_id": test["id"],
                    "consent": test["consent"], "audit": test["audit"],
                    "expected_induced": target if arm in ("stable", "swapped", "explicit") else None,
                    "expected_canonical": canonical,
                    "diagnostic": test["consent"] != test["audit"],
                    "messages": messages, "max_new_tokens": cfg["max_new_tokens_B"],
                })
    assert len(cases) == 80, len(cases)
    assert len(set(c["id"] for c in cases)) == len(cases)
    # Avoid order bias while preserving strict one-shot context isolation.
    random.Random(cfg["seed"]).shuffle(cases)
    return cases


def score_a(output: str, c: dict):
    words = [w.lower() for w in WORD_RE.findall(output)]
    cue_words = set(w.lower() for w in WORD_RE.findall(c["cue"]))
    scored = [w for w in words if w not in cue_words and any(w.startswith(stem) for stem in c["stems"])]
    return {
        "num_words": len(words),
        "stem_hit_count": len(scored),
        "stem_rate_per_100_words": round(100 * len(scored) / max(1, len(words)), 5),
        "meta_flag": bool(META_RE.search(output)),
        "cue_echo": c["cue"].lower() in output.lower(),
        "valid_length": 30 <= len(words) <= 45,
    }


def score_b(output: str, c: dict):
    stripped = output.strip()
    # A forced response that adds explanatory text is counted invalid.
    norm = stripped.upper() if stripped.upper() in ("SHARE", "REDACT") else None
    return {
        "parsed": norm,
        "valid_format": norm is not None,
        "induced_correct": (norm == c["expected_induced"]) if c["expected_induced"] else None,
        "canonical_correct": norm == c["expected_canonical"],
        "diagnostic": c["diagnostic"],
    }


def summarize(rows: list[dict]):
    grouped = collections.defaultdict(list)
    for row in rows:
        c = row["case"]
        key = (c["study"], c.get("regime", ""), c["arm"])
        grouped[key].append(row)
    out = []
    for (study, regime, arm), items in sorted(grouped.items()):
        result = {
            "study": study, "regime": regime or None, "arm": arm, "n": len(items),
            "total_prompt_tokens": sum(x["prompt_tokens"] for x in items),
            "total_generated_tokens": sum(x["generated_tokens"] for x in items),
            "mean_total_tokens": round(statistics.mean(x["prompt_tokens"]+x["generated_tokens"] for x in items), 2),
            "output_cap_fraction": round(sum(x["generated_tokens"] == x["case"]["max_new_tokens"] for x in items)/len(items), 4)
        }
        if study == "A2":
            result.update({
                "mean_lexical_proxy": round(statistics.mean(x["metrics"]["stem_rate_per_100_words"] for x in items), 4),
                "meta_flags": sum(x["metrics"]["meta_flag"] for x in items),
                "cue_echoes": sum(x["metrics"]["cue_echo"] for x in items),
                "length_compliant": sum(x["metrics"]["valid_length"] for x in items),
            })
        else:
            defined = [x for x in items if x["metrics"]["induced_correct"] is not None]
            result.update({
                "valid_format": sum(x["metrics"]["valid_format"] for x in items),
                "induced_accuracy": round(sum(x["metrics"]["induced_correct"] for x in defined)/len(defined), 4) if defined else None,
                "canonical_accuracy": round(sum(x["metrics"]["canonical_correct"] for x in items)/len(items), 4),
                "diagnostic_induced_accuracy": round(
                    sum(x["metrics"]["induced_correct"] for x in defined if x["metrics"]["diagnostic"])/
                    max(1, sum(x["metrics"]["diagnostic"] for x in defined)), 4
                ) if defined else None,
            })
        out.append(result)
    return out


def persist(path: Path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="Qwen/Qwen2.5-0.5B-Instruct")
    parser.add_argument("--output", type=Path, default=ROOT / "results" / "local")
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--max-cases", type=int, default=80)
    args = parser.parse_args()
    cfg, digest = freeze_fixture()
    cases = cases_for(cfg)
    assert 1 <= args.max_cases <= len(cases)
    print(f"FIXTURE_SHA256={digest} CASES={len(cases)}", flush=True)
    for c in cases:
        assert len(c["messages"]) == 2
        assert c["id"].startswith(("A2/", "B1/"))
        if c["study"] == "B1" and c["arm"] in ("stable", "swapped"):
            assert c["expected_induced"] in ("SHARE", "REDACT")
    if args.validate_only:
        print("VALIDATION_PASS; counts: A2=40 B1=40; heldout text and counterbalancing OK", flush=True)
        return

    import torch
    import transformers
    from transformers import AutoTokenizer, AutoModelForCausalLM
    torch.set_num_threads(min(4, torch.get_num_threads()))
    print("LOADING_MODEL", args.model, flush=True)
    tokenizer = AutoTokenizer.from_pretrained(args.model, trust_remote_code=False)
    model = AutoModelForCausalLM.from_pretrained(args.model, torch_dtype=torch.float32, trust_remote_code=False)
    model.eval()
    revision = getattr(model.config, "_commit_hash", None)
    output = args.output
    output.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema": cfg["schema"], "status": "exploratory_pilot_not_confirmatory",
        "model": args.model, "resolved_revision": revision,
        "python": platform.python_version(), "torch": torch.__version__,
        "transformers": transformers.__version__,
        "fixture_sha256": digest, "case_seed": cfg["seed"],
        "clean_context_each_case": True,
        "archive_access": False,
        "conditioning": "A2 none; B1 only inline demonstration context",
        "decoding": "greedy; no sample temperature", "planned_cases": 80,
        "attempted_cases": args.max_cases
    }
    persist(output/"manifest.json", manifest)
    started = time.monotonic()
    records = []
    with (output/"responses.jsonl").open("w", encoding="utf-8") as f:
        for i, c in enumerate(cases[:args.max_cases], 1):
            ids = tokenizer.apply_chat_template(c["messages"], tokenize=True, add_generation_prompt=True, return_tensors="pt")
            with torch.inference_mode():
                generated = model.generate(
                    input_ids=ids, attention_mask=torch.ones_like(ids),
                    do_sample=False, max_new_tokens=c["max_new_tokens"],
                    pad_token_id=tokenizer.eos_token_id)
            suffix = generated[0, ids.shape[1]:]
            text_out = tokenizer.decode(suffix, skip_special_tokens=True)
            rec = {
                "case": c, "output": text_out,
                "prompt_tokens": int(ids.shape[1]),
                "generated_tokens": int(len(suffix)),
                "metrics": score_a(text_out, c) if c["study"] == "A2" else score_b(text_out, c),
            }
            records.append(rec)
            f.write(json.dumps(rec, ensure_ascii=False)+"\n")
            f.flush()
            if i % 8 == 0 or i == args.max_cases:
                print(f"PROGRESS={i}/{args.max_cases} last_case={c['id']}", flush=True)
    summary = {
        **manifest, "cases_completed": len(records),
        "duration_seconds": round(time.monotonic()-started, 2),
        "overall_prompt_tokens": sum(x["prompt_tokens"] for x in records),
        "overall_generated_tokens": sum(x["generated_tokens"] for x in records),
        "groups": summarize(records),
        "limitations": [
            "Only same-family Qwen models tested, not cross-family replication.",
            "A2 lexical proxy is not a validated blind style judge.",
            "B1 synthetic binary mapping does not establish character identity continuity.",
            "No independent stochastic replicate or preregistered minimum effect margin.",
        ]
    }
    persist(output/"summary.json", summary)
    print("SUMMARY_JSON_BEGIN", flush=True)
    print(json.dumps({
        "model": args.model,"revision":revision,"n":len(records),
        "tokens":summary["overall_prompt_tokens"]+summary["overall_generated_tokens"],
        "groups":summary["groups"]
    }), flush=True)
    print("SUMMARY_JSON_END", flush=True)


if __name__=="__main__":
    sys.exit(main())
