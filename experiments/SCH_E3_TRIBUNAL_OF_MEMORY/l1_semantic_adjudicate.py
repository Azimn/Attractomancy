#!/usr/bin/env python3
"""Validate human reviewer responses to original L1 narrative support candidates.

Never fabricate ratings, use the original sidecar as the correct answer, or
upgrade this source-informed calibration to the main independent E3 benchmark.
"""
from __future__ import annotations
import argparse
import itertools
import json
import statistics
from collections import defaultdict
from pathlib import Path

ALLOWED={"supported_by_narrative","contradicted_by_narrative",
         "underdetermined_by_narrative","not_about_this_event"}
REVIEWERS=3

def jsonl(path):
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]

def validate(packet,annotations):
    rows={x["packet_case_id"]:x for x in packet}
    if len(rows)!=len(packet) or not rows:
        raise ValueError("Duplicate or empty source cases")
    outcomes=defaultdict(dict)
    for answer in annotations:
        case=answer.get("packet_case_id")
        reviewer=answer.get("reviewer_id")
        if case not in rows or not isinstance(reviewer,str) or not reviewer.strip():
            raise ValueError("Unknown case or reviewer identity")
        if reviewer in outcomes[case]:
            raise ValueError("Repeated case judgment from same reviewer")
        disclosures=answer.get("reviewer_disclosure")
        if not isinstance(disclosures,dict) or disclosures.get("did_not_consult_original_corpus") is not True or disclosures.get("not_original_case_author") is not True:
            raise ValueError("Reviewer disclosure missing; cannot establish procedural masking")
        candidates=rows[case]["candidate_interpretations"]
        required={x["candidate_id"] for x in candidates}
        assessments=answer.get("candidate_assessments")
        if not isinstance(assessments,list) or len(assessments)!=len(required):
            raise ValueError("Candidate count/labels incomplete")
        refs={}
        for label in assessments:
            cid=label.get("candidate_id")
            status=label.get("label")
            rationale=label.get("rationale")
            confidence=label.get("confidence")
            quote=label.get("exact_narrative_quote")
            if cid not in required or cid in refs or status not in ALLOWED:
                raise ValueError("Unknown candidate, label or duplicate")
            if not isinstance(rationale,str) or len(rationale.strip())<12:
                raise ValueError("Reviewer rationale insufficient")
            if type(confidence) not in (int,float) or not (0<=confidence<=1):
                raise ValueError("Reviewer confidence outside 0-1")
            if status in ("supported_by_narrative","contradicted_by_narrative"):
                if not isinstance(quote,str) or len(quote.strip())<8 or quote not in rows[case]["source_excerpt"]:
                    raise ValueError("Support or contradiction must quote literal narrative span")
            elif quote is not None:
                raise ValueError("Quote is for positive evidence/contradiction only")
            refs[cid]=status
        if set(refs)!=required:
            raise ValueError("Unjudged candidates")
        outcomes[case][reviewer]=refs
    if set(outcomes)!=set(rows):
        raise ValueError("Not all source cases reviewed")
    if any(len(v)<REVIEWERS for v in outcomes.values()):
        raise ValueError("Three distinct reviewers needed for every source case")
    pairwise=[]
    for case,group in outcomes.items():
        for a,b in itertools.combinations(sorted(group),2):
            pairwise.append(sum(group[a][cid]==group[b][cid] for cid in group[a])/len(group[a]))
    summary={
        "status":"completed_schema_checked_human_judgments_not_independently_authenticated",
        "trial":"e3_l1_semantic_calibration_not_main_independent_e3",
        "n_cases":len(packet),"n_votes":len(annotations),
        "n_candidate_evaluations":sum(len(v) for row in outcomes.values() for v in row.values()),
        "min_reviewers":min(len(v) for v in outcomes.values()),
        "pairwise_exact_label_agreement":round(statistics.mean(pairwise),4),
        "source_metadata_is_not_a_truth_label":True,
        "real_source_authority_not_cryptographically_verified":True,
        "no_main_e3_confirmatory_status":True,
        "per_case":[{"case_id":case,"reviewers":len(group),
            "candidate_votes":{cid:{lab:sum(v[cid]==lab for v in group.values()) for lab in sorted(ALLOWED)}
                               for cid in sorted(next(iter(group.values())))}}
                    for case,group in sorted(outcomes.items())]
    }
    return summary

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--packet",type=Path,required=True)
    p.add_argument("--annotations",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    packet=jsonl(args.packet)
    review=jsonl(args.annotations)
    result=validate(packet,review)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
    print("L1_SEMANTIC_REVIEW_SCHEMA_VALID",result["n_votes"],flush=True)

if __name__=="__main__":
    main()
