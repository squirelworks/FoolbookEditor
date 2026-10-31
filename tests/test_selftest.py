"""``--selftest`` saves and loads a book with no window."""

from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SelftestTests(unittest.TestCase):
    def test_selftest_passes_without_a_display(self):
        env = {k: v for k, v in os.environ.items() if k != "DISPLAY"}
        done = subprocess.run(
            [sys.executable, "-m", "foolbookeditor", "--selftest"],
            cwd=ROOT, env=env, capture_output=True, text=True, timeout=60,
        )
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
        self.assertIn("selftest: ok", done.stdout)

    def test_the_reader_opens_the_saved_book_and_using_foolbook(self):
        done = subprocess.run(
            [sys.executable, "-m", "foolbookeditor", "--selftest"],
            cwd=ROOT, capture_output=True, text=True, timeout=120,
        )
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
        self.assertIn("the reader opens the saved book", done.stdout)
        from foolbookeditor.core import shipped_book
        if shipped_book("using_foolbook") is None:
            self.skipTest("Foolbook's sample books are not installed")
        self.assertIn("the reader opens Using Foolbook", done.stdout)

    def test_a_file_the_reader_cannot_open_is_reported(self):
        import tempfile
        from foolbookeditor.selftest import reader_problems
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.fbk"
            bad.write_bytes(b"FBK1\x00not json")
            self.assertTrue(reader_problems(bad))

    def test_a_missing_script_is_reported(self):
        from foolbookeditor.selftest import problems, sample
        book = sample()
        book["pages"][0]["shapes"][0].pop("script")
        self.assertTrue(any("script" in line for line in problems(book)))


if __name__ == "__main__":
    unittest.main()
