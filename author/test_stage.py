"""Author draws a hidden object and can select it."""

from __future__ import annotations

import unittest

from author.document import set_size
from author.stage import DEFAULT_SIZE, hit, page_size, shown, view_box


class StageTests(unittest.TestCase):
    def test_a_hidden_field_is_still_drawn(self):
        page = {"shapes": [{"kind": "rect", "name": "Correct", "visible": False, "x": 1, "y": 2, "w": 3, "h": 4}]}
        rows = shown(page)
        self.assertEqual(len(rows), 1)
        self.assertTrue(rows[0]["visible"])
        self.assertEqual(rows[0]["name"], "Correct")

    def test_the_top_object_is_the_one_hit(self):
        shapes = [
            {"x": 0, "y": 0, "w": 100, "h": 100, "name": "page"},
            {"x": 10, "y": 10, "w": 20, "h": 20, "name": "Next"},
        ]
        self.assertEqual(hit(shapes, 12, 12), 1)
        self.assertEqual(hit(shapes, 80, 80), 0)
        self.assertIsNone(hit(shapes, 200, 200))


class PageSizeTests(unittest.TestCase):
    def test_a_page_with_no_size_is_640_by_480(self):
        self.assertEqual(DEFAULT_SIZE, (640, 480))
        self.assertEqual(page_size({}), (640, 480))
        self.assertEqual(page_size({"size": [0, 10]}), (640, 480))

    def test_the_control_stores_the_size_and_rejects_bad_numbers(self):
        page = {"id": "P0"}
        self.assertTrue(set_size(page, "800", 600))
        self.assertEqual(page["size"], [800, 600])
        self.assertFalse(set_size(page, "wide", 600))
        self.assertFalse(set_size(page, -1, 600))
        self.assertEqual(page["size"], [800, 600])
        self.assertEqual(page_size(page), (800, 600))

    def test_the_stage_shows_the_whole_page_even_when_it_is_empty(self):
        self.assertEqual(view_box({"size": [320, 200]}, []), (0, 0, 320, 200))

    def test_a_shape_past_the_edge_is_kept_and_shown(self):
        page = {"size": [320, 200], "shapes": [{"x": 300, "y": 10, "w": 100, "h": 20}]}
        self.assertEqual(view_box(page, page["shapes"]), (0, 0, 400, 200))
        set_size(page, 200, 100)
        self.assertEqual(page["shapes"][0]["x"], 300)


if __name__ == "__main__":
    unittest.main()
