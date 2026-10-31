"""A record is laid out as one page per row, joined by Previous and Next record."""

from __future__ import annotations

import unittest

from author.records import parse_rows, place_record


def _book():
    return {"id": "b", "pages": [{"id": "P0", "shapes": []}, {"id": "P100", "shapes": []}]}


def _field(page, name):
    return next(s for s in page["shapes"] if s.get("name") == name)


def _jump(page, name):
    found = [s for s in page["shapes"] if s.get("name") == name]
    return found[0]["item"]["page"] if found else None


class Rows(unittest.TestCase):
    def test_rows_are_one_per_line_split_on_commas(self):
        fields, rows = parse_rows("Name, Town", "Ada, Leeds\n\nBen,Bath\n")
        self.assertEqual(fields, ["Name", "Town"])
        self.assertEqual(rows, [["Ada", "Leeds"], ["Ben", "Bath"]])

    def test_a_record_needs_a_field(self):
        with self.assertRaises(ValueError):
            parse_rows(" , ", "Ada")


class Pages(unittest.TestCase):
    def test_each_row_is_its_own_page_after_the_first(self):
        book = _book()
        count = place_record(book, 0, ["Name", "Town"], [["Ada", "Leeds"], ["Ben", "Bath"], ["Cy", "York"]], 40, 40)
        self.assertEqual(count, 3)
        pages = book["pages"]
        self.assertEqual(len(pages), 4)
        self.assertEqual([_field(p, "Name")["text"] for p in pages[:3]], ["Ada", "Ben", "Cy"])
        self.assertEqual(_field(pages[2], "Town")["text"], "York")
        self.assertEqual(pages[3]["id"], "P100")  # the page after the record keeps its place

    def test_previous_and_next_go_to_the_neighbouring_row_pages(self):
        book = _book()
        place_record(book, 0, ["Name"], [["Ada"], ["Ben"], ["Cy"]], 40, 40)
        first, middle, last = book["pages"][:3]
        self.assertIsNone(_jump(first, "Previous record"))
        self.assertEqual(_jump(first, "Next record"), middle["id"])
        self.assertEqual(_jump(middle, "Previous record"), first["id"])
        self.assertEqual(_jump(middle, "Next record"), last["id"])
        self.assertEqual(_jump(last, "Previous record"), middle["id"])
        self.assertIsNone(_jump(last, "Next record"))

    def test_the_book_stores_no_record_data(self):
        book = _book()
        place_record(book, 0, ["Name"], [["Ada"], ["Ben"]], 40, 40)
        self.assertFalse(any("records" in p for p in book["pages"]))

    def test_page_ids_are_unique(self):
        book = _book()
        place_record(book, 0, ["Name"], [["Ada"], ["Ben"], ["Cy"]], 40, 40)
        ids = [p["id"] for p in book["pages"]]
        self.assertEqual(len(ids), len(set(ids)))

    def test_one_row_is_one_page_with_no_buttons(self):
        book = _book()
        self.assertEqual(place_record(book, 0, ["Name"], [["Ada"]], 40, 40), 1)
        self.assertEqual(len(book["pages"]), 2)
        self.assertEqual([s["name"] for s in book["pages"][0]["shapes"]], ["Name"])

    def test_a_field_name_already_on_the_page_is_refused(self):
        book = _book()
        book["pages"][0]["shapes"].append({"kind": "text", "name": "Name"})
        with self.assertRaisesRegex(ValueError, "Name"):
            place_record(book, 0, ["Name"], [], 0, 0)
        self.assertEqual(len(book["pages"]), 2)


class Reader(unittest.TestCase):
    """The reader on main turns the page with nothing new: a button's item names a page."""

    def test_next_record_turns_the_reader_to_the_next_row(self):
        try:
            from engine.engine import press
            from engine.loader import load
            from foolbook.model import RuntimeState
        except ImportError:
            self.skipTest("Foolbook is not on the path")
        import tempfile
        from pathlib import Path
        from foolbookeditor.core import save_book
        book = {"id": "b", "title": "t", "pages": [{"id": "P0", "shapes": []}]}
        place_record(book, 0, ["Name"], [["Ada"], ["Ben"]], 40, 40)
        with tempfile.TemporaryDirectory() as tmp:
            loaded = load(save_book(Path(tmp) / "r.fbk", book))
        state = RuntimeState(book=loaded)
        button = _field(book["pages"][0], "Next record")
        self.assertTrue(press(state, button["text"], button["item"]["page"]))
        self.assertEqual(loaded.pages[state.index].id, book["pages"][1]["id"])


if __name__ == "__main__":
    unittest.main()
