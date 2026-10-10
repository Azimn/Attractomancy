#!/usr/bin/env python3
"""E3 annotation scaffold: method-masked candidate packets, no invented ratings."""
from __future__ import annotations
import argparse
import hashlib
import json
import random
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/"SCH_E2_MULTIMEMORY_DECISIONS"))
from build_cases import load_config
from source_adapter import load_l1

TYPES=("direct_support","contradicts","context_insufficient","irrelevant","provenance_ineligible")
POOL_SEED=20261009
REVIEWER_COUNT=3

def sha(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()

def save(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")

def selected_questions(path,calibration_only):
    if calibration_only:
        cfg,_=load_config()
        return [{"case_id":"CAL-"+x["id"],"question":x["question"],
                 "status":"historically_source_informed_not_independent"}
                for x in cfg["cards"]]
    if path is None:
        raise ValueError("Supply --questions JSONL for newly independently authored E3 cases")
    questions=[json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(questions)<36:
        raise ValueError("E3 main packet requires at least 36 independent questions")
    if len({x["case_id"] for x in questions})!=len(questions):
        raise ValueError("Case IDs are duplicated")
    if any("expected" in x or "gold" in x or "record_ids" in x for x in questions):
        raise ValueError("Unblinded source labels in submitted question fixture")
    if any(not x.get("question") or x.get("status")!="independently_authored" for x in questions):
        raise ValueError("Questions lack independently authored provenance")
    return questions

def build(source,questions,out):
    from graph_retrieval import load_retriever,adjacency,diffuse,rank
    rows,source_meta=load_l1(source)
    retriever=load_retriever(source)
    ids=retriever.ids
    graph,graphinfo=adjacency(rows,ids)
    rng=random.Random(POOL_SEED)
    packet=[]
    organizers=[]
    for case in questions:
        scored=retriever.score(case["question"],mode="lexical")
        source_ids=rank(scored,ids)[:10]
        linked_ids=rank(diffuse(scored,graph),ids)[:10]
        available=[id for id in ids if id not in set(source_ids+linked_ids)]
        random_ids=rng.sample(available,10)
        pooled={}
        for method,collection in (("lexical",source_ids),("source_graph",linked_ids),("random",random_ids)):
            for eid in collection:
                pooled.setdefault(eid,set()).add(method)
        order=list(pooled)
        rng.shuffle(order)
        options=[]
        organizer=[]
        for i,event_id in enumerate(order):
            record=rows[event_id]
            blinded="C"+sha(f"{POOL_SEED}|{case['case_id']}|{event_id}")[:12].upper()
            options.append({"candidate_id":blinded,
                            "title":record["title"],
                            "source_excerpt":record["memory_text"],
                            "source_status":"reconstructed_fiction",
                            "reviewer_label":None,
                            "reviewer_rationale":None})
            organizer.append({"candidate_id":blinded,"event_id":event_id,
                              "methods":sorted(pooled[event_id]),
                              "event_sha256":sha(record["memory_text"])})
        packet.append({"case_id":case["case_id"],"question":case["question"],
                       "candidate_count":len(options),"candidates":options,
                       "example_not_blind_ground_truth":case["status"]!="independently_authored"})
        organizers.append({"case_id":case["case_id"],"mapping":organizer})
    manifest={"protocol":"E3 blind packet v0.1","source":source_meta,
              "question_count":len(questions),"pool_methods":["lexical","source_graph","random"],
              "per_method_candidates":10,"case_seed":POOL_SEED,
              "source_event_ids_hidden_in_reviewer_packet":True,
              "candidate_method_hidden_in_reviewer_packet":True,
              "case_mode":"E2_CALIBRATION_UNBLINDED" if len(questions)==6 else "NEW_E3_UNRATED",
              "annotations_received":0,"independent_reviewer_target":REVIEWER_COUNT,
              "content_warning":"Source author and original public repo remain accessible; masking does not prevent a reviewer from deliberately seeking provenance.",
              "independence_warning":"E2 calibration questions were authored with prior source inspection and can never qualify as independent E3 test data."}
    out.mkdir(parents=True,exist_ok=True)
    with (out/"reviewer_packet.jsonl").open("w",encoding="utf-8") as f:
        for entry in packet: f.write(json.dumps(entry,ensure_ascii=False)+"\n")
    save(out/"packet_manifest.json",manifest)
    # Keep event identity and retrieval provenance in a distinct organizer-only file.
    # Do NOT automatically commit the mapping to the public research repository.
    save(out/"organizer_only_mapping.json",organizers)
    save(out/"blank_adjudication_template.json",{
       "status":"blank_not_completed","candidate_labels_allowed":list(TYPES),
       "reviewers_required":REVIEWER_COUNT,
       "reviewer_records_example":[{"reviewer_id":"R01","case_id":"CASE_ID",
                                   "candidate_id":"C_REDACTED","label":None,
                                   "supporting_text_span":None,"rationale":None}],
       "evidence_sets_example":[{"case_id":"CASE_ID","reviewer_id":"R01",
                                  "sufficient_candidate_id_sets":[],
                                  "decision_supported":None,
                                  "contradictions":[],"rationale":None}],
       "instructions":"For true E3: at least 3 independent reviewers; no lookup of organizer mapping until adjudications frozen; no invented labels."
    })
    print("E3_PACKET_GENERATED",json.dumps({
        "cases":len(packet),"candidates_total":sum(len(x["candidates"]) for x in packet),
        "source_records":source_meta["record_count"],"mode":manifest["case_mode"],
        "labels":0}),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",required=True,type=Path)
    p.add_argument("--output",required=True,type=Path)
    p.add_argument("--questions",type=Path)
    p.add_argument("--calibration-only",action="store_true")
    args=p.parse_args()
    questions=selected_questions(args.questions,args.calibration_only)
    build(args.source,questions,args.output)

if __name__=="__main__":
    main()
