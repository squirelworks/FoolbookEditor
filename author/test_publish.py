"""Publish writes a folder: the .fbk, the linked files that were not embedded, and a one-line README."""

import tempfile
import unittest
from pathlib import Path

from author.publish import linked, publish


def _book():
    return {"id": "b", "title": "Fractions 1", "pages": [
        {"id": "P0", "shapes": [
            {"kind": "image", "src": "art/pie.png"},
            {"kind": "image", "data": "iVBOR"},
            {"kind": "media", "src": "art/pie.png"},
        ]},
        {"id": "P1", "shapes": [{"kind": "media", "src": "sound/ding.wav"},
                                {"kind": "image", "src": "/abs/x.png"},
                                {"kind": "image", "src": "../outside.png"}]},
    ]}


class Publish(unittest.TestCase):
    def test_linked_files_are_relative_srcs_once_each(self):
        self.assertEqual(linked(_book()), ["art/pie.png", "sound/ding.wav"])

    def test_the_folder_holds_the_book_its_links_and_a_readme(self):
        try:
            from author.formats import load
            load  # noqa: B018
        except Exception:
            self.skipTest("saving a book needs Foolbook")
        with tempfile.TemporaryDirectory() as src, tempfile.TemporaryDirectory() as out:
            (Path(src) / "art").mkdir()
            (Path(src) / "art" / "pie.png").write_bytes(b"png")
            written, missing = publish(_book(), out, source=src)
            names = sorted(str(p.relative_to(out)) for p in written)
            self.assertEqual(names, ["Fractions-1.fbk", "README.txt", "art/pie.png", "books.json"])
            self.assertEqual(missing, ["sound/ding.wav"])
            self.assertEqual((Path(out) / "README.txt").read_text().strip(), "Open Fractions-1.fbk with Foolbook.")
            self.assertEqual(load(Path(out) / "Fractions-1.fbk")["title"], "Fractions 1")


if __name__ == "__main__":
    unittest.main()
