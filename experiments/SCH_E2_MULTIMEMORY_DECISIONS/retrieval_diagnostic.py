#!/usr/bin/env python3
"""E2R: existing source-owned lexical retriever over all 450 L1 memories."""
from __future__ import annotations
import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
from build_cases import load_config
from source_adapter import load_l1

def read_models(source):
    sys.path.insert(0,str(source/"src"))
    from pretorius_connectome.associative import AssociativeMemory
    from pretorius_connectome.imprinting import load_v12
    archive=source/"artifacts/shared_memory/v1"
    sidecars=source/"memories/annotations/v12_450_sidecars.jsonl"
    memories=load_v12(
        archive/"pretorius_l1_v1.jsonl.gz",
        sidecars,
        shared_manifest=archive/"manifest.json")
    return AssociativeMemory(memories,topology=None)

def run(source,outdir):
    cfg,cfg_sha=load_config()
    records,provenance=load_l1(source)
    retriever=read_models(source)
    if len(retriever.memories)!=450:
        raise AssertionError("Unexpected source collection")
    report=[]
    for card in cfg["cards"]:
        gold=card["records"]
        assert all(x in records for x in gold)
        cues=[str(records[x]["recall_cues"][0]) for x in gold]
        titles=[str(records[x]["title"]) for x in gold]
        queries={
            "ordinary_dilemma":card["question"],
            "oracle_editorial_cues":" ".join(cues),
            "oracle_source_titles":" ".join(titles),
        }
        sub=[]
        for name,query in queries.items():
            ranked=retriever.rank(query,mode="lexical",top_k=20)
            first=[x["event_id"] for x in ranked]
            positions={id:(first.index(id)+1 if id in first else None) for id in gold}
            sub.append({
                "query_kind":name,"query":query,
                "top_5":first[:5],
                "top_10":first[:10],
                "gold_event_ids":gold,
                "gold_ranks_top20":positions,
                "both_in_top2":all(v is not None and v<=2 for v in positions.values()),
                "both_in_top5":all(v is not None and v<=5 for v in positions.values()),
                "both_in_top10":all(v is not None and v<=10 for v in positions.values()),
                "either_in_top10":any(v is not None and v<=10 for v in positions.values()),
                "hits_at_10":sum(v is not None and v<=10 for v in positions.values()),
            })
        report.append({"card":card["id"],"gold":gold,"queries":sub})
    totals={}
    for kind in ("ordinary_dilemma","oracle_editorial_cues","oracle_source_titles"):
        q=[v for row in report for v in row["queries"] if v["query_kind"]==kind]
        totals[kind]={
            "queries":len(q),
            "both_at_2":sum(x["both_in_top2"] for x in q),
            "both_at_5":sum(x["both_in_top5"] for x in q),
            "both_at_10":sum(x["both_in_top10"] for x in q),
            "either_at_10":sum(x["either_in_top10"] for x in q),
            "total_gold_events_at_10":sum(x["hits_at_10"] for x in q),
        }
    obj={
        "status":"exploratory_retrieval_diagnostic_not_blinded",
        "source_owner":"Azimn/Pretorius-Connectome",
        "source_provenance":provenance,
        "fixture_sha256":cfg_sha,
        "retrieval_engine":"pretorius_connectome.associative.AssociativeMemory lexical word+bigram TF-IDF",
        "mode":"lexical",
        "source_record_count":450,
        "evaluation_card_count":len(cfg["cards"]),
        "metric":"Recall of both selected source events in top-k ranked source memories",
        "source_cue_quality":"unreviewed candidate recall cues",
        "query_scope":"Editorial cue and title conditions receive privileged access to gold-record metadata; they are not information-matched to a natural dilemma query.",
        "fitting":"TF-IDF fit on all 450 narrative texts with no evaluation answer label features; not held-out-corpus estimation.",
        "totals":totals,"cases":report,
        "no_model_generations":True,
        "no_canonical_l1_changes":True,
    }
    outdir.mkdir(parents=True,exist_ok=True)
    (outdir/"retrieval_diagnostic.json").write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("E2R_COMPLETE",json.dumps(totals),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    run(args.source,args.output)

if __name__=="__main__":
    main()
