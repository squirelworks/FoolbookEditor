"""A drag places a button. A backwards drag still starts at the top left."""

from __future__ import annotations

import unittest

from author.tools import new_shape, page_point


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


if __name__ == "__main__":
    unittest.main()
