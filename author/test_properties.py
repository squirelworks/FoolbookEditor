"""The property pane writes good values and keeps the old one for bad text."""

from __future__ import annotations

import unittest

from author.properties import ROWS, read, write


class BasicPropertyTests(unittest.TestCase):
    def setUp(self):
        self.shape = {"kind": "rect", "name": "Box", "text": "", "fill": "#f7f4ee", "outline": "#071428"}
        self.page = {"shapes": [self.shape, {"kind": "button", "name": "Next"}]}

    def test_the_pane_has_name_text_fill_outline_and_line_width(self):
        self.assertEqual([row[0] for row in ROWS[:5]], ["name", "text", "fill", "outline", "stroke"])

    def test_line_width_is_stroke_and_defaults_to_1(self):
        self.assertEqual(read(self.shape, "stroke"), "1")
        self.assertTrue(write(self.shape, "stroke", "3", self.page))
        self.assertEqual(self.shape["stroke"], 3)

    def test_a_bad_line_width_leaves_the_old_one(self):
        write(self.shape, "stroke", "2", self.page)
        self.assertFalse(write(self.shape, "stroke", "thick", self.page))
        self.assertFalse(write(self.shape, "stroke", "-1", self.page))
        self.assertEqual(self.shape["stroke"], 2)

    def test_colours_are_hex(self):
        self.assertTrue(write(self.shape, "fill", "#FF0000", self.page))
        self.assertEqual(self.shape["fill"], "#ff0000")
        self.assertFalse(write(self.shape, "outline", "blueish", self.page))
        self.assertEqual(self.shape["outline"], "#071428")

    def test_a_name_another_object_has_is_refused(self):
        self.assertFalse(write(self.shape, "name", "next", self.page))
        self.assertFalse(write(self.shape, "name", "  ", self.page))
        self.assertEqual(self.shape["name"], "Box")
        self.assertTrue(write(self.shape, "name", "Panel", self.page))

    def test_text_keeps_its_lines_and_spaces(self):
        self.assertTrue(write(self.shape, "text", " two\nlines ", self.page))
        self.assertEqual(self.shape["text"], " two\nlines ")


if __name__ == "__main__":
    unittest.main()
