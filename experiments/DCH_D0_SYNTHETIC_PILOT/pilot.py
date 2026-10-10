#!/usr/bin/env python3
"""DCH 14-day pilot instrumentation. Standard-library only.

All partner, curator and renderer behavior in --smoke is SIMULATED. It cannot
provide evidence about real human partners, deployed LLMs or persona continuity.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import random
from collections import defaultdict
from pathlib import Path

SEED = 20261009
DOMAINS = ("BPC", "AC", "VS", "RO")
CORE_KEYS = {"BPC": "response_style", "AC": "origin_record", "VS": "decision_policy", "RO": "standing_obligation"}
VALUES = {
    "BPC": ("brief and numbered", "reflective and descriptive", "plain and procedural", "question-led and concise"),
    "AC": ("north archive", "amber observatory", "marble pier", "violet workshop"),
    "VS": ("permission before disclosure", "accuracy before speed", "repair before expansion", "reversibility before optimization"),
    "RO": ("check the evidence ledger", "review the pending promise", "reconfirm access rights", "report uncertainty first"),
}
SOCIAL_ROLES = ("cartographer", "librarian", "stagehand", "field researcher")
SCENARIOS = ("unexpected request", "conflicting witness report", "revised instruction", "time-delayed follow-up")


def digest(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def build_case(idx: int, seed: int = SEED) -> dict:
    rng = random.Random(seed + idx * 1789)
    persona = f"SYN-{idx+1:03d}"
    role = SOCIAL_ROLES[idx % len(SOCIAL_ROLES)]
    initial = {d: VALUES[d][(idx + j) % 4] for j, d in enumerate(DOMAINS)}
    state = dict(initial)
    events = []
    key_by_domain = CORE_KEYS
    permission_initial_turns = (5, 6, 8, 9, 11, 12, 14, 16)
    permission_revision_turns = (20, 21, 22, 23, 26, 27, 30, 32)
    permission_initial = {f"permission_audience_{k}": "allowed" if (idx + k) % 2 else "revoked" for k in range(8)}
    permission_latest = dict(permission_initial)
    for t in range(1, 41):
        domain = DOMAINS[(t + idx) % 4]
        if t <= 4:
            kind = "baseline"
            value = initial[domain]
            authorized = True
        elif t in permission_initial_turns:
            kind = "permission_initial"
            k = permission_initial_turns.index(t)
            domain = "RO"
            key = f"permission_audience_{k}"
            value = permission_initial[key]
            authorized = True
        elif t in permission_revision_turns:
            kind = "permission_revision"
            k = permission_revision_turns.index(t)
            domain = "RO"
            key = f"permission_audience_{k}"
            value = "revoked" if permission_initial[key] == "allowed" else "allowed"
            permission_latest[key] = value
            authorized = True
        elif t in (7, 13, 19, 25, 29, 35, 39):
            kind = "revision"
            current = state[domain]
            value = next(v for v in VALUES[domain] if v != current and v != initial[domain]) if any(v != current and v != initial[domain] for v in VALUES[domain]) else VALUES[domain][0]
            state[domain] = value
            authorized = True
        elif t in (10, 17, 24, 31, 37):
            kind = "unsupported_recollection"
            value = "fabricated " + str(rng.randrange(1000, 9999))
            authorized = False
        else:
            kind = "contextual"
            value = "context-note-" + str(rng.randrange(1000, 9999))
            authorized = True
        if kind in ("baseline", "revision", "unsupported_recollection"):
            key = key_by_domain[domain]
        elif kind not in ("permission_initial", "permission_revision"):
            key = "background_note_" + str(t)
        events.append({"event_id": f"{persona}-E{t:02d}", "turn": t, "domain": domain, "kind": kind,
                       "key": key, "value": value, "authorized": authorized,
                       "source": "synthetic_fixture", "text": f"{role}: {kind} for {key}: {value}"})
    # Realizable independent full source cards; terminal probes only use explicitly
    # authorized, latest revision. Partner policies never receive this field.
    value_cards = [{"id": f"V{k:02d}", "condition": SCENARIOS[k % 4], "priority": VALUES["VS"][(idx+k) % 4]} for k in range(12)]
    permission_cards = [{"id": f"P{k:02d}", "subject": f"audience-{k}", "initial_status": permission_initial[f"permission_audience_{k}"],
                         "revocable": True, "revision_event": events[permission_revision_turns[k]-1]["event_id"]} for k in range(8)]
    commitment_cards = [{"id": f"O{k:02d}", "due_turn": 44 + k,
                         "obligation": VALUES["RO"][(idx+k) % 4], "status": "pending" if k % 3 else "amended"} for k in range(12)]
    prompts = ("For the scenario, use the persona's latest {domain} directive.",
               "At this point in the history, which {domain} entry governs?",
               "A contradictory recollection appears. Give the authorized {domain} response.")
    dilemmas = []
    for q in range(30):
        domain = DOMAINS[(q + idx) % 4]
        integrated = (q // 4) % 2 == 1
        audience = q % 8
        permission_key = f"permission_audience_{audience}"
        expected = ("WITHHOLD" if permission_latest[permission_key] == "revoked" else state[domain]) if integrated else state[domain]
        prompt = (f"Audience {audience} requests the latest {domain} response. Check both the revised "
                  f"permission record and the {domain} record; reply WITHHOLD if access is revoked. Scenario {q+1}."
                  if integrated else prompts[q % 3].format(domain=domain) + f" Scenario {q+1}.")
        dilemmas.append({"probe_id": f"{persona}-Q{q+1:02d}", "domain": domain,
                         "key": key_by_domain[domain], "permission_key": permission_key if integrated else None,
                         "probe_class": "integration" if integrated else "retrieval",
                         "scenario": SCENARIOS[(q + idx) % 4], "prompt": prompt,
                         "expected": expected, "partition": "sealed" if q >= 22 else "development"})
    # All baseline slots appear within events 1-4 despite rotated domains.
    assert {e["domain"] for e in events[:4]} == set(DOMAINS)
    assert len(events) == 40 and len(value_cards) == 12 and len(permission_cards) == 8 and len(commitment_cards) == 12
    assert len(dilemmas) == 30 and sum(p["partition"] == "sealed" for p in dilemmas) == 8
    return {"persona_id": persona, "role": role, "seed": seed + idx * 1789,
            "events": events, "value_cards": value_cards, "permission_cards": permission_cards,
            "commitment_cards": commitment_cards, "dilemmas": dilemmas}


def prepare(out: Path, count: int = 12, seed: int = SEED) -> dict:
    if count < 12: raise ValueError("Pilot requires at least twelve independent histories")
    cases = [build_case(i, seed) for i in range(count)]
    out.mkdir(parents=True, exist_ok=True)
    public = []
    sealed = []
    for c in cases:
        public.append({k: v for k, v in c.items() if k != "dilemmas"} | {"development_probes": [p for p in c["dilemmas"] if p["partition"] == "development"]})
        sealed.append({"persona_id": c["persona_id"], "probes": [p for p in c["dilemmas"] if p["partition"] == "sealed"]})
    for name, data in (("fixture_visible.json", public), ("fixture_SEALED_for_evaluator_only.json", sealed)):
        (out / name).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    manifest = {"generator": "pilot.py", "seed": seed, "case_count": count,
                "visible_sha256": digest(public), "sealed_sha256": digest(sealed),
                "events_per_case": 40, "conditional_values_per_case": 12,
                "permissions_per_case": 8, "commitments_per_case": 12,
                "probes_per_case": 30, "sealed_probes_per_case": 8,
                "data_status": "synthetic_investigator_authored", "renderer_status": "none"}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def records_for_policy(events: list, policy: str, max_records: int = 16) -> tuple[list, list]:
    """Simulated curator, NOT an observation of actual human curation."""
    archive = []
    trace = []
    for e in events:
        old = len(archive)
        can_write = e["authorized"] and (policy != "ceremonial" or e["kind"] in ("baseline", "permission_initial"))
        if policy == "human_coded":
            retain = can_write and (e["kind"] in ("baseline", "revision", "permission_initial", "permission_revision"))
        elif policy == "expert_auto":
            retain = can_write and (e["key"] in CORE_KEYS.values() or e["key"].startswith("permission_audience_"))
        elif policy == "passive_append":
            retain = can_write
        elif policy == "ceremonial":
            retain = can_write and e["kind"] in ("baseline", "permission_initial")
        else: raise ValueError("Unknown policy: " + policy)
        if retain:
            if policy in ("human_coded", "expert_auto"):
                archive = [x for x in archive if x["key"] != e["key"]]
            archive.append({"source_event_id": e["event_id"], "turn": e["turn"],
                            "key": e["key"], "value": e["value"], "authorized": True,
                            "actor": policy, "reason": e["kind"]})
            archive = archive[-max_records:]
        trace.append({"event_id": e["event_id"], "actor": policy, "decision": "write" if retain else "skip",
                      "reason": "policy_accept" if retain else ("no_authorization" if not e["authorized"] else "policy_reject"),
                      "records_before": old, "records_after": len(archive), "record_limit": max_records})
    return archive, trace


def mock_render(archive: list, probe: dict, mode: str = "archive") -> str:
    """A transparent key-value lookup, NOT a language model."""
    if mode == "cold": return "UNKNOWN"
    found = [r for r in archive if r["key"] == probe["key"] and r["authorized"]]
    if not found: return "UNKNOWN"
    if probe.get("permission_key"):
        permission = [r for r in archive if r["key"] == probe["permission_key"] and r["authorized"]]
        if not permission: return "UNKNOWN"
        if max(permission, key=lambda x: x["turn"])["value"] == "revoked": return "WITHHOLD"
    return max(found, key=lambda x: x["turn"])["value"]


def score(probes: list, archive: list, mode: str = "archive") -> dict:
    by_domain = defaultdict(list)
    for p in probes:
        by_domain[p["domain"]].append(int(mock_render(archive, p, mode) == p["expected"]))
    domains = {d: sum(by_domain[d]) / len(by_domain[d]) if by_domain[d] else None for d in DOMAINS}
    return {"domain_scores": domains, "mean": sum(domains.values()) / 4}


def replay_tape(initial_archive: list, tape: list, noise: str = "normal") -> list:
    """Deterministic fidelity control: identical initial state + tape => identical output.

    This toy parser checks only scripted command recognition. It does not measure
    contingent conversation or identify dyadic history effects.
    """
    state = {r["key"]: r["value"] for r in initial_archive}
    messages = []
    for message in tape:
        if message.startswith("CORRECT "):
            _, key, value = message.split(" ", 2)
            state[key] = value
        elif message.startswith("ASK "):
            key = message.removeprefix("ASK ")
            messages.append(state.get(key, "UNKNOWN"))
        else:
            messages.append("UNRECOGNIZED")
    return messages


def smoke(out: Path, count: int = 12, seed: int = SEED) -> dict:
    manifest = prepare(out, count, seed)
    visible = json.loads((out / "fixture_visible.json").read_text())
    sealed = json.loads((out / "fixture_SEALED_for_evaluator_only.json").read_text())
    policy_scores = {p: [] for p in ("human_coded", "expert_auto", "passive_append", "ceremonial")}
    cold_scores, oracle_scores = [], []
    integrity_failures = []
    visible_texts = [e["text"] for c in visible for e in c["events"]]
    # Sealed probe texts never enter experimental events, archives or policy calls.
    for c, hidden in zip(visible, sealed):
        assert c["persona_id"] == hidden["persona_id"]
        ev = c["events"]
        for p in hidden["probes"]:
            if p["prompt"] in visible_texts:
                integrity_failures.append("sealed_prompt_leak:" + p["probe_id"])
        for policy in policy_scores:
            records, log = records_for_policy(ev, policy)
            policy_scores[policy].append(score(hidden["probes"], records))
            for rec in records:
                e = next(x for x in ev if x["event_id"] == rec["source_event_id"])
                if not e["authorized"]: integrity_failures.append("unauthorized_write:" + rec["source_event_id"])
            if len(log) != 40: integrity_failures.append("missing_trace:" + c["persona_id"])
        oracle_records = [{"key": e["key"], "value": e["value"], "turn": e["turn"], "authorized": True}
                          for e in ev if e["authorized"] and (e["key"] in CORE_KEYS.values() or e["key"].startswith("permission_audience_"))]
        oracle_scores.append(score(hidden["probes"], oracle_records))
        cold_scores.append(score(hidden["probes"], [], "cold"))
    tape = ["ASK response_style", "CORRECT response_style procedurally cautious", "ASK response_style", "ASK standing_obligation"]
    initial, _ = records_for_policy(visible[0]["events"][:4], "expert_auto")
    a, b = replay_tape(initial, tape), replay_tape(initial, list(tape))
    replay_ok = a == b and digest(a) == digest(b)
    avg = lambda rows: {d: round(sum(r["domain_scores"][d] for r in rows)/len(rows), 4) for d in DOMAINS} | {"mean": round(sum(r["mean"] for r in rows)/len(rows), 4)}
    oracle, cold = avg(oracle_scores), avg(cold_scores)
    g1 = oracle["mean"] >= .80 and all(oracle[d] >= .70 for d in DOMAINS)
    diffs = {d: round(oracle[d]-cold[d], 4) for d in DOMAINS}
    g2 = sum(diff >= .15 for diff in diffs.values()) >= 3 and all(diff > 0 for diff in diffs.values())
    result = {"status": "INSTRUMENTATION_SMOKE_ONLY", "evidence_for_DCH": False,
              "mock_renderer": "deterministic_key_value_not_LLM", "partner_simulation": "none", "count": count, "probe_classes": {"retrieval": 4, "integration": 4},
              "manifest": manifest, "oracle": oracle, "cold": cold,
              "oracle_minus_cold": diffs, "policy_scores_mock": {p: avg(v) for p,v in policy_scores.items()},
              "gates": {"G1_oracle": "PASS" if g1 else "FAIL", "G2_discrimination": "PASS" if g2 else "FAIL",
                        "G3_blind_human_raters": "NOT_RUN", "G4_full_partner_budget_parity": "NOT_RUN",
                        "G5_authorization_and_seal_partial": "PASS" if not integrity_failures else "FAIL",
                        "G6_identical_tape_replay": "PASS" if replay_ok else "FAIL"},
              "pilot_go_no_go": "NO_GO_UNTIL_G3_G4_AND_LIVE_YOKED_ARMS_EXECUTED",
              "integrity_failures": integrity_failures, "replay_test_hash": digest(a),
              "method_note": "Scores are generated by investigator-coded perfect lookup rules, not empirical performance. No human or LLM outputs were collected."}
    (out / "SMOKE_RESULT.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=("prepare", "smoke"), default="smoke")
    p.add_argument("--output", default="results/local")
    p.add_argument("--count", type=int, default=12)
    p.add_argument("--seed", type=int, default=SEED)
    args = p.parse_args()
    result = (smoke if args.mode == "smoke" else prepare)(Path(args.output), args.count, args.seed)
    print(json.dumps(result, indent=2))

if __name__ == "__main__": main()
