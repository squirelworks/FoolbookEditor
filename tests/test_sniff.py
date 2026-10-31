"""Open sniffs the bytes. The extension is a hint."""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from author.files import open_book, save, save_path_for, sniff
from foolbookeditor.core import compile_script, export_book

BOOK = {"id": "s", "title": "S", "pages": [
    {"id": "P0", "text": ["Hello"], "items": [], "shapes": []},
    {"id": "P100", "text": ["Two"], "items": [], "shapes": []},
]}


class SniffTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def toolbook_named(self, name: str) -> Path:
        # The editor's own .tbk shell writer makes an original ToolBook file.
        shell = export_book(self.tmp / "shell.tbk", BOOK, compile_script)
        return Path(shutil.copy(shell, self.tmp / name))

    def test_fbk_fsk_and_json_open(self):
        fbk = save(self.tmp / "a.fbk", BOOK)
        fsk = save(self.tmp / "a.fsk", {"id": "sys", "handlers": []})
        js = self.tmp / "a.json"
        js.write_text(json.dumps(BOOK), encoding="utf-8")
        self.assertEqual([p["id"] for p in open_book(fbk)["pages"]], ["P0", "P100"])
        self.assertEqual(open_book(fsk)["id"], "sys")
        self.assertEqual(open_book(js)["title"], "S")

    def test_a_toolbook_file_named_fbk_opens_as_toolbook(self):
        renamed = self.toolbook_named("course.fbk")
        self.assertEqual(sniff(renamed), "toolbook")
        self.assertEqual([p["id"] for p in open_book(renamed)["pages"]], ["P0", "P100"])

    def test_an_fbk_named_tbk_opens_as_foolbook(self):
        fbk = save(self.tmp / "b.fbk", BOOK)
        named = Path(shutil.copy(fbk, self.tmp / "b.tbk"))
        self.assertEqual(sniff(named), "foolbook")
        self.assertEqual(open_book(named)["title"], "S")

    def test_save_does_not_write_over_a_renamed_toolbook_file(self):
        renamed = self.toolbook_named("course.fbk")
        self.assertIsNone(save_path_for(renamed))
        self.assertEqual(save_path_for(self.toolbook_named("course.tbk")), self.tmp / "course.fbk")
        self.assertEqual(save_path_for(save(self.tmp / "c.fbk", BOOK)), self.tmp / "c.fbk")


if __name__ == "__main__":
    unittest.main()
