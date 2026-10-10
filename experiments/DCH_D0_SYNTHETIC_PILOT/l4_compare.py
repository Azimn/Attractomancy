#!/usr/bin/env python3
"""Descriptive paired L3 model versus explicit-control-law comparison.
Do not treat a deterministic reference solver as a causal intervention trial.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path

def compare(gate_path, model_path, dest):
    if dest.exists():
        raise FileExistsError(dest)
    gate=json.loads(gate_path.read_text(encoding="utf-8"))
    model=json.loads(model_path.read_text(encoding="utf-8"))
    assert gate["DCH_efficacy_claim"]=="NONE"
    assert model["status"]=="REAL_LLM_DEVELOPMENT"
    g={(r["persona_id"],r["stage"],r["arm"]):r for r in gate["rows"]}
    m={}
    for row in model["records"]:
        k=(row["persona_id"],row["stage"],row["arm"])
        if k in m:raise ValueError("duplicate model result key")
        m[k]=row
    if not m or any(k not in g for k in m):raise ValueError("model and gate case misalignment")
    summaries={}
    paired=[]
    for k,row in sorted(m.items()):
        ref=g[k]
        strict=row["strict"]; first=row["first_object"]
        record={"persona_id":row["persona_id"],"stage":row["stage"],"arm":row["arm"],
                "target":ref["expected"],"gate_answer":ref["answer"],"gate_correct":ref["correct"],
                "strict_model_correct":bool(strict["parse_valid"] and strict["answer"]==ref["expected"]),
                "first_object_model_correct":bool(first and first["answer"]==ref["expected"]),
                "strict_format_valid":bool(strict["parse_valid"]),
                "first_object_format_valid":bool(first),
                "reference_minimal_source":ref["minimal_certificate_exact"]}
        if not record["gate_correct"]:
            raise AssertionError("reference-control answer failed independently pinned target")
        paired.append(record)
        label=row["stage"]+":"+row["arm"]
        summaries.setdefault(label,[]).append(record)
    scores={k:{"n":len(v),"gate_accuracy":sum(x["gate_correct"] for x in v)/len(v),
               "model_strict_accuracy":sum(x["strict_model_correct"] for x in v)/len(v),
               "model_first_object_accuracy":sum(x["first_object_model_correct"] for x in v)/len(v),
               "model_strict_format_rate":sum(x["strict_format_valid"] for x in v)/len(v)}
            for k,v in summaries.items()}
    result={"status":"ENGINEERING_REFERENCE_COMPARISON","DCH_efficacy_claim":"NONE",
            "experimental_explanation":"The external gate was programmed with the exact fixture law; its success is a reference-control check, not an unbiased model improvement or test of a human dyad.",
            "paired_n":len(paired),"summary":scores,"paired_rows":paired}
    dest.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    return {k:v for k,v in result.items() if k!="paired_rows"}

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--gate",required=True,type=Path)
    p.add_argument("--model",required=True,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args()
    print(json.dumps(compare(a.gate,a.model,a.out),indent=2))
