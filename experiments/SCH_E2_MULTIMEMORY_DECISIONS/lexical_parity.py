#!/usr/bin/env python3
"""Cross-run lexical-rank discrepancy audit; same source, query, and runtime stages."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import platform
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
from build_cases import load_config
from source_adapter import load_l1

def rank(scores,ids):
    return [ids[i] for i in sorted(range(len(ids)),key=lambda i:(-float(scores[i]),ids[i]))]

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--archive",type=Path,default=HERE/"results")
    opts=p.parse_args()
    import numpy as np
    import scipy
    import sklearn
    # Critical experimental intervention: evaluate the *source-only* lexical ranker
    # BEFORE importing PyTorch / Transformers, which prior lexical runs never imported.
    sys.path.insert(0,str(opts.source/"src"))
    from pretorius_connectome.associative import AssociativeMemory
    from pretorius_connectome.imprinting import load_v12
    cfg,cfg_sha=load_config()
    source,meta=load_l1(opts.source)
    folder=opts.source/"artifacts/shared_memory/v1"
    memories=load_v12(folder/"pretorius_l1_v1.jsonl.gz",
                    opts.source/"memories/annotations/v12_450_sidecars.jsonl",
                    shared_manifest=folder/"manifest.json")
    lexical=AssociativeMemory(memories,topology=None)
    ids=lexical.ids
    questions=[x["question"] for x in cfg["cards"]]
    stage={}
    def run_stage(name):
        ranklist=[]
        vectors=[]
        for q in questions:
            v=np.asarray(lexical.score(q,mode="lexical"),dtype=np.float64)
            ranklist.append(rank(v,ids)[:10])
            vectors.append(v)
        stage[name]={"top10":ranklist,
                     "score_sha256":[hashlib.sha256(v.astype("<f8",copy=False).tobytes()).hexdigest() for v in vectors]}
        return vectors
    original=run_stage("source_only_before_torch")
    import torch
    import transformers
    from transformers import AutoTokenizer,AutoModel
    after_torch=run_stage("after_torch_import")
    torch.set_num_threads(4)
    multithread=run_stage("torch_set_4_threads")
    # Loading the model changes only process runtime, not retrieval algorithm.
    tokenizer=AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2",trust_remote_code=False)
    model=AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2",trust_remote_code=False)
    model.eval()
    after_model=run_stage("after_minilm_model_load")
    # Reproduce E2S's full encoder forward pass before its lexical scoring.
    from semantic_retrieval import embeddings
    vectors, docinfo=embeddings(model,tokenizer,[source[event_id]["memory_text"] for event_id in ids],"cpu")
    after_forward=run_stage("after_full_minilm_forward")
    refpaths={
      "e2r":opts.archive/"retrieval-run-38023843107/retrieval_diagnostic.json",
      "e2g":opts.archive/"graph-run-38024055089/graph_retrieval.json",
      "e2s":opts.archive/"semantic-run-38024250049/semantic_retrieval.json",
    }
    refs={name:json.loads(path.read_text(encoding="utf-8")) for name,path in refpaths.items()}
    assert len(set([refs["e2r"]["fixture_sha256"],refs["e2g"]["fixture_sha256"],refs["e2s"]["fixture_sha256"],cfg_sha]))==1
    assert len(set([refs["e2r"]["source_provenance"]["l1_manifest_sha256"],
                    refs["e2g"]["source"]["l1_manifest_sha256"],
                    refs["e2s"]["source"]["l1_manifest_sha256"],
                    meta["l1_manifest_sha256"]]))==1
    previous={
      "e2r":[row["queries"][0]["top_10"] for row in refs["e2r"]["cases"]],
      "e2g":[row["conditions"]["lexical"]["top10"] for row in refs["e2g"]["cases"]],
      "e2s":[row["conditions"]["lexical"]["top_10"] for row in refs["e2s"]["cases"]],
    }
    allcomparison={}
    for name,section in stage.items():
        allcomparison[name]={
            "same_order_as":{k:sum(section["top10"][i]==rows[i] for i in range(6))
                             for k,rows in previous.items()},
            "top10_overlap_e2r":[len(set(section["top10"][i])&set(previous["e2r"][i]))
                                  for i in range(6)],
        }
    diff={
        name:{"max_abs_difference":max(float(np.max(np.abs(left-right))) for left,right in zip(original,stagevec)),
              "total_queries_with_any_score_difference":sum(bool(np.any(left!=right)) for left,right in zip(original,stagevec))}
        for name,stagevec in [("after_torch_import",after_torch),("torch_set_4_threads",multithread),("after_minilm_model_load",after_model),("after_full_minilm_forward",after_forward)]
    }
    result={
      "study":"E2 lexical baseline stability audit",
      "same_frozen_source":True,"same_frozen_query_fixture":True,
      "source":meta,"fixture_sha256":cfg_sha,
      "python":platform.python_version(),"numpy":np.__version__,
      "scipy":scipy.__version__,"sklearn":sklearn.__version__,
      "torch":torch.__version__,"transformers":transformers.__version__,
      "encoder_revision":getattr(model.config,"_commit_hash",None),
      "encoder_document_count":int(vectors.shape[0]),
      "encoder_truncated_documents":docinfo["truncated"],
      "OMP_NUM_THREADS":os.environ.get("OMP_NUM_THREADS"),
      "OPENBLAS_NUM_THREADS":os.environ.get("OPENBLAS_NUM_THREADS"),
      "MKL_NUM_THREADS":os.environ.get("MKL_NUM_THREADS"),
      "historical_crossrun_exact_top10":{
          k:{j:sum(previous[k][i]==previous[j][i] for i in range(6))
             for j in previous} for k in previous
      },
      "score_stage_differences":diff,
      "stage_vs_original":allcomparison,
      "stage_score_digest":{k:v["score_sha256"] for k,v in stage.items()},
      "stage_top10":{k:v["top10"] for k,v in stage.items()},
      "caveat":"A detected tie/rank difference is not a verified numerical root cause unless the score-stage audit isolates it.",
    }
    opts.output.mkdir(parents=True,exist_ok=True)
    (opts.output/"parity_audit.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("E2_PARITY_AUDIT",json.dumps({"historical":result["historical_crossrun_exact_top10"],
          "score_differences":diff,"comparison":allcomparison}),flush=True)

if __name__=="__main__":
    main()
