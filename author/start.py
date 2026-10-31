"""What the start window offers before a book is open.

New book, Open book, then the recent books that are still on disk, at
most five. The window draws these. It does not decide them.
"""

from __future__ import annotations

from pathlib import Path

NEW = "New book"
OPEN = "Open book"
RECENT = "Open recent"

RECENT_LIMIT = 5


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
