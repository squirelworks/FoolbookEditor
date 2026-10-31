"""What a drop on the program hands over, and what the README promises."""

from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from author.drop import paths_from

README = Path(__file__).resolve().parents[1] / "README.md"


class DropTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_files_are_kept_in_order_and_the_rest_left_out(self):
        a = self.tmp / "a.fbk"
        b = self.tmp / "b.tbk"
        a.write_bytes(b"x")
        b.write_bytes(b"x")
        raw = ["--desktop", str(self.tmp), str(self.tmp / "gone.fbk"), str(b), str(a), ""]
        self.assertEqual(paths_from(raw), [b, a])

    def test_the_readme_says_which_platforms_work(self):
        text = README.read_text(encoding="utf-8")
        self.assertIn("Dropping a book onto the open window does nothing anywhere", text)
        for platform in ("Windows", "Linux", "macOS"):
            self.assertIn(platform, text)


if __name__ == "__main__":
    unittest.main()
