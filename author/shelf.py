"""The catalog: the books in a folder the author picks.

One row per .fbk or .fsk, in file name order, with its title and page
count. A book that will not open is still a row, and the row says why.
This is not the vendor catalog format.
"""

from __future__ import annotations

from pathlib import Path

BOOK_SUFFIXES = (".fbk", ".fsk")


def list_books(folder: str | Path) -> list[dict]:
    from foolbookeditor.core import load
    folder = Path(folder)
    if not folder.is_dir():
        return []
    rows = []
    for path in sorted(folder.iterdir(), key=lambda p: p.name.lower()):
        if not path.is_file() or path.suffix.lower() not in BOOK_SUFFIXES:
            continue
        row = {"file": path.name, "path": path, "title": "", "pages": 0, "error": ""}
        try:
            book = load(path)
        except Exception as exc:  # any reason a file is not a book is a row, not a crash
            row["error"] = f"Cannot open: {exc}" if str(exc) else "Cannot open"
        else:
            row["title"] = str(book.get("title") or path.stem)
            row["pages"] = len(book.get("pages") or [])
        rows.append(row)
    return rows
