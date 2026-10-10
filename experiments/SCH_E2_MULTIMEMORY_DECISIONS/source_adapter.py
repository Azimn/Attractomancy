"""E2 source-owned Pretorius L1 access and deterministic record identity validation."""
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/"SCH_D1_EXTERNAL_RECONSTRUCTION"))
from archive_guard import ArchiveGateError, seal_record, verified_content

OWNER="PRETORIUS"
SOURCE="pretorius_l1_pinned"
SOURCE_COMMIT="6d2768211f5c2184c8bbdb833c06e169b5137197"

def sha(value: str)->str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()

def load_l1(source:Path):
    sys.path.insert(0,str(source/"src"))
    from pretorius_connectome.shared_memory import read_l1
    folder=source/"artifacts/shared_memory/v1"
    raw=(folder/"manifest.json").read_bytes()
    meta=json.loads(raw)
    rows=read_l1(folder/"pretorius_l1_v1.jsonl.gz",folder/"manifest.json")
    assert len(rows)==450 and meta["records"]==450
    assert meta["source_commit_pin"]=="597fb23473a60eecf2e1b50f79c22bfbea816be5"
    return {r["event_id"]:r for r in rows},{
      "source_checkout":SOURCE_COMMIT,
      "source_git_blob":meta["source_git_blob"],
      "l1_manifest_sha256":hashlib.sha256(raw).hexdigest(),
      "record_count":len(rows),
    }

def verified(record):
    if record["provenance"]!="reconstructed":
        raise ArchiveGateError("Non-reconstructed row in frozen L1")
    content="\n".join((
      "IDENTITY RECORD FOR: PRETORIUS",
      "SOURCE: SOURCE_PINNED_RECONSTRUCTED_FICTION",
      "EVENT ID: "+record["event_id"],
      "EPISODE: "+record["episode_id"],
      "TITLE: "+record["title"],
      "NARRATIVE: "+record["memory_text"],
      "BELIEF CHANGE: "+str(record.get("belief_changes") or ""),
      "RELATIONSHIP CHANGE: "+str(record.get("relationship_changes") or "")
    ))
    sealed=seal_record(OWNER,SOURCE,"L1v1",content)
    if verified_content(OWNER,sealed,{OWNER},{SOURCE})!=content:
        raise ArchiveGateError("Mismatch after source validation")
    return content,sha(content)

def wrong_identity_rejected(content):
    foreign=content.replace("IDENTITY RECORD FOR: PRETORIUS",
                            "IDENTITY RECORD FOR: OTHER_SUBJECT",1)
    envelope=seal_record("OTHER_SUBJECT",SOURCE,"L1v1",foreign)
    try:
        verified_content(OWNER,envelope,{OWNER},{SOURCE})
    except ArchiveGateError:
        return True
    return False
