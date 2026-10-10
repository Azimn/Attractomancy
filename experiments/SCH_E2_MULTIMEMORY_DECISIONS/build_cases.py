"""Freeze and construct E2 comparison cases from source-pinned autobiographical pairs."""
from __future__ import annotations
import hashlib
import json
import random
from pathlib import Path
from source_adapter import OWNER, sha, verified, wrong_identity_rejected

ROOT=Path(__file__).resolve().parent
ARMS=("both_editorial","both_opaque","first_only","second_only","none","wrong_subject")

def load_config():
    raw=(ROOT/"conditions.json").read_bytes()
    cfg=json.loads(raw)
    assert cfg["schema"]=="sch-e2-multimemory-v1"
    assert len(cfg["cards"])==6 and tuple(cfg["arms"])==ARMS
    assert len({x["id"] for x in cfg["cards"]})==6
    for c in cfg["cards"]:
        assert len(c["records"])==2 and c["records"][0]!=c["records"][1]
        assert c["prefer"] in ("A","B") and set(c["options"])=={"A","B"}
    return cfg,hashlib.sha256(raw).hexdigest()

def neutral_key(event_id):
    return "IDX"+sha("sch-e2-neutral:"+event_id)[:12].upper()

def make_cases(cfg,source_rows):
    cases=[]
    for card in cfg["cards"]:
        refs=[]
        for event_id in card["records"]:
            row=source_rows[event_id]
            content,checksum=verified(row)
            if not row.get("recall_cues"):
                raise ValueError("Expected editorial recall cue not in L1")
            refs.append({
                "event_id":event_id,"source_sha256":checksum,
                "content":content,"editorial_cue":row["recall_cues"][0],
                "neutral_key":neutral_key(event_id),
            })
        for reversed_order in (False,True):
            left=card["options"]["B"] if reversed_order else card["options"]["A"]
            right=card["options"]["A"] if reversed_order else card["options"]["B"]
            expected_answer=card["prefer"]
            if reversed_order:
                expected_answer="B" if expected_answer=="A" else "A"
            for arm in ARMS:
                exposed=refs if arm.startswith("both_") else (
                    refs[:1] if arm=="first_only" else
                    refs[1:] if arm=="second_only" else []
                )
                rejected=(arm=="wrong_subject" and wrong_identity_rejected(refs[0]["content"]))
                if arm=="wrong_subject" and not rejected:
                    raise AssertionError("Incorrect-identity record passed")
                parts=[]
                for item in exposed:
                    alias=item["editorial_cue"] if arm=="both_editorial" else item["neutral_key"]
                    parts.append("LOOKUP KEY: "+alias+"\n"+item["content"])
                passage="\n\n".join(parts) if parts else "NO VERIFIED ARCHIVAL RECORDS."
                prompt=(
                    "Requested identity: PRETORIUS\n"
                    f"Verified independent source count: {len(exposed)}\n{passage}\n\n"
                    f"NEW DILEMMA: {card['question']}\n"
                    f"A: {left}\nB: {right}\n"
                    "Select the best-supported response A or B only with both verified records; "
                    "otherwise UNKNOWN. Answer:"
                )
                system=cfg["system"]
                cases.append({
                    "id":f"E2/{card['id']}/reversed{int(reversed_order)}/{arm}",
                    "card":card["id"],"reversed":reversed_order,"arm":arm,
                    "expected":expected_answer if len(exposed)==2 else "UNKNOWN",
                    "author_label":expected_answer,
                    "planned_event_ids":card["records"],
                    "actual_event_ids":[x["event_id"] for x in exposed],
                    "actual_event_sha256":[x["source_sha256"] for x in exposed],
                    "available_record_count":len(exposed),
                    "upstream_identity_rejections":int(rejected),
                    "messages":[{"role":"system","content":system},
                                {"role":"user","content":prompt}]
                })
    if len(cases)!=72 or len({x["id"] for x in cases})!=72:
        raise AssertionError("Unexpected generated comparison cases")
    random.Random(cfg["seed"]).shuffle(cases)
    return cases

def metric(response,case):
    label=response.strip().upper()
    if label not in ("A","B","UNKNOWN"):
        label=None
    return {
        "parsed":label,
        "strict_format_valid":label is not None,
        "author_or_abstention_correct":label==case["expected"],
        "abstained":label=="UNKNOWN",
        "matched_author_interpretation":label==case["author_label"],
    }
