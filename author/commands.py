"""Commands the Author window runs.

The window binds keys and buttons to these. Each one takes the book and
the current page index and returns the page index to show. None of them
opens a dialog. The keys are data here so a test can read them.
"""

from __future__ import annotations

from author import document

# Command name to the key shown in the menu and the Tk events bound to it.
SHORTCUTS = {
    "add_page": ("Ctrl+M", "<Control-m>"),
    "undo": ("Ctrl+Z", "<Control-z>"),
    "redo": ("Ctrl+Y or Ctrl+Shift+Z", "<Control-y>", "<Control-Z>"),
    "duplicate_page": ("Ctrl+Shift+D", "<Control-D>"),
    "delete_page": ("Ctrl+Shift+Delete", "<Control-Shift-Delete>"),
    "page_up": ("Ctrl+Shift+Up", "<Control-Shift-Up>"),
    "page_down": ("Ctrl+Shift+Down", "<Control-Shift-Down>"),
    "go_to_page": ("Ctrl+G", "<Control-g>"),
    "first_page": ("Ctrl+Home", "<Control-Home>"),
    "previous_page": ("Ctrl+Page Up", "<Control-Prior>"),
    "next_page": ("Ctrl+Page Down", "<Control-Next>"),
    "last_page": ("Ctrl+End", "<Control-End>"),
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


def page_up(book: dict, current: int) -> int:
    """Swap the current page with the one before it. The first page stays."""
    return document.move_page(book, current, -1)


def page_down(book: dict, current: int) -> int:
    """Swap the current page with the one after it. The last page stays."""
    return document.move_page(book, current, 1)


def go_to_page(book: dict, current: int, typed: str) -> tuple[int, str]:
    """The page whose id was typed, and the status line to show.

    Ids compare without case, as the reader finds them. An unknown id leaves
    the current page where it is.
    """
    wanted = (typed or "").strip()
    if not wanted:
        return current, ""
    for index, page in enumerate(book.get("pages") or []):
        if str(page.get("id") or "").casefold() == wanted.casefold():
            return index, f"Page {page.get('id')}"
    return current, f"Unknown page {wanted}"


# These move the page the editor shows. They are not the book's Next button
# and they do not run any script.

def first_page(book: dict, current: int) -> int:
    return 0 if book.get("pages") else current


def previous_page(book: dict, current: int) -> int:
    return max(0, current - 1) if book.get("pages") else current


def next_page(book: dict, current: int) -> int:
    count = len(book.get("pages") or [])
    return min(count - 1, current + 1) if count else current


def last_page(book: dict, current: int) -> int:
    count = len(book.get("pages") or [])
    return count - 1 if count else current
