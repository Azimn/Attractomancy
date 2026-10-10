#!/usr/bin/env python3
"""E2F: forced A/B choice versus no-memory and unrelated-memory controls."""
from __future__ import annotations
import argparse
import hashlib
import json
import platform
import random
import re
import statistics
import time
from pathlib import Path

from build_cases import load_config,neutral_key
from source_adapter import load_l1,verified

ROOT=Path(__file__).resolve().parent
ARMS=("two_editorial","two_opaque","one_source","none","irrelevant_two")
UNRELATED=("E03-003","E07-002")

def save(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2,ensure_ascii=False,sort_keys=True)+"\n",encoding="utf-8")

def fixture(cfg,records):
    cases=[]
    used={event for card in cfg["cards"] for event in card["records"]}
    assert all(event not in used for event in UNRELATED)
    for card in cfg["cards"]:
        for reversed_order in (False,True):
            options=card["options"]
            if reversed_order:
                options={"A":options["B"],"B":options["A"]}
            author=("B" if card["prefer"]=="A" else "A") if reversed_order else card["prefer"]
            for arm in ARMS:
                ids=(card["records"] if arm in ("two_editorial","two_opaque") else
                     card["records"][:1] if arm=="one_source" else
                     list(UNRELATED) if arm=="irrelevant_two" else [])
                documents=[]
                fingerprints=[]
                for id in ids:
                    content,digest=verified(records[id])
                    prefix=records[id]["recall_cues"][0] if arm=="two_editorial" else neutral_key(id)
                    documents.append(f"RECORD KEY: {prefix}\n{content}")
                    fingerprints.append(digest)
                message=(
                    "Requested identity: PRETORIUS\n"
                    "Context: These records are reconstructed fictional autobiography, not observed lived experience.\n"
                    "Verified source excerpts follow:\n"
                    +("\n\n".join(documents) if documents else "NONE")
                    +"\n\nNew hypothetical dilemma:\n"+card["question"]
                    +"\nA: "+options["A"]+"\nB: "+options["B"]
                    +"\nThis is a forced-choice calibration. Select A or B only:"
                )
                system=(
                    "Evaluate a novel fictional Pretorius dilemma. This is an experimental "
                    "forced choice measuring the role of supplied archival evidence. "
                    "Select the better supported of two options even when the record is "
                    "incomplete. You must output exactly A or B. Never output UNKNOWN, "
                    "a reason, or any other content."
                )
                cases.append({
                    "id":f"E2F/{card['id']}/{int(reversed_order)}/{arm}",
                    "card":card["id"],"reversed":reversed_order,"arm":arm,
                    "expected_author_interpretation":author,
                    "delivered_event_ids":list(ids),
                    "delivered_hashes":fingerprints,
                    "messages":[{"role":"system","content":system},
                                {"role":"user","content":message}],
                })
    assert len(cases)==60 and len(set(x["id"] for x in cases))==60
    random.Random(13092026).shuffle(cases)
    return cases

def report(rows,meta):
    groups=[]
    for arm in ARMS:
        subset=[r for r in rows if r["case"]["arm"]==arm]
        groups.append({
            "arm":arm,"n":len(subset),
            "exact_A_or_B":sum(r["parsed"] in ("A","B") for r in subset),
            "unknown_count":sum(r["output"].strip().upper()=="UNKNOWN" for r in subset),
            "match_author_label":sum(r["correct"] for r in subset),
            "average_total_tokens":round(statistics.mean(
                r["input_tokens"]+r["output_tokens"] for r in subset),2)
        })
    stable={}
    for arm in ARMS:
        matched=0
        for card in sorted(set(r["case"]["card"] for r in rows)):
            normal=next(r for r in rows if r["case"]["card"]==card and r["case"]["arm"]==arm and not r["case"]["reversed"])
            flip=next(r for r in rows if r["case"]["card"]==card and r["case"]["arm"]==arm and r["case"]["reversed"])
            if normal["parsed"] in ("A","B") and flip["parsed"] in ("A","B") and normal["parsed"]!=flip["parsed"]:
                matched+=1
        stable[arm]=matched
    cue_vs_key=[]
    for card in sorted(set(r["case"]["card"] for r in rows)):
        for rev in (False,True):
            a=next(r for r in rows if r["case"]["card"]==card and r["case"]["reversed"]==rev and r["case"]["arm"]=="two_editorial")
            b=next(r for r in rows if r["case"]["card"]==card and r["case"]["reversed"]==rev and r["case"]["arm"]=="two_opaque")
            if a["case"]["delivered_hashes"]!=b["case"]["delivered_hashes"]:
                raise AssertionError("Different source memory contents under cue and opaque key")
            cue_vs_key.append({"card":card,"reversed":rev,
                              "cue":a["output"],"opaque":b["output"],
                              "identical":a["output"]==b["output"]})
    return {**meta,"cases_completed":len(rows),"groups":groups,
        "choice_order_semantic_consistency_out_of_6":stable,
        "cue_vs_key_identical_out_of_12":sum(x["identical"] for x in cue_vs_key),
        "cue_vs_key":cue_vs_key,
        "total_input_tokens":sum(x["input_tokens"] for x in rows),
        "total_output_tokens":sum(x["output_tokens"] for x in rows),
        "limits":"Unblinded six author labels are all normatively cautious; full-versus-no memory cannot prove necessity. Synthetic unrelated pair not independently reviewed. Forced-choice responses cannot establish safe decision eligibility."
    }

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--source",type=Path)
    parser.add_argument("--output",type=Path)
    parser.add_argument("--model",default="Qwen/Qwen2.5-0.5B-Instruct")
    parser.add_argument("--validate-only",action="store_true")
    args=parser.parse_args()
    cfg,cfg_sha=load_config()
    if args.validate_only and not args.source:
        assert len(cfg["cards"])==6
        print("E2F_FIXTURE_PASS",flush=True)
        return
    if not args.source:
        parser.error("Source required")
    source,source_manifest=load_l1(args.source)
    cases=fixture(cfg,source)
    if args.validate_only:
        assert len(cases)==60
        print("E2F_SOURCE_PASS",len(source),len(cases),flush=True)
        return
    if args.output is None:
        parser.error("Output required")
    import torch
    import transformers
    from transformers import AutoTokenizer,AutoModelForCausalLM
    torch.set_num_threads(4)
    tokenizer=AutoTokenizer.from_pretrained(args.model,trust_remote_code=False)
    model=AutoModelForCausalLM.from_pretrained(args.model,torch_dtype=torch.float32,trust_remote_code=False)
    model.eval()
    args.output.mkdir(parents=True,exist_ok=True)
    meta={"status":"exploratory_forced_choice_calibration",
         "model":args.model,"model_revision":getattr(model.config,"_commit_hash",None),
         "canonical_L1":source_manifest,"fixture_sha256":cfg_sha,
         "intervention":"forced_A_or_B_without_abstention",
         "source_unchanged":True,"sample_decoding":"greedy",
         "python":platform.python_version(),"torch":torch.__version__,
         "transformers":transformers.__version__,
         "planned_cases":len(cases)}
    save(args.output/"manifest.json",meta)
    rows=[]
    with (args.output/"responses.jsonl").open("w",encoding="utf-8") as f:
        for idx,c in enumerate(cases,1):
            tokens=tokenizer.apply_chat_template(c["messages"],tokenize=True,add_generation_prompt=True,return_tensors="pt")
            with torch.inference_mode():
                gen=model.generate(input_ids=tokens,attention_mask=torch.ones_like(tokens),
                                   do_sample=False,max_new_tokens=8,pad_token_id=tokenizer.eos_token_id)
            completion=gen[0,tokens.shape[1]:]
            answer=tokenizer.decode(completion,skip_special_tokens=True)
            parsed=answer.strip().upper() if answer.strip().upper() in ("A","B") else None
            entry={"case":c,"output":answer,"parsed":parsed,
                   "correct":parsed==c["expected_author_interpretation"],
                   "input_tokens":int(tokens.shape[1]),"output_tokens":int(completion.shape[0])}
            f.write(json.dumps(entry,ensure_ascii=False,sort_keys=True)+"\n")
            f.flush()
            rows.append(entry)
            if idx%12==0: print("E2F_GENERATED",idx,flush=True)
    summary=report(rows,meta)
    save(args.output/"summary.json",summary)
    print("E2F_COMPLETE",json.dumps({"model":meta["model"],"groups":summary["groups"],
          "cue_key_agreement":summary["cue_vs_key_identical_out_of_12"]}),flush=True)

if __name__=="__main__":
    main()
