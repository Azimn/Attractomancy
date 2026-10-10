#!/usr/bin/env python3
"""E3 reviewer-label validity gate; does not create, infer, or impute judgments."""
from __future__ import annotations
import argparse
import itertools
import json
import statistics
from collections import defaultdict
from pathlib import Path

LABELS={"direct_support","contradicts","context_insufficient","irrelevant","provenance_ineligible"}
CASE_STATES={"sufficient","insufficient","ambiguous"}
REVIEWERS=3

def load_jsonl(path):
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]

def validate(packet,judgments):
    by_case={c["case_id"]:c for c in packet}
    if not by_case or len(by_case)!=len(packet):
        raise ValueError("No cases or duplicated case IDs")
    if any(c.get("example_not_blind_ground_truth") for c in packet):
        raise ValueError("Calibration packet cannot be promoted to independent E3 adjudication")
    coll=defaultdict(dict)
    for entry in judgments:
        case=entry.get("case_id")
        reviewer=entry.get("reviewer_id")
        if case not in by_case or not isinstance(reviewer,str) or not reviewer.strip():
            raise ValueError("Unrecognized case or reviewer")
        if reviewer in coll[case]:
            raise ValueError("Duplicate reviewer-case judgment")
        candidates={c["candidate_id"] for c in by_case[case]["candidates"]}
        labels=entry.get("candidate_labels")
        if not isinstance(labels,list) or len(labels)!=len(candidates):
            raise ValueError("All candidate passages require independent reviewer labels")
        by_id={}
        for c in labels:
            cid=c.get("candidate_id")
            label=c.get("label")
            rationale=c.get("rationale")
            if cid not in candidates or cid in by_id or label not in LABELS or not isinstance(rationale,str) or not rationale.strip():
                raise ValueError("Invalid label, duplicate candidate or absent rationale")
            by_id[cid]=label
        if set(by_id)!=candidates:
            raise ValueError("Some candidate passages were not adjudicated")
        sufficient=entry.get("sufficient_sets")
        status=entry.get("case_sufficiency")
        if status not in CASE_STATES or not isinstance(sufficient,list):
            raise ValueError("Unknown sufficiency judgment")
        if status=="sufficient" and not sufficient:
            raise ValueError("Sufficient classification requires one or more evidence sets")
        if status!="sufficient" and sufficient:
            raise ValueError("Ambiguous/insufficient classifications must not assert a sufficient set")
        sets=[]
        for group in sufficient:
            if not isinstance(group,list) or len(group)<2 or len(set(group))!=len(group):
                raise ValueError("Each sufficient evidence set needs two or more distinct passages")
            if not set(group).issubset(candidates):
                raise ValueError("Evidence set refers to absent candidate")
            if any(by_id[c]!="direct_support" for c in group):
                raise ValueError("Sufficient set includes a passage not labeled as direct support")
            sets.append(tuple(sorted(group)))
        if len(set(sets))!=len(sets):
            raise ValueError("Duplicate sufficient sets")
        if not isinstance(entry.get("case_rationale"),str) or not entry["case_rationale"].strip():
            raise ValueError("Missing case-level sufficiency rationale")
        coll[case][reviewer]={"labels":by_id,"status":status,"sets":sets}
    if set(coll)!=set(by_case):
        raise ValueError("Missing adjudicated cases")
    if any(len(x)<REVIEWERS for x in coll.values()):
        raise ValueError("At least three distinct reviewer IDs per case are required")
    pair_stats=[]
    for case,reviews in coll.items():
        for reviewer_a,reviewer_b in itertools.combinations(sorted(reviews),2):
            a=reviews[reviewer_a]["labels"]
            b=reviews[reviewer_b]["labels"]
            agreement=sum(a[k]==b[k] for k in a)/len(a)
            pair_stats.append(agreement)
    return {
        "status":"verified_label_schema_not_external_reviewer_authentication",
        "n_cases":len(packet),"n_judgments":len(judgments),
        "minimum_reviewers":min(len(x) for x in coll.values()),
        "average_pairwise_candidate_label_agreement":round(statistics.mean(pair_stats),4),
        "source_relevance_truth_not_assumed":True,
        "model_decisions_not_scored_by_this_tool":True,
        "per_case":[{"case_id":c,"reviewers":len(group),
                     "sufficiency_votes":{name:sum(r["status"]==name for r in group.values()) for name in CASE_STATES},
                     "unique_sufficient_sets_proposed":len(set(x for r in group.values() for x in r["sets"]))}
                    for c,group in sorted(coll.items())]
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--packet",type=Path,required=True)
    p.add_argument("--judgments",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    packet=load_jsonl(args.packet)
    annotations=load_jsonl(args.judgments)
    report=validate(packet,annotations)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("E3_INDEPENDENT_LABELS_SCHEMATICALLY_VERIFIED",report["n_cases"],flush=True)

if __name__=="__main__":
    main()
