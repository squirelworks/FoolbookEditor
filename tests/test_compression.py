"""Save writes compressed or not. Compressed is the default."""

from __future__ import annotations

import inspect
import shutil
import tempfile
import unittest
from pathlib import Path

from author.files import is_compressed, open_book, save

BOOK = {"id": "c", "title": "C", "pages": [{"id": "P0", "text": ["x"], "items": [], "shapes": []}]}


class CompressionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_the_default_is_compressed(self):
        self.assertIs(inspect.signature(save).parameters["compress"].default, True)
        out = save(self.tmp / "a.fbk", BOOK)
        self.assertEqual(out.read_bytes()[4], 1)
        self.assertTrue(is_compressed(out))

    def test_uncompressed_saves_and_opens(self):
        out = save(self.tmp / "a.fbk", BOOK, compress=False)
        self.assertEqual(out.read_bytes()[4], 0)
        self.assertFalse(is_compressed(out))
        self.assertEqual(open_book(out)["pages"][0]["text"], ["x"])

    def test_json_and_web_downloads_open_as_uncompressed(self):
        js = self.tmp / "a.json"
        js.write_text('{"id": "j"}', encoding="utf-8")
        web = self.tmp / "web.fbk"
        web.write_bytes(b'FBK1\x00{"id": "w"}')
        self.assertFalse(is_compressed(js))
        self.assertFalse(is_compressed(web))


if __name__ == "__main__":
    unittest.main()
