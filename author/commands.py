"""Commands the Author window runs.

The window binds keys and buttons to these. Each one takes the book and
the current page index and returns the page index to show. None of them
opens a dialog. The keys are data here so a test can read them.
"""

from __future__ import annotations

from author import document

# Command name to the key shown in the menu and the Tk event bound to it.
SHORTCUTS = {
    "add_page": ("Ctrl+M", "<Control-m>"),
}


def add_page(book: dict, current: int) -> int:
    """A blank page right after the current one. Returns where it landed."""
    count = len(book.get("pages") or [])
    at = current + 1 if 0 <= current < count else count
    return document.add_page(book, at)
