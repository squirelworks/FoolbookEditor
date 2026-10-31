"""The start window offers New book, Open book, the demo, and recent books."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from author.start import GARDEN, NEW, OPEN, RECENT, start_choices


class StartTests(unittest.TestCase):
    def test_new_and_open_come_first(self):
        choices = start_choices([])
        self.assertEqual([c[0] for c in choices], [NEW, OPEN, GARDEN])

    def test_a_recent_book_is_offered_by_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            book = Path(tmp) / "course.fbk"
            book.write_bytes(b"FBK1")
            choices = start_choices([str(book)])
        self.assertEqual(choices[3], (RECENT, book))

    def test_a_missing_recent_book_is_left_out(self):
        choices = start_choices(["/nowhere/gone.fbk"])
        self.assertEqual([c[0] for c in choices], [NEW, OPEN, GARDEN])


    def test_only_five_recent_books(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = []
            for n in range(7):
                p = Path(tmp) / f"b{n}.fbk"
                p.write_bytes(b"FBK1")
                paths.append(str(p))
            choices = start_choices(paths)
        self.assertEqual(len([c for c in choices if c[0] == RECENT]), 5)


if __name__ == "__main__":
    unittest.main()
