"""Open and save, the editor's side.

Foolbook packs and unpacks the envelope. This module decides what the
editor hands it. A book loaded and saved again comes back as the same
bytes.
"""

from __future__ import annotations

from pathlib import Path

from foolbookeditor.core import format_version, load, save_book, save_system

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
    """The book without the keys the envelope writer stamps."""
    return {key: value for key, value in book.items() if key not in ENVELOPE}


def open_book(path: str | Path) -> dict:
    return load(path)


def is_compressed(path: str | Path) -> bool:
    """Whether Save should compress, to match the file that was opened.

    An envelope says so in bit 0 of its flags byte. Plain JSON and a web
    editor download are not compressed. Anything else (a ToolBook file,
    an office file) gets the default, compressed, as Foolbook packs it.
    """
    blob = Path(path).read_bytes()[:5]
    if blob[:4] in (b"FBK1", b"FSK1", b"FSC1") and len(blob) == 5:
        return bool(blob[4] & 1)
    if blob.lstrip()[:1] in (b"{", b"["):
        return False
    return True


# What Save writes. Anything else is Export.
SAVE_SUFFIXES = (".fbk", ".fsk", ".json")


def save_target(path: str | Path) -> Path:
    """Where Save writes, given the file the book came from.

    Save writes a book (.fbk), a system book (.fsk), or .json. A book
    opened from a .tbk, an office file, or anything else is saved
    beside it as .fbk; an .sbk as .fsk. The original is never written.
    """
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix in SAVE_SUFFIXES:
        return path
    if suffix == ".sbk":
        return path.with_suffix(".fsk")
    return path.with_suffix(".fbk")


def save(path: str | Path, book: dict, compress: bool = True) -> Path:
    """Save the book. Returns the file written, which ``save_target`` chose."""
    check_version(book)
    target = save_target(path)
    if target.suffix.lower() == ".fsk":
        return save_system(target, payload(book), compress=compress)
    return save_book(target, payload(book), compress=compress)
