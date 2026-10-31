"""Open and save, the editor's side.

Foolbook packs and unpacks the envelope. This module decides what the
editor hands it. A book loaded and saved again comes back as the same
bytes.
"""

from __future__ import annotations

from pathlib import Path

from author.schema import NOT_WRITTEN
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
    """The book as it is written: no envelope keys, no editor state,
    and background shapes ahead of page shapes on every page."""
    out = {
        key: value for key, value in book.items()
        if key not in ENVELOPE and key not in NOT_WRITTEN
    }
    if isinstance(out.get("pages"), list):
        out["pages"] = [background_first(p) if isinstance(p, dict) else p for p in out["pages"]]
    return out


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


class EmptyBook(ValueError):
    """An envelope with no book in it."""


def empty_payload(path: str | Path) -> None:
    """Refuse an FBK1 file whose payload is only zero bytes, and say why.

    The web editor's Download wrote the magic and the flags byte and then
    zeros where the book should be, until the site fixed it. That file has
    nothing to recover.
    """
    blob = Path(path).read_bytes()
    if blob[:4] in FOOLBOOK_MAGIC and not blob[5:].strip(b"\x00"):
        raise EmptyBook(
            f"{Path(path).name} has the {blob[:4].decode()} header and no book after it. "
            "A web editor download from before the fix writes this. Download it again."
        )


def open_book(path: str | Path) -> dict:
    """Open whatever the bytes are, as the book dict the editor holds."""
    kind = sniff(path)
    if kind == "foolbook":
        empty_payload(path)
        return load(path)
    if kind == "toolbook":
        return read(path)
    if kind == "office":
        return to_book(path)
    # Anything else the reader may still know: a TBX folder, notes, an
    # older store. It says so when it cannot.
    return read(path)


def is_compressed(path: str | Path) -> bool:
    """Whether Save should compress, to match the file that was opened.

    An envelope says so in bit 0 of its flags byte. Plain JSON and a web
    editor download are not compressed. Anything else (a ToolBook file,
    an office file) gets the default, compressed, as Foolbook packs it.
    """
    blob = Path(path).read_bytes()[:5]
    if blob[:4] in FOOLBOOK_MAGIC and len(blob) == 5:
        return bool(blob[4] & 1)
    if blob.lstrip()[:1] in (b"{", b"["):
        return False
    return True


def is_dirty(saved: dict | None, current: dict) -> bool:
    """True when ``current`` would write something other than ``saved`` did.

    Compared as written, so envelope keys and editor state do not count.
    ``saved`` is None for a book never saved or opened.
    """
    if saved is None:
        return True
    return payload(saved) != payload(current)


def save_path_for(opened: str | Path) -> Path | None:
    """Where Save goes after opening this file, or None to ask (Save as).

    A Foolbook book saves over itself. Anything else saves beside it.
    A ToolBook file named .fbk has nowhere beside it to go that is not
    itself, so Save asks instead of writing over the original.
    """
    opened = Path(opened)
    target = save_target(opened)
    if sniff(opened) != "foolbook" and target == opened:
        return None
    return target


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
