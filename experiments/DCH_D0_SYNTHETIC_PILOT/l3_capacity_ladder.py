#!/usr/bin/env python3
"""DCH L3 staged LLM competence ladder. Synthetic, development-only; no dyad claims."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from integration_v2 import build_cases
from model_runner import backend_instance, parse_response

STAGES=("S1_single_field","S2_latest_replacement","S3_permission_gate","S4_integrated")
RULES={
"S1_single_field":"Read the single authorized priority record. Answer its uppercase value. If absent, answer UNKNOWN.",
"S2_latest_replacement":"Use the latest authorized turn for priority. Answer its uppercase value. If absent, answer UNKNOWN.",
"S3_permission_gate":"Use the supplied current permission and commitment_status. If either record is missing, UNKNOWN. Otherwise permission revoked means WITHHOLD; else commitment_status cancelled means DECLINE; else PROCEED.",
"S4_integrated":"Use the latest authorized record for permission, commitment_status, due_turn, and priority. If any is missing, UNKNOWN. Else first revoked permission means WITHHOLD; else cancelled commitment means DECLINE; else if current_turn is less than due_turn, SCHEDULE; otherwise FULFILL_ followed by uppercase priority."
}
HEADER=("Synthetic administrative task. Use ONLY listed authorized records. "
        "Return one JSON object with exactly fields answer (string) and source_event_ids (array of strings). "
        "Give supporting source ids for fields actually needed in the decision. "
        "Do not invent event identifiers. Do not explain the answer.")

def sha(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()

def first_json_object(raw):
    """Auditable secondary extraction; preserve strict whole-response score separately."""
    start=raw.find("{")
    if start<0:return None
    depth=0
    quoted=False
    escaped=False
    for i in range(start,len(raw)):
        c=raw[i]
        if quoted:
            if escaped:escaped=False
            elif c=="\\":escaped=True
            elif c=='"':quoted=False
        elif c=='"':quoted=True
        elif c=="{":depth+=1
        elif c=="}":
            depth-=1
            if depth==0:
                try:
                    obj=json.loads(raw[start:i+1])
                except (ValueError,TypeError):return None
                if not isinstance(obj,dict) or not isinstance(obj.get("answer"),str):return None
                if not isinstance(obj.get("source_event_ids"),list) or not all(isinstance(x,str) for x in obj["source_event_ids"]):return None
                return {"answer":obj["answer"].strip(),"source_event_ids":obj["source_event_ids"]}
    return None

def make_example(case,stage,arm):
    if stage not in STAGES or arm not in ("available","cold"):raise ValueError((stage,arm))
    events={e["event_id"].split("-")[-1]:e for e in case["events"] if e["authorized"]}
    picks={
        "S1_single_field":("E12",),
        "S2_latest_replacement":("E04","E12"),
        "S3_permission_gate":("E09","E10"),
        "S4_integrated":("E01","E02","E03","E04","E09","E10","E11","E12")
    }[stage]
    selected=[events[k] for k in picks] if arm=="available" else []
    values={e["key"]:e["value"] for e in selected}
    current=case["current_turn"]
    if arm=="cold":answer="UNKNOWN";certificate=[]
    elif stage in ("S1_single_field","S2_latest_replacement"):
        answer=values["priority"].upper();certificate=[selected[-1]["event_id"]]
    elif stage=="S3_permission_gate":
        if values["permission"]=="revoked":answer="WITHHOLD"; certificate=[events["E09"]["event_id"]]
        elif values["commitment_status"]=="cancelled":answer="DECLINE";certificate=[events["E09"]["event_id"],events["E10"]["event_id"]]
        else:answer="PROCEED";certificate=[events["E09"]["event_id"],events["E10"]["event_id"]]
    else:
        if values["permission"]=="revoked":answer="WITHHOLD";certificate=[events["E09"]["event_id"]]
        elif values["commitment_status"]=="cancelled":answer="DECLINE";certificate=[events["E09"]["event_id"],events["E10"]["event_id"]]
        elif current<int(values["due_turn"]):answer="SCHEDULE";certificate=[events[k]["event_id"] for k in ("E09","E10","E11")]
        else:answer="FULFILL_"+values["priority"].upper();certificate=[events[k]["event_id"] for k in ("E09","E10","E11","E12")]
    visible={"persona_id":case["persona_id"],"stage":stage,"arm":arm,"current_turn":current,
      "records":[{"event_id":x["event_id"],"turn":x["turn"],"key":x["key"],"value":x["value"]} for x in selected]}
    target={"persona_id":case["persona_id"],"stage":stage,"arm":arm,"expected":answer,"required_sources":certificate}
    return visible,target

def prepare(out,count=12):
    if out.exists():raise FileExistsError(out)
    out.mkdir(parents=True)
    cases,_=build_cases(count)
    visible,answers=[],[]
    for case in cases:
        for stage in STAGES:
            for arm in ("available","cold"):
                v,a=make_example(case,stage,arm)
                visible.append(v);answers.append(a)
    (out/"l3_visible.json").write_text(json.dumps(visible,indent=2)+"\n")
    (out/"l3_EVALUATOR_ONLY.json").write_text(json.dumps(answers,indent=2)+"\n")
    manifest={"status":"DEVELOPMENT_NOT_CONFIRMATORY","model_not_run":True,
      "histories":count,"visible_examples":len(visible),
      "visible_sha256":sha(visible),"answer_sha256":sha(answers)}
    (out/"l3_manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    return manifest

def messages_for(v):
    records=v["records"]
    archive="\n".join(f'{e["turn"]} | {e["event_id"]} | {e["key"]}={e["value"]}' for e in records) if records else "(NO AUTHORIZED RECORDS)"
    return [{"role":"system","content":HEADER+" "+RULES[v["stage"]]},
      {"role":"user","content":f'Current turn: {v["current_turn"]}\nAuthorized records:\n{archive}\nGive the result.'}]

def generate(folder,model,backend_name="mock",max_histories=8):
    out=folder/"l3_raw.json"
    if out.exists():raise FileExistsError(out)
    data=json.loads((folder/"l3_visible.json").read_text())
    subjects=list(dict.fromkeys(v["persona_id"] for v in data))[:max_histories]
    selected=[v for v in data if v["persona_id"] in subjects]
    backend=backend_instance(backend_name,model,"http://127.0.0.1:11434")
    records=[]
    for v in selected:
        prompt=messages_for(v)
        result=backend.respond(prompt)
        strict=parse_response(result["text"])
        tolerant=first_json_object(result["text"])
        seen={r["event_id"] for r in v["records"]}
        records.append({"persona_id":v["persona_id"],"stage":v["stage"],"arm":v["arm"],
          "prompt_sha256":sha(prompt),"record_count":len(v["records"]),
          "available_ids":sorted(seen),"raw_text":result["text"],
          "strict":strict,"first_object":tolerant,
          "prompt_tokens":result.get("prompt_tokens"),"output_tokens":result.get("output_tokens"),
          "done_reason":result.get("done_reason"),"model_reported":result.get("model_reported")})
    payload={"status":"REAL_LLM_DEVELOPMENT" if backend_name!="mock" else "MOCK_ONLY",
      "evidence_for_DCH":False,"has_human_partner":False,"model":model,
      "backend":backend_name,"visible_sha256":sha(data),"records":records}
    out.write_text(json.dumps(payload,indent=2)+"\n")
    return {"status":payload["status"],"responses":len(records)}

def evaluate(folder):
    dest=folder/"l3_evaluation.json"
    if dest.exists():raise FileExistsError(dest)
    raw=json.loads((folder/"l3_raw.json").read_text())
    keys=json.loads((folder/"l3_EVALUATOR_ONLY.json").read_text())
    targets={(r["persona_id"],r["stage"],r["arm"]):r for r in keys}
    grouped={}
    for r in raw["records"]:
        key=(r["persona_id"],r["stage"],r["arm"]); target=targets[key]
        p=r["first_object"]
        ids=set(p["source_event_ids"]) if p else set()
        scores={"case":r["persona_id"],"expected":target["expected"],"predicted":p["answer"] if p else None,
          "first_object_valid":p is not None,"strict_valid":r["strict"]["parse_valid"],
          "first_object_accuracy":p is not None and p["answer"]==target["expected"],
          "strict_accuracy":r["strict"]["parse_valid"] and r["strict"]["answer"]==target["expected"],
          "source_ids_valid":p is not None and ids.issubset(set(r["available_ids"])),
          "source_certificate_complete":p is not None and ids.issubset(set(r["available_ids"])) and set(target["required_sources"]).issubset(ids),
          "truncated":r["done_reason"]=="length"}
        grouped.setdefault(r["stage"]+":"+r["arm"],[]).append(scores)
    metric_names=("first_object_valid","strict_valid","first_object_accuracy","strict_accuracy","source_ids_valid","source_certificate_complete","truncated")
    summary={key:{"n":len(items),**{metric:sum(r[metric] for r in items)/len(items) for metric in metric_names}} for key,items in grouped.items()}
    output={"status":"EXPLORATORY_CAPACITY_CALIBRATION","human_partner_present":False,
            "model":raw["model"],"summary":summary,"rows":grouped,"DCH_efficacy_claim":"NONE"}
    dest.write_text(json.dumps(output,indent=2)+"\n")
    return summary

def main():
    p=argparse.ArgumentParser()
    p.add_argument("mode",choices=("prepare","run","evaluate"))
    p.add_argument("--folder",required=True,type=Path)
    p.add_argument("--count",type=int,default=12)
    p.add_argument("--histories",type=int,default=8)
    p.add_argument("--backend",default="mock",choices=("mock","transformers","ollama"))
    p.add_argument("--model",default="Qwen/Qwen2.5-1.5B-Instruct")
    a=p.parse_args()
    output=prepare(a.folder,a.count) if a.mode=="prepare" else generate(a.folder,a.model,a.backend,a.histories) if a.mode=="run" else evaluate(a.folder)
    print(json.dumps(output,indent=2))
if __name__=="__main__":main()
