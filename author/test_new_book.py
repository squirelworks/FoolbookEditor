"""New book takes a page size and a background colour."""

from __future__ import annotations

import unittest

from author.document import PAGE_SIZE, new_book


class NewBookTests(unittest.TestCase):
    def test_the_default_page_is_640_by_480_and_white(self):
        book = new_book()
        page = book["pages"][0]
        self.assertEqual(PAGE_SIZE, (640, 480))
        self.assertEqual(page["size"], [640, 480])
        paper = page["shapes"][0]
        self.assertEqual(paper["fill"], "#ffffff")
        self.assertEqual(paper["layer"], "background")

    def test_the_paper_covers_the_page_it_was_given(self):
        page = new_book((800, 600), "#F7F4EE")["pages"][0]
        self.assertEqual(page["size"], [800, 600])
        paper = page["shapes"][0]
        self.assertEqual((paper["kind"], paper["x"], paper["y"], paper["w"], paper["h"]), ("rect", 0, 0, 800, 600))
        self.assertEqual(paper["fill"], "#f7f4ee")
        self.assertEqual(paper["outline"], "")

    def test_a_colour_that_is_not_hex_is_refused(self):
        with self.assertRaises(ValueError):
            new_book(color="beige")

    def test_a_page_smaller_than_the_minimum_is_refused(self):
        with self.assertRaises(ValueError):
            new_book((0, 480))


if __name__ == "__main__":
    unittest.main()
