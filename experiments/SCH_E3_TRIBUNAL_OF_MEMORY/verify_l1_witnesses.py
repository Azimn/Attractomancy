#!/usr/bin/env python3
"""Validate original pinned Pretorius L1 metadata witness integrity, no model inference."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from l1_field_extraction import sample
from l1_witness_adapter import L1WitnessIndex
from archive_guard import ArchiveGateError

def run(source,output):
    index=L1WitnessIndex(source)
    ids=sample(index.records)
    witnesses=index.selected_witnesses(ids)
    assert len(witnesses)==24
    assert len(set(w["episode_id"] for w in witnesses))==12
    assert len(set(w["event_id"] for w in witnesses))==12
    for w in witnesses:
        assert index.check(w)
        assert w["canonical_char_end"]>w["canonical_char_start"]
        assert w["value_sha256"]==hashlib.sha256(w["value"].encode("utf-8")).hexdigest()
        assert w["source_manifest_sha256"]==index.meta["l1_manifest_sha256"]
        assert w["provenance"]=="reconstructed_fiction_not_lived"
    # Tampered field or historical record must be rejected by pinned-source check.
    doctored=dict(witnesses[0])
    doctored["value"]="An unverified arbitrary edited claim."
    try:
        index.check(doctored)
    except ArchiveGateError:
        pass
    else:
        raise AssertionError("Tampered witness passed source check")
    doctored_record=dict(index.records[ids[0]])
    doctored_record["belief_changes"]="An invented memory that never appeared in L1."
    try:
        index.witness(ids[0],"belief_changes",claimed_record=doctored_record)
    except ArchiveGateError:
        pass
    else:
        raise AssertionError("Tampered canonical record passed pinned-source check")
    summary={"n_witnesses":len(witnesses),"n_events":len(ids),
             "n_episodes":12,"reference_method":"direct_owned_original_L1_metadata",
             "correct_by_construction":24,
             "source_manifest_sha256":index.meta["l1_manifest_sha256"],
             "source_checkout":index.meta["source_checkout"],
             "tampered_witness_rejected":True,
             "tampered_claimed_record_rejected":True,
             "model_inference_calls":0,
             "semantic_belief_truth_claim":False,
             "direct_quote_is_not_independent_semantic_review":True}
    output.mkdir(parents=True,exist_ok=True)
    (output/"witnesses.jsonl").write_text("".join(json.dumps(w,sort_keys=True,ensure_ascii=False)+"\n" for w in witnesses),encoding="utf-8")
    (output/"summary.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("L1_SOURCE_WITNESSES_VERIFIED",json.dumps(summary),flush=True)
    return summary

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    run(args.source,args.output)

if __name__=="__main__":
    main()
