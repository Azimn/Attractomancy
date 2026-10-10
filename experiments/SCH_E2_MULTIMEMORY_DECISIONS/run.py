#!/usr/bin/env python3
"""E2 source-verified two-memory condition runner; CPU and no inference API."""
from __future__ import annotations
import argparse
import json
import platform
import sys
import time
from pathlib import Path

from build_cases import load_config,make_cases,metric
from source_adapter import load_l1

def save(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--validate-only",action="store_true")
    p.add_argument("--source",type=Path)
    p.add_argument("--model",default="Qwen/Qwen2.5-0.5B-Instruct")
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    cfg,cfg_sha=load_config()
    ids={eid for card in cfg["cards"] for eid in card["records"]}
    if args.validate_only and not args.source:
        assert len(ids)==12
        print("E2_FIXTURE_VALID six cards / twelve unique events / six arms / two orders",flush=True)
        return
    if args.source is None:
        p.error("--source required to verify the owner-provided L1")
    rows,source_meta=load_l1(args.source)
    if not ids.issubset(rows):
        raise AssertionError("Frozen E2 pair absent from source L1")
    cases=make_cases(cfg,rows)
    if args.validate_only:
        assert len(cases)==72
        assert sum(x["available_record_count"]==2 for x in cases)==24
        assert sum(x["upstream_identity_rejections"] for x in cases)==12
        for c in cases:
            assert (c["expected"]=="UNKNOWN")==(c["available_record_count"]!=2)
        print("E2_SOURCE_AND_CASE_VALID",len(rows),len(cases),"fixture",cfg_sha,flush=True)
        return
    if args.output is None:
        p.error("--output required to preserve raw generations")
    args.output.mkdir(parents=True,exist_ok=True)
    import torch
    import transformers
    from transformers import AutoTokenizer,AutoModelForCausalLM
    torch.set_num_threads(min(4,torch.get_num_threads()))
    print("MODEL_LOADING",args.model,flush=True)
    tokenizer=AutoTokenizer.from_pretrained(args.model,trust_remote_code=False)
    model=AutoModelForCausalLM.from_pretrained(args.model,torch_dtype=torch.float32,trust_remote_code=False)
    model.eval()
    meta={
        "status":"exploratory_author_interpreted_not_blind",
        "model":args.model,"model_revision":getattr(model.config,"_commit_hash",None),
        "source":source_meta,"fixture_sha256":cfg_sha,
        "python":platform.python_version(),"torch":torch.__version__,
        "transformers":transformers.__version__,
        "cases_planned":len(cases),"seed":cfg["seed"],
        "temperature":"greedy","max_new_tokens":12,
        "independent_clean_model_context_per_case":True,
        "source_L1_unchanged":True,
        "wrong_subject_content_not_supplied_to_model":True,
        "interpretation_labels_human_authored_unblinded":True,
    }
    save(args.output/"manifest.json",meta)
    started=time.monotonic()
    records=[]
    with (args.output/"responses.jsonl").open("w",encoding="utf-8") as stream:
        for index,case in enumerate(cases,1):
            x=tokenizer.apply_chat_template(case["messages"],tokenize=True,
                       add_generation_prompt=True,return_tensors="pt")
            with torch.inference_mode():
                y=model.generate(input_ids=x,attention_mask=torch.ones_like(x),
                     do_sample=False,max_new_tokens=12,pad_token_id=tokenizer.eos_token_id)
            suffix=y[0,x.shape[1]:]
            output=tokenizer.decode(suffix,skip_special_tokens=True)
            item={
                "case":case,"output":output,"metric":metric(output,case),
                "input_tokens":int(x.shape[1]),"output_tokens":int(len(suffix)),
            }
            stream.write(json.dumps(item,ensure_ascii=False,sort_keys=True)+"\n")
            stream.flush()
            records.append(item)
            if index%12==0:
                print(f"E2_COMPLETED_CASES {index}/{len(cases)}",flush=True)
    save(args.output/"run.json",{
        **meta,"cases_completed":len(records),
        "elapsed_seconds":round(time.monotonic()-started,2),
        "actual_input_tokens":sum(x["input_tokens"] for x in records),
        "actual_output_tokens":sum(x["output_tokens"] for x in records)
    })
    print("GENERATIONS_FINISHED",len(records),flush=True)

if __name__=="__main__":
    main()
