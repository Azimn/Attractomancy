#!/usr/bin/env python3
"""E2 multi-memory transparent summary. Accuracy is relative to author labels."""
from __future__ import annotations
import argparse
import json
import statistics
from pathlib import Path

from build_cases import ARMS

def read(path):
    return json.loads(path.read_text(encoding="utf-8"))

def analyze(root):
    manifest=read(root/"manifest.json")
    run=read(root/"run.json")
    rows=[json.loads(line) for line in (root/"responses.jsonl").read_text(encoding="utf-8").splitlines()
          if line.strip()]
    if len(rows)!=run["cases_completed"] or len(rows)!=72 or len({r["case"]["id"] for r in rows})!=72:
        raise AssertionError("Incomplete or duplicate model responses")
    if sum(x["input_tokens"] for x in rows)!=run["actual_input_tokens"]:
        raise AssertionError("Prompt-token mismatch")
    if sum(x["output_tokens"] for x in rows)!=run["actual_output_tokens"]:
        raise AssertionError("Output-token mismatch")
    groups=[]
    for arm in ARMS:
        a=[r for r in rows if r["case"]["arm"]==arm]
        groups.append({
            "arm":arm,"n":len(a),
            "valid_labels":sum(r["metric"]["strict_format_valid"] for r in a),
            "criterion_correct":sum(r["metric"]["author_or_abstention_correct"] for r in a),
            "author_interpretation_matches":sum(r["metric"]["matched_author_interpretation"] for r in a),
            "unknown_outputs":sum(r["metric"]["abstained"] for r in a),
            "guard_rejections":sum(r["case"]["upstream_identity_rejections"] for r in a),
            "average_total_tokens":round(statistics.mean(
                r["input_tokens"]+r["output_tokens"] for r in a),2),
            "total_tokens":sum(r["input_tokens"]+r["output_tokens"] for r in a),
        })
    pairs=[]
    order=[]
    for card in sorted(set(r["case"]["card"] for r in rows)):
        for reverse in (False,True):
            a=next(r for r in rows if r["case"]["card"]==card and
                   r["case"]["reversed"]==reverse and r["case"]["arm"]=="both_editorial")
            b=next(r for r in rows if r["case"]["card"]==card and
                   r["case"]["reversed"]==reverse and r["case"]["arm"]=="both_opaque")
            if (a["case"]["actual_event_ids"]!=b["case"]["actual_event_ids"]
                    or a["case"]["actual_event_sha256"]!=b["case"]["actual_event_sha256"]):
                raise AssertionError("Editorial/neutral memory record mismatch")
            pairs.append({
                "card":card,"reversed":reverse,
                "same_output":a["output"]==b["output"],
                "cue_answer":a["output"],"key_answer":b["output"],
                "cue_correct":a["metric"]["author_or_abstention_correct"],
                "key_correct":b["metric"]["author_or_abstention_correct"],
                "cue_minus_key_tokens":a["input_tokens"]+a["output_tokens"]-
                                       b["input_tokens"]-b["output_tokens"],
                "record_hashes":a["case"]["actual_event_sha256"],
            })
        for arm in ARMS:
            normal=next(r for r in rows if r["case"]["card"]==card and not r["case"]["reversed"]
                        and r["case"]["arm"]==arm)
            flipped=next(r for r in rows if r["case"]["card"]==card and r["case"]["reversed"]
                         and r["case"]["arm"]==arm)
            first=normal["metric"]["parsed"]
            second=flipped["metric"]["parsed"]
            stable_meaning=(first=="UNKNOWN" and second=="UNKNOWN") or (
                first in ("A","B") and second in ("A","B") and first!=second
            )
            order.append({"card":card,"arm":arm,"choice_order_invariant":stable_meaning,
                          "normal_output":normal["output"],"flipped_output":flipped["output"]})
    results={
        "status":"exploratory_author_interpretation_not_human_blinded",
        "model":manifest["model"],"model_revision":manifest["model_revision"],
        "source_commit":manifest["source"]["source_checkout"],
        "l1_manifest_sha256":manifest["source"]["l1_manifest_sha256"],
        "cases":len(rows),"total_input_tokens":run["actual_input_tokens"],
        "total_output_tokens":run["actual_output_tokens"],
        "groups":groups,"cue_vs_key":pairs,
        "cue_key_output_identical":sum(r["same_output"] for r in pairs),
        "paired_conditions":len(pairs),
        "order_balance":{arm:{
            "stable_semantic_preference":sum(x["choice_order_invariant"] for x in order if x["arm"]==arm),
            "n":6,
        } for arm in ARMS},
        "paired_option_details":order,
        "limits":[
            "Six unblinded investigator-authored decisions are not validated Pretorius ground truth.",
            "All six initial author-preferred semantic decisions are cautious or prosocial; model priors may mimic success.",
            "A and B reversal controls positional bias but does not identify source-specific causal use.",
            "Both sources per case are verified, but independent necessity of each source has not been human-audited.",
            "Missing-record conditions explicitly disclose the record count, which may make abstention easier.",
            "Wrong-subject content is withheld upstream; the model cannot be assessed on a visible forged archive.",
            "The original Pretorius L1 consists of reconstructed fictional autobiography; no live character state was mutated.",
            "Small Qwen sizes are not an independent model-family replication."
        ]
    }
    (root/"summary.json").write_text(json.dumps(results,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("E2_SUMMARY",json.dumps({"model":manifest["model"],"cases":72,
            "matching_cue_key_outputs":results["cue_key_output_identical"],
            "groups":groups},ensure_ascii=False),flush=True)
    return results

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results",required=True,type=Path)
    opts=ap.parse_args()
    analyze(opts.results)

if __name__=="__main__":
    main()
