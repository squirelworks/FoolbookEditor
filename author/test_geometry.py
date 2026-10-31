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


if __name__ == "__main__":
    unittest.main()
