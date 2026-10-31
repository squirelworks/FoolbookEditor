"""Author lists every object, including one Reader hides."""

from __future__ import annotations

import unittest

from author.catalog import objects_of, page_ids, page_script, place_shape, restack, set_object_script


class CatalogTests(unittest.TestCase):
    def test_page_order_is_the_book_order(self):
        book = {"pages": [{"id": "P400"}, {"id": "P410"}, {"id": "P420"}]}
        self.assertEqual(page_ids(book), ["P400", "P410", "P420"])

    def test_a_hidden_field_stays_in_the_list(self):
        page = {"shapes": [
            {"kind": "rect", "name": "Correct", "visible": False, "x": 1, "y": 2, "w": 3, "h": 4,
             "script": "to handle buttonClick\nend\n"},
            {"kind": "polygon", "name": "", "bounds": [10, 20, 30, 40]},
        ]}
        rows = objects_of(page)
        self.assertEqual(len(rows), 2)
        self.assertTrue(rows[0]["hidden"])
        self.assertEqual(rows[0]["name"], "Correct")
        self.assertEqual(rows[1]["bounds"], [10, 20, 30, 40])

    def test_script_writes_back_onto_the_shape(self):
        page = {"shapes": [{"kind": "button", "name": "Next", "script": ""}]}
        set_object_script(page, 0, "to handle buttonClick\n  send next")
        self.assertTrue(page["shapes"][0]["script"].endswith("\n"))
        self.assertIn("send next", objects_of(page)[0]["script"])

    def test_page_script_comes_from_the_handlers(self):
        page = {"handlers": [{"name": "buttonClick", "source": "send next"}]}
        self.assertEqual(page_script(page), "send next\n")

    def test_the_background_list_leaves_the_page_out(self):
        page = {"shapes": [
            {"kind": "rect", "name": "paper", "layer": "background"},
            {"kind": "button", "name": "Next", "layer": "page"},
        ]}
        self.assertEqual([row["name"] for row in objects_of(page, "background")], ["paper"])
        self.assertEqual([row["name"] for row in objects_of(page, "page")], ["Next"])

    def test_a_background_object_is_stored_under_the_page(self):
        page = {"shapes": [{"kind": "button", "name": "Next", "layer": "page"}]}
        place_shape(page, {"kind": "rect", "name": "Box", "layer": "background"})
        self.assertEqual([shape["name"] for shape in page["shapes"]], ["Box", "Next"])

    def test_front_does_not_cross_onto_the_other_layer(self):
        page = {"shapes": [
            {"kind": "rect", "name": "paper", "layer": "background"},
            {"kind": "button", "name": "Next", "layer": "page"},
        ]}
        self.assertEqual(restack(page, 0, "front"), 0)
        self.assertEqual(page["shapes"][0]["name"], "paper")

    def _names(self, page):
        return [shape["name"] for shape in page["shapes"]]

    def _page(self):
        return {"shapes": [
            {"name": "paper", "layer": "background"},
            {"name": "A"}, {"name": "B"},
            {"name": "sky", "layer": "background"},
            {"name": "C"}, {"name": "D"},
        ]}

    def test_forward_and_backward_step_one_place_on_the_layer(self):
        page = self._page()
        self.assertEqual(restack(page, 2, "forward"), 4)
        self.assertEqual(self._names(page), ["paper", "A", "C", "sky", "B", "D"])
        self.assertEqual(restack(page, 4, "backward"), 2)
        self.assertEqual(self._names(page), ["paper", "A", "B", "sky", "C", "D"])

    def test_front_and_back_go_all_the_way_on_the_layer(self):
        page = self._page()
        self.assertEqual(restack(page, 1, "front"), 5)
        self.assertEqual(self._names(page), ["paper", "B", "C", "sky", "D", "A"])
        self.assertEqual(restack(page, 5, "back"), 1)
        self.assertEqual(self._names(page), ["paper", "A", "B", "sky", "C", "D"])

    def test_the_front_object_cannot_go_further_forward(self):
        page = self._page()
        self.assertEqual(restack(page, 5, "forward"), 5)
        self.assertEqual(restack(page, 5, "front"), 5)
        self.assertEqual(self._names(page), ["paper", "A", "B", "sky", "C", "D"])


if __name__ == "__main__":
    unittest.main()
