"""Undo and redo for the Author window.

A stack of whole-book snapshots. That is plenty until books get large. The
window commits after each command; a commit that changes nothing is not a
step. Typing in a text box is committed when the box loses focus, so a
paragraph is one step, not one step per character.
"""

from __future__ import annotations

import copy

# How many steps back undo can go.
DEPTH = 50


class History:
    def __init__(self, book: dict | None = None, depth: int = DEPTH):
        self.depth = depth
        self._past: list[dict] = []
        self._future: list[dict] = []
        if book is not None:
            self.reset(book)

    def reset(self, book: dict) -> None:
        """A new or opened book. Nothing to undo."""
        self._past = [copy.deepcopy(book)]
        self._future = []

    def commit(self, book: dict) -> bool:
        """Remember the book as it is now. Returns False when nothing changed."""
        if self._past and self._past[-1] == book:
            return False
        self._past.append(copy.deepcopy(book))
        self._future = []
        # The oldest state is kept as the floor, so ``depth`` steps can be undone.
        del self._past[:-(self.depth + 1)]
        return True

    def can_undo(self) -> bool:
        return len(self._past) > 1

    def can_redo(self) -> bool:
        return bool(self._future)

    def undo(self) -> dict | None:
        """The book as it was one step ago, or None at the start."""
        if not self.can_undo():
            return None
        self._future.append(self._past.pop())
        return copy.deepcopy(self._past[-1])

    def redo(self) -> dict | None:
        """The book as it was before the last undo, or None."""
        if not self._future:
            return None
        state = self._future.pop()
        self._past.append(state)
        return copy.deepcopy(state)
