"""Apply script checks the page script the same way as an object script."""

from __future__ import annotations

import unittest

from author.scripts import apply


def _page() -> dict:
    return {"id": "P1", "shapes": [{"kind": "button", "name": "b"}]}


class PageScriptCheckTests(unittest.TestCase):
    def test_a_page_script_error_is_shown_with_its_line(self):
        page = _page()
        note = apply(page, None, "n = 1\ngo to\n")
        self.assertTrue(note.startswith("Error: line 2"), note)

    def test_a_page_script_with_an_error_is_still_kept(self):
        page = _page()
        apply(page, None, "go to\n")
        self.assertIn("go to", page["script"])

    def test_a_page_script_word_the_reader_does_not_run_is_a_warning(self):
        page = _page()
        self.assertTrue(apply(page, None, "flash\n").startswith("Warning: line 1"))

    def test_a_good_page_script_says_nothing(self):
        page = _page()
        self.assertEqual(apply(page, None, 'go to page "P2"\n'), "")

    def test_an_object_script_is_checked_as_before(self):
        page = _page()
        self.assertTrue(apply(page, 0, "go to\n").startswith("Error: line 1"))
        self.assertIn("go to", page["shapes"][0]["script"])


if __name__ == "__main__":
    unittest.main()
