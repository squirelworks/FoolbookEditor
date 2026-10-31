"""A page can be given a shared background, or have it cleared."""

from __future__ import annotations

import unittest

from author.document import background_of, clear_background, set_background
from author.stage import shown


def _book() -> dict:
    return {
        "id": "b",
        "title": "B",
        "pages": [
            {"id": "Paper", "background": True, "shapes": [
                {"kind": "rect", "name": "band", "x": 0, "y": 0, "w": 640, "h": 40},
            ]},
            {"id": "P0", "shapes": [{"kind": "text", "name": "hello", "x": 20, "y": 60, "text": "Hi"}]},
        ],
    }


class AssignBackground(unittest.TestCase):
    def test_a_page_names_the_background_it_uses(self):
        book = _book()
        set_background(book, book["pages"][1], "paper")
        self.assertEqual(book["pages"][1]["uses"], "Paper")
        self.assertIs(background_of(book, book["pages"][1]), book["pages"][0])

    def test_clearing_drops_the_name(self):
        book = _book()
        page = book["pages"][1]
        set_background(book, page, "Paper")
        clear_background(page)
        self.assertNotIn("uses", page)
        self.assertIsNone(background_of(book, page))

    def test_an_unknown_background_is_refused(self):
        book = _book()
        with self.assertRaises(ValueError):
            set_background(book, book["pages"][1], "P0")
        self.assertNotIn("uses", book["pages"][1])

    def test_a_background_cannot_use_another(self):
        book = _book()
        with self.assertRaises(ValueError):
            set_background(book, book["pages"][0], "Paper")

    def test_the_stage_draws_the_background_first(self):
        book = _book()
        set_background(book, book["pages"][1], "Paper")
        names = [s.get("name") for s in shown(book["pages"][1], book)]
        self.assertEqual(names, ["band", "hello"])
        self.assertEqual(shown(book["pages"][1], book)[0]["layer"], "background")


if __name__ == "__main__":
    unittest.main()
