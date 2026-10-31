"""A .tbk imports as a book the editor can save, with a report of what was left behind."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from author.importer import import_book, report, report_text
from foolbookeditor.core import export_book, pack, unpack


def _grouped_page() -> dict:
    """The page as Foolbook hands it back: a group arrives as loose, tagged objects."""
    return {"id": "P0", "shapes": [
        {"kind": "rect", "name": "a", "groups": ["Answers"]},
        {"kind": "text", "name": "b", "groups": ["Answers"]},
        {"kind": "curve", "name": "wave", "points": [[0, 0], [10, 10], [20, 0]]},
        {"kind": "arc", "name": "bow"},
    ], "handlers": [{"name": "buttonClick", "source": ""}]}


class ImportReport(unittest.TestCase):
    def test_a_group_is_named_in_the_report(self):
        text = report_text(report({"pages": [_grouped_page()]}))
        self.assertIn("group Answers is not kept as a group", text)
        self.assertIn("2 objects", text)

    def test_a_curve_and_an_arc_are_named(self):
        text = report_text(report({"pages": [_grouped_page()]}))
        self.assertIn("curve wave is not drawn", text)
        self.assertIn("arc bow is drawn as the ellipse of its bounds", text)
        self.assertIn("handler buttonClick has no source", text)

    def test_a_tbk_imports_and_is_not_written_back(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "lesson.tbk"
            export_book(src, {"id": "lesson", "title": "Lesson", "pages": [
                {"id": "P0", "text": ["One"]}, {"id": "P100", "text": ["Two"]},
            ]})
            before = src.read_bytes()
            book, lines = import_book(src)
            self.assertEqual(src.read_bytes(), before)
        self.assertEqual([p["id"] for p in book["pages"]], ["P0", "P100"])
        self.assertEqual(book["imported_from"], "lesson.tbk")
        self.assertTrue(lines)
        again = unpack(pack(book))
        self.assertEqual([p["id"] for p in again["pages"]], ["P0", "P100"])


if __name__ == "__main__":
    unittest.main()
