"""``python3 -m foolbookeditor --selftest``.

Build a book in memory, save it, load it, and check that the page id,
one shape, and one script came back. Then the reader opens that file
and Using Foolbook. No window. Every editor pull request runs this.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

PAGE_ID = "P0"
SCRIPT = 'to handle buttonClick\n  go to next page\nend\n'


def sample() -> dict:
    return {
        "id": "selftest",
        "title": "Self test",
        "pages": [{
            "id": PAGE_ID,
            "text": ["Self test"],
            "items": [],
            "shapes": [{
                "kind": "button", "name": "Next", "text": "Next",
                "x": 20, "y": 20, "w": 90, "h": 28,
                "script": SCRIPT,
            }],
        }],
    }


def problems(book: dict) -> list[str]:
    """What is wrong with a loaded self-test book. Empty means it passed."""
    found = []
    pages = book.get("pages") or []
    if len(pages) != 1 or pages[0].get("id") != PAGE_ID:
        found.append(f"page id: expected {PAGE_ID}, got {[p.get('id') for p in pages]}")
        return found
    shapes = pages[0].get("shapes") or []
    if len(shapes) != 1 or shapes[0].get("kind") != "button":
        found.append(f"shape: expected one button, got {shapes}")
        return found
    if shapes[0].get("script") != SCRIPT:
        found.append(f"script: got {shapes[0].get('script')!r}")
    return found


def reader_problems(path: Path, page_ids: list[str] | None = None) -> list[str]:
    """Open a file the way the reader does. Empty means it opened."""
    from foolbookeditor.core import read
    try:
        book = read(path)
    except Exception as exc:
        return [f"reader: {path.name}: {exc}"]
    found = [p.get("id") for p in book.get("pages") or []]
    if not found:
        return [f"reader: {path.name}: no pages"]
    if page_ids is not None and found != page_ids:
        return [f"reader: {path.name}: pages {found}, expected {page_ids}"]
    return []


def run(out=print) -> int:
    from foolbookeditor.core import load, save_book, shipped_book
    with tempfile.TemporaryDirectory() as tmp:
        path = save_book(Path(tmp) / "selftest.fbk", sample())
        book = load(path)
        found = problems(book)
        found += reader_problems(path, [PAGE_ID])
    if not found:
        out("selftest: the reader opens the saved book")
    using = shipped_book("using_foolbook")
    if using is None:
        out("selftest: Using Foolbook is not installed beside the reader, not checked")
    else:
        more = reader_problems(using)
        found += more
        if not more:
            out("selftest: the reader opens Using Foolbook")
    for line in found:
        out(f"selftest: {line}")
    out("selftest: ok" if not found else "selftest: failed")
    return 0 if not found else 1
