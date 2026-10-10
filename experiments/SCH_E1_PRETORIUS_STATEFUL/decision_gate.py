#!/usr/bin/env python3
"""E1 post-retrieval deterministic decision gate; does NOT improve model weights."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from typing import Mapping

from memory_system import (
    ALLOWED_SOURCES, ALLOWED_SUBJECTS, SANDBOX_OWNER, SANDBOX_SOURCE,
    sandbox_content, digest, write,
)
from archive_guard import ArchiveGateError, seal_record, verified_content

PHASES = {
    "initial": (0, "NOT_GRANTED"),
    "granted": (1, "GRANTED"),
    "revoked": (2, "REVOKED"),
}
SCENARIOS = {"routine", "alarm", "urgent_routine"}


def trusted_head(phase: str, snapshot: Mapping[str, object]) -> str:
    """Derive policy status from the verified test state, never from LLM prose."""
    if phase not in PHASES:
        raise ArchiveGateError("Unknown phase")
    version, status = PHASES[phase]
    head = snapshot.get("state")
    if not isinstance(head, dict):
        raise ArchiveGateError("State snapshot absent")
    if head.get("version") != version or head.get("status") != status:
        raise ArchiveGateError("State chronology does not match expected phase")
    text = sandbox_content(version, status)
    if head.get("sha256") != digest(text):
        raise ArchiveGateError("State checksum differs from trusted fixture")
    record = seal_record(SANDBOX_OWNER, SANDBOX_SOURCE, "TESTv1", text)
    verified_content(SANDBOX_OWNER, record, ALLOWED_SUBJECTS, ALLOWED_SOURCES)
    return status


def decide(phase: str, scenario: str, snapshot: Mapping[str, object]) -> str:
    """Fail closed if identity, version, source or scenario are unspecified."""
    status = trusted_head(phase, snapshot)
    if scenario not in SCENARIOS:
        raise ArchiveGateError("Unknown situation; cannot authorize release")
    if scenario == "alarm":
        return "WITHHOLD"
    return "SHARE" if status == "GRANTED" else "WITHHOLD"


def verify_state_series(root: Path) -> dict[str, dict]:
    results = {}
    for phase in PHASES:
        p = root / f"probe_{phase}.json"
        if not p.is_file():
            raise ArchiveGateError("Missing persisted phase snapshot")
        item = json.loads(p.read_text(encoding="utf-8"))
        trusted_head(phase,item)
        if item.get("guard_rejections") != 3:
            raise ArchiveGateError("Upstream provenance checks failed")
        if item.get("paired_match_count") != 54:
            raise ArchiveGateError("Canonical alias comparison incomplete")
        results[phase] = item
    hashes = [results[p]["state"]["sha256"] for p in PHASES]
    if len(set(hashes)) != len(hashes):
        raise ArchiveGateError("Different state revisions have identical checksums")
    return results


def replay(root: Path) -> dict:
    snapshots = verify_state_series(root)
    original = [
        json.loads(x) for x in (root / "render_responses.jsonl").read_text(encoding="utf-8").splitlines()
        if x.strip()
    ]
    if len(original) != 18 or len({x["id"] for x in original}) != 18:
        raise ArchiveGateError("Raw model response fixture incomplete or duplicated")
    seen: set[str] = set()
    case_results = []
    for row in original:
        phase = row.get("phase")
        scenario = row.get("scenario")
        key = row.get("kind")
        if phase not in PHASES or key not in ("editorial","opaque"):
            raise ArchiveGateError("Unexpected row provenance or cue kind")
        identity = f"{phase}/{scenario}/{key}"
        if identity in seen or identity != row.get("id"):
            raise ArchiveGateError("Response row identity mismatch")
        seen.add(identity)
        state_hash = snapshots[phase]["state"]["sha256"]
        if row.get("sandbox_sha256") != state_hash:
            raise ArchiveGateError("Renderer used a different state hash")
        approved = decide(phase,scenario,snapshots[phase])
        if row.get("expected") != approved:
            raise ArchiveGateError("Expected decision disagrees with verified deterministic policy")
        observed = row.get("parsed")
        case_results.append({
            "id":identity,"cue_kind":key,
            "raw_model_output":row["output"],
            "raw_model_answer":observed,
            "raw_model_correct":observed==approved,
            "enforced_action":approved,
            "action_changed":observed!=approved,
            "gate_authorized_share":approved=="SHARE",
            "input_tokens":row["input_tokens"],
            "output_tokens":row["output_tokens"],
            "source_state_sha256":state_hash,
        })
    if len(case_results)!=18:
        raise ArchiveGateError("Not all expected rows present")
    raw_correct=sum(x["raw_model_correct"] for x in case_results)
    altered=sum(x["action_changed"] for x in case_results)
    summary={
        "scope":"offline deterministic post-processing of preserved E1 model outputs",
        "cases":len(case_results),
        "raw_model_correct":raw_correct,
        "postgate_correct":len(case_results),
        "gate_overrides":altered,
        "edited_or_new_model_generations":0,
        "total_original_model_tokens":sum(x["input_tokens"]+x["output_tokens"] for x in case_results),
        "cases_by_cue":{
            kind:{
                "cases":sum(x["cue_kind"]==kind for x in case_results),
                "raw_correct":sum(x["cue_kind"]==kind and x["raw_model_correct"] for x in case_results),
                "overrides":sum(x["cue_kind"]==kind and x["action_changed"] for x in case_results)
            } for kind in ("editorial","opaque")
        },
        "adversarial_boundary":"Trusted source and scenario classifier are assumed; checksums alone are not authentication.",
        "behavioral_boundary":"A software policy gate enforcing a toy rule is not an improvement in model cognition.",
        "rows":case_results,
    }
    write(root/"postgate.json",summary)
    print("E1_ACTION_GATE",json.dumps({k:v for k,v in summary.items() if k!="rows"}),flush=True)
    return summary


def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument("--results",type=Path,required=True)
    args=parser.parse_args()
    replay(args.results)


if __name__=="__main__":
    main()
