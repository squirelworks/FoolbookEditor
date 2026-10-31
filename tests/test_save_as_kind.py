"""Save as picks the kind from the extension. An empty system book is still valid."""

from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from author.files import open_book, save
from foolbookeditor.core import read

BOOK = {"id": "k", "title": "K", "pages": [{"id": "P0", "text": ["x"], "items": [], "shapes": []}]}


class SaveAsKindTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_fbk_is_a_book_and_fsk_is_a_system_book(self):
        self.assertEqual(save(self.tmp / "a.fbk", BOOK).read_bytes()[:4], b"FBK1")
        self.assertEqual(save(self.tmp / "a.fsk", BOOK).read_bytes()[:4], b"FSK1")
        self.assertEqual(save(self.tmp / "b.FSK", BOOK).read_bytes()[:4], b"FSK1")

    def test_no_extension_is_a_book(self):
        out = save(self.tmp / "plain", BOOK)
        self.assertEqual(out.name, "plain.fbk")

    def test_a_system_book_saved_as_fbk_becomes_a_book(self):
        fsk = save(self.tmp / "s.fsk", BOOK)
        out = save(self.tmp / "s.fbk", open_book(fsk))
        self.assertEqual(out.read_bytes()[:4], b"FBK1")
        self.assertEqual(open_book(out)["format"], "fbk")

    def test_an_empty_system_book_is_a_valid_envelope(self):
        out = save(self.tmp / "empty.fsk", {})
        self.assertEqual(out.read_bytes()[:4], b"FSK1")
        self.assertEqual(open_book(out)["format"], "fsk")
        seen = read(out)
        self.assertEqual(seen["handlers"], [])
        self.assertEqual(seen["pages"], [])


if __name__ == "__main__":
    unittest.main()
