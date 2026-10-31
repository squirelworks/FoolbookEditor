"""Right click on a page offers add, duplicate, delete, and properties."""

from __future__ import annotations

import unittest

from author import commands


class PageMenuTests(unittest.TestCase):
    def test_the_page_menu_is_add_duplicate_delete_properties(self):
        self.assertEqual(
            [label for label, _command, _key in commands.page_menu()],
            ["Add page", "Duplicate page", "Delete page", "Properties"],
        )

    def test_each_item_runs_the_command_its_key_runs(self):
        for label, command, key in commands.page_menu():
            if command == "page_properties":
                self.assertEqual(key, "")
                continue
            self.assertTrue(callable(getattr(commands, command)), label)
            self.assertEqual(key, commands.SHORTCUTS[command][0], label)

    def test_add_from_the_menu_puts_the_page_after_the_one_clicked(self):
        book = {"pages": [{"id": "P0"}, {"id": "P100"}, {"id": "P200"}]}
        at = commands.add_page(book, 0)
        self.assertEqual(at, 1)
        self.assertEqual(book["pages"][2]["id"], "P100")


if __name__ == "__main__":
    unittest.main()
