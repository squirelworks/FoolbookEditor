"""A record is fields, rows, and two buttons, laid out on the page as data."""

from __future__ import annotations

import unittest

from author.records import parse_rows, place_record


class RecordTests(unittest.TestCase):
    def test_rows_are_one_per_line_split_on_commas(self):
        fields, rows = parse_rows("Name, Town", "Ada, Leeds\n\nBen,Bath\n")
        self.assertEqual(fields, ["Name", "Town"])
        self.assertEqual(rows, [["Ada", "Leeds"], ["Ben", "Bath"]])

    def test_a_record_needs_a_field(self):
        with self.assertRaises(ValueError):
            parse_rows(" , ", "Ada")

    def test_placing_a_record_adds_the_data_a_field_each_and_two_buttons(self):
        page = {"id": "P0", "shapes": []}
        place_record(page, ["Name", "Town"], [["Ada", "Leeds"]], 40, 40)
        self.assertEqual(page["records"], {"fields": ["Name", "Town"], "rows": [["Ada", "Leeds"]], "at": 0})
        kinds = [(s["kind"], s["name"]) for s in page["shapes"]]
        self.assertEqual(kinds, [("text", "Name"), ("text", "Town"), ("button", "Previous record"), ("button", "Next record")])
        self.assertEqual(page["shapes"][2]["item"], {"record": "previous"})
        self.assertEqual(page["shapes"][3]["item"], {"record": "next"})
        # The field shows the first row in the editor too, so the author sees it.
        self.assertEqual(page["shapes"][0]["text"], "Ada")

    def test_a_field_name_already_on_the_page_is_refused(self):
        page = {"id": "P0", "shapes": [{"kind": "text", "name": "Name"}]}
        with self.assertRaisesRegex(ValueError, "Name"):
            place_record(page, ["Name"], [], 0, 0)

    def test_a_page_holds_one_record(self):
        page = {"id": "P0", "shapes": []}
        place_record(page, ["A"], [], 0, 0)
        with self.assertRaises(ValueError):
            place_record(page, ["B"], [], 0, 100)


if __name__ == "__main__":
    unittest.main()
