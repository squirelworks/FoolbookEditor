"""A recovery copy of the open book, written every five minutes while it has unsaved changes.

The copy lives in the user config directory, never beside the book, so
it is not mistaken for the book. Saving removes it. Opening a book whose
recovery copy is newer than the file asks which to open.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

INTERVAL_MS = 5 * 60 * 1000


def snapshot(book: dict) -> str:
    """What the book holds, to compare with later. Key order does not count."""
    return json.dumps(book, sort_keys=True, default=str)


def changed(saved: str | None, book: dict) -> bool:
    return saved is None or saved != snapshot(book)


def recovery_path(book_path: str | Path | None) -> Path:
    """One file per book path. An unsaved book has one shared name."""
    from author.settings import directory
    if book_path is None:
        name = "untitled"
    else:
        full = str(Path(book_path).resolve())
        name = f"{Path(book_path).stem}-{hashlib.sha1(full.encode('utf-8')).hexdigest()[:8]}"
    return directory() / "recovery" / f"{name}.fbk"


def tick(book: dict, saved: str | None, book_path: str | Path | None) -> Path | None:
    """Write the recovery copy if the book changed since it was saved. Returns it, or None."""
    if not changed(saved, book):
        return None
    from author.safesave import save_safely
    dest = recovery_path(book_path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    return save_safely(dest, book)


def newer(book_path: str | Path) -> Path | None:
    """The recovery copy, if there is one newer than the book file."""
    copy = recovery_path(book_path)
    try:
        if copy.stat().st_mtime > Path(book_path).stat().st_mtime:
            return copy
    except OSError:
        return None
    return None


def clear(book_path: str | Path | None) -> None:
    try:
        recovery_path(book_path).unlink()
    except OSError:
        pass
