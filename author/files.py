"""Open and save, the editor's side.

Foolbook packs and unpacks the envelope. This module decides what the
editor hands it. A book loaded and saved again comes back as the same
bytes.
"""

from __future__ import annotations

from pathlib import Path

from author.schema import NOT_WRITTEN
from foolbookeditor.core import format_version, load, save_book

# Written by Foolbook's save, not by the author. Dropped before a save so
# the reader stamps them again in its own order.
ENVELOPE = ("format", "format_version", "fbk", "foolbook")


class FutureBook(ValueError):
    """A book from a newer Foolbook than the one installed."""


def version_of(book: dict) -> int | None:
    """The book generation the file says, or None for an old book with no key."""
    value = book.get("fbk")
    return value if isinstance(value, int) else None


def check_version(book: dict) -> None:
    """Refuse a book this editor does not know how to write."""
    found = version_of(book)
    known = format_version()
    if found is not None and found > known:
        raise FutureBook(
            f"This book is Foolbook book version {found}. "
            f"This editor writes version {known}. It was not saved."
        )


def payload(book: dict) -> dict:
    """The book without the keys the envelope writer stamps, or editor state."""
    return {
        key: value for key, value in book.items()
        if key not in ENVELOPE and key not in NOT_WRITTEN
    }


def open_book(path: str | Path) -> dict:
    return load(path)


def save(path: str | Path, book: dict, compress: bool = True) -> Path:
    check_version(book)
    return save_book(path, payload(book), compress=compress)
