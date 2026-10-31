"""Commands the window binds, run without the window."""

from __future__ import annotations

import unittest

from author import commands


def _book(*ids):
    return {"id": "b", "pages": [{"id": i, "shapes": []} for i in ids]}


class AddPageTests(unittest.TestCase):
    def test_the_new_page_follows_the_current_one(self):
        book = _book("P0", "P100", "P200")
        at = commands.add_page(book, 0)
        self.assertEqual(at, 1)
        self.assertEqual([p["id"] for p in book["pages"]][0], "P0")
        self.assertNotIn(book["pages"][1]["id"], ("P0", "P100", "P200"))
        self.assertEqual([p["id"] for p in book["pages"]][2:], ["P100", "P200"])

    def test_after_the_last_page_it_is_the_end(self):
        book = _book("P0", "P100")
        self.assertEqual(commands.add_page(book, 1), 2)

    def test_an_empty_book_gets_its_first_page(self):
        book = {"pages": []}
        self.assertEqual(commands.add_page(book, -1), 0)
        self.assertEqual(len(book["pages"]), 1)

    def test_the_shortcut_is_written_down(self):
        label, event = commands.SHORTCUTS["add_page"]
        self.assertEqual(label, "Ctrl+M")
        self.assertEqual(event, "<Control-m>")


if __name__ == "__main__":
    unittest.main()
