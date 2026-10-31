"""Open and save, the editor's side.

Foolbook packs and unpacks the envelope. This module decides what the
editor hands it. A book loaded and saved again comes back as the same
bytes.
"""

from __future__ import annotations

from pathlib import Path

from foolbookeditor.core import load, save_book

# Written by Foolbook's save, not by the author. Dropped before a save so
# the reader stamps them again in its own order.
ENVELOPE = ("format", "format_version", "fbk", "foolbook")


def payload(book: dict) -> dict:
    """The book without the keys the envelope writer stamps."""
    return {key: value for key, value in book.items() if key not in ENVELOPE}


def open_book(path: str | Path) -> dict:
    return load(path)


def save(path: str | Path, book: dict, compress: bool = True) -> Path:
    return save_book(path, payload(book), compress=compress)
