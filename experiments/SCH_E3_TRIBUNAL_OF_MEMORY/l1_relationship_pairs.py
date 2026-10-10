#!/usr/bin/env python3
"""Create a non-adjudicated 24-pair temporal relationship review packet from real L1."""
from __future__ import annotations
import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/"SCH_E2_MULTIMEMORY_DECISIONS"))
from source_adapter import load_l1,verified

PARTNERS=(
    "Clara Weiss","Marta Voss","Jakob Lenz","Mathilde Rosen",
    "Anna Lenz","Emil Reuter","Anton Kappel","Henry Frankenstein",
)
CATEGORIES=(
    "reinforces_prior_context","modifies_prior_context",
    "supersedes_specific_commitment","tension_or_conflict",
    "insufficient_to_reconcile",
)
SEED="E3-T3-book-of-debts-v1"

def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def dump(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")

def make(rows,source_meta):
    packets=[]
    organizer=[]
    partner_sizes={}
    for partner in PARTNERS:
        relevant=[r for r in rows.values() if partner in r.get("participants",[])]
        relevant.sort(key=lambda r:(r["chronological_order"],r["event_id"]))
        assert len(relevant)>=20, "Insufficient eligible recurring relationship history"
        partner_sizes[partner]=len(relevant)
        n=len(relevant)
        anchors=[relevant[i] for i in (n//6,n//2,(5*n)//6)]
        assert len({x["event_id"] for x in anchors})==3
        pairings=[(anchors[0],anchors[1]),(anchors[1],anchors[2]),(anchors[0],anchors[2])]
        for earlier,later in pairings:
            assert earlier["chronological_order"]<later["chronological_order"]
            assert partner in earlier["participants"] and partner in later["participants"]
            _,sha_early=verified(earlier)
            _,sha_later=verified(later)
            ident="T3-"+sha(SEED+"|"+partner+"|"+earlier["event_id"]+"|"+later["event_id"])[:14].upper()
            packet={
                "pair_id":ident,
                "relationship_counterparty":partner,
                "source_class":"FICTIONAL_RECONSTRUCTED_ARCHIVE_NOT_LIVED",
                "earlier_excerpt":earlier["memory_text"],
                "later_excerpt":later["memory_text"],
                "question":"How, if at all, does the later account alter the earlier relationship evidence about the named counterparty? Cite each claim to an exact narrative span, and do not infer revocation from recency alone.",
                "candidate_relation_flags":{k:None for k in CATEGORIES},
                "source_evidence_from_earlier":None,
                "source_evidence_from_later":None,
                "explicit_prior_commitment":None,
                "explicit_superseding_statement":None,
                "reviewer_rationale":None,
                "annotated":False,
            }
            assert "event_id" not in json.dumps(packet).lower()
            assert "relationship_changes" not in json.dumps(packet)
            organizer.append({
                "pair_id":ident,"relationship_counterparty":partner,
                "earlier_event_id":earlier["event_id"],
                "later_event_id":later["event_id"],
                "earlier_chronological_order":earlier["chronological_order"],
                "later_chronological_order":later["chronological_order"],
                "earlier_verified_sha256":sha_early,"later_verified_sha256":sha_later,
                "earlier_source_relationship_change":earlier["relationship_changes"],
                "later_source_relationship_change":later["relationship_changes"],
            })
            packets.append(packet)
    assert len(packets)==24 and len({x["pair_id"] for x in packets})==24
    assert len(set(x["relationship_counterparty"] for x in packets))==8
    assert all(not x["annotated"] and all(v is None for v in x["candidate_relation_flags"].values())
               for x in packets)
    manifest={
        "status":"unreviewed_l1_temporal_relationship_pairs",
        "source":source_meta,"pair_count":len(packets),
        "partner_count":len(PARTNERS),"partner_list":list(PARTNERS),
        "pairings_per_partner":3,"original_source_event_counts":partner_sizes,
        "flags_are_nonexclusive":True,"allowed_flags":list(CATEGORIES),
        "reviewers_required":3,"reviewer_submissions":0,
        "derived_from_original_450_reconstructed_fiction":True,
        "not_independently_authored_new_dilemmas":True,
        "not_main_blind_e3":True,
        "source_role_masking_is_procedural":True,
        "original_event_ids_and_relationship_sidecars_not_in_reviewer_packet":True,
        "correlated_pairs_warning":"Each relationship uses 3 overlapping pair comparisons; n=24 is not 24 independent personal trajectories.",
        "commitment_warning":"An event occurring later does not by itself supersede earlier obligations."
    }
    return packets,organizer,manifest

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    rows,source=load_l1(args.source)
    packet,organizer,manifest=make(rows,source)
    args.output.mkdir(parents=True,exist_ok=True)
    with (args.output/"reviewer_pairs.jsonl").open("w",encoding="utf-8") as fd:
        for row in packet:
            fd.write(json.dumps(row,ensure_ascii=False)+"\n")
    dump(args.output/"review_manifest.json",manifest)
    # Never upload/stage or publish the organizer identity/event map.
    dump(args.output/"ORGANIZER_ONLY_DO_NOT_COMMIT.json",organizer)
    print("E3_T3_L1_RELATIONSHIPS",json.dumps({
        "n_pairs":len(packet),"n_partners":len(PARTNERS),"reviewers":0,
        "source_sha":source["l1_manifest_sha256"]}),flush=True)

if __name__=="__main__":
    main()
