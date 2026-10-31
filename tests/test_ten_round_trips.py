"""An editor book saved and opened ten times is the same book (item 94).

The envelope carries no timestamp, so the bytes match too, compressed or not.
The book uses a shared background, a background-layer shape, a quiz, a
picture, a jump, a script, and the drawing kinds with angles and points.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from author.files import ENVELOPE, open_book, save


def _book() -> dict:
    return {
        "title": "Ten trips",
        "foolbook": 1,
        "firstPage": "P1",
        "pageSize": [640, 480],
        "pages": [
            {"id": "Back", "background": True, "shapes": [
                {"kind": "rect", "name": "paper", "x": 0, "y": 0, "w": 640, "h": 480, "fill": "#f7f4ee"},
            ]},
            {"id": "P1", "uses": "Back", "name": "Start", "size": [640, 480], "text": ["One", "Two"],
             "script": "to handle enterPage\n  n = 1\nend\n",
             "quiz": {"version": 1, "question": "Two and two?", "choices": [
                 {"label": "Four", "correct": True}, {"label": "Five", "correct": False}],
                 "feedback_right": "Yes.", "feedback_wrong": "No."},
             "shapes": [
                {"kind": "rect", "name": "band", "x": 0, "y": 0, "w": 640, "h": 40, "fill": "#071428", "layer": "background"},
                {"kind": "roundrect", "name": "card", "x": 20, "y": 60, "w": 200, "h": 100, "radius": 8,
                 "fill": "", "outline": "#071428", "stroke": 2},
                {"kind": "arc", "name": "arc", "x": 240, "y": 60, "w": 80, "h": 60, "start": 0, "sweep": 180},
                {"kind": "polygon", "name": "tri", "points": [[10, 300], [60, 250], [110, 300]]},
                {"kind": "text", "name": "words", "x": 20, "y": 180, "w": 200, "h": 40,
                 "text": "Hello\nthere", "font": "Helvetica", "size": 12, "bold": True, "align": "center"},
                {"kind": "button", "name": "next", "x": 500, "y": 420, "w": 90, "h": 28, "text": "Next",
                 "item": {"page": "P2"}, "script": "go to next page\n"},
                {"kind": "image", "name": "dot", "x": 300, "y": 300, "w": 1, "h": 1,
                 "data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="},
                {"kind": "hotspot", "name": "spot", "x": 400, "y": 100, "w": 50, "h": 50, "visible": False},
             ]},
            {"id": "P2", "shapes": []},
        ],
    }


def _content(book: dict) -> dict:
    return {k: v for k, v in book.items() if k not in ENVELOPE}


class TenRoundTrips(unittest.TestCase):
    def _trips(self, compress: bool):
        with tempfile.TemporaryDirectory() as tmp:
            path = save(Path(tmp) / "ten.fbk", _book(), compress=compress)
            first_bytes = path.read_bytes()
            first = _content(open_book(path))
            for trip in range(10):
                book = open_book(path)
                path = save(path, book, compress=compress)
                self.assertEqual(_content(open_book(path)), first, f"dict changed on trip {trip + 1}")
                self.assertEqual(path.read_bytes(), first_bytes, f"bytes changed on trip {trip + 1}")
        return first

    def test_ten_trips_uncompressed_keep_the_dict_and_the_bytes(self):
        book = self._trips(compress=False)
        self.assertEqual([p["id"] for p in book["pages"]], ["Back", "P1", "P2"])

    def test_ten_trips_compressed_keep_the_dict_and_the_bytes(self):
        self._trips(compress=True)

    def test_what_the_editor_wrote_is_what_comes_back(self):
        book = self._trips(compress=False)
        wrote = _book()
        page = {p["id"]: p for p in book["pages"]}["P1"]
        self.assertEqual(page["quiz"], wrote["pages"][1]["quiz"])
        self.assertEqual({s["name"] for s in page["shapes"]}, {s["name"] for s in wrote["pages"][1]["shapes"]})


if __name__ == "__main__":
    unittest.main()
