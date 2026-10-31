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

    def test_envelope_keys_and_editor_state_do_not_count(self):
        book = blank_book()
        saved = copy.deepcopy(book)
        book.update({"format": "fbk", "format_version": 1, "foolbook": "x", "_magic": "FBK1"})
        self.assertFalse(is_dirty(saved, book))


if __name__ == "__main__":
    unittest.main()
