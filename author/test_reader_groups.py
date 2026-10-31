"""A group made in Author reaches Foolbook with its children on the page."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from author.geometry import group
from foolbookeditor.core import pack


class ReaderGroupTests(unittest.TestCase):
    def test_the_pinned_reader_keeps_a_group_s_children_clickable(self):
        from engine.loader import load
        from engine.place import click_target

        shapes = [
            {"kind": "button", "name": "A", "x": 10, "y": 10, "w": 90, "h": 28, "item": {"page": "P1"}},
            {"kind": "button", "name": "B", "x": 10, "y": 50, "w": 90, "h": 28, "item": {"page": "P1"}},
        ]
        self.assertIsNotNone(group(shapes, [0, 1]))
        book = {"id": "g", "title": "Groups", "pages": [{"id": "P0", "shapes": shapes}, {"id": "P1"}]}
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "g.fbk"
            path.write_bytes(pack(book))
            page = load(path).pages[0]
        self.assertEqual([s.get("name") for s in page.shapes], ["A", "B"])
        self.assertEqual(click_target(page.shapes, 20, 60)["name"], "B")


if __name__ == "__main__":
    unittest.main()
