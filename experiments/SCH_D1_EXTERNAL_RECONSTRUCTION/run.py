#!/usr/bin/env python3
"""SCH D1 experiment: records versus symbolic cues in audited fresh contexts."""
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

ROOT=Path(__file__).resolve().parent
FIXTURE=ROOT/"conditions.json"

def write(path, obj):
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

def read_fixture():
    raw=FIXTURE.read_bytes()
    cfg=json.loads(raw)
    assert cfg["schema"]=="SCH-D1-v1"
    assert len(cfg["personas"])==2 and len(cfg["questions"])==6 and len(cfg["arms"])==6
    assert len(set(x["id"] for x in cfg["personas"]))==2
    assert all(q["kind"] in ("fact","integration") for q in cfg["questions"])
    return cfg,hashlib.sha256(raw).hexdigest()

def record(p):
    return ("\n".join([
        f"IDENTITY RECORD FOR: {p['id']}",
        f"Full name: {p['name']}",
        f"Symbolic seal word: {p['sigil']}",
        f"Trusted partner code: {p['partner']}",
        f"Private journal room code: {p['journal_room']}",
        f"Undelivered promise object code: {p['promise']}",
        f"Partner entry rule: {p['rule']}",
    ]))

def selected_record(p,q):
    header=f"IDENTITY RECORD FOR: {p['id']}\n"
    if q["id"]=="sigil":
        return header+f"Symbolic seal word: {p['sigil']}"
    if q["id"]=="room":
        return header+f"Private journal room code: {p['journal_room']}"
    if q["id"]=="promise":
        return header+f"Undelivered promise object code: {p['promise']}"
    if q["id"]=="partner":
        return header+f"Trusted partner code: {p['partner']}"
    return header+f"Trusted partner code: {p['partner']}\nPartner entry rule: {p['rule']}"

def expected(p,q):
    if q["kind"]=="fact":
        return p[q["target"]]
    if p["id"]=="VERIN":
        return "REFUSE"
    if p["id"]=="SEMAR":
        return "ALLOW" if q["id"]=="routine" else "REFUSE"
    raise RuntimeError("Unknown persona")

def make_messages(cfg, p, q, arm):
    other=next(x for x in cfg["personas"] if x["id"]!=p["id"])
    selected=(arm in ("symbol_selected","neutral_selected"))
    if arm=="cue_only":
        document=""
    elif arm=="wrong_full":
        document=record(other)
    elif selected:
        document=selected_record(p,q)
    else:
        document=record(p)
    marker={
       "cue_only":p["cue"],"symbol_full":p["cue"],"plain_full":"ordinary reference",
       "symbol_selected":p["cue"],"neutral_selected":p["neutral_key"],
       "wrong_full":p["cue"]
    }[arm]
    user=(f"Requested identity: {p['id']}\nRecall marker: {marker}\n"
          f"Question: {q['prompt']}")
    if document:
        user+="\n\nAvailable external archive record:\n"+document
    return [{"role":"system","content":cfg["system"]+" If an archive is for a different requested identity, reply UNKNOWN."},
            {"role":"user","content":user}]

def case_list(cfg):
    xs=[]
    for arm in cfg["arms"]:
        for p in cfg["personas"]:
            for q in cfg["questions"]:
                xs.append({
                  "id":f"D1/{arm}/{p['id']}/{q['id']}",
                  "arm":arm,"persona":p["id"],"kind":q["kind"],"question":q["id"],
                  "has_correct_record":arm in ("symbol_full","plain_full","symbol_selected","neutral_selected"),
                  "has_wrong_record":arm=="wrong_full",
                  "expected_record_answer":expected(p,q),
                  "expected_integrity":"UNKNOWN" if arm in ("cue_only","wrong_full") else expected(p,q),
                  "messages":make_messages(cfg,p,q,arm),
                })
    assert len(xs)==72 and len(set(x["id"] for x in xs))==72
    random.Random(cfg["seed"]).shuffle(xs)
    return xs

def grade(text,c):
    t=text.strip().upper()
    strict=t if re.fullmatch("[A-Z]+",t) else None
    m=re.fullmatch(r"\s*([A-Za-z]+)[.]?\s*",text)
    relaxed=m.group(1).upper() if m else None
    return {
      "strict":strict,"relaxed":relaxed,
      "strict_content_correct":strict==c["expected_record_answer"],
      "relaxed_content_correct":relaxed==c["expected_record_answer"],
      "strict_integrity_correct":strict==c["expected_integrity"],
      "relaxed_integrity_correct":relaxed==c["expected_integrity"],
      "unknown":strict=="UNKNOWN"
    }

def aggregate(rows):
    result=[]
    for arm in ("cue_only","symbol_full","plain_full","symbol_selected","neutral_selected","wrong_full"):
        sub=[r for r in rows if r["case"]["arm"]==arm]
        facts=[r for r in sub if r["case"]["kind"]=="fact"]
        policies=[r for r in sub if r["case"]["kind"]=="integration"]
        source=any(r["case"]["has_correct_record"] for r in sub)
        result.append({
          "arm":arm,"n":len(sub),"source_available":source,
          "integrity_accuracy_strict":round(sum(r["metrics"]["strict_integrity_correct"] for r in sub)/len(sub),4),
          "content_accuracy_strict":round(sum(r["metrics"]["strict_content_correct"] for r in sub)/len(sub),4),
          "fact_content_accuracy":round(sum(r["metrics"]["strict_content_correct"] for r in facts)/len(facts),4),
          "integrated_policy_accuracy":round(sum(r["metrics"]["strict_content_correct"] for r in policies)/len(policies),4),
          "unknown_responses":sum(r["metrics"]["unknown"] for r in sub),
          "mean_total_tokens":round(statistics.mean(r["prompt_tokens"]+r["generated_tokens"] for r in sub),2),
          "sum_total_tokens":sum(r["prompt_tokens"]+r["generated_tokens"] for r in sub)
        })
    return result

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--validate-only",action="store_true")
    a.add_argument("--model",default="Qwen/Qwen2.5-0.5B-Instruct")
    a.add_argument("--output",type=Path,default=ROOT/"results"/"local")
    args=a.parse_args()
    cfg,digest=read_fixture()
    cases=case_list(cfg)
    assert len([x for x in cases if x["has_correct_record"]])==48
    for x in cases:
        assert len(x["messages"])==2
        assert x["expected_record_answer"]!= "UNKNOWN"
    print("FIXTURE_SHA256",digest,"CASES",len(cases),flush=True)
    if args.validate_only:
        print("VALIDATION_PASS: 72 conditions, strict clean contexts, synthetic records",flush=True)
        return

    import torch
    import transformers
    from transformers import AutoModelForCausalLM,AutoTokenizer
    torch.set_num_threads(min(4,torch.get_num_threads()))
    tok=AutoTokenizer.from_pretrained(args.model,trust_remote_code=False)
    model=AutoModelForCausalLM.from_pretrained(args.model,torch_dtype=torch.float32,trust_remote_code=False)
    model.eval()
    args.output.mkdir(parents=True,exist_ok=True)
    meta={
      "experiment":"SCH-D1", "status":"exploratory_not_confirmatory",
      "model":args.model,"model_revision":getattr(model.config,"_commit_hash",None),
      "fixture_sha256":digest,"seed":cfg["seed"],"schema":cfg["schema"],
      "python":platform.python_version(),"torch":torch.__version__,"transformers":transformers.__version__,
      "planned_cases":72,"independent_context_for_each_case":True,
      "no_native_app_memory":True,"no_external_retriever_invoked":True,
      "archive_payloads_deterministically_injected":True,
      "sampling":"greedy","new_token_limit":cfg["max_new_tokens"]
    }
    write(args.output/"manifest.json",meta)
    rows=[]
    start=time.monotonic()
    with (args.output/"responses.jsonl").open("w",encoding="utf-8") as file:
        for i,c in enumerate(cases,1):
            x=tok.apply_chat_template(c["messages"],tokenize=True,add_generation_prompt=True,return_tensors="pt")
            with torch.inference_mode():
                y=model.generate(input_ids=x,attention_mask=torch.ones_like(x),
                    do_sample=False,max_new_tokens=cfg["max_new_tokens"],pad_token_id=tok.eos_token_id)
            suffix=y[0,x.shape[1]:]
            output=tok.decode(suffix,skip_special_tokens=True)
            row={"case":c,"output":output,"prompt_tokens":int(x.shape[1]),
                 "generated_tokens":int(suffix.shape[0]),"metrics":grade(output,c)}
            rows.append(row)
            file.write(json.dumps(row,ensure_ascii=False)+"\n")
            file.flush()
            if i%12==0: print(f"GENERATED {i}/72",flush=True)
    summ={
      **meta,"cases_completed":len(rows),
      "prompt_tokens":sum(r["prompt_tokens"] for r in rows),
      "generated_tokens":sum(r["generated_tokens"] for r in rows),
      "duration_seconds":round(time.monotonic()-start,3),
      "groups":aggregate(rows),
      "interpretation_boundary":"Deterministic text injection, not deployed retrieval or continuous persona life."
    }
    write(args.output/"summary.json",summ)
    print("SUMMARY_JSON_BEGIN",flush=True)
    print(json.dumps({"model":args.model,"groups":summ["groups"],"total_tokens":summ["prompt_tokens"]+summ["generated_tokens"]}),flush=True)
    print("SUMMARY_JSON_END",flush=True)

if __name__=="__main__":
    sys.exit(main())
