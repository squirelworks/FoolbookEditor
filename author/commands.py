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
    "duplicate_page": ("Ctrl+Shift+D", "<Control-D>"),
    "delete_page": ("Ctrl+Shift+Delete", "<Control-Shift-Delete>"),
}


def add_page(book: dict, current: int) -> int:
    """A blank page right after the current one. Returns where it landed."""
    count = len(book.get("pages") or [])
    at = current + 1 if 0 <= current < count else count
    return document.add_page(book, at)


def duplicate_page(book: dict, current: int) -> int:
    """The copy of the current page becomes the next page and is shown."""
    return document.duplicate_page(book, current)


def delete_question(book: dict, current: int) -> str | None:
    """What the window asks before it deletes. None means there is nothing to ask.

    The model never asks. A book keeps its last page, so there is no question then.
    """
    found = book.get("pages") or []
    if len(found) <= 1 or not (0 <= current < len(found)):
        return None
    page = found[current]
    count = sum(1 for shape in page.get("shapes") or [] if isinstance(shape, dict))
    noun = "object" if count == 1 else "objects"
    return f"Delete page {page.get('id') or '?'} and its {count} {noun}?"


def delete_page(book: dict, current: int) -> int:
    """Remove the current page without asking. Returns the page to show."""
    return document.delete_page(book, current)
