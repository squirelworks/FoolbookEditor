"""The window's safe save keeps a system book a system book, as Save does."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from author.files import save_target
from author.safesave import save_safely

BOOK = {"id": "k", "title": "K", "pages": [{"id": "P0", "text": ["x"], "items": [], "shapes": []}]}


class SafeSaveKindTests(unittest.TestCase):
    def test_each_name_is_written_where_save_target_says_and_as_that_kind(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name, magic in (("a.fbk", b"FBK1"), ("s.fsk", b"FSK1"), ("S.FSK", b"FSK1"),
                                ("c.tbk", b"FBK1"), ("d.sbk", b"FSK1")):
                path = Path(tmp) / name
                out = save_safely(path, BOOK)
                self.assertEqual(out, save_target(path), name)
                self.assertEqual(out.read_bytes()[:4], magic, name)

    def test_no_temporary_file_is_left(self):
        with tempfile.TemporaryDirectory() as tmp:
            save_safely(Path(tmp) / "s.fsk", BOOK)
            save_safely(Path(tmp) / "s.fsk", BOOK)
            self.assertEqual(sorted(p.name for p in Path(tmp).iterdir()), ["s.fsk"])


if __name__ == "__main__":
    unittest.main()
