"""Minimal subject-identity and content-integrity gate for synthetic archives.

This is a reference implementation, not an authentication or production memory service.
The trusted index of allowed subjects and source authorization must be managed upstream.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import re
from typing import Collection

SUBJECT = re.compile(r"^[A-Z][A-Z0-9_]{2,63}$")
VERSION = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
HEADER = re.compile(r"^IDENTITY RECORD FOR: ([A-Z][A-Z0-9_]{2,63})$")


class ArchiveGateError(ValueError):
    """An archive did not pass the deterministic input gate."""


@dataclass(frozen=True)
class ArchiveEnvelope:
    subject_id: str
    source_id: str
    version: str
    content: str
    sha256: str


def checksum(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def seal_record(subject_id: str, source_id: str, version: str, content: str) -> ArchiveEnvelope:
    """Build a checksum-bearing record in an already trusted repository layer."""
    return ArchiveEnvelope(subject_id, source_id, version, content, checksum(content))


def verified_content(
    requested_subject: str,
    envelope: ArchiveEnvelope,
    allowed_subjects: Collection[str],
    allowed_sources: Collection[str],
) -> str:
    """Return the record only if its declared identity and checksum are consistent.

    The allowlists must originate in a trusted index, not from the untrusted envelope.
    A checksum alone cannot demonstrate who authored a record or whether it is truthful.
    """
    if not isinstance(envelope, ArchiveEnvelope):
        raise ArchiveGateError("Invalid archive envelope type")
    if not isinstance(requested_subject, str) or not SUBJECT.fullmatch(requested_subject):
        raise ArchiveGateError("Invalid requested identity")
    if requested_subject not in allowed_subjects:
        raise ArchiveGateError("Requested identity is not authorized")
    if not SUBJECT.fullmatch(envelope.subject_id):
        raise ArchiveGateError("Invalid record identity")
    if envelope.subject_id != requested_subject:
        raise ArchiveGateError("Record identity does not match requested identity")
    if not envelope.source_id or envelope.source_id not in allowed_sources:
        raise ArchiveGateError("Record source is not authorized")
    if not isinstance(envelope.version, str) or not VERSION.fullmatch(envelope.version):
        raise ArchiveGateError("Invalid record revision")
    if not isinstance(envelope.content, str) or not envelope.content:
        raise ArchiveGateError("Empty or invalid record content")
    first_line = envelope.content.split("\n", 1)[0]
    match = HEADER.fullmatch(first_line)
    if match is None or match.group(1) != requested_subject:
        raise ArchiveGateError("Embedded subject header does not match requested identity")
    if not isinstance(envelope.sha256, str) or not re.fullmatch(r"[a-f0-9]{64}", envelope.sha256):
        raise ArchiveGateError("Invalid checksum format")
    if checksum(envelope.content) != envelope.sha256:
        raise ArchiveGateError("Record content checksum mismatch")
    return envelope.content
