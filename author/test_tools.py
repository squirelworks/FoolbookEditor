"""A drag places a button, moves one, or pulls a corner."""

from __future__ import annotations

import unittest

from author.tools import (
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

class RoundRectTests(unittest.TestCase):
    def test_a_rounded_rectangle_has_a_radius_of_8(self):
        shape = new_shape("roundrect", 10, 10, 110, 70, set())
        self.assertEqual(shape["kind"], "roundrect")
        self.assertEqual(shape["radius"], 8)
        self.assertEqual((shape["x"], shape["y"], shape["w"], shape["h"]), (10, 10, 100, 60))
        self.assertEqual((shape["fill"], shape["outline"]), ("#f7f4ee", "#071428"))

class PolygonTests(unittest.TestCase):
    def test_clicks_add_points_and_finish_closes_the_polygon(self):
        from author.tools import PointDraft
        draft = PointDraft("polygon")
        for x, y in ((10, 10), (90, 10), (50, 70)):
            draft.add(x, y)
        draft.add(50, 70)  # the second click of the double-click
        shape = draft.finish(set())
        self.assertEqual(shape["kind"], "polygon")
        self.assertEqual(shape["points"], [[10, 10], [90, 10], [50, 70]])
        self.assertEqual((shape["x"], shape["y"], shape["w"], shape["h"]), (10, 10, 80, 60))

    def test_two_points_are_not_a_polygon(self):
        from author.tools import PointDraft
        draft = PointDraft("polygon")
        draft.add(0, 0)
        draft.add(10, 10)
        self.assertIsNone(draft.finish(set()))

    def test_escape_drops_the_unfinished_polygon_and_keeps_the_tool(self):
        from author.tools import PointDraft, after_escape
        draft = PointDraft("polygon")
        draft.add(0, 0)
        self.assertEqual(after_escape("polygon", draft), "polygon")
        self.assertEqual(after_escape("polygon", None), "select")


if __name__ == "__main__":
    unittest.main()
