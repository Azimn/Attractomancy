#!/usr/bin/env python3
"""E3-T1B: independently extract one source record per prompt and reuse typed facts."""
from __future__ import annotations
import argparse
import json
import platform
import random
from pathlib import Path

from clerk_extraction import (FAMILIES,SUBJECT,SOURCE,VOCAB,decide,save,
                              sha,source_field,verified_docs)

SLOT_QUESTIONS={
    "seal":("Extract the signed obligation's required seal token.",
            "Extract the actual packet's verified seal token."),
    "route":("Extract the signed original EAST/WEST destination.",
             "Extract the newer signed KEEP/FLIP route update."),
    "permission":("Extract the original documented ALLOW/DENY access decision.",
                  "Extract the newer signed KEEP/REVERSE permission amendment."),
}
SEED=20261010

def extraction_cases():
    unique=[]
    for family in FAMILIES:
        for slot in (0,1):
            for value_bit in (0,1):
                a=value_bit if slot==0 else 0
                b=value_bit if slot==1 else 0
                docs,_=verified_docs(family,a,b)
                document=docs[slot]
                # Withheld other-value invariance: local document exactly same across
                # the counterfactual opposite other bit.
                otherdocs,_=verified_docs(family,a,(1-b) if slot==0 else b)
                if slot==1:
                    otherdocs,_=verified_docs(family,1-a,b)
                assert document==otherdocs[slot],"Other input bit leaked into isolated source record"
                expected=source_field(family,slot,document)
                system=("You are a literal source-field reader, not an action decider. "
                        "Read only the FACT sentence in the single verified SYNTHETIC record. "
                        "Return exactly one JSON object with only a key value, "
                        'in the form {"value":"TOKEN"}. '
                        "The token must be an uppercase literal value from the record. "
                        "Do not invent values, read other records, infer outcomes, "
                        "or provide any explanation or Markdown.")
                user=(f"Requested subject: {SUBJECT}\n"
                      f"SINGLE VERIFIED RECORD (slot {slot+1}):\n"
                      f"EVENT ID: {document['event_id']}\n"
                      f"VERIFIED SHA256: {document['sha256']}\n"
                      +document["text"]+"\n\nFIELD REQUEST: "+SLOT_QUESTIONS[family][slot]+"\nJSON:")
                unique.append({
                    "id":f"E3-T1B/{family}/{slot}/{value_bit}",
                    "family":family,"slot":slot,"bit":value_bit,
                    "event_id":document["event_id"],
                    "source_sha256":document["sha256"],
                    "verified_source":document,
                    "expected":expected,
                    "messages":[{"role":"system","content":system},{"role":"user","content":user}]
                })
    assert len(unique)==12 and len({x["event_id"] for x in unique})==12
    assert len({json.dumps(x["messages"]) for x in unique})==12
    random.Random(SEED).shuffle(unique)
    return unique

def parse_token(text):
    try:
        data=json.loads(text.strip())
    except (json.JSONDecodeError,ValueError):
        return None
    if not isinstance(data,dict) or set(data)!={"value"} or not isinstance(data["value"],str):
        return None
    return data["value"] if data["value"].isupper() else None

def validate(case,output):
    raw=parse_token(output)
    exact=raw==case["expected"]
    vocab=raw in VOCAB[case["family"]][case["slot"]]
    verified_value=raw if exact and vocab else None
    return {
        "strict_json_single_value":raw is not None,
        "model_exact_value":exact,
        "source_attested_value":verified_value,
        "rejected":verified_value is None
    }

def combine(rows):
    index={(r["case"]["family"],r["case"]["slot"],r["case"]["bit"]):r for r in rows}
    assert len(index)==12
    tasks=[]
    for family in FAMILIES:
        for a in (0,1):
            for b in (0,1):
                r1=index[(family,0,a)]
                r2=index[(family,1,b)]
                left=r1["metric"]["source_attested_value"]
                right=r2["metric"]["source_attested_value"]
                action=decide(family,left,right)
                ref_docs,expected=verified_docs(family,a,b)
                assert r1["case"]["event_id"]==ref_docs[0]["event_id"]
                assert r2["case"]["event_id"]==ref_docs[1]["event_id"]
                tasks.append({
                    "family":family,"first_bit":a,"second_bit":b,
                    "first_event_id":r1["case"]["event_id"],
                    "second_event_id":r2["case"]["event_id"],
                    "first_verified":left is not None,"second_verified":right is not None,
                    "action":action,"reference":expected,"correct":action==expected
                })
    assert len(tasks)==12
    flips=[]
    for family in FAMILIES:
        for a in (0,1):
            pair=sorted([x for x in tasks if x["family"]==family and x["first_bit"]==a],
                        key=lambda x:x["second_bit"])
            assert len(pair)==2 and pair[0]["reference"]!=pair[1]["reference"]
            flips.append({"family":family,"first_bit":a,"both_correct":all(x["correct"] for x in pair),
                         "correct_output_flip":all(x["correct"] for x in pair)
                             and pair[0]["action"]!=pair[1]["action"]})
    return tasks,flips

def run():
    import sys
    parser=argparse.ArgumentParser()
    parser.add_argument("--validate-only",action="store_true")
    parser.add_argument("--model",default="Qwen/Qwen2.5-0.5B-Instruct")
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    cases=extraction_cases()
    if args.validate_only:
        # The software oracle is a fixture sanity check and a deterministic upper bound,
        # not an independent model-cognition result.
        toy=[{"case":c,"metric":{"source_attested_value":c["expected"]}} for c in cases]
        combined,flips=combine(toy)
        assert sum(x["correct"] for x in combined)==12
        assert all(x["both_correct"] for x in flips)
        print("T1B_VALID 12 source-local prompts, 12 oracle decisions, 6 oracle reversals",flush=True)
        return
    if args.output is None:
        parser.error("Output required")
    import torch,transformers
    from transformers import AutoTokenizer,AutoModelForCausalLM
    torch.set_num_threads(4)
    tokenizer=AutoTokenizer.from_pretrained(args.model,trust_remote_code=False)
    model=AutoModelForCausalLM.from_pretrained(args.model,torch_dtype=torch.float32,trust_remote_code=False)
    model.eval()
    meta={"study":"E3-T1B Private Clerk","model":args.model,
          "revision":getattr(model.config,"_commit_hash",None),
          "script_sha256":sha(Path(__file__).read_text(encoding="utf-8")),
          "fixture_v2_sha256":sha((Path(__file__).parent/"counterfactual_calibration_v2.py").read_text(encoding="utf-8")),
          "cases":len(cases),"max_new_tokens":32,"greedy":True,
          "source_kind":"synthetic_not_canonical",
          "no_hidden_other_fact_in_record_id":True,"cached_extracts":True,
          "python":platform.python_version(),"torch":torch.__version__,
          "transformers":transformers.__version__}
    args.output.mkdir(parents=True,exist_ok=True)
    save(args.output/"manifest.json",meta)
    rows=[]
    with (args.output/"extractions.jsonl").open("w",encoding="utf-8") as f:
        for i,case in enumerate(cases,1):
            inp=tokenizer.apply_chat_template(case["messages"],tokenize=True,
                                add_generation_prompt=True,return_tensors="pt")
            with torch.inference_mode():
                generated=model.generate(input_ids=inp,attention_mask=torch.ones_like(inp),
                              do_sample=False,max_new_tokens=32,pad_token_id=tokenizer.eos_token_id)
            completion=generated[0,inp.shape[1]:]
            answer=tokenizer.decode(completion,skip_special_tokens=True)
            row={"case":case,"output":answer,"metric":validate(case,answer),
                 "input_tokens":int(inp.shape[1]),"output_tokens":int(len(completion))}
            rows.append(row)
            f.write(json.dumps(row,sort_keys=True,ensure_ascii=False)+"\n")
            f.flush()
            if i%4==0: print("T1B_EXTRACTED",i,"/",len(cases),flush=True)
    tasks,flips=combine(rows)
    totals={
        "per_slot":{
           str(slot):{"cases":len([r for r in rows if r["case"]["slot"]==slot]),
                "source_attested":sum(r["metric"]["model_exact_value"] for r in rows if r["case"]["slot"]==slot),
                "strict_output":sum(r["metric"]["strict_json_single_value"] for r in rows if r["case"]["slot"]==slot)}
           for slot in (0,1)
        },
        "model_extractions":len(rows),
        "strict_json":sum(r["metric"]["strict_json_single_value"] for r in rows),
        "attested_values":sum(r["metric"]["model_exact_value"] for r in rows),
        "composed_cases":len(tasks),
        "correct_composed_actions":sum(x["correct"] for x in tasks),
        "correct_counterfactual_flip_pairs":sum(x["correct_output_flip"] for x in flips),
        "reference_oracle_correct_by_construction":12,
        "reference_oracle_correct_flips_by_construction":6,
        "total_model_input_tokens":sum(r["input_tokens"] for r in rows),
        "total_model_output_tokens":sum(r["output_tokens"] for r in rows),
        "mean_tokens_per_source_extraction":round(sum(r["input_tokens"]+r["output_tokens"] for r in rows)/12,2),
        "no_new_model_generations_for_composition":True,
        "source_attestation_fail_closed":True,
        "limitations":"Only synthetic source values; one-source-per-call prompt differs from joint Clerk; source regex and calculator are software oracles; cached pairing reduces inference count."
    }
    save(args.output/"summary.json",{**meta,"metrics":totals,"tasks":tasks,"flips":flips})
    print("T1B_SUMMARY",json.dumps({"model":args.model,**totals}),flush=True)

if __name__=="__main__":
    run()
