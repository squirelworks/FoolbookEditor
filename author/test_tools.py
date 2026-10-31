"""A drag places a button, moves one, or pulls a corner."""

from __future__ import annotations

import unittest

from author.tools import (
    next_fit,
    handle_at,
    move_shape,
    new_shape,
    opposite,
    page_point,
    resize_shape,
    snapshot,
)


class ToolTests(unittest.TestCase):
    def test_a_click_places_a_button(self):
        shape = new_shape("button", 10, 20, 10, 20, set())
        self.assertEqual(shape["kind"], "button")
        self.assertEqual(shape["name"], "Button")
        self.assertEqual(shape["x"], 10)
        self.assertGreater(shape["w"], 8)

    def test_a_backwards_drag_keeps_the_top_left(self):
        shape = new_shape("box", 200, 100, 40, 30, set())
        self.assertEqual(shape["kind"], "rect")
        self.assertEqual((shape["x"], shape["y"]), (40, 30))
        self.assertEqual((shape["w"], shape["h"]), (160, 70))

    def test_the_second_button_gets_another_name(self):
        shape = new_shape("button", 0, 0, 90, 28, {"Button"})
        self.assertEqual(shape["name"], "Button2")

    def test_a_window_pixel_becomes_a_page_point(self):
        view = {"scale": 2, "ox": 10, "oy": 20, "x0": 0, "y0": 0}
        self.assertEqual(page_point(view, 30, 40), (10, 10))

    def test_a_drag_moves_the_object_and_its_points(self):
        shape = {"x": 10, "y": 20, "w": 30, "h": 40, "points": [[10, 20], [40, 60]]}
        move_shape(shape, snapshot(shape), 5, -2)
        self.assertEqual((shape["x"], shape["y"]), (15, 18))
        self.assertEqual(shape["points"][1], [45, 58])

    def test_pulling_a_corner_leaves_the_opposite_one(self):
        shape = {"x": 10, "y": 20, "w": 100, "h": 50}
        stay = opposite(shape, "se")
        self.assertEqual(stay, (10, 20))
        resize_shape(shape, snapshot(shape), stay[0], stay[1], 80, 90)
        self.assertEqual((shape["x"], shape["y"]), (10, 20))
        self.assertEqual((shape["w"], shape["h"]), (70, 70))

    def test_the_corner_under_the_pointer_is_the_one_named(self):
        shape = {"x": 0, "y": 0, "w": 100, "h": 40}
        view = {"scale": 1, "ox": 0, "oy": 0, "x0": 0, "y0": 0}
        self.assertEqual(handle_at(view, shape, 100, 40), "se")
        self.assertIsNone(handle_at(view, shape, 50, 20))


class SelectTests(unittest.TestCase):
    def test_select_is_the_tool_author_starts_with(self):
        from author.tools import DEFAULT_TOOL
        self.assertEqual(DEFAULT_TOOL, "select")

    def test_escape_returns_to_select(self):
        from author.tools import after_escape
        for tool in ("button", "text", "box", "line", "ellipse", "polygon", "arc", "picture", "select"):
            self.assertEqual(after_escape(tool), "select")

class RectangleTests(unittest.TestCase):
    def test_a_new_rectangle_is_paper_with_an_ink_outline(self):
        shape = new_shape("box", 0, 0, 100, 60, set())
        self.assertEqual(shape["kind"], "rect")
        self.assertEqual(shape["fill"], "#f7f4ee")
        self.assertEqual(shape["outline"], "#071428")

    def test_a_label_is_a_text_shape_with_no_border(self):
        shape = new_shape("label", 10, 20, 10, 20, set())
        self.assertEqual(shape["kind"], "text")
        self.assertEqual(shape["preset"], "label")
        self.assertEqual(shape["name"], "Label")
        self.assertEqual(shape["text"], "Label")
        self.assertEqual(shape["fill"], "")
        # The reader draws no frame for border 1, the ToolBook "none" style.
        self.assertEqual(shape["border"], 1)

    def test_a_field_is_not_a_label(self):
        self.assertNotIn("preset", new_shape("text", 0, 0, 160, 36, set()))

    def test_a_field_is_one_the_student_types_into(self):
        self.assertIs(new_shape("text", 0, 0, 160, 36, set())["editable"], True)

    def test_a_label_is_not_typed_into(self):
        self.assertIs(new_shape("label", 0, 0, 120, 24, set())["editable"], False)

    def test_a_checkbox_starts_off_with_a_caption(self):
        shape = new_shape("check", 0, 0, 0, 0, set())
        self.assertEqual((shape["kind"], shape["name"], shape["text"]), ("check", "Check", "Check"))
        self.assertIs(shape["value"], False)

    def test_radios_placed_one_after_another_share_a_group(self):
        first = new_shape("radio", 0, 0, 0, 0, set())
        second = new_shape("radio", 0, 30, 0, 30, {"Radio"})
        self.assertEqual((first["kind"], second["name"]), ("radio", "Radio2"))
        self.assertEqual(first["group"], second["group"])
        self.assertIs(first["value"], False)

    def test_a_list_box_starts_with_three_choices_and_none_chosen(self):
        shape = new_shape("list", 0, 0, 0, 0, set())
        self.assertEqual((shape["kind"], shape["name"]), ("list", "List"))
        self.assertEqual(shape["choices"], ["First", "Second", "Third"])
        self.assertNotIn("value", shape)
        self.assertEqual(shape["text"], "")

    def test_a_combo_box_is_one_row_high_and_closed(self):
        shape = new_shape("combo", 0, 0, 0, 0, set())
        self.assertEqual((shape["kind"], shape["name"], shape["h"]), ("combo", "Combo", 22))
        self.assertEqual(shape["choices"], ["First", "Second", "Third"])
        self.assertNotIn("open", shape)

    def test_fit_steps_from_fill_to_contain_to_none_and_back(self):
        picture = new_shape("picture", 0, 0, 0, 0, set())
        self.assertNotIn("fit", picture)
        self.assertEqual(next_fit(picture), "contain")
        self.assertEqual(next_fit(picture), "none")
        self.assertEqual(next_fit(picture), "fill")
        self.assertEqual(picture["fit"], "fill")

    def test_fit_leaves_a_shape_that_is_not_a_picture(self):
        box = new_shape("box", 0, 0, 0, 0, set())
        self.assertIsNone(next_fit(box))
        self.assertNotIn("fit", box)


if __name__ == "__main__":
    unittest.main()
