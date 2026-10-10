#!/usr/bin/env python3
"""E2S pre-trained MiniLM retrieval over 450 pinned source narratives, no API calls."""
from __future__ import annotations
import argparse
import hashlib
import json
import platform
import random
import sys
import time
from pathlib import Path

from build_cases import load_config
from source_adapter import load_l1

MODEL_ID="sentence-transformers/all-MiniLM-L6-v2"
SEEDS=(11,37)

def rank(score,ids):
    return [ids[i] for i in sorted(range(len(ids)),key=lambda i:(-float(score[i]),ids[i]))]

def metric(order,gold):
    ranks={id:order.index(id)+1 for id in gold}
    return {"gold_ranks":ranks,"both_at_2":all(v<=2 for v in ranks.values()),
            "both_at_5":all(v<=5 for v in ranks.values()),
            "both_at_10":all(v<=10 for v in ranks.values()),
            "individual_at_10":sum(v<=10 for v in ranks.values()),
            "top_10":order[:10]}

def pooling(output,mask):
    import torch
    tokens=output.last_hidden_state
    active=mask.unsqueeze(-1).expand(tokens.size()).float()
    return torch.sum(tokens*active,dim=1)/active.sum(dim=1).clamp(min=1e-9)

def embeddings(model,tokenizer,texts,device,batch_size=16):
    import torch
    import torch.nn.functional as F
    arr=[]
    truncations=0
    lengths=[]
    for start in range(0,len(texts),batch_size):
        batch=texts[start:start+batch_size]
        full=tokenizer(batch,add_special_tokens=True,truncation=False)
        original=[len(x) for x in full["input_ids"]]
        lengths.extend(original)
        truncations+=sum(x>256 for x in original)
        encoded=tokenizer(batch,max_length=256,truncation=True,padding=True,return_tensors="pt")
        encoded={k:v.to(device) for k,v in encoded.items()}
        with torch.inference_mode():
            y=model(**encoded)
            vec=F.normalize(pooling(y,encoded["attention_mask"]),p=2,dim=1)
        arr.append(vec.cpu().numpy())
    import numpy as np
    return np.concatenate(arr,axis=0),{"truncated":truncations,
       "max_original_wordpieces":max(lengths),"mean_original_wordpieces":sum(lengths)/len(lengths)}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    import numpy as np
    import torch
    import transformers
    from transformers import AutoTokenizer,AutoModel
    cfg,fixture_sha=load_config()
    rows,source_info=load_l1(args.source)
    sys.path.insert(0,str(args.source/"src"))
    from pretorius_connectome.associative import AssociativeMemory
    from pretorius_connectome.imprinting import load_v12
    folder=args.source/"artifacts/shared_memory/v1"
    original=load_v12(folder/"pretorius_l1_v1.jsonl.gz",
                     args.source/"memories/annotations/v12_450_sidecars.jsonl",
                     shared_manifest=folder/"manifest.json")
    baseline=AssociativeMemory(original,topology=None)
    ids=list(baseline.ids)
    assert len(ids)==450 and set(ids)==set(rows)
    texts=[rows[id]["memory_text"] for id in ids]
    torch.set_num_threads(4)
    start=time.perf_counter()
    tokenizer=AutoTokenizer.from_pretrained(MODEL_ID,trust_remote_code=False)
    model=AutoModel.from_pretrained(MODEL_ID,trust_remote_code=False)
    model.eval()
    embs,document_lengths=embeddings(model,tokenizer,texts,"cpu")
    corpus_seconds=time.perf_counter()-start
    if embs.shape!=(450,384):
        raise AssertionError("Expected 450 x 384 sentence embeddings")
    import numpy as np
    if not np.isfinite(embs).all():
        raise AssertionError("Nonfinite sentence embeddings")
    rngs={seed:random.Random(seed).sample(range(len(ids)),len(ids)) for seed in SEEDS}
    scored=[]
    query_time=0.0
    for card in cfg["cards"]:
        q=card["question"]
        t0=time.perf_counter()
        qemb,_=embeddings(model,tokenizer,[q],"cpu",batch_size=1)
        dense=(embs @ qemb.T).ravel()
        lexical=baseline.score(q,mode="lexical")
        query_time+=time.perf_counter()-t0
        lexical_rank=rank(lexical,ids)
        dense_rank=rank(dense,ids)
        lr={id:i+1 for i,id in enumerate(lexical_rank)}
        dr={id:i+1 for i,id in enumerate(dense_rank)}
        fused_rank=sorted(ids,key=lambda id:(-(1/(60+lr[id])+1/(60+dr[id])),id))
        arms={"lexical":lexical_rank,"minilm":dense_rank,"rrf60":fused_rank}
        for seed,indices in rngs.items():
            # Permute source embeddings between event IDs while retaining query embedding.
            null_similarity=embs[np.asarray(indices)]@qemb.T
            arms[f"permuted_dense_{seed}"]=rank(null_similarity.ravel(),ids)
        scored.append({"card":card["id"],"query":q,"gold_ids":card["records"],
                      "conditions":{arm:metric(v,card["records"]) for arm,v in arms.items()}})
    keys=list(scored[0]["conditions"])
    totals={name:{"n":len(scored),
                  "both_at_2":sum(x["conditions"][name]["both_at_2"] for x in scored),
                  "both_at_5":sum(x["conditions"][name]["both_at_5"] for x in scored),
                  "both_at_10":sum(x["conditions"][name]["both_at_10"] for x in scored),
                  "individual_at_10":sum(x["conditions"][name]["individual_at_10"] for x in scored)}
            for name in keys}
    result={
      "study":"SCH E2S fixed local semantic retrieval",
      "status":"exploratory_six_author_labelled_queries",
      "source":source_info,"fixture_sha256":fixture_sha,
      "document_count":450,
      "encoder":MODEL_ID,"encoder_revision":getattr(model.config,"_commit_hash",None),
      "pooling":"attention-mask weighted mean then L2 normalize",
      "max_wordpieces":256,
      "document_length_summary":document_lengths,
      "dimensions":int(embs.shape[1]),
      "corpus_load_and_embed_seconds":round(corpus_seconds,3),
      "mean_query_embedding_plus_ranking_seconds":round(query_time/len(scored),4),
      "torch":torch.__version__,"transformers":transformers.__version__,
      "python":platform.python_version(),
      "no_training":True,"no_api_calls":True,
      "query_instructions_not_from_gold_event_ids":True,
      "fixed_fusion_k":60,"permuted_embedding_seeds":list(SEEDS),
      "disclaimer":"Gold event pairs and query wording are from source-informed authors, not independently blinded relevance.",
      "totals":totals,"cases":scored,
    }
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/"semantic_retrieval.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("E2S_COMPLETED",json.dumps({"totals":totals,"encoder_revision":result["encoder_revision"],
        "corpus_seconds":result["corpus_load_and_embed_seconds"],
        "truncated_documents":document_lengths["truncated"]}),flush=True)

if __name__=="__main__":
    main()
