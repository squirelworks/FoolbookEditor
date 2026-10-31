"""A picture placed on the page.

The book is one file, so a picture is embedded as base64 PNG by default.
Linking keeps a path beside the book instead. A file too large to embed
is refused with a sentence the window can show.
"""

from __future__ import annotations

import base64
import os
from pathlib import Path

# Pictures at or under this many bytes are taken. A larger file is refused.
LIMIT = 20 * 1024 * 1024


class PictureRefused(ValueError):
    """Why a picture was not placed. The message is the sentence to show."""


def picture_fields(path: str | Path, embed: bool = True, book: str | Path | None = None) -> dict:
    """The ``data`` or ``src`` for an image shape made from that file."""
    path = Path(path)
    size = path.stat().st_size
    if size > LIMIT:
        raise PictureRefused(
            f"{path.name} is {size / (1024 * 1024):.1f} MB. "
            f"Author places pictures up to {LIMIT // (1024 * 1024)} MB."
        )
    if not embed:
        return {"src": _beside(path, book)}
    from author.bitmap import import_bitmap
    try:
        data, pixels = import_bitmap(path.read_bytes())
    except ValueError as exc:
        raise PictureRefused(f"{path.name} is not a picture Author can read. {exc}") from exc
    return {"data": base64.b64encode(data).decode("ascii"), "pixels": list(pixels)}


def _beside(path: Path, book: str | Path | None) -> str:
    """The path as the book will look for it: relative to the book's folder when it can be."""
    if book:
        try:
            return Path(os.path.relpath(path.resolve(), Path(book).resolve().parent)).as_posix()
        except ValueError:
            pass
    return path.as_posix()
