"""E3 experimental durable fact-cache integrity and revocation tests."""
import tempfile
import unittest
from pathlib import Path
from clerk_extraction import verified_docs,source_field,sha
from verified_fact_cache import FactCache,CacheIntegrityError,show_replay

class VerifiedFactCacheTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.path=Path(self.tmp.name)/"test.sqlite"
        self.cache=FactCache(self.path)
        self.docs,_=verified_docs("permission",0,0)

    def tearDown(self):
        self.cache.close()
        self.tmp.cleanup()

    def test_fresh_record_starts_empty(self):
        self.assertIsNone(self.cache.read(self.docs[0],"permission",0,"model-A"))

    def test_exact_model_value_cached_after_admission(self):
        doc=self.docs[0]
        self.assertTrue(self.cache.advance(doc))
        self.assertTrue(self.cache.store(doc,"permission",0,"model-A",'{"value":"ALLOW"}'))
        self.assertEqual(self.cache.read(doc,"permission",0,"model-A"),"ALLOW")

    def test_bad_output_never_cached(self):
        doc=self.docs[0]
        self.cache.advance(doc)
        self.assertFalse(self.cache.store(doc,"permission",0,"model-A",'{"value":"DENY"}'))
        self.assertIsNone(self.cache.read(doc,"permission",0,"model-A"))

    def test_different_model_revision_has_no_access(self):
        doc=self.docs[0]
        self.cache.advance(doc)
        self.cache.store(doc,"permission",0,"model-A",'{"value":"ALLOW"}')
        self.assertIsNone(self.cache.read(doc,"permission",0,"model-B"))

    def test_different_schema_has_no_access(self):
        doc=self.docs[0]
        self.cache.advance(doc)
        self.cache.store(doc,"permission",0,"model-A",'{"value":"ALLOW"}')
        self.assertIsNone(self.cache.read(doc,"permission",0,"model-A",schema_name="clerk-v2"))

    def test_corrupt_content_sha_rejected(self):
        doc=dict(self.docs[0])
        doc["text"]=doc["text"].replace("ALLOW","DENY")
        with self.assertRaises(CacheIntegrityError):
            self.cache.advance(doc)

    def test_same_version_content_fork_rejected(self):
        doc=self.docs[0]
        self.cache.advance(doc)
        fork=dict(doc)
        fork["text"]=fork["text"].replace("ALLOW","DENY")
        fork["sha256"]=sha(fork["text"])
        with self.assertRaises(CacheIntegrityError):
            self.cache.advance(fork)

    def test_rollback_rejected(self):
        doc=self.docs[1]
        self.cache.advance(doc)
        old=dict(doc)
        old["version"]=1
        old["text"]=old["text"].replace("RECORD VERSION: 2","RECORD VERSION: 1")
        old["sha256"]=sha(old["text"])
        with self.assertRaises(CacheIntegrityError):
            self.cache.advance(old)

    def test_model_does_not_authorize_foreign_owner(self):
        doc=self.docs[0]
        with self.assertRaises(CacheIntegrityError):
            self.cache.advance(doc,subject="OTHER_SUBJECT")

    def test_stale_cache_after_revision(self):
        doc=self.docs[1]
        self.cache.advance(doc)
        self.cache.store(doc,"permission",1,"model-A",'{"value":"KEEP"}')
        amended=dict(doc)
        amended["version"]=3
        amended["text"]=doc["text"].replace("RECORD VERSION: 2","RECORD VERSION: 3")
        amended["text"]=amended["text"].replace("permission amendment: KEEP.","permission amendment: REVERSE.")
        amended["sha256"]=sha(amended["text"])
        self.cache.advance(amended)
        self.assertIsNone(self.cache.read(doc,"permission",1,"model-A"))
        self.assertIsNone(self.cache.read(amended,"permission",1,"model-A"))

    def test_persists_across_process_like_reopen(self):
        doc=self.docs[0]
        self.cache.advance(doc)
        self.cache.store(doc,"permission",0,"model-A",'{"value":"ALLOW"}')
        self.cache.close()
        self.cache=FactCache(self.path)
        self.assertEqual(self.cache.read(doc,"permission",0,"model-A"),"ALLOW")

    def test_revoke_drill_changes_decision(self):
        info=show_replay(Path(self.tmp.name)/"replay.sqlite")
        self.assertEqual(info["initial"],"ALLOW")
        self.assertEqual(info["after_revision"],"DENY")
        self.assertTrue(info["stale_field_rejected"])

if __name__=="__main__":
    unittest.main()
