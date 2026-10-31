"""The quiz schema. The questions here are written for this test."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from author.document import set_quiz
from author.quiz import make_quiz, right_index, validate


def _quiz():
    return make_quiz(
        "Which file starts with FBK1?",
        ["A picture", "A Foolbook book", "A font"],
        1,
        "Yes. FBK1 is the book envelope.",
        "Not that one. Look at the first four bytes.",
        next_page="P3",
    )


class QuizSchemaTests(unittest.TestCase):
    def test_make_a_quiz(self):
        quiz = _quiz()
        self.assertEqual(quiz["version"], 1)
        self.assertEqual(quiz["question"], "Which file starts with FBK1?")
        self.assertEqual(right_index(quiz), 1)
        self.assertEqual([c["correct"] for c in quiz["choices"]], [False, True, False])
        self.assertEqual(quiz["next"], "P3")
        self.assertNotIn("again", quiz)
        self.assertEqual(validate(quiz), [])

    def test_the_right_choice_must_be_a_choice(self):
        with self.assertRaises(ValueError):
            make_quiz("How many sides has a square?", ["Three", "Four"], 2)

    def test_what_is_missing_is_said(self):
        self.assertIn("the quiz has no question", validate({"choices": [{"label": "x", "correct": True}]}))
        self.assertIn("a quiz has exactly one right choice, not 2",
                      validate({"question": "q", "choices": [{"label": "a", "correct": True}, {"label": "b", "correct": True}]}))
        self.assertIn("quiz version 9 is newer than this editor knows (1)",
                      validate({"version": 9, "question": "q", "choices": [{"label": "a", "correct": True}, {"label": "b"}]}))

    def test_an_old_quiz_with_no_version_still_validates_its_choices(self):
        old = {"question": "Is water wet?", "choices": [{"label": "Yes", "correct": True}, {"label": "No"}], "next": "P2"}
        self.assertEqual(validate(old), [])

    def test_the_quiz_round_trips_through_a_saved_book(self):
        from foolbookeditor.core import load, save_book
        page = {"id": "P1"}
        set_quiz(page, _quiz())
        book = {"title": "t", "pages": [page]}
        with tempfile.TemporaryDirectory() as tmp:
            loaded = load(save_book(Path(tmp) / "q.fbk", book))
        self.assertEqual(loaded["pages"][0]["quiz"], _quiz())


if __name__ == "__main__":
    unittest.main()
