"""Book fields round-trip. ``_magic`` is envelope state and is not written."""

from __future__ import annotations

import json
import tempfile
import unittest
import zlib
from pathlib import Path

from author import schema
from author.files import open_book, save
from foolbookeditor.core import read

ROOT = Path(__file__).resolve().parents[1]


def payload_of(path: Path) -> dict:
    blob = path.read_bytes()
    body = blob[5:]
    if blob[4] & 1:
        body = zlib.decompress(body)
    return json.loads(body)


class BookFieldTests(unittest.TestCase):
    def book(self):
        return {
            "id": "b", "title": "Book", "_magic": "FBK1",
            "pages": [{"id": "P0", "text": ["One"], "items": []}],
        }

    def test_book_fields_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = save(Path(tmp) / "b.fbk", self.book())
            again = open_book(out)
        for field in schema.BOOK_FIELDS:
            self.assertEqual(again[field], self.book()[field], field)

    def test_magic_is_not_written_into_the_payload(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = save(Path(tmp) / "b.fbk", self.book())
            self.assertNotIn("_magic", payload_of(out))
            self.assertEqual(out.read_bytes()[:4], b"FBK1")

    def test_the_reader_opens_the_book_with_and_without_magic(self):
        # The web editor's download drops _magic; an older one may not have.
        with tempfile.TemporaryDirectory() as tmp:
            for name, data in (("with", self.book()), ("without", {**self.book()})):
                if name == "without":
                    data.pop("_magic")
                path = Path(tmp) / f"{name}.fbk"
                path.write_bytes(b"FBK1\x00" + json.dumps(data).encode())
                self.assertEqual([p["id"] for p in read(path)["pages"]], ["P0"])

    def test_schema_md_names_every_field(self):
        text = (ROOT / "schema.md").read_text(encoding="utf-8")
        for field in schema.BOOK_FIELDS + schema.NOT_WRITTEN:
            self.assertIn(f"`{field}`", text)


if __name__ == "__main__":
    unittest.main()
