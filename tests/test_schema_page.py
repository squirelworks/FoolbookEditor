"""Page fields round-trip through Save, Open, and the reader."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from author import schema
from author.document import blank_page
from author.files import open_book, save
from foolbookeditor.core import read

ROOT = Path(__file__).resolve().parents[1]

PAGE = {
    "id": "P100",
    "text": ["First paragraph.", "Second paragraph."],
    "items": [{"label": "Next", "page": "P200"}],
    "shapes": [{"kind": "rect", "x": 0, "y": 0, "w": 10, "h": 10}],
    "script": "to handle enterPage\n  go to next page\nend\n",
    "name": "Opening",
    "size": [800, 600],
}


class PageFieldTests(unittest.TestCase):
    def test_every_page_field_round_trips(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = save(Path(tmp) / "p.fbk", {"id": "b", "title": "B", "pages": [dict(PAGE)]})
            again = open_book(out)["pages"][0]
        self.assertEqual(set(PAGE), set(schema.PAGE_FIELDS))
        for field in schema.PAGE_FIELDS:
            self.assertEqual(again[field], PAGE[field], field)

    def test_the_reader_sees_the_page(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = save(Path(tmp) / "p.fbk", {"id": "b", "title": "B", "pages": [dict(PAGE)]})
            seen = read(out)["pages"][0]
        self.assertEqual(seen["id"], "P100")
        self.assertEqual(seen["text"], PAGE["text"])
        self.assertEqual(len(seen["shapes"]), 1)
        self.assertEqual(seen["size"], [800, 600])
        self.assertEqual([h["name"] for h in seen["handlers"]], ["enterPage"])

    def test_a_new_page_has_shapes_not_widgets(self):
        page = blank_page("P0")
        self.assertEqual(page["shapes"], [])
        self.assertNotIn("widgets", page)
        self.assertIsInstance(page["text"], list)

    def test_schema_md_names_every_page_field(self):
        text = (ROOT / "schema.md").read_text(encoding="utf-8")
        for field in schema.PAGE_FIELDS:
            self.assertIn(f"`{field}`", text)


if __name__ == "__main__":
    unittest.main()
