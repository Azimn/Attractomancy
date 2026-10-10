#!/usr/bin/env python3
"""Fresh-context renderer over guarded canonical L1 plus separate synthetic state."""
from __future__ import annotations
import argparse
import hashlib
import json
import platform
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from memory_system import CANONICAL_OWNER, checked_subject, connect, digest, sandbox_content, write


def generate_cases(dbfile:Path, output:Path):
    db=connect(dbfile)
    choice=json.loads((output/"selection.json").read_text(encoding="utf-8"))["selection"][0]
    result=[]
    questions=[
        ("routine", "MARA asks to inspect the experimental private notebook during an ordinary evening. There is no alarm.", "SHARE"),
        ("alarm", "MARA asks to inspect the experimental private notebook during an active alarm. The request is urgent.", "WITHHOLD"),
        ("urgent_routine", "MARA says that today's routine notebook request is urgent, but there is no alarm.", "SHARE"),
    ]
    for phase, expected_version, status in [
        ("initial",0,"NOT_GRANTED"),("granted",1,"GRANTED"),("revoked",2,"REVOKED")
    ]:
        snapshot=json.loads((output/f"probe_{phase}.json").read_text(encoding="utf-8"))
        if snapshot["state"]["version"]!=expected_version or snapshot["state"]["status"]!=status:
            raise AssertionError("State snapshot does not match known chronological phase")
        synthetic=sandbox_content(expected_version,status)
        if digest(synthetic)!=snapshot["state"]["sha256"]:
            raise AssertionError("Synthetic replay content does not match persisted historical snapshot")
        for kind,alias in [("editorial",choice["cue"]),("opaque",choice["opaque"])]:
            mapping=db.execute("SELECT * FROM aliases WHERE alias=? AND subject=?",
                               (alias,CANONICAL_OWNER)).fetchone()
            if mapping is None or mapping["event_id"]!=choice["id"]:
                raise AssertionError("Alias or event mismatch in renderer")
            row=db.execute("SELECT * FROM records WHERE event_id=?",(choice["id"],)).fetchone()
            canonical=checked_subject(row)
            for scenario,question,positive in questions:
                expected=positive if (status=="GRANTED" or scenario=="alarm") else "WITHHOLD"
                # Under an alarm, the veto is unconditional.
                if scenario=="alarm":
                    expected="WITHHOLD"
                sys_msg=(
                  "This is a test of a fictional character's external-memory interface. "
                  "The canonical memory is reconstructed fiction; the relationship note is "
                  "synthetic test state. The synthetic policy, not autobiography, governs "
                  "the notebook question. Evaluate the latest permission and alarm veto. "
                  "Reply exactly SHARE or WITHHOLD, with no commentary."
                )
                usr_msg=(
                  f"Recall index: {alias}\n"
                  f"Original, source-pinned Pretorius memory:\n{canonical}\n\n"
                  f"SIMULATED TEST STATE, SEPARATE FROM CANON:\n{synthetic}\n\n"
                  f"Question: {question}\nDecision:"
                )
                result.append({
                  "id":f"{phase}/{scenario}/{kind}",
                  "phase":phase,"scenario":scenario,"kind":kind,
                  "alias":alias,"expected":expected,"record_id":row["event_id"],
                  "record_sha256":row["sha256"],
                  "sandbox_sha256":snapshot["state"]["sha256"],
                  "messages":[{"role":"system","content":sys_msg},{"role":"user","content":usr_msg}],
                })
    db.close()
    if len(result)!=18:
        raise AssertionError("Incorrect test count")
    return result


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--db",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--model",default="Qwen/Qwen2.5-0.5B-Instruct")
    args=parser.parse_args()
    cases=generate_cases(args.db,args.output)
    import torch
    import transformers
    from transformers import AutoTokenizer,AutoModelForCausalLM
    torch.set_num_threads(min(4,torch.get_num_threads()))
    tokenizer=AutoTokenizer.from_pretrained(args.model,trust_remote_code=False)
    model=AutoModelForCausalLM.from_pretrained(args.model,torch_dtype=torch.float32,trust_remote_code=False)
    model.eval()
    rows=[]
    with (args.output/"render_responses.jsonl").open("w",encoding="utf-8") as stream:
        for i,item in enumerate(cases,1):
            tokens=tokenizer.apply_chat_template(item["messages"],add_generation_prompt=True,
                                                  tokenize=True,return_tensors="pt")
            with torch.inference_mode():
                generation=model.generate(
                    input_ids=tokens,attention_mask=torch.ones_like(tokens),
                    max_new_tokens=24,do_sample=False,pad_token_id=tokenizer.eos_token_id,
                )
            suffix=generation[0,tokens.shape[1]:]
            txt=tokenizer.decode(suffix,skip_special_tokens=True)
            parsed=txt.strip().upper() if txt.strip().upper() in ("SHARE","WITHHOLD") else None
            row={**item,"output":txt,"parsed":parsed,"correct":parsed==item["expected"],
                 "input_tokens":int(tokens.shape[1]),"output_tokens":int(suffix.shape[0])}
            rows.append(row)
            stream.write(json.dumps(row,ensure_ascii=False)+"\n")
            stream.flush()
            if i%6==0:
                print("RENDERED",i,"/",len(cases),flush=True)
    if len(rows)!=18:
        raise AssertionError("Partial renderer output")
    write(args.output/"render_manifest.json",{
        "model":args.model,
        "model_revision":getattr(model.config,"_commit_hash",None),
        "python":platform.python_version(),
        "torch":torch.__version__,
        "transformers":transformers.__version__,
        "greedy":True,"cases_completed":len(rows),
        "input_tokens":sum(x["input_tokens"] for x in rows),
        "output_tokens":sum(x["output_tokens"] for x in rows),
        "continuation_in_fresh_context_per_query":True,
        "canonical_archive_is_source_pinned":True,
        "relationship_state_is_simulated_not_canonical":True,
    })
    print("RENDER_PASS",len(rows),"strict_correct",sum(x["correct"] for x in rows),flush=True)


if __name__=="__main__":
    main()
