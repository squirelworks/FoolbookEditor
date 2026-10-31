"""The status line shows the first error in a script. Save is not blocked."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from author.catalog import set_object_script
from author.scripts import first_error, status


class ScriptCheckTests(unittest.TestCase):
    def test_a_good_script_has_no_error(self):
        self.assertEqual(first_error('go to page "P2"'), "")

    def test_the_first_error_has_its_line(self):
        self.assertEqual(first_error('n = 1\ngo to\nif then'), "Error: line 2: go to needs a page. Saved anyway.")

    def test_an_error_comes_before_a_warning(self):
        self.assertTrue(status('flash\ngo to').startswith("Error: line 2"))
        self.assertTrue(status('flash').startswith("Warning: line 1"))

    def test_a_script_with_an_error_is_still_saved(self):
        from foolbookeditor.core import load, save_book
        book = {"title": "t", "pages": [{"id": "P1", "shapes": [{"kind": "button", "name": "b"}]}]}
        set_object_script(book["pages"][0], 0, "go to\n")
        self.assertTrue(first_error(book["pages"][0]["shapes"][0]["script"]))
        with tempfile.TemporaryDirectory() as tmp:
            path = save_book(Path(tmp) / "b.fbk", book)
            loaded = load(path)
        self.assertIn("go to", loaded["pages"][0]["shapes"][0]["script"])


if __name__ == "__main__":
    unittest.main()
