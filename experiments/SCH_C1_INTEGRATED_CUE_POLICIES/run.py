#!/usr/bin/env python3
"""SCH C1 integrated cue-to-policy transfer and full-token cost pilot."""
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

HERE=Path(__file__).resolve().parent
FIXTURE=HERE/"conditions.json"


def file_json(path, val):
    path.write_text(json.dumps(val,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")


def load():
    raw=FIXTURE.read_bytes()
    cfg=json.loads(raw)
    assert cfg["schema"]=="SCH-C1-v1"
    assert len(cfg["examples"])==6 and len(cfg["holdouts"])==6
    assert len(cfg["arms"])==6 and len(cfg["tags"])==2
    assert len({x["id"] for x in cfg["examples"]+cfg["holdouts"]})==12
    assert all(x["urgency"]=="routine" for x in cfg["examples"])
    assert all(x["urgency"]=="urgent" for x in cfg["holdouts"])
    assert cfg["output_values"]==["SHARE","WITHHOLD"]
    return cfg,hashlib.sha256(raw).hexdigest()


def mapping(arm):
    if arm=="fewshot_swapped":
        return {"VORNA":"audit","KELVO":"consent"}
    return {"VORNA":"consent","KELVO":"audit"}


def policy_result(policy,case):
    return "SHARE" if case["risk"]=="low" and case[policy]=="yes" else "WITHHOLD"


def examples(cfg,arm):
    if arm in ("fresh","plain_rules","compact_rules"):
        return ""
    lines=["Historical decisions from the fictional archive office:"]
    bad={"VORNA":{2,3},"KELVO":{3,5}}
    # For each label, two SHARE and four WITHHOLD demonstrations.
    for i,example in enumerate(cfg["examples"]):
        for tag in cfg["tags"]:
            if arm=="mismatched_examples":
                value="SHARE" if i in bad[tag] else "WITHHOLD"
            else:
                value=policy_result(mapping(arm)[tag],example)
            lines.append("Tag={tag}; consent={consent}; public_audit={audit}; "
                         "sensitive_risk={risk}; urgency={urgency}; decision={answer}"
                         .format(tag=tag,consent=example["consent"],audit=example["audit"],
                                 risk=example["risk"],urgency=example["urgency"],answer=value))
    return "\n".join(lines)


def setup_text(cfg,arm):
    if arm=="plain_rules":
        return ("Archive policy: VORNA shares a record only if consent is granted and the "
                "risk is low. KELVO shares a record only if a public audit exists and the "
                "risk is low. High risk always means WITHHOLD, even if urgent. "
                "Otherwise output WITHHOLD.")
    if arm=="compact_rules":
        return ("C=consent yes; A=public audit yes; R=high risk; "
                "VORNA: SHARE iff C and not R. KELVO: SHARE iff A and not R. "
                "Else WITHHOLD. Urgency never overrides.")
    return examples(cfg,arm)


def messages(cfg,arm,tag,case):
    facts=("Urgent archive request. {story}\n"
           "Report tag: {tag}\nConsent granted: {consent}\n"
           "Public audit exists: {audit}\nSensitive risk: {risk}\n"
           "Urgency: {urgency}\nDecision:"
          ).format(story=case["story"],tag=tag,consent=case["consent"],
                   audit=case["audit"],risk=case["risk"],urgency=case["urgency"])
    context=setup_text(cfg,arm)
    prompt=((context+"\n\n") if context else "")+facts
    return [{"role":"system","content":cfg["system"]},{"role":"user","content":prompt}]


def cases(cfg):
    out=[]
    for arm in cfg["arms"]:
        for tag in cfg["tags"]:
            for case in cfg["holdouts"]:
                out.append({
                  "id":f"C1/{arm}/{tag}/{case['id']}",
                  "arm":arm,"tag":tag,
                  "test_id":case["id"],
                  "diagnostic":case["id"] in ("T1","T2"),
                  "safety_veto":case["risk"]=="high",
                  "expected_induced":policy_result(mapping(arm)[tag],case) if arm in
                                     ("fewshot_stable","fewshot_swapped","plain_rules","compact_rules") else None,
                  "expected_canonical":policy_result(mapping("fewshot_stable")[tag],case),
                  "features":case,
                  "messages":messages(cfg,arm,tag,case)
                })
    assert len(out)==72 and len(set(x["id"] for x in out))==72
    random.Random(cfg["seed"]).shuffle(out)
    return out


def score(txt,case):
    norm=txt.strip().upper()
    strict=norm if norm in ("SHARE","WITHHOLD") else None
    m=re.fullmatch(r"\s*(SHARE|WITHHOLD)[.]?\s*",txt,re.I)
    relaxed=m.group(1).upper() if m else None
    return {
       "strict_parsed":strict,"relaxed_parsed":relaxed,
       "strict_valid":strict is not None,"relaxed_valid":relaxed is not None,
       "strict_induced_correct":(strict==case["expected_induced"]) if case["expected_induced"] else None,
       "relaxed_induced_correct":(relaxed==case["expected_induced"]) if case["expected_induced"] else None,
       "strict_canonical_correct":strict==case["expected_canonical"],
       "relaxed_canonical_correct":relaxed==case["expected_canonical"]
    }


def summary(records):
    groups=[]
    for arm in ("fewshot_stable","fewshot_swapped","mismatched_examples",
                "plain_rules","compact_rules","fresh"):
        sub=[r for r in records if r["case"]["arm"]==arm]
        known=[r for r in sub if r["metrics"]["strict_induced_correct"] is not None]
        diag=[r for r in known if r["case"]["diagnostic"]]
        veto=[r for r in known if r["case"]["safety_veto"]]
        groups.append({
          "arm":arm,"n":len(sub),
          "strict_format_count":sum(r["metrics"]["strict_valid"] for r in sub),
          "relaxed_format_count":sum(r["metrics"]["relaxed_valid"] for r in sub),
          "induced_accuracy_strict":round(sum(r["metrics"]["strict_induced_correct"] for r in known)/len(known),4) if known else None,
          "induced_accuracy_relaxed":round(sum(r["metrics"]["relaxed_induced_correct"] for r in known)/len(known),4) if known else None,
          "diagnostic_accuracy_strict":round(sum(r["metrics"]["strict_induced_correct"] for r in diag)/len(diag),4) if diag else None,
          "veto_accuracy_strict":round(sum(r["metrics"]["strict_induced_correct"] for r in veto)/len(veto),4) if veto else None,
          "canonical_accuracy_strict":round(sum(r["metrics"]["strict_canonical_correct"] for r in sub)/len(sub),4),
          "input_tokens":sum(r["prompt_tokens"] for r in sub),
          "output_tokens":sum(r["generated_tokens"] for r in sub),
          "avg_total_tokens":round(statistics.mean(r["prompt_tokens"]+r["generated_tokens"] for r in sub),2),
          "cost_per_strict_correct_case_tokens":round(
              sum(r["prompt_tokens"]+r["generated_tokens"] for r in known)/
              sum(r["metrics"]["strict_induced_correct"] for r in known),2
          ) if known and any(r["metrics"]["strict_induced_correct"] for r in known) else None
        })
    stable={(r["case"]["tag"],r["case"]["test_id"]):r for r in records if r["case"]["arm"]=="fewshot_stable"}
    swapped={(r["case"]["tag"],r["case"]["test_id"]):r for r in records if r["case"]["arm"]=="fewshot_swapped"}
    diagnostic=[k for k in stable if k[1] in ("T1","T2")]
    flips=sum(stable[k]["metrics"]["strict_parsed"] is not None and
              swapped[k]["metrics"]["strict_parsed"] is not None and
              stable[k]["metrics"]["strict_parsed"]!=swapped[k]["metrics"]["strict_parsed"]
              for k in diagnostic)
    correct_flips=sum(stable[k]["metrics"]["strict_induced_correct"] and swapped[k]["metrics"]["strict_induced_correct"]
                      for k in diagnostic)
    return {"groups":groups,"diagnostic_pairs":len(diagnostic),
            "observed_diagnostic_flips":flips,"correctly_reversed_pairs":correct_flips}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--validate-only",action="store_true")
    p.add_argument("--model",default="Qwen/Qwen2.5-0.5B-Instruct")
    p.add_argument("--output",type=Path,default=HERE/"results"/"local")
    args=p.parse_args()
    cfg,digest=load()
    cs=cases(cfg)
    assert all(len(c["messages"])==2 for c in cs)
    assert len([c for c in cs if c["diagnostic"]])==24
    for case in cfg["examples"]:
        for tag in cfg["tags"]:
            assert policy_result(mapping("fewshot_stable")[tag],case) in cfg["output_values"]
    assert sum(policy_result(mapping("fewshot_stable")["VORNA"],ex)=="SHARE" for ex in cfg["examples"])==2
    assert sum(policy_result(mapping("fewshot_stable")["KELVO"],ex)=="SHARE" for ex in cfg["examples"])==2
    assert all(policy_result("audit",x)=="WITHHOLD" for x in cfg["holdouts"] if x["risk"]=="high")
    print("FIXTURE_SHA256",digest,"TOTAL_CASES",len(cs),flush=True)
    if args.validate_only:
        print("VALIDATION_PASS: frozen 72 cases, balanced example labels, reference rules and diagnostic swaps",flush=True)
        return

    import torch
    import transformers
    from transformers import AutoModelForCausalLM,AutoTokenizer
    torch.set_num_threads(min(4,torch.get_num_threads()))
    tok=AutoTokenizer.from_pretrained(args.model,trust_remote_code=False)
    model=AutoModelForCausalLM.from_pretrained(args.model,torch_dtype=torch.float32,trust_remote_code=False)
    model.eval()
    args.output.mkdir(parents=True,exist_ok=True)
    manifest={
      "study":"SCH-C1 integrated cue policy transfer",
      "research_status":"exploratory_not_confirmatory",
      "model":args.model,"model_revision":getattr(model.config,"_commit_hash",None),
      "fixture_sha256":digest,"schema":cfg["schema"],"case_order_seed":cfg["seed"],
      "python":platform.python_version(),"torch":torch.__version__,"transformers":transformers.__version__,
      "planned_cases":72,"sampling":"greedy decoding","max_new_tokens":cfg["max_new_tokens"],
      "independent_chat_context_per_case":True,"external_memory":False,
      "weight_updates":False,
    }
    file_json(args.output/"manifest.json",manifest)
    began=time.monotonic()
    records=[]
    with (args.output/"responses.jsonl").open("w",encoding="utf-8") as file:
        for index,c in enumerate(cs,1):
            inp=tok.apply_chat_template(c["messages"],tokenize=True,return_tensors="pt",add_generation_prompt=True)
            with torch.inference_mode():
                y=model.generate(input_ids=inp,attention_mask=torch.ones_like(inp),
                      max_new_tokens=cfg["max_new_tokens"],do_sample=False,
                      pad_token_id=tok.eos_token_id)
            outids=y[0,inp.shape[1]:]
            txt=tok.decode(outids,skip_special_tokens=True)
            record={"case":c,"output":txt,"prompt_tokens":int(inp.shape[1]),
                    "generated_tokens":int(len(outids)),"metrics":score(txt,c)}
            records.append(record)
            file.write(json.dumps(record,ensure_ascii=False)+"\n")
            file.flush()
            if index%12==0:
                print(f"GENERATED {index}/72",flush=True)
    result={
       **manifest,**summary(records),
       "cases_completed":len(records),
       "prompt_tokens":sum(r["prompt_tokens"] for r in records),
       "generated_tokens":sum(r["generated_tokens"] for r in records),
       "duration_seconds":round(time.monotonic()-began,3),
       "scope_warning":"Toy integrated policy generalization. No identity persistence or metacognitive effect tested."
    }
    file_json(args.output/"summary.json",result)
    print("SUMMARY_JSON_BEGIN",flush=True)
    print(json.dumps({"model":args.model,"revision":manifest["model_revision"],"cases":len(records),
           "tokens":result["prompt_tokens"]+result["generated_tokens"],
           "diagnostic_flips":result["observed_diagnostic_flips"],
           "correct_flips":result["correctly_reversed_pairs"],
           "groups":result["groups"]},ensure_ascii=False),flush=True)
    print("SUMMARY_JSON_END",flush=True)

if __name__=="__main__":
    sys.exit(main())
