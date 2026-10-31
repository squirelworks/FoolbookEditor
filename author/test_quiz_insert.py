"""The editor puts a quiz on the page as shapes, and Foolbook grades them by choice index.

The question is written for this test.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from author.quiz import insert_quiz, make_quiz


def _quiz():
    return make_quiz("What colour do you get from blue and yellow paint?", ["Purple", "Green", "Orange"], 1,
                     "Green. Well mixed.", "Not quite. Mix again.", next_page="P2")


class QuizInsertTests(unittest.TestCase):
    def test_the_shapes(self):
        page = {"id": "P1"}
        added = insert_quiz(page, _quiz())
        self.assertEqual([s["kind"] for s in added], ["text", "button", "button", "button", "text", "text"])
        self.assertEqual([s.get("choice") for s in added[1:4]], [0, 1, 2])
        self.assertEqual([s["text"] for s in added[1:4]], ["Purple", "Green", "Orange"])
        self.assertEqual([(s["feedback"], s["visible"]) for s in added[4:]], [("right", False), ("wrong", False)])
        self.assertIs(page["quiz"]["choices"][1]["correct"], True)
        self.assertEqual(page["shapes"], added)

    def test_a_broken_quiz_is_refused(self):
        with self.assertRaises(ValueError):
            insert_quiz({"id": "P1"}, {"question": "", "choices": []})

    def test_foolbook_grades_the_saved_page(self):
        from engine.engine import click
        from engine.loader import load
        from foolbook.model import RuntimeState
        from foolbookeditor.core import save_book
        page = {"id": "P1"}
        added = insert_quiz(page, _quiz())
        book = {"title": "Paint", "pages": [page, {"id": "P2"}]}
        with tempfile.TemporaryDirectory() as tmp:
            loaded = load(save_book(Path(tmp) / "paint.fbk", book))
        state = RuntimeState(book=loaded)
        shapes = state.page.shapes
        self.assertFalse(click(state, shapes[1]))
        self.assertIs(shapes[5]["visible"], True)
        self.assertTrue(click(state, shapes[2]))
        self.assertEqual(state.page.id, "P2")


if __name__ == "__main__":
    unittest.main()
