"""A 200-page book with 20 shapes a page opens in under two seconds."""

from __future__ import annotations

import shutil
import tempfile
import time
import unittest
from pathlib import Path

from author.files import open_book, save
from author.sample import large_book
from foolbookeditor.core import read

LIMIT = 2.0


class LargeBookTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp())
        cls.path = save(cls.tmp / "large.fbk", large_book(200, 20))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp)

    def test_the_editor_opens_it_in_time(self):
        start = time.perf_counter()
        book = open_book(self.path)
        took = time.perf_counter() - start
        self.assertEqual(len(book["pages"]), 200)
        self.assertEqual(sum(len(p["shapes"]) for p in book["pages"]), 4000)
        self.assertLess(took, LIMIT, f"editor open took {took:.2f}s")

    def test_the_reader_opens_it_in_time(self):
        start = time.perf_counter()
        book = read(self.path)
        took = time.perf_counter() - start
        self.assertEqual(len(book["pages"]), 200)
        self.assertLess(took, LIMIT, f"reader open took {took:.2f}s")


if __name__ == "__main__":
    unittest.main()
