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
    from foolbookeditor.core import save_book, save_system
    from author.files import check_version, payload, save_target
    check_version(book)
    # The same file Save picks everywhere: .fbk, .fsk, or .json, and an
    # import saved beside its original (.sbk as .fsk, anything else as .fbk).
    dest = save_target(path)
    suffix = dest.suffix.lower()
    write = save_system if suffix == ".fsk" else save_book
    temp = dest.with_name(f".{dest.stem}.saving{suffix}")
    try:
        written = write(temp, payload(book), compress=compress)
        replace(written, dest)
    except BaseException:
        try:
            temp.unlink()
        except OSError:
            pass
        raise
    return dest
