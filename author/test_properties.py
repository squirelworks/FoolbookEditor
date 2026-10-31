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


class FontPropertyTests(unittest.TestCase):
    def setUp(self):
        self.shape = {"kind": "text", "name": "Title", "text": "Hello"}

    def test_face_size_and_styles_are_set(self):
        self.assertTrue(write(self.shape, "font", "Georgia"))
        self.assertTrue(write(self.shape, "size", "18"))
        for key in ("bold", "italic", "underline"):
            self.assertTrue(write(self.shape, key, "true"))
        self.assertEqual(
            {k: self.shape[k] for k in ("font", "size", "bold", "italic", "underline")},
            {"font": "Georgia", "size": 18, "bold": True, "italic": True, "underline": True},
        )
        self.assertTrue(write(self.shape, "italic", "false"))
        self.assertIs(self.shape["italic"], False)

    def test_alignment_is_left_center_or_right(self):
        self.assertEqual(read(self.shape, "align"), "left")
        self.assertTrue(write(self.shape, "align", "center"))
        self.assertEqual(self.shape["align"], "center")
        self.assertFalse(write(self.shape, "align", "justify"))
        self.assertEqual(self.shape["align"], "center")

    def test_a_tbk_number_reads_as_its_word(self):
        self.assertEqual(read({"align": 2}, "align"), "center")
        self.assertEqual(read({"align": 1}, "align"), "right")

    def test_a_bad_size_keeps_the_old_one(self):
        write(self.shape, "size", "12")
        self.assertFalse(write(self.shape, "size", "big"))
        self.assertFalse(write(self.shape, "size", "0"))
        self.assertEqual(self.shape["size"], 12)

    def test_an_empty_face_falls_back_to_the_reader_face(self):
        write(self.shape, "font", "Georgia")
        self.assertTrue(write(self.shape, "font", ""))
        self.assertNotIn("font", self.shape)


if __name__ == "__main__":
    unittest.main()
