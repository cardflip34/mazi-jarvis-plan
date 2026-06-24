import tempfile
import unittest
from pathlib import Path

from mazi_voice.source_registry import RegistryRoot, build_source_registry


class SourceRegistryTests(unittest.TestCase):
    def test_reports_observed_sources_and_gaps(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "ops").mkdir()
            (root / "ops" / "active_bots.json").write_text('{"bots":[]}', encoding="utf-8")
            (root / "ops" / "gemini_identity_updates.jsonl").write_text('{"event":"read"}\n', encoding="utf-8")

            registry = build_source_registry([RegistryRoot(machine="m4", root=root)])

        self.assertEqual(registry["artifacts"]["active_bots"]["status"], "observed")
        self.assertEqual(registry["artifacts"]["gemini_ocr_ledger"]["status"], "observed")
        observed = registry["artifacts"]["gemini_ocr_ledger"]["observed"][0]
        self.assertEqual(observed["machine"], "m4")
        self.assertEqual(observed["relative_path"], "ops/gemini_identity_updates.jsonl")
        self.assertEqual(observed["confidence"], "high")
        self.assertIn("live_append source not located", registry["source_gaps"])


if __name__ == "__main__":
    unittest.main()
