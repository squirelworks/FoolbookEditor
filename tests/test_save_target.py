"""Save writes .fbk, .fsk, or .json. It never writes the file a book was imported from."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from author.document import blank_book
from author.files import save, save_target


class SaveTargetTests(unittest.TestCase):
    def test_the_save_kinds_are_kept(self):
        for name in ("a.fbk", "a.fsk", "a.json", "A.FBK"):
            self.assertEqual(save_target(Path(name)), Path(name))

    def test_imports_are_saved_beside_the_original(self):
        self.assertEqual(save_target(Path("a.tbk")), Path("a.fbk"))
        self.assertEqual(save_target(Path("a.pptx")), Path("a.fbk"))
        self.assertEqual(save_target(Path("a.sbk")), Path("a.fsk"))

    def test_save_after_opening_a_tbk_leaves_the_tbk_alone(self):
        with tempfile.TemporaryDirectory() as tmp:
            tbk = Path(tmp) / "course.tbk"
            tbk.write_bytes(b"not touched")
            out = save(tbk, blank_book())
            self.assertEqual(out, Path(tmp) / "course.fbk")
            self.assertEqual(out.read_bytes()[:4], b"FBK1")
            self.assertEqual(tbk.read_bytes(), b"not touched")

    def test_a_system_book_stays_a_system_book(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = save(Path(tmp) / "shared.fsk", {"id": "shared", "handlers": []})
            self.assertEqual(out.name, "shared.fsk")
            self.assertEqual(out.read_bytes()[:4], b"FSK1")
            self.assertFalse((Path(tmp) / "shared.fbk").exists())


if __name__ == "__main__":
    unittest.main()
