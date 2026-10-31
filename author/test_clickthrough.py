"""The definition of up to snuff for Part A.

A headless Foolbook opens the demo book, follows Next, answers the quiz
wrong and then right, and lands on the last page. Nothing here draws a
window. Do not weaken this test to make it pass. Fix the reader or the
book.
"""

from __future__ import annotations

import unittest

from author.start import DEMO


def _named(page, name: str) -> dict:
    for shape in page.shapes:
        if shape.get("name") == name:
            return shape
    raise AssertionError(f"{page.id} has no shape called {name}")


class ClickThrough(unittest.TestCase):
    def test_next_the_quiz_and_the_last_page(self):
        from engine.choice import score
        from engine.engine import click, enter_book, enter_page
        from engine.loader import load
        from foolbook.model import RuntimeState

        state = RuntimeState(book=load(DEMO))
        enter_book(state)
        enter_page(state)
        self.assertEqual([p.id for p in state.book.pages], ["P0", "P100", "P200"])
        self.assertEqual(state.page.id, "P0")

        # The shared background is painted first, then the page.
        self.assertEqual([s.get("name") for s in state.page.shapes[:3]], ["Paper", "Band", "Title"])
        self.assertTrue(any(s.get("kind") == "image" and s.get("data") for s in state.page.shapes))

        self.assertTrue(click(state, _named(state.page, "Next")))
        enter_page(state)
        self.assertEqual(state.page.id, "P100")

        wrong = _named(state.page, "Choice 2")
        self.assertFalse(click(state, wrong))
        self.assertEqual(state.page.id, "P100")
        self.assertIs(_named(state.page, "Feedback wrong")["visible"], True)
        self.assertIs(_named(state.page, "Feedback right")["visible"], False)

        right = _named(state.page, "Choice 1")
        self.assertTrue(click(state, right))
        enter_page(state)
        self.assertEqual(state.page.id, "P200")
        self.assertEqual(state.index, len(state.book.pages) - 1)
        self.assertEqual(score(state), (1, 1))


if __name__ == "__main__":
    unittest.main()
