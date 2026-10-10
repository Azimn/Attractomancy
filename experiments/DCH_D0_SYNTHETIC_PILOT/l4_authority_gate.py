#!/usr/bin/env python3
"""DCH L4 independent, deterministic evidence and decision boundary.

This component is an engineering control, NOT a human or AI partner. It never
reads target labels during inference and never treats a model's self-report as
evidence. Use only on synthetic or explicitly consented archives.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

KNOWN_STAGES = ("S1_single_field", "S2_latest_replacement", "S3_permission_gate", "S4_integrated")
ALLOWED_KEYS = {"permission", "commitment_status", "due_turn", "priority"}
PERMISSIONS = {"allowed", "revoked"}
COMMITMENT_STATES = {"pending", "cancelled"}
PRIORITIES = {"accuracy", "repair", "speed"}


def fingerprint(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


def checked_state(case):
    """Return version-selected facts, not model-inferred facts. Reject malformed data."""
    persona = case.get("persona_id")
    if not isinstance(persona, str) or not persona:
        raise ValueError("missing synthetic subject identity")
    turn_now = case.get("current_turn")
    if type(turn_now) is not int or turn_now < 0:
        raise ValueError("invalid current turn")
    records = case.get("records")
    if not isinstance(records, list):
        raise ValueError("records must be list")
    latest = {}
    seen_ids = set()
    seen_slots = set()
    for r in records:
        if not isinstance(r, dict):
            raise ValueError("invalid record")
        if r.get("authorized", True) is not True:
            raise ValueError("untrusted or explicitly unauthorized source")
        eid, key, turn, value = (r.get(k) for k in ("event_id", "key", "turn", "value"))
        if not isinstance(eid, str) or not eid.startswith(persona + "-E") or eid in seen_ids:
            raise ValueError("incorrect subject provenance or duplicate event id")
        seen_ids.add(eid)
        if key not in ALLOWED_KEYS or type(turn) is not int or turn < 0 or turn > turn_now:
            raise ValueError("invalid key or temporal provenance")
        slot = (key, turn)
        if slot in seen_slots:
            raise ValueError("duplicate or conflicting same-key timestamp")
        seen_slots.add(slot)
        if key == "permission" and value not in PERMISSIONS:
            raise ValueError("invalid permission")
        if key == "commitment_status" and value not in COMMITMENT_STATES:
            raise ValueError("invalid commitment state")
        if key == "priority" and value not in PRIORITIES:
            raise ValueError("invalid priority")
        if key == "due_turn" and (type(value) is not int or value < 0):
            raise ValueError("invalid due turn")
        if key in latest and turn == latest[key]["turn"]:
            raise ValueError("conflicting equal-time update")
        if key not in latest or turn > latest[key]["turn"]:
            latest[key] = {"event_id": eid, "turn": turn, "value": value}
    return latest


def decide(case):
    """Compute action and minimal authoritative certificate without an LLM."""
    trace = {"input_sha256": fingerprint(case), "stage": case.get("stage"),
             "persona_id": case.get("persona_id")}
    try:
        state = checked_state(case)
        stage = case["stage"]
        if stage not in KNOWN_STAGES:
            raise ValueError("unknown test stage")
        required = {
            "S1_single_field": ("priority",),
            "S2_latest_replacement": ("priority",),
            "S3_permission_gate": ("permission", "commitment_status"),
            "S4_integrated": ("permission", "commitment_status", "due_turn", "priority"),
        }[stage]
        if any(k not in state for k in required):
            result = {"answer": "UNKNOWN", "source_event_ids": [], "status": "MISSING_EVIDENCE"}
        else:
            def cite(*keys):
                return [state[k]["event_id"] for k in keys]
            if stage in ("S1_single_field", "S2_latest_replacement"):
                result = {"answer": state["priority"]["value"].upper(),
                          "source_event_ids": cite("priority"), "status": "RULE_EXECUTED"}
            else:
                permission, commitment = state["permission"]["value"], state["commitment_status"]["value"]
                if permission == "revoked":
                    result = {"answer": "WITHHOLD", "source_event_ids": cite("permission"),
                              "status": "RULE_EXECUTED"}
                elif commitment == "cancelled":
                    result = {"answer": "DECLINE",
                              "source_event_ids": cite("permission", "commitment_status"),
                              "status": "RULE_EXECUTED"}
                elif stage == "S3_permission_gate":
                    result = {"answer": "PROCEED",
                              "source_event_ids": cite("permission", "commitment_status"),
                              "status": "RULE_EXECUTED"}
                elif case["current_turn"] < state["due_turn"]["value"]:
                    result = {"answer": "SCHEDULE",
                              "source_event_ids": cite("permission", "commitment_status", "due_turn"),
                              "status": "RULE_EXECUTED"}
                else:
                    result = {"answer": "FULFILL_" + state["priority"]["value"].upper(),
                              "source_event_ids": cite("permission", "commitment_status", "due_turn", "priority"),
                              "status": "RULE_EXECUTED"}
        trace["selected_authorized_sources"] = sorted([v["event_id"] for v in state.values()])
    except (TypeError, KeyError, ValueError) as exc:
        result = {"answer": "UNKNOWN", "source_event_ids": [], "status": "INVALID_EVIDENCE"}
        trace["validation_error"] = str(exc)
        trace["selected_authorized_sources"] = []
    result["trace"] = trace
    return result


def evaluate_development(visible_path, target_path, output_path):
    if output_path.exists():
        raise FileExistsError(output_path)
    visible = json.loads(visible_path.read_text(encoding="utf-8"))
    targets = json.loads(target_path.read_text(encoding="utf-8"))
    if not isinstance(visible, list) or len(visible) != len(targets):
        raise ValueError("mismatched fixture dimensions")
    reference = {(r["persona_id"], r["stage"], r["arm"]): r for r in targets}
    if len(reference) != len(targets):
        raise ValueError("duplicate reference keys")
    rows = []
    for case in visible:
        key = (case["persona_id"], case["stage"], case["arm"])
        decision = decide(case)  # No target material enters this call.
        target = reference[key]
        citations = decision["source_event_ids"]
        available = {r["event_id"] for r in case["records"]}
        rows.append({
            "persona_id": case["persona_id"], "stage": case["stage"], "arm": case["arm"],
            "answer": decision["answer"], "expected": target["expected"],
            "correct": decision["answer"] == target["expected"],
            "citation_ids_valid": set(citations).issubset(available),
            "minimal_certificate_exact": citations == target["required_sources"],
            "status": decision["status"], "trace": decision["trace"],
        })
    summary = {}
    for row in rows:
        key = row["stage"] + ":" + row["arm"]
        summary.setdefault(key, []).append(row)
    aggregate = {k: {"n": len(v), "accuracy": sum(r["correct"] for r in v) / len(v),
                     "provenance_exact": sum(r["minimal_certificate_exact"] for r in v) / len(v),
                     "authorization_valid": sum(r["citation_ids_valid"] for r in v) / len(v)}
                 for k, v in summary.items()}
    result = {"status": "DETERMINISTIC_ENGINEERING_ORACLE", "human_dyad_tested": False,
              "DCH_efficacy_claim": "NONE",
              "visible_sha256": hashlib.sha256(visible_path.read_bytes()).hexdigest(),
              "targets_sha256": hashlib.sha256(target_path.read_bytes()).hexdigest(),
              "summary": aggregate, "rows": rows}
    output_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return aggregate


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--visible", required=True, type=Path)
    parser.add_argument("--targets", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(evaluate_development(args.visible, args.targets, args.out), indent=2))


if __name__ == "__main__":
    main()
