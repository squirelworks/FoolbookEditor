"""The book the editor holds.

The editor holds the same book dict Foolbook reads. foolbook.core writes it.
This module only mutates the dict.

A page is text, items (jumps), an optional script, an optional quiz,
and widgets dropped on the slide. That is the scaffold. Groups,
backgrounds, and pictures are not in it yet.
"""

from __future__ import annotations


WIDGET_KINDS = ("text", "box", "button")

_WIDGET = {
    "text": {"w": 160, "h": 24, "label": "Text"},
    "box": {"w": 100, "h": 60},
    "button": {"w": 80, "h": 24, "label": "Button"},
}


# The book generation. Foolbook's save stamps the same key. A new book
# carries it from the start, so the editor can refuse a newer one.
BOOK_VERSION = 1


def blank_book() -> dict:
    return {
        "fbk": BOOK_VERSION,
        "id": "new",
        "title": "New book",
        "pages": [blank_page("P0")],
    }


def blank_page(page_id: str) -> dict:
    return {"id": page_id, "text": ["New slide"], "items": [], "shapes": []}


def pages(book: dict) -> list:
    return book.setdefault("pages", [])


def page_at(book: dict, index: int) -> dict | None:
    found = book.get("pages") or []
    if 0 <= index < len(found):
        return found[index]
    return None


def fresh_id(book: dict) -> str:
    """Next page id in the P0, P100, P200 style already used by courses."""
    used = {(p.get("id") or "").lower() for p in book.get("pages") or []}
    n = 0
    while True:
        candidate = "P0" if n == 0 else f"P{n * 100}"
        if candidate.lower() not in used:
            return candidate
        n += 1


def add_page(book: dict, index: int | None = None) -> int:
    """Insert a blank page. None appends. Returns where it landed."""
    found = pages(book)
    at = len(found) if index is None else index
    if at < 0 or at > len(found):
        at = len(found)
    found.insert(at, blank_page(fresh_id(book)))
    return at


def delete_page(book: dict, index: int) -> int:
    """Drop a page. The last page stays. Returns the index to show."""
    found = book.get("pages") or []
    if len(found) <= 1 or not (0 <= index < len(found)):
        return index if found else 0
    del found[index]
    return min(index, len(found) - 1)


def move_page(book: dict, index: int, delta: int) -> int:
    found = book.get("pages") or []
    j = index + delta
    if not (0 <= index < len(found)) or not (0 <= j < len(found)):
        return index
    found[index], found[j] = found[j], found[index]
    return j


class DuplicateId(ValueError):
    """Another page in the book already has that id."""


def rename_page(book: dict, index: int, page_id: str) -> str:
    """Give the page at ``index`` a new id. Returns the id it has now.

    Ids are unique in a book. The reader finds a page by id without
    regard to case, so ``p100`` collides with ``P100``. The casing the
    author typed is the one stored. A blank id keeps the old one.
    """
    found = book.get("pages") or []
    page = found[index]
    wanted = (page_id or "").strip()
    if not wanted:
        return page.get("id") or ""
    for i, other in enumerate(found):
        if i != index and (other.get("id") or "").lower() == wanted.lower():
            raise DuplicateId(f"Another page is already {other.get('id')}.")
    page["id"] = wanted
    return wanted


def set_id(page: dict, page_id: str) -> None:
    page["id"] = page_id.strip() or page.get("id") or "P0"


def text_from_editor(raw: str) -> list[str]:
    """Blank line splits paragraphs. A line starting with - or * stays in its block."""
    return [block.strip() for block in raw.split("\n\n") if block.strip()]


def text_to_editor(blocks: list[str] | None) -> str:
    return "\n\n".join(blocks or [])


def set_text(page: dict, blocks: list[str]) -> None:
    page["text"] = list(blocks)


def nav_of(page: dict) -> tuple[str, str]:
    nxt = back = ""
    for item in page.get("items") or []:
        label = (item.get("label") or "").lower()
        if label == "next":
            nxt = item.get("page") or ""
        elif label == "back":
            back = item.get("page") or ""
    return nxt, back


def set_nav(page: dict, nxt: str, back: str) -> None:
    """Replace only the Next and Back jumps. Other items stay."""
    kept = [
        item for item in page.get("items") or []
        if (item.get("label") or "").lower() not in ("next", "back")
    ]
    items = []
    if nxt.strip():
        items.append({"label": "Next", "page": nxt.strip()})
    if back.strip():
        items.append({"label": "Back", "page": back.strip()})
    page["items"] = items + kept


def set_script(page: dict, source: str) -> None:
    """Page script. The loader turns a non-empty script into one handler."""
    source = source.strip()
    if not source:
        page.pop("script", None)
        return
    page["script"] = source if source.endswith("\n") else source + "\n"


def set_quiz(page: dict, quiz: dict | None) -> None:
    if quiz:
        page["quiz"] = quiz
    else:
        page.pop("quiz", None)


def set_item(shape: dict, page: str, book: str = "", label: str = "") -> None:
    """The jump a click on this shape follows. An empty page clears it.

    The reader follows ``item`` when the shape has no script, or when
    its script did not move the page.
    """
    page = (page or "").strip()
    if not page:
        shape.pop("item", None)
        return
    item = {"page": page}
    if (book or "").strip():
        item["book"] = book.strip()
    if (label or "").strip():
        item["label"] = label.strip()
    shape["item"] = item


def widgets(page: dict) -> list:
    return page.setdefault("widgets", [])


def add_widget(page: dict, kind: str, x: int, y: int) -> dict:
    if kind not in _WIDGET:
        raise ValueError(f"unknown widget {kind}")
    spec = _WIDGET[kind]
    widget = {"kind": kind, "x": int(x), "y": int(y), "w": spec["w"], "h": spec["h"]}
    if "label" in spec:
        widget["label"] = spec["label"]
    widgets(page).append(widget)
    return widget
