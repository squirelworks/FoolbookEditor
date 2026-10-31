"""Shape fields round-trip through Save, Open, and the reader."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from author import schema
from author.files import open_book, save
from author.tools import new_shape
from foolbookeditor.core import read

ROOT = Path(__file__).resolve().parents[1]

# A 1x1 PNG. Long enough that the envelope shares it as a #N token.
PNG = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk"
    "YPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
)

SHAPE = {
    "kind": "image", "name": "Logo", "text": "", "x": 10, "y": 20, "w": 30, "h": 40,
    "fill": "", "outline": "#071428", "size": 12, "points": [[10, 20], [40, 60]],
    "item": {"page": "P200", "label": "Next"}, "script": "", "src": "logo.png",
    "data": PNG, "visible": True, "layer": "background",
}


def saved(shapes: list[dict]) -> tuple[dict, dict]:
    book = {"id": "s", "title": "S", "pages": [{"id": "P0", "text": [], "items": [], "shapes": shapes}]}
    with tempfile.TemporaryDirectory() as tmp:
        out = save(Path(tmp) / "s.fbk", book)
        return open_book(out), read(out)


class ShapeFieldTests(unittest.TestCase):
    def test_every_shape_field_round_trips(self):
        self.assertEqual(set(SHAPE), set(schema.SHAPE_FIELDS))
        again, _ = saved([dict(SHAPE)])
        shape = again["pages"][0]["shapes"][0]
        for field in schema.SHAPE_FIELDS:
            self.assertEqual(shape[field], SHAPE[field], field)

    def test_the_reader_keeps_every_shape_field(self):
        _, seen = saved([dict(SHAPE)])
        shape = seen["pages"][0]["shapes"][0]
        for field in schema.SHAPE_FIELDS:
            self.assertEqual(shape.get(field), SHAPE[field], field)

    def test_the_tk_tools_write_only_schema_fields(self):
        for tool in ("button", "text", "box", "line", "ellipse", "polygon", "arc", "picture"):
            shape = new_shape(tool, 0, 0, 50, 50, set())
            extra = set(schema.SHAPE_EXTRA.get(shape["kind"], ()))
            self.assertLessEqual(set(shape), set(schema.SHAPE_FIELDS) | extra, tool)

    def test_schema_md_names_every_shape_field(self):
        text = (ROOT / "schema.md").read_text(encoding="utf-8")
        fields = list(schema.SHAPE_FIELDS)
        for more in schema.SHAPE_EXTRA.values():
            fields += list(more)
        for field in fields:
            self.assertIn(f"`{field}`", text)


if __name__ == "__main__":
    unittest.main()
