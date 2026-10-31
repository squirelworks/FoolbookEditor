"""Open and save, the editor's side.

Foolbook packs and unpacks the envelope. This module decides what the
editor hands it. A book loaded and saved again comes back as the same
bytes.
"""

from __future__ import annotations

from pathlib import Path

from foolbookeditor.core import (
    format_version,
    is_office,
    is_toolbook,
    load,
    read,
    save_book,
    save_system,
    to_book,
)

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


FOOLBOOK_MAGIC = (b"FBK1", b"FSK1", b"FSC1")


def sniff(path: str | Path) -> str:
    """What the bytes are: ``foolbook``, ``toolbook``, ``office``, or ``unknown``.

    The extension is a hint. A ToolBook file renamed to .fbk is ToolBook,
    and an .fbk envelope named .tbk is a Foolbook book.
    """
    path = Path(path)
    with path.open("rb") as handle:
        head = handle.read(8)
    if head[:4] in FOOLBOOK_MAGIC or head.lstrip()[:1] in (b"{", b"["):
        return "foolbook"
    if is_toolbook(path):
        return "toolbook"
    if is_office(path):
        return "office"
    return "unknown"


def open_book(path: str | Path) -> dict:
    """Open whatever the bytes are, as the book dict the editor holds."""
    kind = sniff(path)
    if kind == "foolbook":
        return load(path)
    if kind == "toolbook":
        return read(path)
    if kind == "office":
        return to_book(path)
    # Anything else the reader may still know: a TBX folder, notes, an
    # older store. It says so when it cannot.
    return read(path)


def save_path_for(opened: str | Path) -> Path | None:
    """Where Save goes after opening this file, or None to ask (Save as).

    A Foolbook book saves over itself. A ToolBook file named .fbk, .fsk
    or .json would be written over by Save, so Save asks instead.
    """
    opened = Path(opened)
    if sniff(opened) != "foolbook" and opened.suffix.lower() in (".fbk", ".fsk", ".json"):
        return None
    return opened


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
