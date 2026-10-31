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

    def test_naming_it_pushes_it_onto_sysbooks_on_enter_book(self):
        book = blank_book()
        set_system(book, "shared.fsk")
        self.assertEqual(book["script"], (
            "to handle enterBook\n"
            '    if "shared.fsk" is not in sysBooks\n'
            '        push "shared.fsk" onto sysBooks\n'
            "    end if\n"
            "end\n"
        ))

    def test_a_new_name_replaces_the_push_and_keeps_the_rest(self):
        book = blank_book()
        book["script"] = 'to handle enterBook\n    x = 1\nend\nto get two\n    return 2\nend\n'
        set_system(book, "one.fsk")
        set_system(book, "two.fsk")
        self.assertEqual(book["script"].count("onto sysBooks"), 1)
        self.assertIn('push "two.fsk" onto sysBooks', book["script"])
        self.assertIn("    x = 1\n", book["script"])
        self.assertIn("to get two", book["script"])

    def test_clearing_it_takes_the_push_out(self):
        book = blank_book()
        set_system(book, "shared.fsk")
        clear_system(book)
        self.assertNotIn("script", book)
        book["script"] = "to handle enterBook\n    x = 1\nend\n"
        set_system(book, "shared.fsk")
        clear_system(book)
        self.assertEqual(book["script"], "to handle enterBook\n    x = 1\nend\n")

    def test_the_reader_runs_the_system_books_handler(self):
        from engine.engine import RuntimeState, enter_book, run_handler
        from engine.loader import load as read_book
        from author.files import save
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / "shared.fsk").write_bytes(pack({"id": "shared", "script": SHARED}, "fsk", compress=False))
            book = blank_book()
            set_system(book, "shared.fsk")
            save(folder / "lesson.fbk", book, compress=False)
            state = RuntimeState(book=read_book(folder / "lesson.fbk"))
            enter_book(state)
            run_handler(state, 'x = echo("hello")')
            self.assertEqual([name for name, _ in state.sysbooks], ["shared.fsk"])
            self.assertEqual(state.variables["x"], "hello")

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
