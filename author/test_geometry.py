"""Stage geometry, in page coordinates."""

from __future__ import annotations

import unittest

from author import geometry


class HitTests(unittest.TestCase):
    def test_the_topmost_shape_wins(self):
        shapes = [
            {"kind": "rect", "x": 0, "y": 0, "w": 100, "h": 100},
            {"kind": "button", "x": 10, "y": 10, "w": 20, "h": 20},
        ]
        self.assertEqual(geometry.hit(shapes, 12, 12), 1)
        self.assertEqual(geometry.hit(shapes, 80, 80), 0)
        self.assertIsNone(geometry.hit(shapes, 200, 200))

    def test_background_is_hit_only_when_it_is_the_target(self):
        shapes = [
            {"kind": "rect", "x": 0, "y": 0, "w": 100, "h": 100, "layer": "background"},
            {"kind": "rect", "x": 50, "y": 50, "w": 10, "h": 10},
        ]
        self.assertIsNone(geometry.hit(shapes, 5, 5, "page"))
        self.assertEqual(geometry.hit(shapes, 5, 5, "background"), 0)
        self.assertEqual(geometry.hit(shapes, 55, 55, "background"), 0)
        self.assertEqual(geometry.hit(shapes, 55, 55, "page"), 1)

    def test_a_shape_stored_as_points_is_hit(self):
        triangle = {"kind": "polygon", "points": [[10, 10], [60, 10], [60, 40]]}
        self.assertEqual(geometry.hit([triangle], 30, 20), 0)

    def test_a_line_is_hit_near_its_stroke_not_its_box(self):
        line = {"kind": "line", "x": 0, "y": 0, "w": 100, "h": 100, "points": [[0, 0], [100, 100]]}
        self.assertEqual(geometry.hit([line], 50, 52), 0)
        self.assertIsNone(geometry.hit([line], 90, 10))

    def test_a_flat_line_is_hit(self):
        line = {"kind": "line", "points": [[10, 50], [90, 50]]}
        self.assertEqual(geometry.hit([line], 40, 51), 0)


class MarqueeTests(unittest.TestCase):
    shapes = [
        {"kind": "rect", "x": 0, "y": 0, "w": 20, "h": 20},
        {"kind": "rect", "x": 100, "y": 100, "w": 20, "h": 20},
        {"kind": "line", "points": [[30, 40], [60, 40]]},
        {"kind": "rect", "x": 15, "y": 15, "w": 10, "h": 10, "layer": "background"},
    ]

    def test_every_shape_the_box_meets_is_chosen(self):
        self.assertEqual(geometry.marquee(self.shapes, 10, 10, 50, 50), [0, 2, 3])

    def test_a_backwards_drag_is_the_same_box(self):
        self.assertEqual(geometry.marquee(self.shapes, 50, 50, 10, 10), [0, 2, 3])

    def test_a_flat_line_is_caught_by_its_points(self):
        self.assertEqual(geometry.marquee(self.shapes, 40, 35, 45, 45), [2])

    def test_the_layer_filters(self):
        self.assertEqual(geometry.marquee(self.shapes, 10, 10, 50, 50, "page"), [0, 2])
        self.assertEqual(geometry.marquee(self.shapes, 10, 10, 50, 50, "background"), [3])

    def test_an_empty_box_far_away_chooses_nothing(self):
        self.assertEqual(geometry.marquee(self.shapes, 300, 300, 400, 400), [])


class NudgeTests(unittest.TestCase):
    def test_the_steps_are_one_and_eight(self):
        self.assertEqual((geometry.NUDGE, geometry.NUDGE_BIG), (1, 8))
        self.assertEqual(geometry.arrow_step("Left", False), (-1, 0))
        self.assertEqual(geometry.arrow_step("Down", False), (0, 1))
        self.assertEqual(geometry.arrow_step("Right", True), (8, 0))
        self.assertEqual(geometry.arrow_step("Up", True), (0, -8))

    def test_every_selected_shape_moves_and_keeps_its_size(self):
        shapes = [
            {"kind": "rect", "x": 10, "y": 20, "w": 30, "h": 40},
            {"kind": "line", "points": [[0, 0], [10, 10]]},
            {"kind": "rect", "x": 0, "y": 0, "w": 5, "h": 5},
        ]
        geometry.nudge(shapes, [0, 1], *geometry.arrow_step("Right", True))
        self.assertEqual((shapes[0]["x"], shapes[0]["y"], shapes[0]["w"], shapes[0]["h"]), (18, 20, 30, 40))
        self.assertEqual(shapes[1]["points"], [[8, 0], [18, 10]])
        self.assertNotIn("x", shapes[1])
        self.assertEqual((shapes[2]["x"], shapes[2]["y"]), (0, 0))

    def test_a_shape_named_twice_moves_once(self):
        shapes = [{"x": 0, "y": 0, "w": 5, "h": 5}]
        geometry.nudge(shapes, [0, 0], 1, 0)
        self.assertEqual(shapes[0]["x"], 1)


if __name__ == "__main__":
    unittest.main()
