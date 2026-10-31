"""Open and save, the editor's side.

Foolbook packs and unpacks the envelope. This module decides what the
editor hands it. A book loaded and saved again comes back as the same
bytes.
"""

from __future__ import annotations

from pathlib import Path

from author.schema import NOT_WRITTEN
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


def background_first(page: dict) -> dict:
    """The page with its background shapes ahead of its page shapes.

    The reader paints a page's shapes in array order and does not read
    ``layer``. A background shape after a page shape would be drawn over
    it. Order inside each layer is kept.
    """
    shapes = page.get("shapes")
    if not isinstance(shapes, list):
        return page
    back = [s for s in shapes if isinstance(s, dict) and s.get("layer") == "background"]
    if not back:
        return page
    rest = [s for s in shapes if not (isinstance(s, dict) and s.get("layer") == "background")]
    ordered = back + rest
    if ordered == shapes:
        return page
    return {**page, "shapes": ordered}


def payload(book: dict) -> dict:
    """The book as it is written: no envelope keys, no editor state, and
    background shapes ahead of page shapes on every page."""
    out = {
        key: value for key, value in book.items()
        if key not in ENVELOPE and key not in NOT_WRITTEN
    }
    if isinstance(out.get("pages"), list):
        out["pages"] = [background_first(p) if isinstance(p, dict) else p for p in out["pages"]]
    return out


def open_book(path: str | Path) -> dict:
    return load(path)


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
