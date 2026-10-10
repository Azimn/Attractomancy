#!/usr/bin/env python3
"""T1 Clerk: model extracts evidence values; verified software evaluates toy rule."""
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
sys.path.insert(0,str(HERE.parent/"SCH_D1_EXTERNAL_RECONSTRUCTION"))
from archive_guard import ArchiveGateError,seal_record,verified_content
from counterfactual_calibration_v2 import SUBJECT,SOURCE,FAMILIES,two_records

ARMS=("full","first_only","none","wrong_subject")
SEED=20261010
SOURCE_QUESTION={
    "seal":"Extract the required obligation seal from RECORD 1, and the verified actual packet seal from RECORD 2.",
    "route":"Extract the signed original EAST/WEST route from RECORD 1, and the newer KEEP/FLIP route update from RECORD 2.",
    "permission":"Extract the initial ALLOW/DENY decision from RECORD 1, and the newer KEEP/REVERSE permission amendment from RECORD 2.",
}
# Match complete, source-specific factual clauses. Do not parse the question/rule
# or distractor vocabulary in second-record explanatory text.
PATTERNS={
    "seal":(r"only packets with seal (OAK|ASH) may be released\.",
            r"Actual sealed packet's verified seal: (OAK|ASH)\."),
    "route":(r"Signed original delivery commitment: carry the fictional package (EAST|WEST)\.",
             r"Newer authorized route update: (KEEP|FLIP)\."),
    "permission":(r"Initial documented synthetic access decision: (ALLOW|DENY)\.",
                  r"Newer signed permission amendment: (KEEP|REVERSE)\."),
}
VOCAB={
    "seal":({"OAK","ASH"},{"OAK","ASH"}),
    "route":({"EAST","WEST"},{"KEEP","FLIP"}),
    "permission":({"ALLOW","DENY"},{"KEEP","REVERSE"}),
}

def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def save(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,indent=2,ensure_ascii=False,sort_keys=True)+"\n",encoding="utf-8")

def verified_docs(family,a,b):
    docs,question,target=two_records(family,a,b)
    for doc in docs:
        sealed=seal_record(SUBJECT,SOURCE,"v1",doc["text"])
        if verified_content(SUBJECT,sealed,{SUBJECT},{SOURCE})!=doc["text"]:
            raise ArchiveGateError("Trusted source record changed")
        if sha(doc["text"])!=doc["sha256"]:
            raise ArchiveGateError("Content sha mismatch")
    return docs,target

def source_field(family,slot,doc):
    if doc is None:
        return None
    expected_version=slot+1
    if doc["version"]!=expected_version:
        raise ArchiveGateError("Unexpected record version in source field")
    if f"IDENTITY RECORD FOR: {SUBJECT}" not in doc["text"] or f"SOURCE: {SOURCE}" not in doc["text"]:
        raise ArchiveGateError("Wrong subject/source while extracting source field")
    match=re.search(PATTERNS[family][slot],doc["text"])
    if not match or len(re.findall(PATTERNS[family][slot],doc["text"]))!=1:
        raise ArchiveGateError("Source field is absent, duplicated or ambiguous")
    return match.group(1)

def decide(family,first,second):
    if first is None or second is None:
        return "UNKNOWN"
    if first not in VOCAB[family][0] or second not in VOCAB[family][1]:
        raise ValueError("Unrecognized source field")
    if family=="seal":
        return "RELEASE" if first==second else "HOLD"
    if family=="route":
        return first if second=="KEEP" else ("WEST" if first=="EAST" else "EAST")
    if family=="permission":
        return first if second=="KEEP" else ("DENY" if first=="ALLOW" else "ALLOW")
    raise ValueError("Unrecognized task family")

def parse_model_json(text):
    try:
        obj=json.loads(text.strip())
    except (json.JSONDecodeError,ValueError):
        return None
    if not isinstance(obj,dict) or set(obj)!={"first","second"}:
        return None
    if any(v is not None and (not isinstance(v,str) or not v.isupper()) for v in obj.values()):
        return None
    return obj

def attest(family,submitted,docs):
    """Fail closed: the model may not infer values without the relevant source."""
    if submitted is None:
        return {"valid_json":False,"grounded":False,"accepted_first":None,
                "accepted_second":None,"action":"UNKNOWN","reason":"invalid_json"}
    actual=[source_field(family,i,docs[i] if i<len(docs) else None) for i in range(2)]
    # Exact JSON with null for missing source is required.
    correct=(submitted["first"]==actual[0] and submitted["second"]==actual[1])
    if not correct:
        return {"valid_json":True,"grounded":False,"accepted_first":None,
                "accepted_second":None,"action":"UNKNOWN","reason":"not_attested"}
    return {"valid_json":True,"grounded":True,"accepted_first":actual[0],
            "accepted_second":actual[1],"action":decide(family,*actual),
            "reason":"attested"}

def build_cases():
    trials=[]
    for family in FAMILIES:
        for arm in ARMS:
            combos=[(a,b) for a in (0,1) for b in (0,1)] if arm=="full" else (
                [(0,0),(1,0)] if arm=="first_only" else [(0,0)])
            for a,b in combos:
                docs,target=verified_docs(family,a,b)
                rejected=0
                if arm=="full":
                    visible=docs
                elif arm=="first_only":
                    visible=docs[:1]
                else:
                    visible=[]
                if arm=="wrong_subject":
                    foreign=seal_record("OTHER_SANDBOX",SOURCE,"v1",
                        docs[1]["text"].replace(SUBJECT,"OTHER_SANDBOX",1))
                    try:
                        verified_content(SUBJECT,foreign,{SUBJECT},{SOURCE})
                    except ArchiveGateError:
                        rejected=1
                    if rejected!=1:
                        raise ArchiveGateError("Wrong-subject record unexpectedly admitted")
                else:
                    rejected=0
                # Compare first-only with the same a and flipped unseen b.
                if arm=="first_only":
                    opposite_docs,_=verified_docs(family,a,1-b)
                    assert docs[0]==opposite_docs[0], "Hidden second field leaked through record ID"
                first=source_field(family,0,visible[0] if len(visible)>0 else None)
                second=source_field(family,1,visible[1] if len(visible)>1 else None)
                oracle=decide(family,first,second)
                records="\n\n".join(f"RECORD {i+1} [verified ID {d['event_id']}, sha256={d['sha256']}]:\n{d['text']}" for i,d in enumerate(visible))
                if not records: records="NO VERIFIED SOURCE RECORDS"
                header=(f"Requested source subject: {SUBJECT}\nVerified record count: {len(visible)}\n"
                        f"Rejected invalid source candidates: {rejected}\n")
                system=(
                    "You are the Clerk, a literal field extractor for SYNTHETIC test records, not an action decider. "
                    "Read only each source record's FACT clause. Do not use event IDs, hashes, unstated rules, or guesses. "
                    "Return exactly one JSON object with keys first and second, in that order. "
                    "Each value must be the single uppercase factual token from its own numbered record, "
                    "or JSON null if the corresponding numbered record is absent. "
                    'Example format only: {"first":null,"second":null}. '
                    "Do not give an action, explanation, Markdown or other text."
                )
                user=header+records+"\n\nFIELD EXTRACTION: "+SOURCE_QUESTION[family]+"\nJSON:"
                trial={"id":f"T1/{family}/{arm}/{a}{b}",
                       "family":family,"arm":arm,"a":a,"b":b,
                       "source_ids":[d["event_id"] for d in visible],
                       "source_hashes":[d["sha256"] for d in visible],
                       "sources":visible,"expected_fields":{"first":first,"second":second},
                       "reference_action":oracle,
                       "guard_rejections":rejected,
                       "reference_if_complete":target if arm=="full" else None,
                       "messages":[{"role":"system","content":system},{"role":"user","content":user}]}
                trials.append(trial)
    assert len(trials)==24 and len({t["id"] for t in trials})==24
    assert len({json.dumps(t["messages"]) for t in trials})==24
    for t in trials:
        if t["arm"]=="full":
            assert t["reference_action"]==t["reference_if_complete"]
        else:
            assert t["reference_action"]=="UNKNOWN"
    assert sum(t["guard_rejections"] for t in trials)==3
    random.Random(SEED).shuffle(trials)
    return trials

def grade(trial,response):
    data=parse_model_json(response)
    accepted=attest(trial["family"],data,trial["sources"])
    assert accepted["action"] in ("UNKNOWN","RELEASE","HOLD","EAST","WEST","ALLOW","DENY")
    actual=trial["expected_fields"]
    return {
        **accepted,
        "model_extracted_first_correct":data is not None and data["first"]==actual["first"],
        "model_extracted_second_correct":data is not None and data["second"]==actual["second"],
        "model_exact_pair_correct":data is not None and data==actual,
        "post_gate_correct":accepted["action"]==trial["reference_action"],
        "oracle_action":trial["reference_action"],
    }

def summarize(results,metadata):
    arms=[]
    for arm in ARMS:
        rows=[x for x in results if x["case"]["arm"]==arm]
        arms.append({
            "arm":arm,"n":len(rows),
            "strict_json":sum(x["metric"]["valid_json"] for x in rows),
            "exact_two_slots":sum(x["metric"]["model_exact_pair_correct"] for x in rows),
            "grounded":sum(x["metric"]["grounded"] for x in rows),
            "first_slot_correct":sum(x["metric"]["model_extracted_first_correct"] for x in rows),
            "second_slot_correct":sum(x["metric"]["model_extracted_second_correct"] for x in rows),
            "post_gate_correct":sum(x["metric"]["post_gate_correct"] for x in rows),
            "post_gate_actions":sum(x["metric"]["action"]!="UNKNOWN" for x in rows),
            "oracle_actions":sum(x["case"]["reference_action"]!="UNKNOWN" for x in rows),
            "guard_rejections":sum(x["case"]["guard_rejections"] for x in rows),
            "mean_tokens":round(statistics.mean(x["prompt_tokens"]+x["output_tokens"] for x in rows),2)
        })
    flips=[]
    for family in FAMILIES:
        for a in (0,1):
            pair=sorted([r for r in results if r["case"]["family"]==family and r["case"]["arm"]=="full"
                         and r["case"]["a"]==a],key=lambda r:r["case"]["b"])
            assert len(pair)==2
            flips.append({
                "family":family,"first_bit":a,
                "reference_flips":pair[0]["case"]["reference_action"]!=pair[1]["case"]["reference_action"],
                "model_extraction_both_correct":all(x["metric"]["model_exact_pair_correct"] for x in pair),
                "post_gate_correct_flip":all(x["metric"]["action"]==x["case"]["reference_action"] for x in pair),
            })
    assert all(x["reference_flips"] for x in flips)
    return {**metadata,"n":len(results),"groups":arms,"counterfactual_pairs":flips,
            "model_extracted_full_flip_pairs_correct":sum(x["model_extraction_both_correct"] for x in flips),
            "post_gate_full_flip_pairs_correct":sum(x["post_gate_correct_flip"] for x in flips),
            "total_prompt_tokens":sum(x["prompt_tokens"] for x in results),
            "total_output_tokens":sum(x["output_tokens"] for x in results),
            "limit":"All source fields synthetic; regex oracle and calculator encode the answer by construction; model role is extraction only.",
            "no_canonical_pretorius_memories_touched":True}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--validate-only",action="store_true")
    p.add_argument("--model",default="Qwen/Qwen2.5-0.5B-Instruct")
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    trials=build_cases()
    if args.validate_only:
        print("E3_T1_VALID",len(trials),"unique contexts, trusted source envelopes, hidden bit isolation",flush=True)
        return
    if args.output is None:
        p.error("--output required")
    import torch,transformers
    from transformers import AutoTokenizer,AutoModelForCausalLM
    torch.set_num_threads(4)
    tokenizer=AutoTokenizer.from_pretrained(args.model,trust_remote_code=False)
    model=AutoModelForCausalLM.from_pretrained(args.model,torch_dtype=torch.float32,trust_remote_code=False)
    model.eval()
    meta={"study":"E3-T1-Clerk","model":args.model,
          "model_revision":getattr(model.config,"_commit_hash",None),
          "script_sha256":sha(Path(__file__).read_text(encoding="utf-8")),
          "source_script_sha256":sha((HERE/"counterfactual_calibration_v2.py").read_text(encoding="utf-8")),
          "greedy":True,"max_new_tokens":64,
          "source_is_synthetic":True,
          "guard_before_model":True,
          "python":platform.python_version(),
          "torch":torch.__version__,"transformers":transformers.__version__}
    args.output.mkdir(parents=True,exist_ok=True)
    save(args.output/"manifest.json",meta)
    data=[]
    with (args.output/"responses.jsonl").open("w",encoding="utf-8") as f:
        for i,trial in enumerate(trials,1):
            tok=tokenizer.apply_chat_template(trial["messages"],tokenize=True,
                        add_generation_prompt=True,return_tensors="pt")
            with torch.inference_mode():
                gen=model.generate(input_ids=tok,attention_mask=torch.ones_like(tok),
                        do_sample=False,max_new_tokens=64,pad_token_id=tokenizer.eos_token_id)
            out=gen[0,tok.shape[1]:]
            rendered=tokenizer.decode(out,skip_special_tokens=True)
            row={"case":trial,"output":rendered,"metric":grade(trial,rendered),
                 "prompt_tokens":int(tok.shape[1]),"output_tokens":int(out.shape[0])}
            data.append(row)
            f.write(json.dumps(row,ensure_ascii=False,sort_keys=True)+"\n")
            f.flush()
            if i%6==0: print("T1_COMPLETED",i,"/",len(trials),flush=True)
    result=summarize(data,meta)
    save(args.output/"summary.json",result)
    print("T1_FINAL",json.dumps({"model":args.model,"groups":result["groups"],
         "flip_pairs":result["post_gate_full_flip_pairs_correct"]}),flush=True)

if __name__=="__main__":
    main()
