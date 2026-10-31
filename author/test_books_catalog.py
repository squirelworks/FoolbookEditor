"""A published folder lists its books in books.json: title, file, and page count."""

import json
import tempfile
import unittest
from pathlib import Path

from author.publish import write_catalog


class BooksCatalog(unittest.TestCase):
    def test_each_book_has_one_line_and_others_stay(self):
        with tempfile.TemporaryDirectory() as out:
            write_catalog(out, {"title": "One", "pages": [{}, {}]}, "one.fbk")
            write_catalog(out, {"title": "Two", "pages": [{}]}, "two.fbk")
            write_catalog(out, {"title": "One again", "pages": [{}, {}, {}]}, "one.fbk")
            data = json.loads((Path(out) / "books.json").read_text())
            self.assertEqual(data, {"books": [
                {"title": "Two", "file": "two.fbk", "pages": 1},
                {"title": "One again", "file": "one.fbk", "pages": 3},
            ]})

    def test_an_unreadable_catalog_is_replaced(self):
        with tempfile.TemporaryDirectory() as out:
            (Path(out) / "books.json").write_text("not json")
            write_catalog(out, {"title": "One", "pages": []}, "one.fbk")
            self.assertEqual(json.loads((Path(out) / "books.json").read_text())["books"][0]["file"], "one.fbk")


if __name__ == "__main__":
    unittest.main()
