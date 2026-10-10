#!/usr/bin/env python3
"""Require independent, text-grounded judgment before temporal relation labels."""
from __future__ import annotations
import argparse
import itertools
import json
import statistics
from collections import defaultdict
from pathlib import Path

FLAGS=("reinforces_prior_context","modifies_prior_context",
       "supersedes_specific_commitment","tension_or_conflict",
       "insufficient_to_reconcile")

def load_jsonl(path):
    return [json.loads(v) for v in path.read_text(encoding="utf-8").splitlines() if v.strip()]

def validate(packet,reviews):
    pool={x["pair_id"]:x for x in packet}
    if not pool or len(pool)!=len(packet):
        raise ValueError("Missing or duplicate study cases")
    collected=defaultdict(dict)
    for r in reviews:
        pair=r.get("pair_id")
        reviewer=r.get("reviewer_id")
        if pair not in pool or not isinstance(reviewer,str) or not reviewer.strip():
            raise ValueError("Invalid reviewer or case")
        if reviewer in collected[pair]:
            raise ValueError("Duplicate reviewer judgment")
        disclosure=r.get("reviewer_disclosure")
        if not isinstance(disclosure,dict) or disclosure.get("not_original_case_author") is not True or disclosure.get("did_not_consult_organizer_mapping") is not True:
            raise ValueError("Required procedural masking disclosure missing")
        flags=r.get("candidate_relation_flags")
        if not isinstance(flags,dict) or set(flags)!=set(FLAGS) or any(type(v)!=bool for v in flags.values()):
            raise ValueError("Every explicit relation flag requires a boolean")
        positive=any(flags[x] for x in FLAGS if x!="insufficient_to_reconcile")
        if flags["insufficient_to_reconcile"] and positive:
            raise ValueError("Insufficient evidence cannot simultaneously be a confident positive inference")
        if not flags["insufficient_to_reconcile"] and not positive:
            raise ValueError("Choose at least one interpretation or explicit insufficient evidence")
        justification=r.get("reviewer_rationale")
        confidence=r.get("confidence")
        if not isinstance(justification,str) or len(justification.strip())<25:
            raise ValueError("Reviewer rationale is missing")
        if type(confidence) not in (int,float) or not (0<=confidence<=1):
            raise ValueError("Confidence out of range")
        a=r.get("earlier_exact_quote")
        b=r.get("later_exact_quote")
        if positive:
            if not isinstance(a,str) or len(a.strip())<8 or a not in pool[pair]["earlier_excerpt"]:
                raise ValueError("Earlier source span must be an exact quote")
            if not isinstance(b,str) or len(b.strip())<8 or b not in pool[pair]["later_excerpt"]:
                raise ValueError("Later source span must be an exact quote")
        else:
            if a is not None or b is not None:
                raise ValueError("Insufficient interpretation should not claim positive evidence spans")
        commitment=r.get("explicit_prior_commitment")
        change=r.get("explicit_superseding_statement")
        if flags["supersedes_specific_commitment"]:
            if not isinstance(commitment,str) or commitment not in pool[pair]["earlier_excerpt"]:
                raise ValueError("Revocation requires an exact prior commitment quote")
            if not isinstance(change,str) or change not in pool[pair]["later_excerpt"]:
                raise ValueError("Revocation requires an exact later revision quote")
            if len(commitment)<8 or len(change)<8:
                raise ValueError("Revocation quote too short")
        elif commitment is not None or change is not None:
            raise ValueError("Only explicit supersession claims may provide revocation spans")
        collected[pair][reviewer]=flags
    if set(collected)!=set(pool):
        raise ValueError("Not every source pair reviewed")
    if any(len(entries)<3 for entries in collected.values()):
        raise ValueError("Require three independently disclosed reviewers per case")
    agreements=[]
    for group in collected.values():
        for a,b in itertools.combinations(sorted(group),2):
            agreements.append(sum(group[a][flag]==group[b][flag] for flag in FLAGS)/len(FLAGS))
    result={
        "status":"checked_submitted_reviewer_schema_not_authenticated_human_independence",
        "cases":len(pool),"reviewer_case_submissions":len(reviews),
        "min_distinct_reviewers":min(len(v) for v in collected.values()),
        "mean_pairwise_flag_agreement":round(statistics.mean(agreements),4),
        "source_sidecar_never_used_as_truth":True,
        "original_temporal_order_not_equivalent_to_revocation":True,
        "not_full_main_e3":True,
        "per_pair":[{"pair_id":pair,"reviewers":len(group),
                      "votes":{flag:sum(j[flag] for j in group.values()) for flag in FLAGS}}
                     for pair,group in sorted(collected.items())]
    }
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--packet",type=Path,required=True)
    p.add_argument("--reviews",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    result=validate(load_jsonl(args.packet),load_jsonl(args.reviews))
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("E3_T3_RELATIONSHIP_REVIEW_SCHEMA_OK",result["reviewer_case_submissions"])

if __name__=="__main__":
    main()
