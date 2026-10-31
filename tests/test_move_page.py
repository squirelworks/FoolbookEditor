"""Page order is the array order. Moving at the ends does nothing."""

from __future__ import annotations

import unittest

from author.document import move_page


def book(*ids: str) -> dict:
    return {"pages": [{"id": i} for i in ids]}


def ids(b: dict) -> list[str]:
    return [p["id"] for p in b["pages"]]


class MovePageTests(unittest.TestCase):
    def test_the_first_page_moves_down(self):
        b = book("A", "B", "C")
        self.assertEqual(move_page(b, 0, 1), 1)
        self.assertEqual(ids(b), ["B", "A", "C"])

    def test_the_first_page_cannot_move_up(self):
        b = book("A", "B", "C")
        self.assertEqual(move_page(b, 0, -1), 0)
        self.assertEqual(ids(b), ["A", "B", "C"])

    def test_the_last_page_moves_up(self):
        b = book("A", "B", "C")
        self.assertEqual(move_page(b, 2, -1), 1)
        self.assertEqual(ids(b), ["A", "C", "B"])

    def test_the_last_page_cannot_move_down(self):
        b = book("A", "B", "C")
        self.assertEqual(move_page(b, 2, 1), 2)
        self.assertEqual(ids(b), ["A", "B", "C"])

    def test_a_one_page_book_does_not_move(self):
        b = book("A")
        self.assertEqual(move_page(b, 0, 1), 0)
        self.assertEqual(move_page(b, 0, -1), 0)
        self.assertEqual(ids(b), ["A"])

    def test_an_index_off_the_book_does_nothing(self):
        b = book("A", "B")
        self.assertEqual(move_page(b, 5, -1), 5)
        self.assertEqual(move_page(b, -1, 1), -1)
        self.assertEqual(ids(b), ["A", "B"])


if __name__ == "__main__":
    unittest.main()
