"""The page list's small drawings, as data."""

from __future__ import annotations

import unittest

from author.thumbs import SIZE, miniature


class MiniatureTests(unittest.TestCase):
    def test_an_empty_page_is_just_the_page(self):
        ops = miniature({"id": "P0"})
        self.assertEqual(len(ops), 1)
        kind, coords, _fill, _outline = ops[0]
        self.assertEqual(kind, "page")
        self.assertEqual(coords, (0.0, 0.0, 96.0, 72.0))
        self.assertEqual(SIZE, (96, 72))

    def test_shapes_are_scaled_and_kept_in_paint_order(self):
        page = {"size": [640, 480], "shapes": [
            {"kind": "rect", "x": 0, "y": 0, "w": 320, "h": 240, "fill": "#ff0000"},
            {"kind": "ellipse", "x": 320, "y": 240, "w": 320, "h": 240},
            {"kind": "line", "points": [[0, 480], [640, 0]]},
            {"kind": "polygon", "points": [[0, 0], [320, 0], [320, 240]], "fill": "#00ff00"},
        ]}
        ops = miniature(page)
        self.assertEqual([op[0] for op in ops], ["page", "rect", "oval", "line", "polygon"])
        self.assertEqual(ops[1][1], (0.0, 0.0, 48.0, 36.0))
        self.assertEqual(ops[1][2], "#ff0000")
        self.assertEqual(ops[2][1], (48.0, 36.0, 96.0, 72.0))
        self.assertEqual(ops[3][1], (0.0, 72.0, 96.0, 0.0))
        self.assertEqual(ops[4][1], (0.0, 0.0, 48.0, 0.0, 48.0, 36.0))

    def test_a_hidden_shape_is_left_out(self):
        page = {"shapes": [{"kind": "rect", "x": 1, "y": 1, "w": 5, "h": 5, "visible": False}]}
        self.assertEqual(len(miniature(page)), 1)

    def test_a_tall_page_fits_by_height(self):
        ops = miniature({"size": [240, 480]})
        self.assertEqual(ops[0][1], (0.0, 0.0, 36.0, 72.0))


if __name__ == "__main__":
    unittest.main()
