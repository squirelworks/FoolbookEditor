"""A book the web editor downloaded opens in the desktop editor."""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from author.files import EmptyBook, open_book, save

# What editor/editor.js blank() makes, with _magic removed as download() does.
WEB_BOOK = {
    "id": "new",
    "title": "New book",
    "pages": [{
        "id": "P0",
        "text": [""],
        "items": [],
        "shapes": [
            {"kind": "rect", "name": "paper", "x": 0, "y": 0, "w": 640, "h": 480,
             "fill": "#f7f4ee", "outline": "#c8c0b0", "layer": "background"},
            {"kind": "button", "name": "Button", "x": 40, "y": 40, "w": 90, "h": 28,
             "text": "Button", "fill": "#c0c0c0", "outline": "#000000", "layer": "page"},
        ],
    }],
}


def web_bytes(book: dict) -> bytes:
    """FBK1, a zero flags byte, then the JSON, as the web Download writes it."""
    return b"FBK1\x00" + json.dumps(book, separators=(",", ":")).encode("utf-8")


class WebDownloadTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_a_web_download_opens_under_its_own_name(self):
        path = self.tmp / "New book (1).fbk"
        path.write_bytes(web_bytes(WEB_BOOK))
        book = open_book(path)
        self.assertEqual([p["id"] for p in book["pages"]], ["P0"])
        self.assertEqual([s["name"] for s in book["pages"][0]["shapes"]], ["paper", "Button"])

    def test_it_saves_and_opens_again_with_the_same_shapes(self):
        path = self.tmp / "web.fbk"
        path.write_bytes(web_bytes(WEB_BOOK))
        again = open_book(save(self.tmp / "desk.fbk", open_book(path)))
        self.assertEqual(again["pages"][0]["shapes"], WEB_BOOK["pages"][0]["shapes"])

    def test_a_download_with_no_payload_says_so(self):
        path = self.tmp / "broken.fbk"
        path.write_bytes(b"FBK1\x00" + b"\x00" * 200)
        with self.assertRaises(EmptyBook) as caught:
            open_book(path)
        self.assertIn("no book after it", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
