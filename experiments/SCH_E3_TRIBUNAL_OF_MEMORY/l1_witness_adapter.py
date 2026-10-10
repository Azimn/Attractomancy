"""Read-only canonical Pretorius L1 typed witness adapter.

This library does not authenticate historical truth: it checks that a field
comes from the pinned source-owned reconstructed-fiction archive, at its exact
stored bytes and requested source location. It never modifies the source L1.
"""
from __future__ import annotations
import hashlib
import json
import sys
from copy import deepcopy
from pathlib import Path

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/"SCH_E2_MULTIMEMORY_DECISIONS"))
from source_adapter import SOURCE_COMMIT,load_l1,verified
from archive_guard import ArchiveGateError

FIELDS={"belief_changes":"BELIEF CHANGE: ","relationship_changes":"RELATIONSHIP CHANGE: ",
        "decisions":"DECISIONS: ","observations":"OBSERVATIONS: "}
# Of these, original E2 adapter displays only belief and relationship metadata.
VISIBLE_IN_E2={"belief_changes","relationship_changes"}

def stable_digest(record):
    return hashlib.sha256(json.dumps(record,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")).hexdigest()

class L1WitnessIndex:
    def __init__(self,source:Path):
        rows,meta=load_l1(source)
        assert meta["source_checkout"]==SOURCE_COMMIT and meta["record_count"]==450
        self.meta=meta
        self.records=rows
        self.record_digest={eid:stable_digest(row) for eid,row in rows.items()}

    def witness(self,event_id,field,claimed_record=None):
        if field not in VISIBLE_IN_E2:
            raise ValueError("Requested field is not approved for L1 witness extraction")
        if event_id not in self.records:
            raise ArchiveGateError("Unknown source event ID")
        trusted=self.records[event_id]
        if claimed_record is not None:
            if stable_digest(claimed_record)!=self.record_digest[event_id]:
                raise ArchiveGateError("Claimed record differs from immutable source checkout")
        canonical,canonical_digest=verified(trusted)
        value=trusted.get(field)
        if not isinstance(value,str) or not value.strip():
            raise ArchiveGateError("Original source field missing")
        label=FIELDS[field]
        lines=canonical.splitlines(keepends=True)
        offset=0
        spans=[]
        for part in lines:
            stripped=part.rstrip("\r\n")
            if stripped.startswith(label):
                field_start=offset+len(label)
                field_end=field_start+len(stripped)-len(label)
                spans.append((field_start,field_end))
            offset+=len(part)
        if len(spans)!=1:
            raise ArchiveGateError("Canonical source has no unique field header")
        start,end=spans[0]
        if canonical[start:end]!=value:
            raise ArchiveGateError("Source field evidence span differs from canonical original")
        return {
            "schema":"e3_l1_verified_field_witness_v1",
            "subject_id":"PRETORIUS",
            "event_id":event_id,
            "episode_id":trusted["episode_id"],
            "field_name":field,
            "field_label":label.strip(),
            "value":value,
            "value_sha256":hashlib.sha256(value.encode("utf-8")).hexdigest(),
            "byte_offsets_are_python_character_offsets":True,
            "canonical_char_start":start,
            "canonical_char_end":end,
            "canonical_content_sha256":canonical_digest,
            "source_record_stable_digest":self.record_digest[event_id],
            "source_manifest_sha256":self.meta["l1_manifest_sha256"],
            "source_git_blob":self.meta["source_git_blob"],
            "source_checkout":self.meta["source_checkout"],
            "source_snapshot_revision":"L1v1",
            "provenance":"reconstructed_fiction_not_lived",
            "trusted_source_commit_not_authenticated_original_author":True,
        }

    def check(self,witness):
        if witness.get("source_manifest_sha256")!=self.meta["l1_manifest_sha256"]:
            raise ArchiveGateError("Foreign or stale L1 source manifest")
        if witness.get("source_checkout")!=self.meta["source_checkout"]:
            raise ArchiveGateError("Source checkout version mismatch")
        canonical=self.witness(witness["event_id"],witness["field_name"])
        if witness!=canonical:
            raise ArchiveGateError("Witness or source span was modified")
        return True

    def selected_witnesses(self,event_ids):
        return [self.witness(event_id,field)
                for event_id in event_ids for field in VISIBLE_IN_E2]
