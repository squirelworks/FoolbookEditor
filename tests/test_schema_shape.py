"""Every shape field the Tk editor writes is written down, and round-trips."""

from __future__ import annotations

import re
import tempfile
import unittest
from pathlib import Path

from author import properties, schema, tools
from author.files import open_book, save
from foolbookeditor.core import read

ROOT = Path(__file__).resolve().parents[1]

# A 1x1 PNG.
PNG = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk"
    "YPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
)

SHAPE = {
    "kind": "image", "name": "Logo", "x": 10, "y": 20, "w": 30, "h": 40, "visible": True,
    "layer": "background", "script": "", "item": {"page": "P200", "label": "Next"},
    "fill": "", "outline": "#071428", "stroke": 2, "tile": [[1, 0], [0, 1]],
    "points": [[10, 20], [40, 60]], "ends": [[10, 20], [40, 20]], "radius": 8, "start": 0, "sweep": 90,
    "text": "", "font": "Arial", "size": 12, "bold": True, "italic": False, "underline": False,
    "align": "center", "border": 1, "editable": False, "preset": "icon",
    "src": "logo.png", "data": PNG, "pixels": [1, 1], "fit": "contain",
    "value": False, "group": "g", "choices": ["One", "Two"],
}


def tool_shapes() -> list[dict]:
    shapes = [tools.new_shape(tool, 0, 0, 50, 50, set()) for tool in tools._KIND]
    for tool, fewest in tools.POINT_TOOLS.items():
        maker = tools.PointDraft(tool)
        for n in range(fewest):
            maker.add(n * 10, n * 7 % 13)
        shapes.append(maker.finish(set()))
    return shapes


class ShapeFieldTests(unittest.TestCase):
    def test_every_key_a_tk_tool_writes_is_listed(self):
        for shape in tool_shapes():
            self.assertLessEqual(set(shape), set(schema.SHAPE_FIELDS), shape["kind"])

    def test_every_kind_a_tk_tool_makes_is_listed(self):
        self.assertLessEqual({s["kind"] for s in tool_shapes()}, set(schema.SHAPE_KINDS))

    def test_every_property_row_writes_only_listed_keys(self):
        typed = {"color": "#102030", "width": "2", "face": "Arial", "points": "12", "flag": "true",
                 "choice": "center", "place": "5", "extent": "20", "pointlist": "0, 0\n10, 10",
                 "jump": "P2", "name": "Shape", "text": "Words"}
        shape = tools.new_shape("button", 0, 0, 50, 50, set())
        for key, _label, kind in properties.ROWS:  # in pane order: the page comes before its book and label
            self.assertTrue(properties.write(shape, key, typed[kind]), key)
            self.assertLessEqual(set(shape), set(schema.SHAPE_FIELDS), key)

    def test_every_shape_field_round_trips(self):
        self.assertEqual(set(SHAPE), set(schema.SHAPE_FIELDS))
        book = {"id": "s", "title": "S", "pages": [{"id": "P0", "text": [], "items": [], "shapes": [dict(SHAPE)]}]}
        with tempfile.TemporaryDirectory() as tmp:
            out = save(Path(tmp) / "s.fbk", book)
            again = open_book(out)["pages"][0]["shapes"][0]
            seen = read(out)["pages"][0]["shapes"][0]
        for field in schema.SHAPE_FIELDS:
            self.assertEqual(again[field], SHAPE[field], field)
            self.assertEqual(seen.get(field), SHAPE[field], field)

    def test_schema_md_names_every_shape_field_and_kind(self):
        text = (ROOT / "schema.md").read_text(encoding="utf-8")
        named = set(re.findall(r"`([a-z]+)`", text))
        self.assertLessEqual(set(schema.SHAPE_FIELDS), named)
        self.assertLessEqual(set(schema.SHAPE_KINDS), named)


if __name__ == "__main__":
    unittest.main()
