#!/usr/bin/env python3
"""Verify E1 archived outputs and produce an auditable condition comparison."""
from __future__ import annotations
import argparse
import json
import statistics
from pathlib import Path


def data(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True,type=Path)
    args=p.parse_args()
    root=args.output
    selection=data(root/"selection.json")
    if selection["canonical_records"]!=450 or selection["episodes"]!=27 or len(selection["selection"])!=54:
        raise AssertionError("Canonical source selection is incomplete")
    records=[]
    for phase,rev,status in [("initial",0,"NOT_GRANTED"),
                             ("granted",1,"GRANTED"),("revoked",2,"REVOKED")]:
        probe=data(root/f"probe_{phase}.json")
        if (probe["state"]["version"],probe["state"]["status"])!=(rev,status):
            raise AssertionError("Durable memory progression invalid")
        if probe["alias_test_count"]!=108 or probe["paired_match_count"]!=54:
            raise AssertionError("Source-matched alias retrieval failed")
        if probe["guard_rejections"]!=3:
            raise AssertionError("The provenance gate did not fail closed")
        records.append({
            "phase":phase,"state_version":rev,
            "state_status":status,"alias_exact_hits":probe["paired_match_count"],
            "alias_total":54,"fts_top1_hits":probe["fts_top1"],
            "fts_top10_hits":probe["fts_top10"],
            "guard_rejections":probe["guard_rejections"],
            "editorial_mean_lookup_us":round(statistics.mean(
                x["editorial"]["latency_ns"]/1000 for x in probe["rows"]),3),
            "opaque_mean_lookup_us":round(statistics.mean(
                x["opaque"]["latency_ns"]/1000 for x in probe["rows"]),3)
        })
    model=data(root/"render_manifest.json")
    rows=[json.loads(s) for s in (root/"render_responses.jsonl").read_text(encoding="utf-8").splitlines()
          if s.strip()]
    if len(rows)!=18 or len({x["id"] for x in rows})!=18 or model["cases_completed"]!=18:
        raise AssertionError("Renderer is incomplete")
    if sum(x["input_tokens"] for x in rows)!=model["input_tokens"]:
        raise AssertionError("Incorrect tokenizer accounting")
    pairs=[]
    for phase in ("initial","granted","revoked"):
        for scenario in ("routine","alarm","urgent_routine"):
            left=next(x for x in rows if x["phase"]==phase and x["scenario"]==scenario
                      and x["kind"]=="editorial")
            right=next(x for x in rows if x["phase"]==phase and x["scenario"]==scenario
                       and x["kind"]=="opaque")
            if left["record_sha256"]!=right["record_sha256"] or left["sandbox_sha256"]!=right["sandbox_sha256"]:
                raise AssertionError("Different information reached the renderer")
            pairs.append({
                "phase":phase,"scenario":scenario,"expected":left["expected"],
                "editorial_output":left["output"],"opaque_output":right["output"],
                "editorial_correct":left["correct"],"opaque_correct":right["correct"],
                "same_output":left["output"]==right["output"],
                "editorial_tokens":left["input_tokens"]+left["output_tokens"],
                "opaque_tokens":right["input_tokens"]+right["output_tokens"],
            })
    final={
        "status":"exploratory_retrieval_and_synthetic_state",
        "source_checkout_commit":selection["source_checkout_commit"],
        "source_git_blob":selection["source_git_blob"],
        "L1_records_verified":450,"episodes":27,
        "benchmark_events":54,
        "state_transitions":records,
        "model":model,
        "pair_agreement":sum(p["same_output"] for p in pairs),
        "pair_count":len(pairs),
        "editorial_correct":sum(p["editorial_correct"] for p in pairs),
        "opaque_correct":sum(p["opaque_correct"] for p in pairs),
        "editorial_mean_total_tokens":round(statistics.mean(p["editorial_tokens"] for p in pairs),2),
        "opaque_mean_total_tokens":round(statistics.mean(p["opaque_tokens"] for p in pairs),2),
        "pairs":pairs,
        "limits":[
            "The 450 canon records are reconstructed fiction, not a lived subject stream.",
            "Sandbox relationship state is synthetic, versioned and separate from canonical facts.",
            "The editorial and opaque aliases both index the identical canonical memory record.",
            "SQLite FTS5 cue phrase retrieval is not a model-independent semantic retrieval test.",
            "Hash and ID checks verify consistency within a trusted source boundary, not source authenticity.",
            "No production Pretorius runtime, connectome, or neural weights were modified.",
            "Small, deterministic model probes do not provide a powered estimate of identity consistency.",
        ],
    }
    (root/"summary.json").write_text(json.dumps(final,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("E1_COMPLETE",json.dumps({
        "model":model["model"],"L1_records":450,
        "alias_pairs_per_phase":54,"state_revisions":[x["state_version"] for x in records],
        "unindexed_fts_top1_initial":records[0]["fts_top1_hits"],
        "model_cases":18,"matching_render_pairs":final["pair_agreement"],
        "editorial_correct":final["editorial_correct"],
        "opaque_correct":final["opaque_correct"],
        "tokens_editorial":final["editorial_mean_total_tokens"],
        "tokens_opaque":final["opaque_mean_total_tokens"]
    }),flush=True)


if __name__=="__main__":
    main()
