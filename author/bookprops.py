"""Book properties: title, author, default page size, and first page.

They are stored on the book. Foolbook opens the book at `firstPage`
when it names a page, else at the first page.
"""

from __future__ import annotations

import re

PAGE_SIZE = (640, 480)
PAGE_MIN = 64
_SIZE = re.compile(r"^\s*(\d+)\s*[x×,]\s*(\d+)\s*$", re.IGNORECASE)


def properties(book: dict) -> dict:
    w, h = book.get("pageSize") or PAGE_SIZE
    return {
        "title": str(book.get("title") or ""),
        "author": str(book.get("author") or ""),
        "size": f"{w} x {h}",
        "firstPage": str(book.get("firstPage") or ""),
    }


def set_properties(book: dict, title: str, author: str, size: str, first_page: str) -> None:
    """Check everything first. A bad value changes nothing."""
    m = _SIZE.match(size or "")
    if not m:
        raise ValueError(f"Page size is width x height, like 640 x 480, not {size!r}.")
    w, h = int(m.group(1)), int(m.group(2))
    if w < PAGE_MIN or h < PAGE_MIN:
        raise ValueError(f"A page is at least {PAGE_MIN} by {PAGE_MIN}.")
    first_page = (first_page or "").strip()
    ids = [str(p.get("id") or "") for p in book.get("pages") or []]
    if first_page and first_page not in ids:
        raise ValueError(f"There is no page {first_page}.")
    book["title"] = (title or "").strip() or book.get("title") or "Untitled"
    for key, value in (("author", (author or "").strip()), ("firstPage", first_page)):
        if value:
            book[key] = value
        else:
            book.pop(key, None)
    book["pageSize"] = [w, h]
