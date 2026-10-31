"""The catalog lists the books in a folder: title, page count, file name."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

from author.shelf import list_books

HAVE_FOOLBOOK = importlib.util.find_spec("foolbook") is not None


@unittest.skipUnless(HAVE_FOOLBOOK, "Foolbook is the core; install it to load and save books")
class ShelfTests(unittest.TestCase):
    def setUp(self):
        from author.document import add_page, new_book
        from foolbookeditor.core import save_book
        self.tmp = tempfile.TemporaryDirectory()
        self.folder = Path(self.tmp.name)
        one = new_book()
        one["title"] = "Bees"
        two = new_book()
        two["title"] = "Ants"
        add_page(two)
        add_page(two)
        save_book(self.folder / "b-bees.fbk", one)
        save_book(self.folder / "a-ants.fbk", two)
        (self.folder / "notes.txt").write_text("not a book")
        (self.folder / "broken.fbk").write_bytes(b"FBK1\x01not zlib")

    def tearDown(self):
        self.tmp.cleanup()

    def test_each_book_has_title_pages_and_file_in_file_order(self):
        rows = [r for r in list_books(self.folder) if not r["error"]]
        self.assertEqual(
            [(r["file"], r["title"], r["pages"]) for r in rows],
            [("a-ants.fbk", "Ants", 3), ("b-bees.fbk", "Bees", 1)],
        )

    def test_a_file_that_is_not_a_book_is_not_listed(self):
        self.assertNotIn("notes.txt", [r["file"] for r in list_books(self.folder)])

    def test_a_book_that_will_not_open_is_listed_and_says_so(self):
        [broken] = [r for r in list_books(self.folder) if r["file"] == "broken.fbk"]
        self.assertTrue(broken["error"])
        self.assertEqual(broken["pages"], 0)

    def test_a_missing_folder_is_an_empty_catalog(self):
        self.assertEqual(list_books(self.folder / "nowhere"), [])


if __name__ == "__main__":
    unittest.main()
