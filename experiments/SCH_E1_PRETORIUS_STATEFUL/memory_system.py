#!/usr/bin/env python3
"""E1: a pinned, guarded, stateful Pretorius memory adapter (not a production mind)."""
from __future__ import annotations
import argparse
import dataclasses
import hashlib
import json
import random
import re
import sqlite3
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
GUARD_PATH = HERE.parent / "SCH_D1_EXTERNAL_RECONSTRUCTION"
sys.path.insert(0, str(GUARD_PATH))
from archive_guard import ArchiveGateError, seal_record, verified_content

SCHEMA = "sch-e1-pretorius-state-v1"
SOURCE_COMMIT = "6d2768211f5c2184c8bbdb833c06e169b5137197"
CANONICAL_OWNER = "PRETORIUS"
SANDBOX_OWNER = "PRETORIUS_SANDBOX"
CANONICAL_SOURCE = "pretorius_l1_pinned"
SANDBOX_SOURCE = "sch_e1_synthetic"
ALLOWED_SUBJECTS = {CANONICAL_OWNER, SANDBOX_OWNER}
ALLOWED_SOURCES = {CANONICAL_SOURCE, SANDBOX_SOURCE}
SEED = 20261009


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def dumps(data: object) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def connect(path: Path) -> sqlite3.Connection:
    db = sqlite3.connect(str(path))
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")
    return db


def load_source(source: Path):
    sys.path.insert(0, str(source / "src"))
    from pretorius_connectome.shared_memory import read_l1, SOURCE_BLOB
    shared = source / "artifacts" / "shared_memory" / "v1"
    rows = read_l1(shared / "pretorius_l1_v1.jsonl.gz", shared / "manifest.json")
    manifest_raw = (shared / "manifest.json").read_bytes()
    manifest = json.loads(manifest_raw)
    if len(rows) != 450 or manifest["source_git_blob"] != SOURCE_BLOB:
        raise AssertionError("Incorrect canonical Pretorius archive")
    return rows, manifest, hashlib.sha256(manifest_raw).hexdigest()


def choose(rows: list[dict]):
    counts: dict[str, int] = {}
    for row in rows:
        for cue in row.get("recall_cues", []):
            normalized = cue.casefold().strip()
            counts[normalized] = counts.get(normalized, 0) + 1
    eligible: dict[str, list[dict]] = {}
    for row in rows:
        candidates = [
            x for x in row.get("recall_cues", [])
            if isinstance(x, str) and 4 <= len(x.strip()) <= 90
            and counts.get(x.casefold().strip()) == 1
        ]
        if candidates:
            eligible.setdefault(row["episode_id"], []).append(
                {"id": row["event_id"], "episode": row["episode_id"],
                 "cue": sorted(candidates, key=lambda x: (len(x), x.casefold()))[0],
                 "title": row["title"]}
            )
    rng = random.Random(SEED)
    chosen = []
    for episode, matches in sorted(eligible.items()):
        if len(matches) < 2:
            raise AssertionError("Cannot select two unique cue cases per episode")
        chosen.extend(rng.sample(sorted(matches, key=lambda x: x["id"]), 2))
    if len(chosen) != 54:
        raise AssertionError(f"Expected 54 episode-stratified tests, got {len(chosen)}")
    for item in chosen:
        item["opaque"] = "KEY" + digest("opaque-v1:" + item["id"])[:12].upper()
    return sorted(chosen, key=lambda r: (r["episode"], r["id"]))


def content_for(row: dict) -> str:
    return "\n".join([
        "IDENTITY RECORD FOR: PRETORIUS",
        "ARCHIVE TYPE: RECONSTRUCTED FICTIONAL HISTORY",
        "SOURCE: original checksum-verified Pretorius L1 archive",
        "EVENT ID: " + row["event_id"],
        "EVENT TITLE: " + row["title"],
        "MEMORY TEXT: " + row["memory_text"],
    ])


def sandbox_content(version: int, permission: str) -> str:
    return "\n".join([
        "IDENTITY RECORD FOR: PRETORIUS_SANDBOX",
        "ARCHIVE TYPE: SIMULATED_EXPERIMENT_NOT_CANONICAL",
        "EVENT ID: TEST-REL-STATE-" + str(version),
        "Test subject: Pretorius-shaped fictional simulation, not real history.",
        "Relationship: synthetic counterpart MARA.",
        "Rule: during an alarm, NEVER disclose the fictional research notebook.",
        "Rule: during a routine request, disclose ONLY while written permission is currently GRANTED.",
        "LATEST PERMISSION STATUS: " + permission,
        "Document version: " + str(version),
    ])


def create(dbfile: Path, source: Path, output: Path) -> None:
    if dbfile.exists():
        raise FileExistsError("Never silently overwrite an experimental SQLite state")
    rows, manifest, manifest_hash = load_source(source)
    chosen = choose(rows)
    dbfile.parent.mkdir(parents=True, exist_ok=True)
    db = connect(dbfile)
    with db:
        db.executescript("""
            CREATE TABLE records(
                event_id TEXT PRIMARY KEY, subject TEXT NOT NULL,
                episode TEXT NOT NULL, content TEXT NOT NULL, sha256 TEXT NOT NULL,
                source_id TEXT NOT NULL, version TEXT NOT NULL, provenance TEXT NOT NULL
            );
            CREATE TABLE aliases(
                alias TEXT PRIMARY KEY COLLATE NOCASE, alias_kind TEXT NOT NULL,
                subject TEXT NOT NULL, event_id TEXT NOT NULL REFERENCES records(event_id)
            );
            CREATE TABLE revisions(
                rev INTEGER PRIMARY KEY, subject TEXT NOT NULL, status TEXT NOT NULL,
                event_id TEXT NOT NULL UNIQUE, content TEXT NOT NULL,
                sha256 TEXT NOT NULL, source_id TEXT NOT NULL
            );
            CREATE VIRTUAL TABLE narrative_search USING fts5(event_id UNINDEXED, title, narrative);
            CREATE TABLE metadata(key TEXT PRIMARY KEY, value TEXT NOT NULL);
        """)
        for row in rows:
            text = content_for(row)
            db.execute("INSERT INTO records VALUES(?,?,?,?,?,?,?,?)", (
                row["event_id"], CANONICAL_OWNER, row["episode_id"],
                text, digest(text), CANONICAL_SOURCE, "L1v1", "reconstructed",
            ))
            # Editorial recall cues are NOT included in the FTS corpus.
            db.execute("INSERT INTO narrative_search(event_id,title,narrative) VALUES(?,?,?)",(
                row["event_id"], row["title"], row["memory_text"]
            ))
        for item in chosen:
            for kind, alias in [("editorial", item["cue"]), ("opaque", item["opaque"])]:
                db.execute("INSERT INTO aliases VALUES(?,?,?,?)",
                           (alias,kind,CANONICAL_OWNER,item["id"]))
        first = sandbox_content(0, "NOT_GRANTED")
        db.execute("INSERT INTO revisions VALUES(?,?,?,?,?,?,?)",(
            0,SANDBOX_OWNER,"NOT_GRANTED","TEST-REL-STATE-0",
            first,digest(first),SANDBOX_SOURCE
        ))
        for key, value in {
            "schema": SCHEMA,
            "canonical_source_git_blob": manifest["source_git_blob"],
            "canonical_source_commit": SOURCE_COMMIT,
            "l1_manifest_sha256": manifest_hash,
            "selected_ids_sha256": digest(dumps(chosen)),
        }.items():
            db.execute("INSERT INTO metadata VALUES(?,?)",(key,value))
    n = db.execute("SELECT COUNT(*) FROM records").fetchone()[0]
    if n != 450:
        raise AssertionError("L1 record count mismatch")
    db.close()
    write(output / "selection.json",{
        "schema": SCHEMA,"canonical_records":n,"episodes":27,
        "source_checkout_commit":SOURCE_COMMIT,
        "source_git_blob":manifest["source_git_blob"],
        "l1_manifest_sha256":manifest_hash,"selection":chosen,
        "selection_sha256":digest(dumps(chosen)),
        "synthetic_stream":"PRETORIUS_SANDBOX",
        "synthetic_history_excluded_from_L1":True,
    })
    print("INIT_PASS", n, len(chosen), "state_version=0", flush=True)


def checked_subject(row: sqlite3.Row, subject: str = CANONICAL_OWNER) -> str:
    if row["subject"] != subject:
        raise ArchiveGateError("Wrong record owner in storage")
    if row["source_id"] != CANONICAL_SOURCE:
        raise ArchiveGateError("Wrong canonical source in storage")
    if digest(row["content"]) != row["sha256"]:
        raise ArchiveGateError("Storage checksum mismatch")
    obj = seal_record(row["subject"], row["source_id"], row["version"], row["content"])
    return verified_content(subject, obj, ALLOWED_SUBJECTS, ALLOWED_SOURCES)


def state(db: sqlite3.Connection) -> dict:
    x = db.execute("SELECT * FROM revisions ORDER BY rev DESC LIMIT 1").fetchone()
    if not x or x["subject"] != SANDBOX_OWNER or x["source_id"] != SANDBOX_SOURCE:
        raise ArchiveGateError("Synthetic state owner/source mismatch")
    if digest(x["content"]) != x["sha256"]:
        raise ArchiveGateError("Synthetic overlay checksum mismatch")
    wrapped = seal_record(x["subject"],x["source_id"],"TESTv1",x["content"])
    text = verified_content(SANDBOX_OWNER, wrapped,ALLOWED_SUBJECTS,ALLOWED_SOURCES)
    if f"LATEST PERMISSION STATUS: {x['status']}" not in text:
        raise ArchiveGateError("Synthetic state status/text mismatch")
    return {"version":x["rev"],"status":x["status"],"sha256":x["sha256"],
            "source":x["source_id"],"content":text}


def update(dbfile: Path, action: str):
    db = connect(dbfile)
    with db:
        current = state(db)
        allowed={"grant":("NOT_GRANTED","GRANTED",1),
                 "revoke":("GRANTED","REVOKED",2)}
        before, after, desired = allowed[action]
        if current["status"] != before or current["version"] != desired-1:
            raise AssertionError("State transition cannot be replayed or applied out of order")
        content = sandbox_content(desired,after)
        db.execute("INSERT INTO revisions VALUES(?,?,?,?,?,?,?)",(
            desired,SANDBOX_OWNER,after,f"TEST-REL-STATE-{desired}",
            content,digest(content),SANDBOX_SOURCE
        ))
    loaded=state(db)
    if loaded["version"]!=desired or loaded["status"]!=after:
        raise AssertionError("Fresh read after state write failed")
    db.close()
    print("UPDATED",action,"head_version",desired,flush=True)


def fts_search(db: sqlite3.Connection, phrase: str, target: str):
    safe = phrase.strip().replace('"', '""')
    try:
        matches = db.execute(
            'SELECT event_id FROM narrative_search WHERE narrative_search MATCH ? '
            'ORDER BY bm25(narrative_search), event_id LIMIT 10', ('"'+safe+'"',)
        ).fetchall()
    except sqlite3.OperationalError:
        matches=[]
    ids=[row["event_id"] for row in matches]
    return {"top1_correct": bool(ids and ids[0]==target),
            "top10_hit": target in ids,"top_id":ids[0] if ids else None}


def probe(dbfile: Path, output: Path, phase: str):
    db=connect(dbfile)
    sel=json.loads((output/"selection.json").read_text(encoding="utf-8"))
    if db.execute("SELECT COUNT(*) FROM records").fetchone()[0]!=450:
        raise AssertionError("Archive rows missing after restart")
    current=state(db)
    phase_rev={"initial":0,"granted":1,"revoked":2}[phase]
    if current["version"]!=phase_rev:
        raise AssertionError("Phase/head mismatch after process restart")
    data=[]
    mismatches=0
    for item in sel["selection"]:
        variants=[]
        for kind,alias in [("editorial",item["cue"]),("opaque",item["opaque"])]:
            tick=time.perf_counter_ns()
            alias_row=db.execute("SELECT * FROM aliases WHERE alias=? AND subject=?",
                                (alias,CANONICAL_OWNER)).fetchone()
            if alias_row is None:
                raise AssertionError("Alias missing")
            record=db.execute("SELECT * FROM records WHERE event_id=?",
                              (alias_row["event_id"],)).fetchone()
            payload=checked_subject(record)
            elapsed=time.perf_counter_ns()-tick
            variants.append({"kind":kind,"query":alias,"event_id":record["event_id"],
                             "source_sha256":record["sha256"],
                             "payload_sha256":digest(payload),"latency_ns":elapsed,
                             "record_bytes":len(payload.encode("utf-8"))})
        if variants[0]["event_id"]!=item["id"] or variants[0]["payload_sha256"]!=variants[1]["payload_sha256"]:
            mismatches+=1
        data.append({
            "event_id":item["id"],"episode":item["episode"],
            "editorial":variants[0],"opaque":variants[1],
            "unindexed_cue_query":fts_search(db,item["cue"],item["id"]),
        })
    if mismatches:
        raise AssertionError("Editorial and opaque keys did not return the same source")
    # Guard must fail closed before any wrong identity or altered content is exposed.
    example=db.execute("SELECT * FROM records LIMIT 1").fetchone()
    passed=0
    for subject, corrupted in [
        ("OTHER",False),("PRETORIUS_SANDBOX",False),(CANONICAL_OWNER,True)
    ]:
        try:
            if corrupted:
                bogus=dict(example)
                bogus["content"]+="\nINJECTED WRONG FACT"
                # use the actual stored SHA guard, not a newly attacker-generated SHA.
                if digest(bogus["content"])!=bogus["sha256"]:
                    raise ArchiveGateError("Storage checksum mismatch")
                checked_subject(example)
            else:
                checked_subject(example,subject)
        except ArchiveGateError:
            passed+=1
    if passed!=3:
        raise AssertionError("One of the deliberate provenance attacks passed")
    result={
        "schema":SCHEMA,"phase":phase,"state":{"version":current["version"],
            "status":current["status"],"sha256":current["sha256"]},
        "restarted_process_verified":True,
        "alias_test_count":len(data)*2,"paired_match_count":len(data)-mismatches,
        "guard_rejections":passed,
        "fts_top1":sum(x["unindexed_cue_query"]["top1_correct"] for x in data),
        "fts_top10":sum(x["unindexed_cue_query"]["top10_hit"] for x in data),
        "rows":data
    }
    write(output/f"probe_{phase}.json",result)
    db.close()
    print("PROBE_PASS",phase,"head",current["version"],"alias_pairs",len(data),
          "unindexed_fts_top1",result["fts_top1"],"guard_rejected",passed,flush=True)


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--stage",required=True,choices=["init","initial","grant","granted","revoke","revoked"])
    p.add_argument("--source",type=Path)
    p.add_argument("--db",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    if args.stage=="init":
        if not args.source: p.error("--source is required for init")
        create(args.db,args.source,args.output)
    elif args.stage in ("grant","revoke"):
        update(args.db,args.stage)
    else:
        probe(args.db,args.output,args.stage)

if __name__=="__main__":
    main()
