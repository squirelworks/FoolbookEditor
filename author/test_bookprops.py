"""Book properties are stored on the book, and a bad one changes nothing."""

import unittest

from author.bookprops import properties, set_properties


def _book():
    return {"id": "b", "title": "Old", "pages": [{"id": "P0"}, {"id": "P1"}]}


class BookProperties(unittest.TestCase):
    def test_title_author_size_and_first_page_are_stored(self):
        book = _book()
        set_properties(book, "New", "Ana", "800x600", "P1")
        self.assertEqual((book["title"], book["author"], book["pageSize"], book["firstPage"]),
                         ("New", "Ana", [800, 600], "P1"))
        self.assertEqual(properties(book), {"title": "New", "author": "Ana", "size": "800 x 600", "firstPage": "P1"})

    def test_a_blank_author_or_first_page_is_removed(self):
        book = _book()
        set_properties(book, "New", "Ana", "640 x 480", "P1")
        set_properties(book, "New", "", "640 x 480", "")
        self.assertNotIn("author", book)
        self.assertNotIn("firstPage", book)

    def test_a_bad_size_or_unknown_page_changes_nothing(self):
        for size, first in (("big", ""), ("10 x 10", ""), ("640 x 480", "P9")):
            book = _book()
            with self.assertRaises(ValueError):
                set_properties(book, "New", "Ana", size, first)
            self.assertEqual(book, _book())

    def test_a_new_book_shows_the_default_size(self):
        self.assertEqual(properties({})["size"], "640 x 480")


if __name__ == "__main__":
    unittest.main()
