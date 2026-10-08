#!/usr/bin/env python3
"""Audit Attractomancy's versioned CSV research catalog. Python standard library only.

Run from the repository root:
    python scripts/audit_catalog.py

Exit status 0 means structural checks passed; it does not validate scholarly
claims, link accessibility, licenses, actual capture completeness, or provenance
assertions made by third-party sources.
"""
from __future__ import annotations

import csv
import hashlib
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qsl, unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATASETS = {
    "source": ("source_catalog.csv", "id"),
    "edges": ("source_graph_edges.csv", "edge_id"),
    "pairs": ("named_pair_registry.csv", "pair_id"),
    "pair_edges": ("pair_graph_edges.csv", "pair_edge_id"),
    "procedures": ("reproducible_procedure_index.csv", "procedure_id"),
    "versions": ("version_lineage.csv", "lineage_id"),
    "duplicate_reviews": ("duplicate_url_review.csv", "review_id"),
    "preservation_reviews": ("preservation_claim_review.csv", "source_id"),
    "retrieval": ("retrieval_log.csv", "batch_id"),
    "captures": ("repository_capture_manifest.csv", "capture_id"),
    "scope_reviews": ("source_scope_review.csv", "source_id"),
}
README_METRICS = {
    "data/source_catalog.csv": "source",
    "data/source_graph_edges.csv": "edges",
    "data/named_pair_registry.csv": "pairs",
    "data/pair_graph_edges.csv": "pair_edges",
    "data/reproducible_procedure_index.csv": "procedures",
    "data/version_lineage.csv": "versions",
    "data/repository_capture_manifest.csv": "captures",
}


def normalized_url(value: str) -> str:
    """Normalize for duplicate *review*, not for rewriting source URLs."""
    if not value.startswith(("http://", "https://")):
        return value.strip()
    u = urlsplit(value)
    host = (u.hostname or "").lower().removeprefix("www.")
    path = unquote(u.path).rstrip("/").lower()
    query = sorted((k, v) for k, v in parse_qsl(u.query) if not k.lower().startswith("utm_"))
    return host + path + ("?" + repr(query) if query else "")


def read_csv(name: str, errors: list[str]) -> list[dict[str, str]]:
    path = DATA / name
    if not path.is_file():
        errors.append(f"Missing dataset: {path.relative_to(ROOT)}")
        return []
    with path.open(newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        if not reader.fieldnames:
            errors.append(f"{name}: missing CSV header")
            return []
        rows = []
        for line, row in enumerate(reader, start=2):
            if None in row or any(v is None for v in row.values()):
                errors.append(f"{name}: row starting near line {line} has wrong column count")
            rows.append(row)
        return rows


def valid_utc(value: str) -> bool:
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return dt.tzinfo is not None and dt.utcoffset().total_seconds() == 0
    except (ValueError, TypeError, AttributeError):
        return False


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    data = {key: read_csv(name, errors) for key, (name, _) in DATASETS.items()}

    for key, (_, id_col) in DATASETS.items():
        values = [r.get(id_col, "") for r in data[key]]
        if not values or all(not value for value in values):
            # The retrieval-log header may use 'batch_id' or a different stable name.
            if key == "retrieval" and data[key]:
                header = list(data[key][0])
                id_col = header[0]
                values = [r.get(id_col, "") for r in data[key]]
            else:
                errors.append(f"{key}: missing or empty ID column {id_col}")
                continue
        bad = [x for x in values if not x]
        if bad:
            errors.append(f"{key}: {len(bad)} blank IDs")
        repeated = [x for x, n in Counter(values).items() if n > 1 and x]
        if repeated:
            errors.append(f"{key}: duplicate IDs: {', '.join(repeated[:8])}")

    sources = data["source"]
    ids = {r.get("id", "") for r in sources}
    pairs = {r.get("pair_id", "") for r in data["pairs"]}

    expected = {f"S{i:03d}" for i in range(1, len(sources) + 1)}
    if ids != expected:
        errors.append(f"Source-ID sequence has {len(expected - ids)} gaps and {len(ids - expected)} out-of-sequence IDs")

    allowed_status = {"recovered", "verified", "lead", "unavailable", "superseded", "local-only"}
    allowed_preservation = {"A", "B", "C", "D"}
    allowed_confidence = {"high", "medium", "low"}
    for r in sources:
        source_id = r.get("id", "<unknown>")
        if r.get("status") not in allowed_status:
            errors.append(f"{source_id}: invalid status {r.get('status')!r}")
        if r.get("preservation_level") not in allowed_preservation:
            errors.append(f"{source_id}: invalid legacy A-D preservation level {r.get('preservation_level')!r}")
        if r.get("confidence") not in allowed_confidence:
            errors.append(f"{source_id}: invalid confidence {r.get('confidence')!r}")
        if not r.get("title", "").strip():
            errors.append(f"{source_id}: missing title")
        if not valid_utc(r.get("retrieved_at_utc", "")):
            errors.append(f"{source_id}: retrieval time is not UTC ISO 8601")

    def source_ref(ref: str, where: str) -> None:
        if ref and ref not in ids:
            errors.append(f"{where}: unknown source {ref}")

    for r in data["edges"]:
        edge = r.get("edge_id", "<unknown>")
        for key in ("from_id", "to_id", "evidence_source_id"):
            source_ref(r.get(key, ""), f"{edge}.{key}")
    for r in data["pairs"]:
        source_ref(r.get("source_id", ""), r.get("pair_id", "?"))
    for r in data["pair_edges"]:
        edge = r.get("pair_edge_id", "<unknown>")
        for key in ("from_pair_id", "to_pair_id"):
            if r.get(key) not in pairs:
                errors.append(f"{edge}.{key}: unknown pair {r.get(key)!r}")
        source_ref(r.get("evidence_source_id", ""), edge)
    for r in data["procedures"]:
        source_ref(r.get("source_id", ""), r.get("procedure_id", "?"))
    for r in data["versions"]:
        for key in ("earlier_source_id", "later_source_id", "evidence_source_id"):
            source_ref(r.get(key, ""), f"{r.get('lineage_id', '?')}.{key}")

    # Verify saved evidence from the repository checkout, including file content.
    scoped_sources = set()
    for r in data["captures"]:
        capture_id = r.get("capture_id", "?")
        sid = r.get("source_id", "")
        source_ref(sid, capture_id)
        scoped_sources.add(sid)
        path_text = r.get("repository_path", "")
        rel = Path(path_text)
        if not path_text or rel.is_absolute() or ".." in rel.parts:
            errors.append(f"{capture_id}: invalid capture path {path_text!r}")
            continue
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"{capture_id}: missing capture {path_text}")
            continue
        payload = path.read_bytes()
        digest = hashlib.sha1(b"blob " + str(len(payload)).encode("ascii") + b"\0" + payload).hexdigest()
        if digest != r.get("git_blob_sha1", "").lower():
            errors.append(f"{capture_id}: Git blob mismatch for {path_text}")
        if r.get("capture_kind") not in {"readme_license", "primary_text", "metadata_only"}:
            errors.append(f"{capture_id}: unknown capture kind")
        if r.get("capture_scope") not in {
            "partial_repository_documentation", "single_primary_document", "metadata_only"
        }:
            errors.append(f"{capture_id}: invalid capture scope")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", r.get("verified_date_utc", "")):
            errors.append(f"{capture_id}: invalid verification date")

    partial_a = {
        r["id"] for r in sources
        if r.get("preservation_level") == "A"
        and r["id"] in scoped_sources
        and "repository" in r.get("source_type", "").lower()
    }
    if "S263" in scoped_sources:
        partial_a.add("S263")
    scoped_reviews = {r.get("source_id", "") for r in data["scope_reviews"]}
    if partial_a - scoped_reviews:
        errors.append(f"{len(partial_a - scoped_reviews)} partial A-level captures missing scope review")
    for r in data["scope_reviews"]:
        source_ref(r.get("source_id", ""), "source_scope_review")
        if r.get("review_status") != "partial_source_capture":
            errors.append(f"{r.get('source_id')}: invalid source-scope review status")

    url_groups: dict[str, set[str]] = defaultdict(set)
    for r in sources:
        if r.get("url", "").strip():
            url_groups[normalized_url(r["url"])].add(r["id"])
    actual_duplicates = {frozenset(v) for v in url_groups.values() if len(v) > 1}
    reviewed = set()
    for r in data["duplicate_reviews"]:
        a, b = r.get("first_source_id", ""), r.get("second_source_id", "")
        source_ref(a, r.get("review_id", "?"))
        source_ref(b, r.get("review_id", "?"))
        reviewed.add(frozenset((a, b)))
        if r.get("canonical_source_id") not in {a, b}:
            errors.append(f"{r.get('review_id', '?')}: invalid canonical source ID")
        if r.get("resolution_status") not in {"resolved_alias", "resolved_distinct_component"}:
            errors.append(f"{r.get('review_id', '?')}: duplicate resolution is open/invalid")
        if r.get("identity_relation") not in {
            "same_artifact_alias", "same_thread_analytical_alias", "distinct_component_of_thread"
        }:
            errors.append(f"{r.get('review_id', '?')}: invalid duplicate relationship")
    unreviewed = actual_duplicates - reviewed
    stale = reviewed - actual_duplicates
    if unreviewed:
        errors.append(f"{len(unreviewed)} URL-duplicate groups have no explicit review record: {sorted(map(sorted, unreviewed))}")
    if stale:
        warnings.append(f"{len(stale)} duplicate-review entries no longer correspond to normalized URL duplicates")
    if actual_duplicates:
        warnings.append(f"{len(actual_duplicates)} duplicate-URL groups have recorded identity resolutions; IDs retained")

    # Legacy A claims full preservation. Missing catalog pointers are a review
    # obligation, not proof that a copy does not exist elsewhere.
    unlocated_a = {r["id"] for r in sources if r.get("preservation_level") == "A" and not r.get("local_artifact", "").strip()}
    queued_a = {r.get("source_id", "") for r in data["preservation_reviews"]}
    if unlocated_a - queued_a:
        errors.append(f"{len(unlocated_a - queued_a)} A-level records with no artifact locator are not in preservation_claim_review.csv")
    if queued_a - unlocated_a:
        warnings.append(f"{len(queued_a - unlocated_a)} A-level preservation reviews may now be resolved or obsolete")
    if unlocated_a:
        warnings.append(f"{len(unlocated_a)} A-level records have no catalog artifact locator; manual preservation audit pending")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    start_token = "<!-- ATTRACTOMANCY_STATUS_START -->"
    end_token = "<!-- ATTRACTOMANCY_STATUS_END -->"
    if readme.count(start_token) != 1 or readme.count(end_token) != 1:
        errors.append("README must have exactly one current inventory block")
    else:
        summary = readme.split(start_token, 1)[1].split(end_token, 1)[0]
        for filename, key in README_METRICS.items():
            match = re.search(r"\|[^\n|]*`" + re.escape(filename) + r"`[^\n|]*\|\s*(\d+)\s*\|", summary)
            if not match:
                errors.append(f"README current inventory has no count for {filename}")
            elif int(match.group(1)) != len(data[key]):
                errors.append(f"README {filename}: says {match.group(1)}, actual {len(data[key])}")

    print("Attractomancy catalog audit")
    for key in ("source", "edges", "pairs", "pair_edges", "procedures", "versions"):
        print(f"  {key:13s} {len(data[key]):4d}")
    print(f"  captures      {len(data['captures']):4d} (file hash checked)")
    print(f"  URL duplicates {len(actual_duplicates):4d} (resolved)")
    for warning in warnings:
        print("WARNING:", warning)
    for error in errors:
        print("ERROR:", error, file=sys.stderr)
    print("RESULT:", "PASS" if not errors else f"FAIL ({len(errors)} errors)")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
