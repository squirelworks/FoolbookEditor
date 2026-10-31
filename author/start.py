"""What the editor opens, and what the start window offers.

A path opens that book. No path opens the demo book that ships with the
editor, as an unsaved copy, so Save asks where to put it and the shipped
file is never written.

The start window offers New book, Open book, then the recent books that
are still on disk, at most five. The window draws these. It does not
decide them.
"""

from __future__ import annotations

from pathlib import Path

DEMO = Path(__file__).resolve().parents[1] / "foolbookeditor" / "demo" / "garden.fbk"

NEW = "New book"
OPEN = "Open book"
RECENT = "Open recent"

RECENT_LIMIT = 5


def first_book(path: str | Path | None) -> tuple[dict | None, Path | None]:
    """(book, path to save to). (None, path) means open the path as usual."""
    if path is not None:
        return None, Path(path)
    from foolbookeditor.core import load
    if DEMO.is_file():
        return load(DEMO), None
    return None, None


def start_choices(recent: list[str]) -> list[tuple[str, Path | None]]:
    """One row per button, in the order the window shows them."""
    choices: list[tuple[str, Path | None]] = [(NEW, None), (OPEN, None)]
    for raw in recent:
        path = Path(raw)
        if not path.is_file():
            continue
        choices.append((RECENT, path))
        if len(choices) - 2 >= RECENT_LIMIT:
            break
    return choices
