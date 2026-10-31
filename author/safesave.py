"""Save beside, then replace. A crash while saving leaves the previous file.

Foolbook writes the book to a temporary file in the same folder. Only a
finished file replaces the old one, and `os.replace` does that in one
step on the same disk. If anything fails first, the temporary file is
removed and the old book is untouched.
"""

from __future__ import annotations

import os
from pathlib import Path


def save_safely(path: str | Path, book: dict, compress: bool = True, replace=os.replace) -> Path:
    """Write `book` to `path` through a temporary file. `replace` is the step a test can fail."""
    from foolbookeditor.core import save_book
    from author.files import check_version, payload
    check_version(book)
    dest = Path(path)
    suffix = dest.suffix.lower()
    if suffix not in (".fbk", ".json"):
        dest = dest.with_suffix(".fbk")
        suffix = ".fbk"
    temp = dest.with_name(f".{dest.stem}.saving{suffix}")
    try:
        written = save_book(temp, payload(book), compress=compress)
        replace(written, dest)
    except BaseException:
        try:
            temp.unlink()
        except OSError:
            pass
        raise
    return dest
