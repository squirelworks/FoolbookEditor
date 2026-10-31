"""Page ids are unique in a book, compared without regard to case."""

from __future__ import annotations

import unittest

from author.document import DuplicateId, add_page, fresh_id, rename_page


def book(*ids: str) -> dict:
    return {"id": "b", "pages": [{"id": i, "text": [], "items": [], "shapes": []} for i in ids]}


class PageIdTests(unittest.TestCase):
    def test_a_rename_onto_another_page_is_refused(self):
        b = book("P0", "P100")
        with self.assertRaises(DuplicateId):
            rename_page(b, 1, "P0")
        self.assertEqual(b["pages"][1]["id"], "P100")

    def test_case_does_not_make_an_id_different(self):
        b = book("P0", "P100")
        with self.assertRaises(DuplicateId):
            rename_page(b, 0, "p100")

    def test_the_casing_typed_is_stored(self):
        b = book("P0", "P100")
        self.assertEqual(rename_page(b, 0, " Intro "), "Intro")
        self.assertEqual(rename_page(b, 0, "INTRO"), "INTRO")
        self.assertEqual(b["pages"][0]["id"], "INTRO")

    def test_a_blank_rename_keeps_the_id(self):
        b = book("P0")
        self.assertEqual(rename_page(b, 0, "  "), "P0")

    def test_a_fresh_id_does_not_collide_in_another_case(self):
        b = book("P0", "p100")
        self.assertEqual(fresh_id(b), "P200")
        add_page(b)
        ids = [p["id"].lower() for p in b["pages"]]
        self.assertEqual(len(ids), len(set(ids)))


if __name__ == "__main__":
    unittest.main()
