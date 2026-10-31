"""The author writes the book's menu bar as an outline and it is stored in the book."""

import unittest

from author import menubar

OUTLINE = 'Go\n  Contents -> P0\n  Glossary: go to page "Glossary"\nHelp\n  About -> P9'


class MenuBar(unittest.TestCase):
    def test_an_outline_becomes_menus_of_page_and_script_items(self):
        bar = menubar.parse(OUTLINE)
        self.assertEqual([m["label"] for m in bar], ["Go", "Help"])
        self.assertEqual(bar[0]["items"][0], {"label": "Contents", "page": "P0"})
        self.assertEqual(bar[0]["items"][1]["script"],
                         'to handle buttonClick\n  go to page "Glossary"\nend')

    def test_the_outline_reads_back_the_same(self):
        self.assertEqual(menubar.render(menubar.parse(OUTLINE)), OUTLINE)

    def test_the_bar_is_stored_in_the_book_and_an_empty_outline_removes_it(self):
        book = {"pages": []}
        menubar.set_menubar(book, OUTLINE)
        self.assertEqual(book["menubar"][1]["items"], [{"label": "About", "page": "P9"}])
        menubar.set_menubar(book, "")
        self.assertNotIn("menubar", book)

    def test_an_item_with_nowhere_to_go_is_refused(self):
        for bad in ("  Lost -> P0", "Go\n  Lost", "Go\n  -> P0", "Go\n  Empty:", "Go\n  Lost -> "):
            with self.assertRaises(ValueError, msg=bad):
                menubar.parse(bad)


if __name__ == "__main__":
    unittest.main()
