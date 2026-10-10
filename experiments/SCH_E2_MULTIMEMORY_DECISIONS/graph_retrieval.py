#!/usr/bin/env python3
"""E2G source-owned L1 association graph diffusion; nonneural, no LLM calls."""
from __future__ import annotations
import argparse
import json
import random
import sys
from pathlib import Path

from build_cases import load_config
from source_adapter import load_l1

SEEDS=(11,19,37)
RESTART=0.75
STEPS=3

def load_retriever(source):
    sys.path.insert(0,str(source/"src"))
    from pretorius_connectome.associative import AssociativeMemory
    from pretorius_connectome.imprinting import load_v12
    artifact=source/"artifacts/shared_memory/v1"
    memories=load_v12(artifact/"pretorius_l1_v1.jsonl.gz",
                     source/"memories/annotations/v12_450_sidecars.jsonl",
                     shared_manifest=artifact/"manifest.json")
    return AssociativeMemory(memories,topology=None)

def adjacency(records,ids,seed=None):
    import numpy as np
    from scipy import sparse
    positions={id:i for i,id in enumerate(ids)}
    if set(positions)!=set(records):
        raise ValueError("Retrieval and L1 event IDs do not match")
    rng=random.Random(seed)
    n=len(ids)
    pairs=set()
    source_edges=0
    for id in ids:
        row=records[id]
        neighbors=row.get("links_to_prior_events") or []
        source_edges+=len(neighbors)
        for neighbor in neighbors:
            if neighbor not in positions:
                raise ValueError("Unrecognized source association event ID")
            to=positions[neighbor]
            if seed is not None:
                candidates=[i for i in range(n) if i!=positions[id]]
                to=rng.choice(candidates)
            a,b=sorted((positions[id],to))
            if a!=b: pairs.add((a,b))
    xs,ys=[],[]
    for a,b in pairs:
        xs.extend((a,b));ys.extend((b,a))
    xs.extend(range(n));ys.extend(range(n))
    weights=np.ones(len(xs),dtype=np.float64)
    graph=sparse.coo_matrix((weights,(xs,ys)),shape=(n,n)).tocsr()
    graph.sum_duplicates()
    deg=np.asarray(graph.sum(axis=1)).ravel()
    normalized=(sparse.diags(1.0/deg) @ graph).tocsr()
    return normalized,{"source_directed_links":source_edges,
                       "undirected_unique_links":len(pairs),
                       "shuffled_seed":seed,
                       "node_count":n}

def rank(scores,ids):
    return [ids[i] for i in sorted(range(len(ids)),key=lambda i:(-float(scores[i]),ids[i]))]

def diffuse(x,P):
    import numpy as np
    scores=np.asarray(x,dtype=np.float64).reshape(-1)
    if np.min(scores)<0: raise ValueError("Negative retrieval score")
    peak=float(np.max(scores))
    if peak>0: scores=scores/peak
    z=scores.copy()
    for _ in range(STEPS):
        z=RESTART*scores+(1-RESTART)*P.transpose().dot(z)
    return z

def metrics(ranking,gold):
    loc={id:i+1 for i,id in enumerate(ranking)}
    ranks={id:loc[id] for id in gold}
    return {"gold_ranks":ranks,
            "both_at_2":all(ranks[id]<=2 for id in gold),
            "both_at_5":all(ranks[id]<=5 for id in gold),
            "both_at_10":all(ranks[id]<=10 for id in gold),
            "gold_hits_at_10":sum(ranks[id]<=10 for id in gold),
            "top10":ranking[:10]}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    import numpy as np
    cfg,fixture_sha=load_config()
    rows,manifest=load_l1(args.source)
    lexical=load_retriever(args.source)
    ids=lexical.ids
    real,real_meta=adjacency(rows,ids)
    nulls={}
    for seed in SEEDS:
        nulls[seed]=adjacency(rows,ids,seed=seed)
    comparisons=[]
    for card in cfg["cards"]:
        query=card["question"]
        gold=card["records"]
        lexical_score=lexical.score(query,mode="lexical")
        ranking={"lexical":rank(lexical_score,ids),
                 "source_link_diffusion":rank(diffuse(lexical_score,real),ids)}
        for seed,(graph,meta) in nulls.items():
            ranking[f"shuffled_links_seed{seed}"]=rank(diffuse(lexical_score,graph),ids)
        comparisons.append({"card":card["id"],"query":query,"gold":gold,
                            "conditions":{mode:metrics(ranklist,gold)
                                          for mode,ranklist in ranking.items()}})
    arms=list(comparisons[0]["conditions"])
    summary={}
    for arm in arms:
        xs=[case["conditions"][arm] for case in comparisons]
        summary[arm]={"n":len(xs),
                      "both_at_2":sum(v["both_at_2"] for v in xs),
                      "both_at_5":sum(v["both_at_5"] for v in xs),
                      "both_at_10":sum(v["both_at_10"] for v in xs),
                      "individual_gold_hits_at_10":sum(v["gold_hits_at_10"] for v in xs)}
    result={
       "study":"E2G source association graph candidate recall",
       "status":"exploratory_authored_source_links_not_biological",
       "source":manifest,
       "fixture_sha256":fixture_sha,
       "lexical_engine":"source-owned AssociativeMemory lexical word+bigram TF-IDF",
       "association_field":"source-owned links_to_prior_events",
       "original_graph":real_meta,
       "null_graphs":{str(seed):meta for seed,(_,meta) in nulls.items()},
       "restart_weight":RESTART,"diffusion_steps":STEPS,
       "candidate_budgets":[2,5,10],
       "scored_queries":len(comparisons),
       "no_gold_labels_used_in_ranking":True,
       "no_neural_connectome_transplant":True,
       "no_model_generations":True,
       "limitations":"Gold pairs and links are author-produced on the same corpus; shuffled links preserve only per-source edge count.",
       "totals":summary,"cases":comparisons,
    }
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/"graph_retrieval.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("E2G_COMPLETE",json.dumps(summary),flush=True)

if __name__=="__main__":
    main()
