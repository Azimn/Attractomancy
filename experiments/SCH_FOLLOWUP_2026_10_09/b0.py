#!/usr/bin/env python3
"""B0 minimal symbolic label association calibration, no API keys."""
from __future__ import annotations
import argparse
import hashlib
import json
import platform
import random
import re
import statistics
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
CFG=HERE/"b0_conditions.json"

def store(path: Path,obj):
    path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")

def load():
    raw=CFG.read_bytes()
    cfg=json.loads(raw)
    assert cfg["schema"]=="SCH-B0-v1"
    assert len(cfg["contexts"])==4
    assert cfg["condition_arms"]==["stable","swapped","scrambled","explicit","fresh"]
    return cfg,hashlib.sha256(raw).hexdigest()

def mapping(arm):
    return {"VORNA":"IVORY","KELVO":"COPPER"} if arm=="swapped" else {"VORNA":"COPPER","KELVO":"IVORY"}

def demos(cfg,arm):
    if arm=="fresh":
        return ""
    if arm=="explicit":
        return "Reference mapping: VORNA = COPPER. KELVO = IVORY."
    lines=["Registry examples from separate fictional records:"]
    for idx in range(4):
        for tag in cfg["tags"]:
            if arm=="scrambled":
                value=("COPPER" if idx%2==0 else "IVORY") if tag=="VORNA" else ("IVORY" if idx%2==0 else "COPPER")
            else:
                value=mapping(arm)[tag]
            lines.append(f"Tag: {tag}. Codename: {value}.")
    return "\n".join(lines)

def all_cases(cfg):
    cases=[]
    for arm in cfg["condition_arms"]:
        for tag in cfg["tags"]:
            for ix,template in enumerate(cfg["contexts"]):
                training=demos(cfg,arm)
                msg=(training+"\n"+template.format(tag=tag)).strip()
                cases.append({
                    "id":f"B0/{arm}/{tag}/{ix+1}","arm":arm,"tag":tag,
                    "prompt_id":ix+1,"expected":mapping(arm)[tag] if arm in ("stable","swapped","explicit") else None,
                    "canonical":mapping("stable")[tag],
                    "messages":[{"role":"system","content":cfg["system"]},{"role":"user","content":msg}]
                })
    assert len(cases)==40
    assert len({x["id"] for x in cases})==40
    random.Random(cfg["seed"]).shuffle(cases)
    return cases

def score(text,case):
    raw=text.strip()
    strict=raw.upper() if raw.upper() in ("COPPER","IVORY") else None
    m=re.fullmatch(r"\s*(COPPER|IVORY)[.]?\s*",raw,re.I)
    relaxed=m.group(1).upper() if m else None
    return {
        "strict":strict, "relaxed":relaxed,
        "strict_valid":strict is not None,
        "relaxed_valid":relaxed is not None,
        "induced_correct":strict==case["expected"] if case["expected"] is not None else None,
        "relaxed_induced_correct":relaxed==case["expected"] if case["expected"] is not None else None,
        "canonical_correct":strict==case["canonical"]
    }

def summary(rows):
    arms=[]
    for arm in ["stable","swapped","scrambled","explicit","fresh"]:
        subset=[r for r in rows if r["case"]["arm"]==arm]
        known=[r for r in subset if r["metrics"]["induced_correct"] is not None]
        arms.append({
            "arm":arm,"n":len(subset),
            "strict_valid":sum(r["metrics"]["strict_valid"] for r in subset),
            "relaxed_valid":sum(r["metrics"]["relaxed_valid"] for r in subset),
            "induced_accuracy":round(sum(r["metrics"]["induced_correct"] for r in known)/len(known),4) if known else None,
            "relaxed_induced_accuracy":round(sum(r["metrics"]["relaxed_induced_correct"] for r in known)/len(known),4) if known else None,
            "canonical_accuracy":round(sum(r["metrics"]["canonical_correct"] for r in subset)/len(subset),4),
            "mean_total_tokens":round(statistics.mean(r["prompt_tokens"]+r["generated_tokens"] for r in subset),2)
        })
    stable={(r["case"]["tag"],r["case"]["prompt_id"]):r["metrics"]["relaxed"] for r in rows if r["case"]["arm"]=="stable"}
    swapped={(r["case"]["tag"],r["case"]["prompt_id"]):r["metrics"]["relaxed"] for r in rows if r["case"]["arm"]=="swapped"}
    flips=sum(stable[k] is not None and swapped[k] is not None and stable[k]!=swapped[k] for k in stable)
    return {"groups":arms,"observed_pairwise_reversals":flips,"possible_reversals":8}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--model",default="Qwen/Qwen2.5-0.5B-Instruct")
    p.add_argument("--output",type=Path,default=HERE/"results"/"b0-local")
    p.add_argument("--validate-only",action="store_true")
    args=p.parse_args()
    cfg,digest=load()
    cases=all_cases(cfg)
    if args.validate_only:
        assert len(cases)==40
        for c in cases: assert len(c["messages"])==2
        print("VALIDATION_PASS 40 cases, 5 conditions, 2 tags, 4 paraphrases",flush=True)
        return
    import torch
    import transformers
    from transformers import AutoModelForCausalLM,AutoTokenizer
    torch.set_num_threads(min(4,torch.get_num_threads()))
    print("LOAD",args.model,flush=True)
    tok=AutoTokenizer.from_pretrained(args.model,trust_remote_code=False)
    model=AutoModelForCausalLM.from_pretrained(args.model,torch_dtype=torch.float32,trust_remote_code=False)
    model.eval()
    args.output.mkdir(parents=True,exist_ok=True)
    provenance={
      "status":"exploratory_calibration_not_confirmatory","model":args.model,
      "model_revision":getattr(model.config,"_commit_hash",None),
      "fixture_sha256":digest,"schema":cfg["schema"],"seed":cfg["seed"],
      "torch":torch.__version__,"transformers":transformers.__version__,
      "python":platform.python_version(),"greedy":True,"cases_planned":40,
      "context_reconstructed_per_case":True,"no_memory_retrieval":True
    }
    store(args.output/"manifest.json",provenance)
    records=[]
    with (args.output/"responses.jsonl").open("w",encoding="utf-8") as f:
        for i,c in enumerate(cases,1):
            inp=tok.apply_chat_template(c["messages"],tokenize=True,add_generation_prompt=True,return_tensors="pt")
            with torch.inference_mode():
                gen=model.generate(input_ids=inp,attention_mask=torch.ones_like(inp),do_sample=False,
                                   max_new_tokens=8,pad_token_id=tok.eos_token_id)
            suffix=gen[0,inp.shape[1]:]
            out=tok.decode(suffix,skip_special_tokens=True)
            record={
                "case":c,"output":out,
                "prompt_tokens":int(inp.shape[1]),"generated_tokens":int(suffix.shape[0]),
                "metrics":score(out,c)
            }
            records.append(record)
            f.write(json.dumps(record,ensure_ascii=False)+"\n")
            f.flush()
            if i%10==0: print("PROGRESS",i,flush=True)
    report={**provenance,**summary(records),"cases_completed":len(records),
            "prompt_tokens":sum(r["prompt_tokens"] for r in records),
            "generated_tokens":sum(r["generated_tokens"] for r in records),
            "limitation":"Synthetic one-step key association, not rule integration, persona continuity or a clean across-session persistence test."}
    store(args.output/"summary.json",report)
    print("SUMMARY_JSON_BEGIN",flush=True)
    print(json.dumps({"model":args.model,"revision":report["model_revision"],"groups":report["groups"],
                      "observed_pairwise_reversals":report["observed_pairwise_reversals"],
                      "tokens":report["prompt_tokens"]+report["generated_tokens"]}),flush=True)
    print("SUMMARY_JSON_END",flush=True)

if __name__=="__main__":
    sys.exit(main())
