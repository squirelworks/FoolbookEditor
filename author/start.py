"""What the start window offers before a book is open.

New book, Open book, A Small Garden, then the recent books that are still
on disk, at most five. The window draws these. It does not decide them.
"""

from __future__ import annotations

from pathlib import Path

NEW = "New book"
OPEN = "Open book"
GARDEN = "A Small Garden"
RECENT = "Open recent"

RECENT_LIMIT = 5

DEMO = Path(__file__).resolve().parents[1] / "foolbookeditor" / "demo" / "garden.fbk"


def first_book(path: str | Path | None) -> tuple[dict | None, Path | None]:
    """(book, path to save to). A path is opened as usual.

    No path is the demo, as an unsaved copy, so Save asks where to put it
    and the shipped file is never written.
    """
    if path is not None:
        return None, Path(path)
    if not DEMO.is_file():
        return None, None
    from foolbookeditor.core import load
    return load(DEMO), None


def start_choices(recent: list[str]) -> list[tuple[str, Path | None]]:
    """One row per button, in the order the window shows them."""
    choices: list[tuple[str, Path | None]] = [(NEW, None), (OPEN, None), (GARDEN, None)]
    for raw in recent:
        path = Path(raw)
        if not path.is_file():
            continue
        choices.append((RECENT, path))
        if sum(1 for label, _ in choices if label == RECENT) >= RECENT_LIMIT:
            break
    return choices
