"""A book says its version. The editor will not save one from the future."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from author.document import blank_book
from author.files import FutureBook, open_book, save, version_of


class VersionTests(unittest.TestCase):
    def test_a_new_book_carries_the_version(self):
        self.assertEqual(blank_book()["fbk"], 1)

    def test_a_future_book_is_refused_and_the_number_is_said(self):
        book = {**blank_book(), "fbk": 7}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "future.fbk"
            with self.assertRaises(FutureBook) as caught:
                save(path, book)
            self.assertIn("7", str(caught.exception))
            self.assertFalse(path.exists())

    def test_an_old_book_with_no_key_opens_and_saves(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "old.json"
            path.write_text('{"id": "old", "pages": [{"id": "P0"}]}', encoding="utf-8")
            book = open_book(path)
            self.assertIsNone(version_of(book))
            out = save(Path(tmp) / "old.fbk", book)
            self.assertEqual(open_book(out)["fbk"], 1)


if __name__ == "__main__":
    unittest.main()
