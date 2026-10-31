"""A page book names one system book. An .fsk opens as a book of handlers."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from author.document import blank_book, clear_system, handler_names, set_system, system_of
from author.formats import load
from foolbookeditor.core import pack

SHARED = """to handle goEnd
    go to page "P200"
end
to get echo word
    return word
end
"""


class SystemBook(unittest.TestCase):
    def test_a_book_names_its_system_book(self):
        book = blank_book()
        set_system(book, " shared.fsk ")
        self.assertEqual(system_of(book), "shared.fsk")
        clear_system(book)
        self.assertNotIn("system", book)

    def test_only_a_system_book_can_be_named(self):
        book = blank_book()
        with self.assertRaises(ValueError):
            set_system(book, "lesson.fbk")
        self.assertIsNone(system_of(book))

    def test_an_fsk_opens_as_handlers_and_no_pages(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "shared.fsk"
            path.write_bytes(pack({"id": "shared", "script": SHARED}, "fsk", compress=False))
            book = load(path)
        self.assertEqual(handler_names(book), ["goEnd", "echo"])
        self.assertEqual(book.get("pages") or [], [])


if __name__ == "__main__":
    unittest.main()
