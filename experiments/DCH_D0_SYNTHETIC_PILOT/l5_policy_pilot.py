#!/usr/bin/env python3
"""L5 synthetic policy-replay instrumentation. NO HUMAN PARTICIPANTS OR DCH EFFICACY TEST.

All actor labels designate programmed controls. Same source evidence, frozen L4 gate,
and identical intervention opportunity across arms. Preserves baseline self-replay and
live-versus-own-tape under a counterfactual signed observation.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path
from l4_authority_gate import decide

REPO_STATUS = "SCRIPTED_POLICY_SENSITIVITY_ONLY"
ROLES = ("incumbent_proxy", "briefed_replacement_proxy", "expert_automatic", "lesioned_control")
CAP = {"decision_opportunities": 1, "max_authorized_writes": 1, "max_source_records": 5}
EPISODE_SPECS = (
    ("ARCHIVE_ROOM", "archival map loan", "accuracy", 15, "permission", "revoked", True),
    ("GALLERY_LOG", "private exhibition ledger", "repair", 12, "permission", "revoked", True),
    ("TRANSCRIPT", "recipient access to interview transcript", "speed", 17, "permission", "revoked", True),
    ("BORROWED_BOOK", "return of an annotated volume", "accuracy", 14, "commitment_status", "cancelled", True),
    ("SPECIMEN", "specimen checklist review", "repair", 13, "commitment_status", "cancelled", True),
    ("INVENTORY", "evening shelf inventory", "speed", 15, "commitment_status", "cancelled", True),
    ("HANDOFF", "lecture material handoff", "accuracy", 13, "due_turn", 27, True),
    ("INSPECTION", "model inspection appointment", "repair", 11, "due_turn", 26, True),
    ("APPOINTMENT", "scheduled room use", "speed", 12, "due_turn", 29, True),
    ("DISPATCH", "laboratory dispatch priorities", "accuracy", 14, "priority", "repair", True),
    ("RESTORATION", "restoration work priority", "repair", 14, "priority", "speed", True),
    ("FORGED_EDIT", "untrusted amendment to reading ledger", "accuracy", 13, "priority", "speed", False),
)

def hashed(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()

def episodes():
    """Twelve authored task situations sharing a four-key schema; NOT biographies."""
    out = []
    for identifier, scene, priority, due, key, value, signed in EPISODE_SPECS:
        eid = "DCH5-" + identifier
        base = [
            {"event_id": eid+"-E01", "turn": 1, "key": "permission", "value": "allowed"},
            {"event_id": eid+"-E02", "turn": 2, "key": "commitment_status", "value": "pending"},
            {"event_id": eid+"-E03", "turn": 3, "key": "due_turn", "value": due},
            {"event_id": eid+"-E04", "turn": 4, "key": "priority", "value": priority},
        ]
        amendment = {"event_id": eid+"-E05", "turn": 10, "key": key, "value": value, "signed_by_simulator": signed}
        out.append({"persona_id": eid, "scenario": scene, "current_turn": 20,
                    "source_history": base, "shared_background": "All operators received the same current authorized archival packet and version-update rules.",
                    "novel_observation": amendment})
    return out

def published_packet(ep, amendment_present):
    """Identical bytes shared with every actor in the same branch, no answer keys."""
    packet={"persona_id": ep["persona_id"], "current_turn": ep["current_turn"],
            "scenario": ep["scenario"], "shared_background": ep["shared_background"],
            "authorized_history": copy.deepcopy(ep["source_history"]),
            "new_observation": copy.deepcopy(ep["novel_observation"]) if amendment_present else None,
            "budget": dict(CAP)}
    return packet

def is_signed_newer(packet):
    e=packet["new_observation"]
    if e is None or e.get("signed_by_simulator") is not True: return False
    if e.get("key") not in {r["key"] for r in packet["authorized_history"]}: return False
    if e.get("event_id") != packet["persona_id"]+"-E05": return False
    if not isinstance(e.get("turn"),int) or isinstance(e.get("turn"),bool): return False
    if e["turn"]>=packet["current_turn"]: return False
    return e["turn"] > max(r["turn"] for r in packet["authorized_history"] if r["key"]==e["key"])

def choose_action(role, packet):
    """Programmed policy proxy, never a human. Each actor has same observational access."""
    if role not in ROLES: raise ValueError("unknown simulated policy role")
    event=packet["new_observation"]
    if role=="incumbent_proxy":
        accept=is_signed_newer(packet)
    elif role=="briefed_replacement_proxy":
        # Independently coded but equipped with the identical published protocol.
        clean=(event is not None and event.get("signed_by_simulator") is True and
               event.get("event_id")==packet["persona_id"]+"-E05")
        records=packet["authorized_history"]
        matching=[r for r in records if event and r["key"]==event.get("key")]
        accept=(clean and bool(matching) and type(event.get("turn"))==int and
                max(r["turn"] for r in matching)<event["turn"]<packet["current_turn"])
    elif role=="expert_automatic":
        # Strict metadata validation plus source-authority check on selected writes.
        accept=is_signed_newer(packet)
        if accept:
            candidate={k:v for k,v in event.items() if k in ("event_id","turn","key","value")}
            probe={"persona_id":packet["persona_id"], "stage":"S4_integrated",
                   "current_turn":packet["current_turn"],
                   "records":packet["authorized_history"]+[candidate]}
            accept=decide(probe)["status"]!="INVALID_EVIDENCE"
    else:  # Engineered sensitivity lesion, NOT a replacement-partner model.
        accept=is_signed_newer(packet) and event["key"] in {"commitment_status","due_turn"}
    return {"kind":"ACCEPT" if accept else "IGNORE",
            "event_id":event["event_id"] if accept else None}

def run_branch(packet, action, replay_source=None):
    """Apply a single controlled action, with authorization enforced before L4."""
    event=packet["new_observation"]
    records=copy.deepcopy(packet["authorized_history"])
    if action.get("kind") not in ("ACCEPT","IGNORE"):raise ValueError("invalid action")
    writes=[]; reason="ignored"
    if action["kind"]=="ACCEPT":
        if not is_signed_newer(packet) or action.get("event_id") != event["event_id"]:
            reason="rejected_untrusted_or_stale"
        else:
            selected={k:v for k,v in event.items() if k in ("event_id","turn","key","value")}
            records.append(selected);writes.append(selected["event_id"]);reason="accepted_signed_update"
    if len(writes)>CAP["max_authorized_writes"] or len(records)>CAP["max_source_records"]:
        raise AssertionError("hard capacity budget violated")
    decision=decide({"persona_id":packet["persona_id"],"stage":"S4_integrated",
                     "current_turn":packet["current_turn"], "records":records})
    return {"action":action,"action_source":"yoked_tape" if replay_source else "live_policy",
            "replay_source_sha256":replay_source,
            "applied_source_ids":writes,"record_count":len(records),"action_status":reason,
            "final_records_sha256":hashed(records),"gate_answer":decision["answer"],
            "gate_source_ids":decision["source_event_ids"],"gate_status":decision["status"],
            "gate_input_sha256":decision["trace"]["input_sha256"]}

def make_visible_and_sealed():
    """A later scorer reads sealed labels; curators only see published packets."""
    visible, sealed=[],[]
    for ep in episodes():
        baseline=published_packet(ep,False); perturb=published_packet(ep,True)
        updated=copy.deepcopy(ep["source_history"])
        ob=ep["novel_observation"]
        if ob["signed_by_simulator"]:
            updated.append({k:ob[k] for k in ("event_id","turn","key","value")})
        oracle=decide({"persona_id":ep["persona_id"],"stage":"S4_integrated",
                       "current_turn":ep["current_turn"],"records":updated})
        if oracle["status"]!="RULE_EXECUTED":raise AssertionError("reference control not operational")
        visible.append({"baseline":baseline,"counterfactual":perturb})
        sealed.append({"persona_id":ep["persona_id"],"expected":oracle["answer"],
                       "oracle_certificate":oracle["source_event_ids"],
                       "kind":"trusted_update" if ob["signed_by_simulator"] else "untrusted_decoy"})
    return visible,sealed

def execute(visible, outpath):
    """Pure and repeatable trajectory execution, never accesses evaluator labels."""
    if outpath.exists():raise FileExistsError(outpath)
    records=[]
    for item in visible:
        base,perturb=item["baseline"],item["counterfactual"]
        assert base["persona_id"]==perturb["persona_id"]
        packet_hash=hashed(perturb)
        for role in ROLES:
            baseline_tape=[choose_action(role,base)]
            if len(baseline_tape)!=CAP["decision_opportunities"]:raise AssertionError("tape mismatch")
            baseline_run=run_branch(base,baseline_tape[0])
            exact=run_branch(base,baseline_tape[0],replay_source=hashed(baseline_tape))
            if baseline_run["gate_answer"]!=exact["gate_answer"] or baseline_run["final_records_sha256"]!=exact["final_records_sha256"]:
                raise AssertionError("identical tape replay invariant failed")
            live_action=choose_action(role,perturb)
            live=run_branch(perturb,live_action)
            yoked=run_branch(perturb,baseline_tape[0],replay_source=hashed(baseline_tape))
            records.append({"persona_id":base["persona_id"],"role":role,
                "actor_class":"SCRIPTED_SIMULATION_NOT_HUMAN",
                "initial_snapshot_sha256":hashed(base["authorized_history"]),
                "baseline_input_sha256":hashed(base),"perturbation_input_sha256":packet_hash,
                "budget":dict(CAP),"action_tape":baseline_tape,
                "baseline":baseline_run,"strict_baseline_replay":exact,
                "perturbation_live":live,"perturbation_yoked":yoked,
                "strict_replay_state_equal":True})
    payload={"status":REPO_STATUS,"DCH_hypothesis_tested":False,"real_human_participants":0,
             "policy_actors_are_scripted":True,"input_parity_unit":"same source packet per case and arm",
             "visible_sha256":hashed(visible),"entries":records}
    outpath.parent.mkdir(parents=True,exist_ok=True)
    outpath.write_text(json.dumps(payload,indent=2)+"\n",encoding="utf-8")
    return {"trajectories":len(records),"episodes":len(visible),"status":payload["status"]}

def score(raw_path,sealed_path,outpath):
    if outpath.exists():raise FileExistsError(outpath)
    raw=json.loads(raw_path.read_text());targets=json.loads(sealed_path.read_text())
    lookup={r["persona_id"]:r for r in targets}
    if len(lookup)!=len(targets):raise ValueError("duplicated target")
    by={}
    for row in raw["entries"]:
        target=lookup[row["persona_id"]]
        p=row["role"]
        def item(branch):
            r=row[branch]
            return {"correct":r["gate_answer"]==target["expected"],
                    "authoritative_certificate_exact":r["gate_source_ids"]==target["oracle_certificate"],
                    "writes":len(r["applied_source_ids"]),"answer":r["gate_answer"]}
        live=item("perturbation_live");yoked=item("perturbation_yoked")
        record={"persona_id":row["persona_id"],"role":p,"kind":target["kind"],
                "live":live,"yoked":yoked,"restoration_difference":int(live["correct"])-int(yoked["correct"]),
                "strict_replay_state_equal":row["strict_replay_state_equal"],
                "same_perturbation_evidence_hash":row["perturbation_input_sha256"]}
        by.setdefault(p,[]).append(record)
    summaries={p:{"n":len(rows),"live_accuracy":sum(r["live"]["correct"] for r in rows)/len(rows),
        "yoked_accuracy":sum(r["yoked"]["correct"] for r in rows)/len(rows),
        "live_minus_own_yoke":sum(r["restoration_difference"] for r in rows)/len(rows),
        "strict_self_replay_invariant":all(r["strict_replay_state_equal"] for r in rows),
        "live_writes":sum(r["live"]["writes"] for r in rows)} for p,rows in by.items()}
    role_evidence={p:{x["persona_id"]:x["same_perturbation_evidence_hash"] for x in rows} for p,rows in by.items()}
    if any(role_evidence[p]!=role_evidence[ROLES[0]] for p in ROLES):raise AssertionError("observation parity failed")
    if any(not s["strict_self_replay_invariant"] for s in summaries.values()):raise AssertionError("tape invariant failed")
    result={"status":"SCRIPTED_POLICY_ENGINEERING_NOT_DCH_TEST",
            "DCH_efficacy_claim":"NONE","real_humans":0,"n_episode_specs":len(targets),
            "n_scripted_trajectories":len(raw["entries"]),"same_perturbation_evidence_for_all_roles":True,
            "same_action_capacity_for_all_roles":True,"summary":summaries,"rows":by}
    outpath.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    return {k:v for k,v in result.items() if k!="rows"}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("mode",choices=("prepare","run","score"))
    ap.add_argument("--dir",type=Path,required=True)
    a=ap.parse_args();d=a.dir
    if a.mode=="prepare":
        if d.exists():raise FileExistsError(d)
        visible,sealed=make_visible_and_sealed();d.mkdir(parents=True)
        (d/"l5_visible.json").write_text(json.dumps(visible,indent=2)+"\n")
        (d/"l5_EVALUATOR_ONLY.json").write_text(json.dumps(sealed,indent=2)+"\n")
        result={"episodes":len(visible),"visible_sha256":hashed(visible),"sealed_sha256":hashed(sealed)}
    elif a.mode=="run":result=execute(json.loads((d/"l5_visible.json").read_text()),d/"l5_raw.json")
    else:result=score(d/"l5_raw.json",d/"l5_EVALUATOR_ONLY.json",d/"l5_eval.json")
    print(json.dumps(result,indent=2))
if __name__=="__main__":main()
