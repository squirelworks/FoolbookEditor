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


class HotspotStageTests(unittest.TestCase):
    def test_a_hotspot_is_placed_with_no_fill(self):
        from author.tools import new_shape
        shape = new_shape("hotspot", 10, 10, 90, 70, set())
        self.assertEqual((shape["kind"], shape["fill"]), ("hotspot", ""))

    def test_author_draws_a_hotspot_as_an_outline(self):
        page = {"shapes": [{"kind": "hotspot", "name": "Door", "x": 1, "y": 2, "w": 30, "h": 40, "fill": "",
                            "outline": "#071428", "item": {"page": "P200"}}]}
        row = shown(page)[0]
        self.assertEqual(row["kind"], "rect")
        self.assertEqual((row["fill"], row["outline"]), ("", "#071428"))
        self.assertEqual(row["item"], {"page": "P200"})
        self.assertEqual(page["shapes"][0]["kind"], "hotspot")

class GhostTests(unittest.TestCase):
    def test_a_hidden_object_is_drawn_ghosted_and_the_book_keeps_it_hidden(self):
        page = {"shapes": [{"kind": "rect", "name": "Answer", "visible": False, "fill": "#000000",
                            "outline": "#071428", "x": 0, "y": 0, "w": 10, "h": 10}]}
        row = shown(page)[0]
        self.assertTrue(row["ghost"])
        self.assertEqual(row["fill"], "#b2b2b2")
        self.assertNotEqual(row["outline"], "#071428")
        self.assertIs(page["shapes"][0]["visible"], False)
        self.assertEqual(page["shapes"][0]["fill"], "#000000")

    def test_the_visible_flag_reads_true_when_missing_and_hides_when_false(self):
        from author.properties import read, write
        shape = {"kind": "rect"}
        self.assertEqual(read(shape, "visible"), "true")
        self.assertTrue(write(shape, "visible", "false"))
        self.assertIs(shape["visible"], False)
        self.assertEqual(read(shape, "visible"), "false")


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
