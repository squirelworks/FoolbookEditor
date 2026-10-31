"""A save that fails part way leaves the previous file as it was."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from author.safesave import save_safely
from foolbookeditor.core import load


def _book(title: str) -> dict:
    return {"id": "safe", "title": title, "pages": [{"id": "P0", "text": [title]}]}


class SafeSave(unittest.TestCase):
    def test_a_save_replaces_the_book(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "safe.fbk"
            save_safely(path, _book("First"))
            save_safely(path, _book("Second"))
            self.assertEqual(load(path)["title"], "Second")
            self.assertEqual(sorted(p.name for p in Path(tmp).iterdir()), ["safe.fbk"])

    def test_a_failed_replace_keeps_the_old_file(self):
        def broken(_src, _dst):
            raise OSError("disk pulled out")

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "safe.fbk"
            save_safely(path, _book("First"))
            before = path.read_bytes()
            with self.assertRaises(OSError):
                save_safely(path, _book("Second"), replace=broken)
            self.assertEqual(path.read_bytes(), before)
            self.assertEqual(sorted(p.name for p in Path(tmp).iterdir()), ["safe.fbk"])

    def test_a_failed_write_keeps_the_old_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "safe.fbk"
            save_safely(path, _book("First"))
            before = path.read_bytes()
            with self.assertRaises(TypeError):
                save_safely(path, {"id": "safe", "pages": [{"id": "P0", "bad": object()}]})
            self.assertEqual(path.read_bytes(), before)
            self.assertEqual(sorted(p.name for p in Path(tmp).iterdir()), ["safe.fbk"])


if __name__ == "__main__":
    unittest.main()
