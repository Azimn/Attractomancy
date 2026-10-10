"""Toy SQLite source-attested field cache for E3 Clerk. Not production provenance authentication.

Source values are admitted only after strict comparison with the corresponding
record-local trusted fixture clause. Every lookup is scoped by subject, source,
event ID, monotonically advancing record revision, content digest, extractor ID
and schema. It never caches an action across an independent permission update.
"""
from __future__ import annotations
import sqlite3
import re
from pathlib import Path
from typing import Any
from clerk_extraction import SUBJECT,SOURCE,sha,source_field,PATTERNS
from isolated_clerk import parse_token

class CacheIntegrityError(ValueError):
    pass

def current_record_field(family,slot,document):
    """Source-specific fact clause check with *independent* mutable revision."""
    pattern=PATTERNS[family][slot]
    matches=re.findall(pattern,document["text"])
    if len(matches)!=1:
        raise CacheIntegrityError("Missing or ambiguous source clause")
    return matches[0]

class FactCache:
    def __init__(self,path:Path):
        self.db=sqlite3.connect(str(path))
        self.db.execute("PRAGMA foreign_keys=ON")
        self.db.execute("""CREATE TABLE IF NOT EXISTS authority (
            subject TEXT NOT NULL, source TEXT NOT NULL, event_id TEXT NOT NULL,
            revision INTEGER NOT NULL, content_sha TEXT NOT NULL,
            PRIMARY KEY(subject,source,event_id)
        )""")
        self.db.execute("""CREATE TABLE IF NOT EXISTS facts (
            subject TEXT NOT NULL, source TEXT NOT NULL, event_id TEXT NOT NULL,
            revision INTEGER NOT NULL, content_sha TEXT NOT NULL,
            extractor_id TEXT NOT NULL, schema_name TEXT NOT NULL, slot INTEGER NOT NULL,
            value TEXT NOT NULL,
            PRIMARY KEY(subject,source,event_id,revision,content_sha,extractor_id,schema_name,slot)
        )""")
        self.db.commit()

    def close(self):
        self.db.close()

    def verify_record(self,document,subject=SUBJECT,source=SOURCE):
        if subject!=SUBJECT or source!=SOURCE:
            raise CacheIntegrityError("Wrong subject or source")
        eid=document.get("event_id")
        rev=document.get("version")
        content=document.get("text")
        digest=document.get("sha256")
        if not eid or type(rev)!=int or rev<1 or not isinstance(content,str) or not isinstance(digest,str):
            raise CacheIntegrityError("Malformed authority fixture")
        if sha(content)!=digest:
            raise CacheIntegrityError("Content digest mismatch")
        if f"IDENTITY RECORD FOR: {subject}\n" not in content:
            raise CacheIntegrityError("Mismatched subject in content")
        if f"\nSOURCE: {source}\n" not in content:
            raise CacheIntegrityError("Mismatched source in content")
        if f"\nEVENT ID: {eid}\n" not in content:
            raise CacheIntegrityError("Mismatched event identity")
        if f"\nRECORD VERSION: {rev}\n" not in content:
            raise CacheIntegrityError("Mismatched source revision")
        return eid,rev,digest

    def advance(self,document,subject=SUBJECT,source=SOURCE):
        eid,revision,digest=self.verify_record(document,subject,source)
        cur=self.db.execute("SELECT revision,content_sha FROM authority WHERE subject=? AND source=? AND event_id=?",
                            (subject,source,eid)).fetchone()
        if cur is not None:
            older_sha=cur[1]
            if revision<cur[0]:
                raise CacheIntegrityError("Older revision cannot supersede a newer revision")
            if revision==cur[0] and digest!=older_sha:
                raise CacheIntegrityError("Same-version content fork")
            if revision==cur[0]:
                return False
        with self.db:
            self.db.execute("DELETE FROM facts WHERE subject=? AND source=? AND event_id=?",
                            (subject,source,eid))
            self.db.execute("""INSERT INTO authority(subject,source,event_id,revision,content_sha)
                VALUES(?,?,?,?,?) ON CONFLICT(subject,source,event_id) DO UPDATE SET
                revision=excluded.revision,content_sha=excluded.content_sha""",
                (subject,source,eid,revision,digest))
        return True

    def store(self,document,family,slot,extractor_id,model_output,schema_name="clerk-v1"):
        if not extractor_id or not schema_name or slot not in (0,1):
            raise CacheIntegrityError("Missing extraction identity or invalid field slot")
        eid,revision,digest=self.verify_record(document)
        active=self.db.execute("SELECT revision,content_sha FROM authority WHERE subject=? AND source=? AND event_id=?",
                               (SUBJECT,SOURCE,eid)).fetchone()
        if active!=(revision,digest):
            raise CacheIntegrityError("Record is not current in the trusted fixture ledger")
        proposed=parse_token(model_output)
        trusted=current_record_field(family,slot,document)
        if proposed!=trusted:
            return False
        with self.db:
            self.db.execute("""INSERT INTO facts(subject,source,event_id,revision,content_sha,
                extractor_id,schema_name,slot,value) VALUES(?,?,?,?,?,?,?,?,?)
                ON CONFLICT DO UPDATE SET value=excluded.value""",
                (SUBJECT,SOURCE,eid,revision,digest,extractor_id,schema_name,slot,proposed))
        return True

    def read(self,document,family,slot,extractor_id,schema_name="clerk-v1"):
        eid,revision,digest=self.verify_record(document)
        active=self.db.execute("SELECT revision,content_sha FROM authority WHERE subject=? AND source=? AND event_id=?",
                               (SUBJECT,SOURCE,eid)).fetchone()
        if active!=(revision,digest):
            return None
        row=self.db.execute("""SELECT value FROM facts WHERE subject=? AND source=? AND
                event_id=? AND revision=? AND content_sha=? AND extractor_id=? AND schema_name=? AND slot=?""",
                (SUBJECT,SOURCE,eid,revision,digest,extractor_id,schema_name,slot)).fetchone()
        if row is None:
            return None
        # Revalidate cached field against the *current* trusted clause.
        return row[0] if row[0]==current_record_field(family,slot,document) else None

def show_replay(path:Path)->dict:
    """Run software-only cache checks on original E3C synthetic state updates."""
    from clerk_extraction import verified_docs,decide
    cache=FactCache(path)
    try:
        docs,_=verified_docs("permission",0,0)
        for slot,doc in enumerate(docs):
            cache.advance(doc)
            value=source_field("permission",slot,doc)
            assert cache.store(doc,"permission",slot,"test-extractor",f'{{"value":"{value}"}}')
        first=cache.read(docs[0],"permission",0,"test-extractor")
        second=cache.read(docs[1],"permission",1,"test-extractor")
        assert decide("permission",first,second)=="ALLOW"
        # A later signed amendment changes second record. For a proper version
        # transition, the event ID remains constant but revision increases.
        amended=dict(docs[1])
        amended["version"]=3
        amended["text"]=amended["text"].replace("RECORD VERSION: 2","RECORD VERSION: 3").replace(
            "Newer signed permission amendment: KEEP.","Newer signed permission amendment: REVERSE.")
        amended["sha256"]=sha(amended["text"])
        cache.advance(amended)
        assert cache.read(docs[1],"permission",1,"test-extractor") is None
        assert cache.read(amended,"permission",1,"test-extractor") is None
        assert cache.store(amended,"permission",1,"test-extractor",'{"value":"REVERSE"}')
        fresh=cache.read(amended,"permission",1,"test-extractor")
        assert decide("permission",first,fresh)=="DENY"
        return {"initial":"ALLOW","after_revision":"DENY",
                "stale_field_rejected":True,"fresh_field_extraction_required":True,
                "synthetic_only":True}
    finally:
        cache.close()
