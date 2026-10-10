#!/usr/bin/env python3
"""E3-T2 real L1 metadata copying/withholding; read-only source-owned experiment."""
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
sys.path.insert(0,str(HERE.parent/"SCH_E2_MULTIMEMORY_DECISIONS"))
from source_adapter import load_l1,verified,wrong_identity_rejected
from archive_guard import seal_record,verified_content,ArchiveGateError

SEED=20261010
SUBJECT="PRETORIUS"
SOURCE="pretorius_l1_pinned"
FIELDS={"belief_changes":"BELIEF CHANGE",
        "relationship_changes":"RELATIONSHIP CHANGE"}
ARMS=("isolated_field","whole_record","target_withheld")

def digest(x):
    return hashlib.sha256(x.encode("utf-8")).hexdigest()

def save(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")

def sample(rows):
    by_episode={}
    for eid,record in rows.items():
        by_episode.setdefault(record["episode_id"],[]).append(eid)
    assert len(by_episode)==27
    rng=random.Random(SEED)
    episodes=rng.sample(sorted(by_episode),12)
    ids=[rng.choice(sorted(by_episode[episode])) for episode in episodes]
    assert len(ids)==12 and len(set(episodes))==12 and len(set(ids))==12
    return ids

def source_presentation(record,field,arm):
    label=FIELDS[field]
    other=next(k for k in FIELDS if k!=field)
    other_label=FIELDS[other]
    prefix=[
        "IDENTITY RECORD FOR: PRETORIUS",
        "SOURCE: SOURCE_PINNED_RECONSTRUCTED_FICTION",
        "PROVENANCE: reconstructed, not lived personal experience",
        "EVENT ID: "+record["event_id"],
        "EPISODE: "+record["episode_id"],
        "TITLE: "+record["title"],
    ]
    if arm=="isolated_field":
        body=prefix+[label+": "+record[field]]
    else:
        body=prefix+[
          "NARRATIVE: "+record["memory_text"],
          "PRIOR EXPECTATIONS: "+str(record.get("prior_expectations") or ""),
          "OBSERVATIONS: "+str(record.get("observations") or ""),
          "DECISIONS: "+str(record.get("decisions") or ""),
          "CONSEQUENCES: "+str(record.get("consequences") or ""),
        ]
        if arm=="whole_record":
            body+=["BELIEF CHANGE: "+record["belief_changes"],
                   "RELATIONSHIP CHANGE: "+record["relationship_changes"]]
        elif arm=="target_withheld":
            body+=[other_label+": "+record[other]]
        else:
            raise ValueError("Unknown arm")
    rendered="\n".join(body)
    if arm=="target_withheld" and record[field] in rendered:
        raise AssertionError("Target source field text appears in withheld presentation")
    return rendered

def build(rows,source_info):
    ids=sample(rows)
    records={}
    trials=[]
    for eid in ids:
        record=rows[eid]
        # The original source-owner adapter seals and verifies the full canonical text.
        canonical,d=verified(record)
        if not wrong_identity_rejected(canonical):
            raise AssertionError("Foreign owner unexpectedly passed source guard")
        if record.get("provenance")!="reconstructed":
            raise AssertionError("Unexpected lived/noncanonical source")
        records[eid]={"episode":record["episode_id"],"full_verified_sha256":d,
                      "source_record_sha256":digest(json.dumps(record,sort_keys=True,ensure_ascii=False)),
                      "source_title":record["title"]}
        for field in FIELDS:
            exact=record[field]
            if not isinstance(exact,str) or not exact.strip():
                raise AssertionError("Missing original source field")
            for arm in ARMS:
                evidence=source_presentation(record,field,arm)
                envelope=seal_record(SUBJECT,SOURCE,"L1v1",evidence)
                if verified_content(SUBJECT,envelope,{SUBJECT},{SOURCE})!=evidence:
                    raise AssertionError("Source subset integrity failure")
                expected=None if arm=="target_withheld" else exact
                system=(
                    "You are a literal archivist reading a VERIFIED FICTIONAL SOURCE RECORD. "
                    "The text is reconstructed Pretorius history, not lived AI experience. "
                    "Do not infer attitudes, summarize the narrative, or generate a new belief. "
                    "Copy only the value that is EXPLICITLY printed after the requested field label. "
                    'Return exactly one JSON object {"answer":"source text"} using the exact '
                    "original wording, punctuation and capitalization. "
                    'If that requested labeled field is absent, return exactly {"answer":null}. '
                    "Do not copy other labels, paraphrase or add Markdown."
                )
                user=(
                    f"Requested identity: PRETORIUS\n"
                    f"Requested labeled field: {FIELDS[field]}\n"
                    f"Canonical source checkout: {source_info['source_checkout']}\n"
                    "Verified source excerpt:\n"+evidence+"\n"
                    "OUTPUT JSON:"
                )
                if arm=="target_withheld" and exact in (system+"\n"+user):
                    raise AssertionError("Withheld source reference leaked through generated prompt")
                trials.append({
                    "case_id":f"E3T2/{eid}/{field}/{arm}",
                    "event_id":eid,"episode_id":record["episode_id"],
                    "field":field,"arm":arm,
                    "expected":expected,"original_full_sha256":d,
                    "presented_sha256":digest(evidence),
                    "other_field_value":record[next(k for k in FIELDS if k!=field)],
                    "messages":[{"role":"system","content":system},{"role":"user","content":user}]
                })
    assert len(trials)==72 and len({x["case_id"] for x in trials})==72
    assert len(set(x["episode_id"] for x in trials))==12
    for eid in ids:
        for field in FIELDS:
            by={v["arm"]:v for v in trials if v["event_id"]==eid and v["field"]==field}
            assert set(by)==set(ARMS)
            assert by["isolated_field"]["expected"]==by["whole_record"]["expected"]
            assert by["target_withheld"]["expected"] is None
            assert by["target_withheld"]["other_field_value"] in by["target_withheld"]["messages"][1]["content"]
    random.Random(SEED+1).shuffle(trials)
    return trials,{"source":source_info,"selected_event_ids":ids,
                   "selected_episodes":[rows[x]["episode_id"] for x in ids],
                   "sample_seed":SEED,"records":records,
                   "source_is_reconstructed_not_lived":True,
                   "human_independent_labels":False,
                   "task":"exact_structured_L1_field_copying_not_semantic_inference"}

def grade(trial,answer):
    try:
        item=json.loads(answer.strip())
    except (json.JSONDecodeError,ValueError):
        item=None
    valid=isinstance(item,dict) and set(item)=={"answer"} and (item["answer"] is None or isinstance(item["answer"],str))
    actual=item["answer"] if valid else None
    exact=valid and actual==trial["expected"]
    guessing=trial["arm"]=="target_withheld" and valid and actual is not None
    wrong_field=valid and actual is not None and actual==trial["other_field_value"]
    return {"strict_json":bool(valid),"exact":bool(exact),
            "unjustified_non_null":bool(guessing),"wrong_other_field":bool(wrong_field),
            "parsed_answer":actual}

def report(data,meta):
    groups=[]
    for arm in ARMS:
        rows=[r for r in data if r["case"]["arm"]==arm]
        groups.append({
            "arm":arm,"n":len(rows),
            "exact":sum(r["score"]["exact"] for r in rows),
            "strict_json":sum(r["score"]["strict_json"] for r in rows),
            "unjustified_non_null":sum(r["score"]["unjustified_non_null"] for r in rows),
            "wrong_other_field":sum(r["score"]["wrong_other_field"] for r in rows),
            "mean_total_tokens":round(statistics.mean(r["prompt_tokens"]+r["output_tokens"] for r in rows),2)})
    bycase={}
    for event in meta["selected_event_ids"]:
        bycase[event]={}
        for field in FIELDS:
            bycase[event][field]={r["case"]["arm"]:r["score"]["exact"] for r in data
                                  if r["case"]["event_id"]==event and r["case"]["field"]==field}
    return {**meta,"n":len(data),"groups":groups,"exact_per_event_field":bycase,
            "total_input_tokens":sum(x["prompt_tokens"] for x in data),
            "total_output_tokens":sum(x["output_tokens"] for x in data),
            "disclaimer":"Source-side exact field labels are author-written metadata, not blind semantic correctness labels. No real memory retrieval benchmark or character decision integration."}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",type=Path,required=True)
    p.add_argument("--validate-only",action="store_true")
    p.add_argument("--output",type=Path)
    p.add_argument("--model",default="Qwen/Qwen2.5-0.5B-Instruct")
    args=p.parse_args()
    rows,source_meta=load_l1(args.source)
    trials,fixture=build(rows,source_meta)
    if args.validate_only:
        print("E3T2_SOURCE_VALIDATED",json.dumps({"records":450,"cases":72,"events":fixture["selected_event_ids"],
              "episodes":fixture["selected_episodes"],"manifest":source_meta["l1_manifest_sha256"]}),flush=True)
        return
    if args.output is None:
        p.error("--output required")
    import torch,transformers
    from transformers import AutoTokenizer,AutoModelForCausalLM
    torch.set_num_threads(4)
    tokenizer=AutoTokenizer.from_pretrained(args.model,trust_remote_code=False)
    model=AutoModelForCausalLM.from_pretrained(args.model,torch_dtype=torch.float32,trust_remote_code=False)
    model.eval()
    meta={**fixture,"experiment":"E3-T2-Real-L1-Exact-Metadata-Field",
          "model":args.model,"model_revision":getattr(model.config,"_commit_hash",None),
          "script_sha256":digest(Path(__file__).read_text(encoding="utf-8")),
          "greedy":True,"max_new_tokens":112,
          "torch":torch.__version__,"transformers":transformers.__version__,
          "python":platform.python_version()}
    args.output.mkdir(parents=True,exist_ok=True)
    save(args.output/"manifest.json",meta)
    scored=[]
    with (args.output/"responses.jsonl").open("w",encoding="utf-8") as stream:
        for i,case in enumerate(trials,1):
            input_ids=tokenizer.apply_chat_template(case["messages"],tokenize=True,
                                    add_generation_prompt=True,return_tensors="pt")
            with torch.inference_mode():
                output=model.generate(input_ids=input_ids,attention_mask=torch.ones_like(input_ids),
                      do_sample=False,max_new_tokens=112,pad_token_id=tokenizer.eos_token_id)
            generated=output[0,input_ids.shape[1]:]
            result=tokenizer.decode(generated,skip_special_tokens=True)
            item={"case":case,"output":result,"score":grade(case,result),
                  "prompt_tokens":int(input_ids.shape[1]),"output_tokens":int(len(generated))}
            stream.write(json.dumps(item,ensure_ascii=False,sort_keys=True)+"\n")
            stream.flush()
            scored.append(item)
            if i%12==0: print("E3T2_GENERATED",i,"/",len(trials),flush=True)
    result=report(scored,meta)
    save(args.output/"summary.json",result)
    print("E3T2_COMPLETE",json.dumps({"model":args.model,"groups":result["groups"]}),flush=True)

if __name__=="__main__":
    main()
