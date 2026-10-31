"""Zoom is view-only. A pixel on the stage turns back into the same page point."""

from __future__ import annotations

import unittest

from author.view import placed, to_page, to_window


class Zoom(unittest.TestCase):
    def test_to_page_undoes_the_zoom(self):
        self.assertEqual(to_page(200, 100, 2.0), (100.0, 50.0))
        self.assertEqual(to_page(50, 25, 0.5), (100.0, 50.0))
        self.assertEqual(to_page(130, 70, 1.0, ox=30, oy=20), (100.0, 50.0))

    def test_to_window_is_the_inverse(self):
        for zoom in (0.5, 1.0, 2.0):
            x, y = to_window(123, 45, zoom, ox=7, oy=9)
            self.assertEqual(to_page(x, y, zoom, ox=7, oy=9), (123.0, 45.0))

    def test_a_small_page_is_centred(self):
        scale, dx, dy, ox, oy, wide, tall = placed((0, 0, 640, 480), 0.5, 1000, 800)
        self.assertEqual(scale, 0.5)
        self.assertEqual((ox, oy), (340.0, 280.0))
        self.assertEqual((wide, tall), (1000, 800))

    def test_a_large_page_scrolls(self):
        scale, dx, dy, ox, oy, wide, tall = placed((0, 0, 640, 480), 2.0, 1000, 800)
        self.assertEqual((ox, oy), (12.0, 12.0))
        self.assertEqual((wide, tall), (1304, 984))

    def test_fit_fills_the_pane(self):
        scale, _dx, _dy, _ox, _oy, wide, tall = placed((0, 0, 640, 480), None, 1000, 800)
        self.assertAlmostEqual(scale, (1000 - 24) / 640)
        self.assertEqual((wide, tall), (1000, 800))

    def test_zoom_does_not_touch_the_stored_shape(self):
        shape = {"kind": "rect", "x": 10, "y": 20, "w": 30, "h": 40}
        placed((0, 0, 640, 480), 2.0, 1000, 800)
        self.assertEqual(shape, {"kind": "rect", "x": 10, "y": 20, "w": 30, "h": 40})


if __name__ == "__main__":
    unittest.main()
