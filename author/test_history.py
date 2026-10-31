"""Undo and redo, driven without the window."""

from __future__ import annotations

import unittest

from author import geometry
from author.history import DEPTH, History


def _book():
    return {"id": "b", "pages": [{"id": "P0", "shapes": [{"kind": "rect", "x": 10, "y": 10, "w": 20, "h": 20}]}]}


class HistoryTests(unittest.TestCase):
    def test_do_undo_and_redo_one_move(self):
        book = _book()
        history = History(book)
        geometry.nudge(book["pages"][0]["shapes"], [0], 8, 0)
        self.assertTrue(history.commit(book))
        back = history.undo()
        self.assertEqual(back["pages"][0]["shapes"][0]["x"], 10)
        again = history.redo()
        self.assertEqual(again["pages"][0]["shapes"][0]["x"], 18)
        self.assertIsNone(history.redo())

    def test_the_snapshot_is_not_the_live_book(self):
        book = _book()
        history = History(book)
        book["pages"][0]["shapes"][0]["x"] = 99
        history.commit(book)
        book["pages"][0]["shapes"][0]["x"] = 5
        self.assertEqual(history.undo()["pages"][0]["shapes"][0]["x"], 10)

    def test_a_commit_that_changes_nothing_is_not_a_step(self):
        book = _book()
        history = History(book)
        self.assertFalse(history.commit(book))
        self.assertFalse(history.can_undo())

    def test_a_new_change_after_undo_drops_redo(self):
        book = _book()
        history = History(book)
        book["title"] = "one"
        history.commit(book)
        book = history.undo()
        book["title"] = "two"
        history.commit(book)
        self.assertIsNone(history.redo())

    def test_the_stack_stops_at_fifty(self):
        self.assertEqual(DEPTH, 50)
        book = _book()
        history = History(book)
        for n in range(60):
            book["title"] = str(n)
            history.commit(book)
        steps = 0
        while history.undo() is not None:
            steps += 1
        self.assertEqual(steps, 50)

    def test_nothing_to_undo_at_the_start(self):
        self.assertIsNone(History(_book()).undo())


if __name__ == "__main__":
    unittest.main()
