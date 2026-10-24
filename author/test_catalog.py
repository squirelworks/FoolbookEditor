"""Author lists every object, including one Reader hides."""

from __future__ import annotations

import unittest

from author.catalog import objects_of, page_ids, page_script, set_object_script


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


if __name__ == "__main__":
    unittest.main()
