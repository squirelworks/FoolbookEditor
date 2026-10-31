"""Background shapes stay on the page and are written under the page shapes."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from author.files import open_book, save
from foolbookeditor.core import read

ROOT = Path(__file__).resolve().parents[1]


def shape(name: str, layer: str | None) -> dict:
    s = {"kind": "rect", "name": name, "x": 0, "y": 0, "w": 10, "h": 10}
    if layer:
        s["layer"] = layer
    return s


class BackgroundLayerTests(unittest.TestCase):
    def page(self):
        return {"id": "P0", "text": [], "items": [], "shapes": [
            shape("title", "page"), shape("paper", "background"),
            shape("note", None), shape("frame", "background"),
        ]}

    def test_save_writes_background_shapes_first(self):
        book = {"id": "b", "title": "B", "pages": [self.page()]}
        with tempfile.TemporaryDirectory() as tmp:
            out = save(Path(tmp) / "b.fbk", book)
            names = [s["name"] for s in open_book(out)["pages"][0]["shapes"]]
            painted = [s["name"] for s in read(out)["pages"][0]["shapes"]]
        self.assertEqual(names, ["paper", "frame", "title", "note"])
        self.assertEqual(painted, names)

    def test_the_book_in_the_editor_is_not_reordered(self):
        book = {"id": "b", "title": "B", "pages": [self.page()]}
        with tempfile.TemporaryDirectory() as tmp:
            save(Path(tmp) / "b.fbk", book)
        self.assertEqual([s["name"] for s in book["pages"][0]["shapes"]], ["title", "paper", "note", "frame"])

    def test_the_decision_is_written_down(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Backgrounds live on the page, for now", text)


if __name__ == "__main__":
    unittest.main()
