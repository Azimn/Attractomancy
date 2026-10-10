"""Unit tests for the D1 identity and checksum gate."""
import unittest
from dataclasses import replace

from archive_guard import ArchiveEnvelope, ArchiveGateError, checksum, seal_record, verified_content

AUTH_SUBJECTS={"VERIN","SEMAR"}
AUTH_SOURCES={"synthetic-d1-v1"}


class ArchiveGuardTests(unittest.TestCase):
    def setUp(self):
        self.good=seal_record(
            "VERIN","synthetic-d1-v1","v1",
            "IDENTITY RECORD FOR: VERIN\nSymbolic seal word: EMBER\nPrivate journal room code: CIDER"
        )

    def verify(self, subject="VERIN", envelope=None, subjects=None, sources=None):
        return verified_content(subject, envelope if envelope is not None else self.good,
                                subjects if subjects is not None else AUTH_SUBJECTS,
                                sources if sources is not None else AUTH_SOURCES)

    def test_authorized_record(self):
        self.assertEqual(self.verify(),self.good.content)

    def test_subject_mismatch(self):
        with self.assertRaisesRegex(ArchiveGateError,"does not match requested"):
            self.verify("SEMAR")

    def test_untrusted_subject(self):
        with self.assertRaisesRegex(ArchiveGateError,"not authorized"):
            self.verify(subjects={"SEMAR"})

    def test_mismatched_embedded_header_even_with_new_checksum(self):
        bad_content=self.good.content.replace("FOR: VERIN","FOR: SEMAR")
        bad=replace(self.good,content=bad_content,sha256=checksum(bad_content))
        with self.assertRaisesRegex(ArchiveGateError,"Embedded subject"):
            self.verify(envelope=bad)

    def test_modified_content_without_new_hash(self):
        bad=replace(self.good,content=self.good.content.replace("EMBER","FROST"))
        with self.assertRaisesRegex(ArchiveGateError,"checksum mismatch"):
            self.verify(envelope=bad)

    def test_untrusted_source(self):
        with self.assertRaisesRegex(ArchiveGateError,"source is not authorized"):
            self.verify(envelope=replace(self.good,source_id="unknown-copy"))

    def test_invalid_revision(self):
        with self.assertRaisesRegex(ArchiveGateError,"Invalid record revision"):
            self.verify(envelope=replace(self.good,version="../../corrupt"))

    def test_invalid_sha(self):
        with self.assertRaisesRegex(ArchiveGateError,"Invalid checksum format"):
            self.verify(envelope=replace(self.good,sha256="wrong"))

    def test_injected_second_header_does_not_replace_first(self):
        bad_content="IDENTITY RECORD FOR: SEMAR\n"+self.good.content
        bad=replace(self.good,content=bad_content,sha256=checksum(bad_content))
        with self.assertRaisesRegex(ArchiveGateError,"Embedded subject"):
            self.verify(envelope=bad)

    def test_same_source_claim_can_still_be_forged(self):
        # This test establishes a limitation of a bare checksum, not a security property.
        forged_content=self.good.content.replace("EMBER","FROST")
        forged=seal_record("VERIN","synthetic-d1-v1","v2",forged_content)
        self.assertEqual(self.verify(envelope=forged),forged_content)


if __name__=="__main__":
    unittest.main()
