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


class TypedTextTests(unittest.TestCase):
    def test_typed_lines_are_kept_as_lines(self):
        from author.catalog import set_object_text
        page = {"shapes": [{"kind": "text", "name": "Field", "text": "Field"}]}
        set_object_text(page, 0, "First line\nSecond line\n")
        self.assertEqual(page["shapes"][0]["text"], "First line\nSecond line")

    def test_typing_nothing_leaves_an_empty_field(self):
        from author.catalog import set_object_text
        page = {"shapes": [{"kind": "text", "text": "Field"}]}
        set_object_text(page, 0, "\n")
        self.assertEqual(page["shapes"][0]["text"], "")

class ScriptPaneTests(unittest.TestCase):
    def test_tab_is_two_spaces(self):
        from author.properties import SCRIPT_TAB
        self.assertEqual(SCRIPT_TAB, "  ")

    def test_the_page_script_is_stored_as_the_typed_string(self):
        from author.catalog import set_page_script
        page = {"id": "P0"}
        source = 'to handle enterPage\n  go to page "P100"\nend'
        self.assertTrue(set_page_script(page, source + "\n"))
        self.assertEqual(page["script"], source + "\n")
        self.assertIsInstance(page["script"], str)

    def test_an_unchanged_pane_does_not_turn_handlers_into_a_script(self):
        from author.catalog import page_script, set_page_script
        page = {"id": "P0", "handlers": [{"source": "to handle enterPage\nend\n"}]}
        self.assertFalse(set_page_script(page, page_script(page)))
        self.assertNotIn("script", page)

    def test_clearing_the_pane_clears_the_script(self):
        from author.catalog import set_page_script
        page = {"id": "P0", "script": "to handle enterPage\nend\n"}
        self.assertTrue(set_page_script(page, "\n"))
        self.assertNotIn("script", page)


if __name__ == "__main__":
    unittest.main()
