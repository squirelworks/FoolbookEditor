"""Author draws a hidden object and can select it."""

from __future__ import annotations

import unittest

from author.stage import hit, shown


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


if __name__ == "__main__":
    unittest.main()
