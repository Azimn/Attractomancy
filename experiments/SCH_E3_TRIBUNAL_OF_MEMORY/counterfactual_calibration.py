#!/usr/bin/env python3
"""E3-C: synthetic two-evidence factorial counterfactual model calibration."""
from __future__ import annotations
import argparse
import hashlib
import json
import platform
import random
import statistics
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/"SCH_D1_EXTERNAL_RECONSTRUCTION"))
from archive_guard import ArchiveGateError,seal_record,verified_content

SUBJECT="PRETORIUS_SANDBOX"
SOURCE="e3c_synthetic_calibration_v1"
FAMILIES=("seal","route","permission")
ARMS=("full_symbol_forced","full_key_forced","first_only_forced",
      "none_forced","full_key_eligible","first_only_eligible","wrong_subject_eligible")
SEED=20261009
SCHEMA="E3-C-v1"

def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def save(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,indent=2,ensure_ascii=False,sort_keys=True)+"\n",encoding="utf-8")

def two_records(family,a,b):
    caseid=f"{family}-{a}{b}"
    if family=="seal":
        required="OAK" if a==0 else "ASH"
        offered="OAK" if b==0 else "ASH"
        text1=f"Signed relationship obligation: only packets with seal {required} may be released."
        text2=f"Actual sealed packet's verified seal: {offered}."
        result="RELEASE" if required==offered else "HOLD"
        question=("Two independent records control a synthetic packet decision. "
            "If the verified packet seal matches the obligation's required seal, reply RELEASE. "
            "Otherwise reply HOLD. Reply with the action only.")
    elif family=="route":
        original="EAST" if a==0 else "WEST"
        revision="KEEP" if b==0 else "FLIP"
        text1=f"Signed original delivery commitment: carry the fictional package {original}."
        text2=f"Newer authorized route update: {revision}. KEEP retains the original direction; FLIP changes EAST to WEST or WEST to EAST."
        result=original if revision=="KEEP" else ("WEST" if original=="EAST" else "EAST")
        question=("Determine the effective delivery route. Read the original commitment AND the newer update. "
                  "KEEP preserves the old route and FLIP reverses it. Reply EAST or WEST only.")
    elif family=="permission":
        status="ALLOW" if a==0 else "DENY"
        revision="KEEP" if b==0 else "REVERSE"
        text1=f"Initial documented synthetic access decision: {status}."
        text2=f"Newer signed permission amendment: {revision}. KEEP retains the earlier permission; REVERSE swaps ALLOW and DENY."
        result=status if revision=="KEEP" else ("DENY" if status=="ALLOW" else "ALLOW")
        question=("Determine the effective access permission. Combine the initial permission and the newer "
                  "signed amendment: KEEP preserves the initial action; REVERSE swaps ALLOW and DENY. "
                  "Reply ALLOW or DENY only.")
    else:
        raise ValueError("Unknown family")
    docs=[]
    for i,statement in enumerate((text1,text2),1):
        body="\n".join([
            f"IDENTITY RECORD FOR: {SUBJECT}",
            "STATUS: SIMULATED_EXPERIMENT_NON_CANONICAL",
            f"EVENT ID: E3C-{caseid}-{i}",
            f"SOURCE: {SOURCE}",
            f"RECORD VERSION: {i}",
            "FACT: "+statement
        ])
        obj=seal_record(SUBJECT,SOURCE,"v1",body)
        checked=verified_content(SUBJECT,obj,{SUBJECT},{SOURCE})
        if checked!=body:
            raise AssertionError("Archive envelope modified text")
        docs.append({"event_id":f"E3C-{caseid}-{i}","text":body,
                     "sha256":sha(body),"version":i})
    return docs,question,result

def cases():
    rows=[]
    expected_values={"seal":("RELEASE","HOLD"),"route":("EAST","WEST"),"permission":("ALLOW","DENY")}
    for family in FAMILIES:
        for a in (0,1):
            for b in (0,1):
                docs,question,expected=two_records(family,a,b)
                for arm in ARMS:
                    if arm.startswith("full"):
                        shown=docs
                    elif arm.startswith("first_only"):
                        shown=docs[:1]
                    else:
                        shown=[]
                    guard_fail=0
                    if arm=="wrong_subject_eligible":
                        foreign=seal_record("OTHER_SANDBOX",SOURCE,"v1",
                           docs[1]["text"].replace(SUBJECT,"OTHER_SANDBOX",1))
                        try:
                            verified_content(SUBJECT,foreign,{SUBJECT},{SOURCE})
                        except ArchiveGateError:
                            guard_fail=1
                        if not guard_fail:
                            raise AssertionError("Foreign record passed identity guard")
                    forced=arm.endswith("_forced")
                    key_style="symbol" if arm=="full_symbol_forced" else "key"
                    mem=[]
                    for doc in shown:
                        alias=("✣ OBELISK "+doc["event_id"] if key_style=="symbol"
                                else "INDEX"+sha(doc["event_id"])[:12].upper())
                        mem.append("RECALL INDEX: "+alias+"\n"+doc["text"])
                    sys_msg=(
                        "You are a literal inference renderer over simulated fictional records. "
                        "Never pretend these records are real Pretorius memories. "
                        "Use the question's explicit rule to combine evidence. "
                        + ("You must give the best two-alternative decision as one uppercase word, even if a source is missing. "
                           "Do not output UNKNOWN." if forced else
                           "If both distinct valid records are present, give the one-word decision. "
                           "If either necessary record is absent, output exactly UNKNOWN.")
                        + " Do not explain."
                    )
                    user_msg=(f"Requested subject: {SUBJECT}\nVerified distinct record count: {len(shown)}\n"
                              +("\n\n".join(mem) if mem else "NO VERIFIED RECORDS AVAILABLE")
                              +"\n\nTASK: "+question+"\nOUTPUT:")
                    required=expected if forced or len(shown)==2 else "UNKNOWN"
                    rows.append({
                        "id":f"{SCHEMA}/{family}/{a}{b}/{arm}",
                        "family":family,"a":a,"b":b,"arm":arm,
                        "gold_if_complete":expected,"expected":required,
                        "record_ids":[d["event_id"] for d in shown],
                        "record_sha256":[d["sha256"] for d in shown],
                        "wrong_owner_guard_rejection":guard_fail,
                        "forced":forced,
                        "messages":[{"role":"system","content":sys_msg},
                                    {"role":"user","content":user_msg}]
                    })
    if len(rows)!=84 or len(set(x["id"] for x in rows))!=84:
        raise AssertionError("Incomplete factorial case matrix")
    for family in FAMILIES:
        for arm in ARMS:
            subset=[x for x in rows if x["family"]==family and x["arm"]==arm]
            assert len(subset)==4
            if arm.startswith("full") or arm.endswith("_forced"):
                assert {x["gold_if_complete"] for x in subset}==set(expected_values[family])
    assert sum(x["wrong_owner_guard_rejection"] for x in rows)==12
    random.Random(SEED).shuffle(rows)
    return rows

def summary(rows,model_meta):
    groups=[]
    for arm in ARMS:
        subset=[r for r in rows if r["case"]["arm"]==arm]
        groups.append({
            "arm":arm,"cases":len(subset),
            "strict_expected_hits":sum(r["parsed"]==r["case"]["expected"] for r in subset),
            "outputs_unknown":sum(r["parsed"]=="UNKNOWN" for r in subset),
            "complete_correct_choices":sum(r["parsed"]==r["case"]["gold_if_complete"] for r in subset),
            "valid_outputs":sum(r["valid"] for r in subset),
            "guard_rejections":sum(r["case"]["wrong_owner_guard_rejection"] for r in subset),
            "mean_total_tokens":round(statistics.mean(r["prompt_tokens"]+r["output_tokens"] for r in subset),2)
        })
    flip_scores={}
    for arm in ARMS:
        n=0;correct=0;observed=0
        for family in FAMILIES:
            for a in (0,1):
                pair=sorted([r for r in rows if r["case"]["family"]==family and r["case"]["a"]==a
                             and r["case"]["arm"]==arm],key=lambda r:r["case"]["b"])
                assert len(pair)==2
                assert pair[0]["case"]["gold_if_complete"]!=pair[1]["case"]["gold_if_complete"]
                n+=1
                if pair[0]["parsed"]!=pair[1]["parsed"] and pair[0]["parsed"] is not None and pair[1]["parsed"] is not None:
                    observed+=1
                if all(x["parsed"]==x["case"]["gold_if_complete"] for x in pair):
                    correct+=1
        flip_scores[arm]={"pairs":n,"output_flipped":observed,"both_counterfactuals_correct":correct}
    equivalent=[]
    for family in FAMILIES:
        for a in (0,1):
            for b in (0,1):
                e=next(r for r in rows if r["case"]["family"]==family and r["case"]["a"]==a
                       and r["case"]["b"]==b and r["case"]["arm"]=="full_symbol_forced")
                k=next(r for r in rows if r["case"]["family"]==family and r["case"]["a"]==a
                       and r["case"]["b"]==b and r["case"]["arm"]=="full_key_forced")
                assert e["case"]["record_sha256"]==k["case"]["record_sha256"]
                equivalent.append({"family":family,"bits":f"{a}{b}",
                                   "identical_response":e["output"]==k["output"],
                                   "symbol_answer":e["output"],"key_answer":k["output"],
                                   "expected":e["case"]["expected"]})
    return {**model_meta,"completed_cases":len(rows),"groups":groups,
            "counterfactual_flip":flip_scores,
            "matched_symbol_key_agreement":sum(x["identical_response"] for x in equivalent),
            "matched_symbol_key_pairs":len(equivalent),
            "pairs":equivalent,
            "input_tokens":sum(r["prompt_tokens"] for r in rows),
            "output_tokens":sum(r["output_tokens"] for r in rows),
            "limitations":[
                "All states are synthetic PRETORIUS_SANDBOX calibration records, never canonical autobiography.",
                "The task explicitly gives the combining algorithm; source use does not demonstrate emergent identity.",
                "Only 12 deliberately constructed factorial contexts; no independent model-family replication.",
                "The examples are not statistically independent across repeated arms or counterfactual pairs.",
                "Forced response is distinct from policy-authorized real-world action.",
                "Source record checksum consistency is not third-party authenticated provenance."
            ]}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--validate-only",action="store_true")
    parser.add_argument("--model",default="Qwen/Qwen2.5-0.5B-Instruct")
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    trials=cases()
    code_digest=sha(Path(__file__).read_text(encoding="utf-8"))
    if args.validate_only:
        print("E3C_MATRIX_VALID",len(trials),"families",FAMILIES,"source_guarded",12,flush=True)
        return
    if args.output is None:
        parser.error("--output required for full inference")
    import torch
    import transformers
    from transformers import AutoTokenizer,AutoModelForCausalLM
    torch.set_num_threads(4)
    tokenizer=AutoTokenizer.from_pretrained(args.model,trust_remote_code=False)
    model=AutoModelForCausalLM.from_pretrained(args.model,torch_dtype=torch.float32,trust_remote_code=False)
    model.eval()
    metadata={
        "study":SCHEMA,"status":"synthetic_causal_calibration_not_E3_blind_trial",
        "seed":SEED,"model":args.model,
        "model_revision":getattr(model.config,"_commit_hash",None),
        "script_sha256":code_digest,"records_are_simulated_not_canonical":True,
        "subjects_are_guard_checked_prior_to_injection":True,
        "fresh_two_message_context_each_case":True,
        "greedy":True,"max_new_tokens":12,
        "python":platform.python_version(),"torch":torch.__version__,
        "transformers":transformers.__version__
    }
    args.output.mkdir(parents=True,exist_ok=True)
    save(args.output/"manifest.json",metadata)
    rows=[]
    with (args.output/"responses.jsonl").open("w",encoding="utf-8") as stream:
        for i,trial in enumerate(trials,1):
            tokenized=tokenizer.apply_chat_template(trial["messages"],tokenize=True,
                                      add_generation_prompt=True,return_tensors="pt")
            with torch.inference_mode():
                generated=model.generate(input_ids=tokenized,attention_mask=torch.ones_like(tokenized),
                        do_sample=False,max_new_tokens=12,pad_token_id=tokenizer.eos_token_id)
            out=generated[0,tokenized.shape[1]:]
            answer=tokenizer.decode(out,skip_special_tokens=True)
            candidate=answer.strip().upper()
            eligible={"UNKNOWN","RELEASE","HOLD","EAST","WEST","ALLOW","DENY"}
            parsed=candidate if candidate in eligible else None
            row={"case":trial,"output":answer,"parsed":parsed,
                 "valid":parsed is not None,"prompt_tokens":int(tokenized.shape[1]),
                 "output_tokens":int(out.shape[0])}
            rows.append(row)
            stream.write(json.dumps(row,ensure_ascii=False,sort_keys=True)+"\n")
            stream.flush()
            if i%12==0: print("E3C_PROGRESS",i,"/",len(trials),flush=True)
    report=summary(rows,metadata)
    save(args.output/"summary.json",report)
    print("E3C_RESULTS",json.dumps({
        "model":args.model,"groups":report["groups"],
        "flip":report["counterfactual_flip"],
        "cue_key_agreement":report["matched_symbol_key_agreement"],
        "total_tokens":report["input_tokens"]+report["output_tokens"]}),flush=True)

if __name__=="__main__":
    main()
