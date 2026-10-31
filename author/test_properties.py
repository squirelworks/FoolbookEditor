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

class ColourWellTests(unittest.TestCase):
    def test_the_well_is_eight_plain_hex_colours(self):
        from author.properties import WELL
        self.assertEqual(len(WELL), 8)
        self.assertEqual(len(set(WELL)), 8)
        for color in WELL:
            self.assertRegex(color, r"^#[0-9a-f]{6}$")

    def test_a_well_colour_and_a_typed_one_both_set_the_fill(self):
        from author.properties import WELL
        shape = {"kind": "rect"}
        self.assertTrue(write(shape, "fill", WELL[3]))
        self.assertEqual(shape["fill"], WELL[3])
        self.assertTrue(write(shape, "fill", "#123abc"))
        self.assertEqual(shape["fill"], "#123abc")

class NoFillTests(unittest.TestCase):
    def test_an_empty_fill_is_no_fill(self):
        button = {"kind": "button", "name": "Next", "fill": "#c0c0c0", "outline": "#000000"}
        self.assertTrue(write(button, "fill", ""))
        self.assertEqual(button["fill"], "")
        self.assertEqual(read(button, "fill"), "")

    def test_an_outline_still_needs_a_colour(self):
        shape = {"kind": "rect", "outline": "#071428"}
        self.assertFalse(write(shape, "outline", ""))
        self.assertEqual(shape["outline"], "#071428")

    def test_a_button_with_no_fill_survives_a_save_and_is_drawn_empty(self):
        from foolbookeditor.core import pack, unpack
        button = {"kind": "button", "name": "Next", "x": 10, "y": 10, "w": 90, "h": 28,
                  "text": "Next", "fill": "#c0c0c0", "outline": "#000000"}
        write(button, "fill", "")
        book = {"id": "nofill", "title": "No fill", "pages": [{"id": "P0", "shapes": [button]}]}
        back = unpack(pack(book, "fbk", compress=False))
        loaded = back["pages"][0]["shapes"][0]
        self.assertEqual(loaded["fill"], "")

        from engine import graphics

        class Canvas:
            calls = []

            def __getattr__(self, name):
                return lambda *a, **k: self.calls.append((name, k))

            def find_all(self):
                return ()

        canvas = Canvas()
        graphics.draw(canvas, [loaded])
        boxes = [k for name, k in canvas.calls if name == "create_rectangle"]
        self.assertEqual(boxes[0]["fill"], "")

class PositionSizeTests(unittest.TestCase):
    def test_typing_left_and_top_moves_the_shape(self):
        shape = {"kind": "rect", "x": 10, "y": 20, "w": 100, "h": 50}
        self.assertTrue(write(shape, "x", "40"))
        self.assertTrue(write(shape, "y", "-5"))
        self.assertEqual((shape["x"], shape["y"], shape["w"], shape["h"]), (40, -5, 100, 50))

    def test_a_polygon_moves_and_sizes_with_its_points(self):
        shape = {"kind": "polygon", "x": 0, "y": 0, "w": 10, "h": 10, "points": [[0, 0], [10, 0], [10, 10]]}
        write(shape, "x", "5")
        self.assertEqual(shape["points"], [[5, 0], [15, 0], [15, 10]])
        write(shape, "w", "20")
        self.assertEqual(shape["points"], [[5, 0], [25, 0], [25, 10]])

    def test_bad_input_leaves_the_old_value(self):
        shape = {"kind": "rect", "x": 10, "y": 20, "w": 100, "h": 50}
        self.assertFalse(write(shape, "x", "left"))
        self.assertFalse(write(shape, "w", "3"))
        self.assertFalse(write(shape, "h", ""))
        self.assertEqual((shape["x"], shape["y"], shape["w"], shape["h"]), (10, 20, 100, 50))
        self.assertEqual(read(shape, "w"), "100")

class PointsTests(unittest.TestCase):
    def test_points_are_one_pair_per_line(self):
        shape = {"kind": "polygon", "points": [[0, 0], [10, 0], [10, 10]]}
        self.assertEqual(read(shape, "points"), "0, 0\n10, 0\n10, 10")

    def test_typed_points_replace_the_outline_and_the_bounds(self):
        shape = {"kind": "polygon", "x": 0, "y": 0, "w": 10, "h": 10, "points": [[0, 0], [10, 0], [10, 10]]}
        self.assertTrue(write(shape, "points", "5, 5\n45 5\n\n25, 35\n"))
        self.assertEqual(shape["points"], [[5, 5], [45, 5], [25, 35]])
        self.assertEqual((shape["x"], shape["y"], shape["w"], shape["h"]), (5, 5, 40, 30))

    def test_bad_points_leave_the_old_ones(self):
        shape = {"kind": "polygon", "points": [[0, 0], [10, 0], [10, 10]]}
        self.assertFalse(write(shape, "points", "0, 0\nten, 0\n10, 10"))
        self.assertFalse(write(shape, "points", "0, 0, 1\n10, 0\n10, 10"))
        self.assertFalse(write(shape, "points", "0, 0\n10, 0"))
        self.assertEqual(shape["points"], [[0, 0], [10, 0], [10, 10]])
        self.assertTrue(write({"kind": "line"}, "points", "0, 0\n10, 0"))


if __name__ == "__main__":
    unittest.main()
