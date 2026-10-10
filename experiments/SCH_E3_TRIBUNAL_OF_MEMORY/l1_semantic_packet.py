#!/usr/bin/env python3
"""Build unlabeled E3 actual-L1 semantic evidence-review packets.

Source-authored structured belief/relationship statements are NOT blind ground
truth for what narrative actually implies. An independent human review may
determine that author sidecar assertions are ambiguous or unsupported.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import random
import sys
from pathlib import Path
from l1_field_extraction import sample,digest,FIELDS
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/"SCH_E2_MULTIMEMORY_DECISIONS"))
from source_adapter import load_l1,verified

SEED=20261010
VOTING_LABELS=("supported_by_narrative","contradicted_by_narrative",
               "underdetermined_by_narrative","not_about_this_event")

def dump(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,indent=2,ensure_ascii=False,sort_keys=True)+"\n",encoding="utf-8")

def build(source,output):
    rows,source_info=load_l1(source)
    event_ids=sample(rows)
    rng=random.Random(SEED+137)
    packets=[]
    organizer=[]
    for eid in event_ids:
        rec=rows[eid]
        _,verified_digest=verified(rec)
        episode=rec["episode_id"]
        peer_ids=sorted([i for i,r in rows.items() if r["episode_id"]==episode and i!=eid])
        other_ids=sorted(i for i in rows if i!=eid and rows[i]["episode_id"]!=episode)
        assert peer_ids and other_ids
        peer=rows[rng.choice(peer_ids)]
        remote=rows[rng.choice(other_ids)]
        for field,label in FIELDS.items():
            source_claim=rec[field]
            candidate_sources=[
              ("source_sidecar",rec),
              ("same_episode_decoy",peer),
              ("other_episode_decoy",remote)
            ]
            # Independent rater may judge *any* candidate supported, including
            # a nominal decoy; file records no truth labels.
            candidates=[]
            organizer_rows=[]
            for kind,candidate_rec in candidate_sources:
                statement=candidate_rec[field]
                cid="C"+hashlib.sha256((str(SEED)+eid+field+statement).encode()).hexdigest()[:12].upper()
                candidates.append({
                    "candidate_id":cid,
                    "proposed_interpretation":statement,
                    "reviewer_label":None,
                    "supporting_quote_from_narrative":None,
                    "reviewer_explanation":None,
                    "confidence":None
                })
                organizer_rows.append({"candidate_id":cid,
                          "source_kind":kind,"claim_source_event_id":candidate_rec["event_id"],
                          "statement_sha256":digest(statement)})
            rng.shuffle(candidates)
            assert len({x["candidate_id"] for x in candidates})==3
            packets.append({
                "packet_case_id":"L1SEM-"+digest(eid+"|"+field)[:12].upper(),
                "source_excerpt":rec["memory_text"],
                "requested_dimension":"belief_change" if field=="belief_changes" else "relationship_change",
                "instructions":"For EACH candidate, determine whether the narrative directly supports, contradicts, leaves underdetermined, or is unrelated to the proposed interpretation. Quote exact evidence if supported or contradicted. Do not assume any candidate is correct.",
                "source_class":"RECONSTRUCTED_FICTION_NOT_LIVED",
                "reviewer_outcomes_ready":False,
                "candidate_interpretations":candidates,
            })
            organizer.append({
                "case_id":packets[-1]["packet_case_id"],
                "original_event_id":eid,"source_sha256":verified_digest,
                "relationship_or_belief_source_field":field,
                "candidate_sources":organizer_rows
            })
    assert len(packets)==24 and sum(len(v["candidate_interpretations"]) for v in packets)==72
    # Explicitly prevent method/provenance label leakage in a reviewer item.
    assert all("event_id" not in json.dumps(v) and "source_sidecar" not in json.dumps(v) for v in packets)
    manifest={
        "status":"unreviewed_source_semantics_packet_not_e3_blind_confirmation",
        "source":source_info,
        "source_sample_seed":SEED,
        "review_packet_count":len(packets),
        "candidate_statements_count":72,
        "reviewers_required":3,
        "reviewer_votes_received":0,
        "allowed_judgments":list(VOTING_LABELS),
        "narrative_source_event_ids_redacted":True,
        "candidate_source_identity_redacted":True,
        "public_corpus_is_recoverable_so_blinding_is_procedural_not_cryptographic":True,
        "source_authored_sidecar_is_not_human_relevance_ground_truth":True,
        "independently_authored_e3_cases":False,
        "caveat":"Sidecar descriptions and within-episode decoys can each be supported, contradictory or ambiguous; raters must evaluate all independently and may disagree."
    }
    output.mkdir(parents=True,exist_ok=True)
    with (output/"review_packet.jsonl").open("w",encoding="utf-8") as f:
        for entry in packets:
            f.write(json.dumps(entry,ensure_ascii=False)+"\n")
    dump(output/"review_manifest.json",manifest)
    # This file should be retained by the experiment coordinator outside
    # the public repository. CI intentionally must NOT stage or upload it.
    dump(output/"ORGANIZER_ONLY_DO_NOT_COMMIT.json",organizer)
    print("E3_L1_SEMANTIC_PACKET",json.dumps({"cases":24,"candidate_claims":72,
        "reviewer_votes":0,"source_manifest":source_info["l1_manifest_sha256"]}),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    build(args.source,args.output)

if __name__=="__main__":
    main()
