#!/usr/bin/env python3
"""E3-T2P v3: plain-text L1 source-field copying with explicit missing-field marker."""
from __future__ import annotations
import argparse
import json
import platform
import statistics
from pathlib import Path
from l1_field_extraction_v2 import build,load_l1,digest,save,ARMS

HERE=Path(__file__).resolve().parent
MARKER="FIELD_ABSENT"
STUDY="E3-T2P-v3"

def conditions(rows,source_meta):
    original,manifest=build(rows,source_meta)
    for case in original:
        case["case_id"]=case["case_id"].replace("E3T2V2/","E3T2P3/")
        case["messages"][0]["content"]=(
            "You are a literal reader of a trusted but fictional reconstructed archive. "
            "You are not Pretorius and do not infer new memories or attitudes. "
            "Find the EXACT requested labeled field in the presented text. "
            "If the requested label appears, output ONLY the entire text following that label, "
            "verbatim as a SINGLE PLAIN-TEXT LINE. Preserve spelling, punctuation, and capitalization. "
            "Do not include the label name, a JSON object, quotes, Markdown, or an explanation. "
            "If the requested labeled field is ABSENT, output ONLY FIELD_ABSENT in uppercase. "
            "Do not infer a field's value from narrative or the other labeled field."
        )
        case["messages"][1]["content"]=case["messages"][1]["content"].replace("OUTPUT JSON:","ONE-LINE OUTPUT:")
        system,user=(m["content"] for m in case["messages"])
        assert "source text" not in system and '"answer"' not in system
        assert user.endswith("ONE-LINE OUTPUT:")
        assert (case["expected"] is None)==(case["arm"]=="target_withheld")
        if case["expected"] is not None:
            assert case["expected"] in user
        else:
            assert case["expected"] is None
    assert len(original)==72 and len(set(c["case_id"] for c in original))==72
    return original,manifest

def grade(case,output):
    answer=output.strip()
    expected=MARKER if case["expected"] is None else case["expected"]
    match=answer==expected
    returned_absent=answer==MARKER
    return {
        "strict_exact":bool(match),
        "returned_missing_marker":returned_absent,
        "correct_missing_field":bool(case["expected"] is None and returned_absent),
        "unjustified_field_response":bool(case["expected"] is None and not returned_absent),
        "wrong_field_response":bool(case["expected"] is not None and answer==case["other_field_value"]),
        "contains_reference_text":bool(case["expected"] is not None and case["expected"] in answer),
        "format_extra_text":bool(case["expected"] is not None and case["expected"] in answer and not match),
    }

def summarize(data,meta):
    groups=[]
    for arm in ARMS:
        rows=[r for r in data if r["case"]["arm"]==arm]
        groups.append({
            "arm":arm,"n":len(rows),
            "strict_exact":sum(r["score"]["strict_exact"] for r in rows),
            "correct_missing_field":sum(r["score"]["correct_missing_field"] for r in rows),
            "unjustified_field_response":sum(r["score"]["unjustified_field_response"] for r in rows),
            "wrong_other_field":sum(r["score"]["wrong_field_response"] for r in rows),
            "raw_contains_correct_text":sum(r["score"]["contains_reference_text"] for r in rows),
            "mean_total_tokens":round(statistics.mean(r["prompt_tokens"]+r["output_tokens"] for r in rows),2),
        })
    return {**meta,"cases_completed":len(data),"groups":groups,
            "total_input_tokens":sum(r["prompt_tokens"] for r in data),
            "total_output_tokens":sum(r["output_tokens"] for r in data),
            "source_is_structured_quoted_autobiography":True,
            "not_semantic_relevance_adjudication":True,
            "not_confirmatory_due_to_prior_prompt_inspection":True}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",required=True,type=Path)
    p.add_argument("--output",type=Path)
    p.add_argument("--model",default="Qwen/Qwen2.5-0.5B-Instruct")
    p.add_argument("--validate-only",action="store_true")
    args=p.parse_args()
    source,source_meta=load_l1(args.source)
    cases,fixture=conditions(source,source_meta)
    if args.validate_only:
        print("L1_T2P3_FIXTURE_VALID",len(cases),fixture["selected_event_ids"],flush=True)
        return
    if args.output is None:
        p.error("--output required")
    import torch,transformers
    from transformers import AutoTokenizer,AutoModelForCausalLM
    torch.set_num_threads(4)
    tokenizer=AutoTokenizer.from_pretrained(args.model,trust_remote_code=False)
    model=AutoModelForCausalLM.from_pretrained(args.model,torch_dtype=torch.float32,trust_remote_code=False)
    model.eval()
    meta={**fixture,"experiment":STUDY,"model":args.model,
          "model_revision":getattr(model.config,"_commit_hash",None),
          "script_sha256":digest(Path(__file__).read_text(encoding="utf-8")),
          "v2_script_sha256":digest((HERE/"l1_field_extraction_v2.py").read_text(encoding="utf-8")),
          "source_commit_is_pinned":True,"greedy":True,"max_new_tokens":112,
          "python":platform.python_version(),"torch":torch.__version__,
          "transformers":transformers.__version__,
          "field_missing_marker":MARKER}
    args.output.mkdir(parents=True,exist_ok=True)
    save(args.output/"manifest.json",meta)
    results=[]
    with (args.output/"responses.jsonl").open("w",encoding="utf-8") as fd:
        for i,case in enumerate(cases,1):
            inp=tokenizer.apply_chat_template(case["messages"],tokenize=True,
                  add_generation_prompt=True,return_tensors="pt")
            with torch.inference_mode():
                gen=model.generate(input_ids=inp,attention_mask=torch.ones_like(inp),
                                   do_sample=False,max_new_tokens=112,pad_token_id=tokenizer.eos_token_id)
            out=gen[0,inp.shape[1]:]
            response=tokenizer.decode(out,skip_special_tokens=True)
            row={"case":case,"output":response,"score":grade(case,response),
                 "prompt_tokens":int(inp.shape[1]),"output_tokens":int(len(out))}
            fd.write(json.dumps(row,ensure_ascii=False,sort_keys=True)+"\n")
            fd.flush()
            results.append(row)
            if i%12==0:print("E3_T2P3",i,"/",len(cases),flush=True)
    report=summarize(results,meta)
    save(args.output/"summary.json",report)
    print("E3_T2P3_DONE",json.dumps({"model":args.model,"groups":report["groups"]}),flush=True)

if __name__=="__main__":
    main()
