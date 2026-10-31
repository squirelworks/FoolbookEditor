"""The dirty flag is a pure function of the saved book and the current one."""

from __future__ import annotations

import copy
import unittest

from author.document import blank_book
from author.files import is_dirty


class DirtyTests(unittest.TestCase):
    def test_a_book_never_saved_is_dirty(self):
        self.assertTrue(is_dirty(None, blank_book()))

    def test_an_unchanged_book_is_clean(self):
        book = blank_book()
        self.assertFalse(is_dirty(copy.deepcopy(book), book))

    def test_a_change_makes_it_dirty_and_undoing_it_cleans_it(self):
        book = blank_book()
        saved = copy.deepcopy(book)
        book["pages"][0]["text"] = ["Changed"]
        self.assertTrue(is_dirty(saved, book))
        book["pages"][0]["text"] = copy.deepcopy(saved["pages"][0]["text"])
        self.assertFalse(is_dirty(saved, book))

    def test_envelope_keys_do_not_count(self):
        book = blank_book()
        saved = copy.deepcopy(book)
        book.update({"format": "fbk", "format_version": 1, "foolbook": "x"})
        self.assertFalse(is_dirty(saved, book))


class DirtyWindowTests(unittest.TestCase):
    def test_the_title_bar_star_follows_a_change_and_a_save(self):
        try:
            import tkinter as tk
            from unittest import mock
            from author import gui
        except ImportError:
            self.skipTest("no tkinter")
        import tempfile
        from pathlib import Path
        from author.document import new_book
        with mock.patch.object(tk.Tk, "mainloop", lambda self: None), \
                mock.patch.object(gui.Editor, "_start", lambda self, recent: None):
            try:
                ed = gui.Editor(None)
            except tk.TclError:
                self.skipTest("no display")
        try:
            ed._open_new(new_book())
            self.assertFalse(ed.root.title().startswith("*"))
            ed.book["pages"][0]["text"] = ["Changed"]
            ed._preview()
            self.assertTrue(ed.root.title().startswith("*"))
            with tempfile.TemporaryDirectory() as tmp:
                ed.path = Path(tmp) / "d.fbk"
                ed._save()
                self.assertFalse(ed.root.title().startswith("*"))
                self.assertTrue(ed._discard_ok())
        finally:
            ed.root.destroy()


if __name__ == "__main__":
    unittest.main()
