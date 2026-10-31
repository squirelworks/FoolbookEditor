"""The book the editor holds.

The editor holds the same book dict Foolbook reads. foolbook.core writes it.
This module only mutates the dict.

A page is text, items (jumps), an optional script, an optional quiz,
and widgets dropped on the slide. A page with `"background": true` is a
shared background, and a page names the one it uses in `uses`. Groups
are not in it yet.
"""

from __future__ import annotations

import re

import copy


WIDGET_KINDS = ("text", "box", "button")

_WIDGET = {
    "text": {"w": 160, "h": 24, "label": "Text"},
    "box": {"w": 100, "h": 60},
    "button": {"w": 80, "h": 24, "label": "Button"},
}


# The book generation. Foolbook's save stamps the same key. A new book
# carries it from the start, so the editor can refuse a newer one.
BOOK_VERSION = 1

PAGE_SIZE = (640, 480)
PAGE_MIN = 64
_HEX = "0123456789abcdef"


def new_book(size: tuple[int, int] = PAGE_SIZE, color: str = "#ffffff") -> dict:
    """A one-page book of that size on paper of that colour.

    The paper is a page-sized rect on the background layer, the same
    shape the reader already paints first and does not treat as a control.
    The reader draws page text only when a page has no shapes, so the
    new page carries no placeholder words.
    """
    w, h = int(size[0]), int(size[1])
    if w < PAGE_MIN or h < PAGE_MIN:
        raise ValueError(f"A page is at least {PAGE_MIN} by {PAGE_MIN}, not {w} by {h}.")
    color = color.strip().lower()
    if len(color) != 7 or color[0] != "#" or any(c not in _HEX for c in color[1:]):
        raise ValueError(f"The background colour is #rrggbb, not {color!r}.")
    book = blank_book()
    book["fbk"] = BOOK_VERSION
    page = book["pages"][0]
    page["size"] = [w, h]
    page["text"] = []
    page["shapes"] = [{
        "kind": "rect",
        "name": "paper",
        "x": 0,
        "y": 0,
        "w": w,
        "h": h,
        "fill": color,
        "outline": "",
        "layer": "background",
    }]
    return book


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


def duplicate_page(book: dict, index: int) -> int:
    """Copy a page, shapes and scripts and all, to right after it.

    The copy gets a fresh id. Nothing in it is shared with the original.
    Returns where the copy landed, or ``index`` when there is no such page.
    """
    found = book.get("pages") or []
    if not (0 <= index < len(found)):
        return index
    twin = copy.deepcopy(found[index])
    twin["id"] = fresh_id(book)
    found.insert(index + 1, twin)
    return index + 1


class LastPage(ValueError):
    """A book keeps at least one page. The reader cannot show a book with none."""


def delete_page(book: dict, index: int) -> int:
    """Drop a page. Returns the index to show.

    Deleting the only page is refused with ``LastPage``. No blank page is
    made in its place. The caller says so; this function does not ask.
    """
    found = book.get("pages") or []
    if not (0 <= index < len(found)):
        return index if found else 0
    if len(found) <= 1:
        raise LastPage("A book keeps at least one page. Add a page before deleting this one.")
    del found[index]
    return min(index, len(found) - 1)


def move_page(book: dict, index: int, delta: int) -> int:
    found = book.get("pages") or []
    j = index + delta
    if not (0 <= index < len(found)) or not (0 <= j < len(found)):
        return index
    found[index], found[j] = found[j], found[index]
    return j


def set_size(page: dict, width, height) -> bool:
    """Store ``size`` as ``[w, h]``. Bad or non-positive numbers leave the old size.

    Shapes are not moved or clipped. A shape past the edge stays in the file.
    """
    try:
        w, h = int(width), int(height)
    except (TypeError, ValueError):
        return False
    if w <= 0 or h <= 0:
        return False
    page["size"] = [w, h]
    return True


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


def set_transition(page: dict, name: str) -> None:
    """Store the page's transition. Foolbook ignores it: pages change with no animation.

    It is kept so a later reader can honour it without a migration. "none"
    or blank stores nothing.
    """
    name = (name or "").strip()
    if name and name.lower() != "none":
        page["transition"] = name
    else:
        page.pop("transition", None)


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


def background_page(book: dict, page_id: str) -> dict | None:
    """The background page with this id, compared without case."""
    wanted = str(page_id or "").lower()
    if not wanted:
        return None
    for page in book.get("pages") or []:
        if page.get("background") and str(page.get("id") or "").lower() == wanted:
            return page
    return None


def background_of(book: dict, page: dict) -> dict | None:
    """The shared background this page uses, or None."""
    return background_page(book, page.get("uses") or "")


def set_background(book: dict, page: dict, page_id: str) -> None:
    """Give a page a shared background. The name must be a background page."""
    if page.get("background"):
        raise ValueError(f"{page.get('id')} is a background and cannot use another")
    found = background_page(book, page_id)
    if found is None:
        raise ValueError(f"no background called {page_id}")
    page["uses"] = found.get("id")


def clear_background(page: dict) -> None:
    page.pop("uses", None)


def backgrounds(book: dict) -> list[dict]:
    """The shared backgrounds, in book order."""
    return [page for page in book.get("pages") or [] if page.get("background")]


def add_background(book: dict) -> dict:
    """A new, empty shared background at the end of the book."""
    used = {str(p.get("id") or "").lower() for p in book.get("pages") or []}
    n = 1
    while True:
        candidate = "Background" if n == 1 else f"Background {n}"
        if candidate.lower() not in used:
            break
        n += 1
    page = {"id": candidate, "background": True, "shapes": []}
    pages(book).append(page)
    return page


def page_label(page: dict) -> str:
    """How the page list names a page. A background says so."""
    name = page.get("id") or "?"
    return f"{name} (background)" if page.get("background") else name


VIEWER_BUTTONS = ("previous", "next", "page")


def viewer_of(book: dict) -> dict | None:
    """The viewer the reader shows: the first one on the book."""
    for viewer in book.get("viewers") or []:
        if isinstance(viewer, dict):
            return viewer
    return None


def set_viewer(book: dict, name: str, size: list[int], buttons: list[str]) -> dict:
    """Store the first viewer. Buttons are previous, next, and page, in that order."""
    asked = [str(b).lower() for b in buttons]
    unknown = [b for b in asked if b not in VIEWER_BUTTONS]
    if unknown:
        raise ValueError(f"no viewer button called {unknown[0]}")
    viewer = {
        "name": name.strip() or "Main",
        "size": [int(size[0]), int(size[1])],
        "buttons": [b for b in VIEWER_BUTTONS if b in asked],
    }
    found = book.setdefault("viewers", [])
    if found and isinstance(found[0], dict):
        found[0] = viewer
    else:
        found.insert(0, viewer)
    return viewer


def system_of(book: dict) -> str | None:
    """The system book this book names, or None."""
    return book.get("system") or None


_ENTER_BOOK = re.compile(r"(?im)^[ \t]*to[ \t]+handle[ \t]+enterBook\b[^\n]*\n")
_PUSH = re.compile(
    r'(?im)^[ \t]*if "[^"\n]+" is not in sysBooks[ \t]*\n'
    r'[ \t]*push "[^"\n]+" onto sysBooks[ \t]*\n'
    r'[ \t]*end if[ \t]*\n'
)


def _push_lines(name: str) -> str:
    return (f'    if "{name}" is not in sysBooks\n'
            f'        push "{name}" onto sysBooks\n'
            f'    end if\n')


def _without_push(script: str) -> str:
    """The book script with the system-book push taken out, and an enterBook left empty by it."""
    script = _PUSH.sub("", script)
    return re.sub(r"(?im)^[ \t]*to[ \t]+handle[ \t]+enterBook\b[^\n]*\n[ \t]*end(?:[ \t]+enterBook)?[ \t]*(?:\n|$)", "", script)


def set_system(book: dict, name: str) -> None:
    """Name the one system book. It is an .fsk file name.

    The reader runs OpenScript and reads no key for this, so the book
    script's enterBook pushes it onto sysBooks, as a ToolBook course does.
    `system` is kept for the editor's own box.
    """
    name = name.strip()
    if not name.lower().endswith(".fsk"):
        raise ValueError(f"{name or 'that'} is not an .fsk system book")
    book["system"] = name
    script = _without_push(str(book.get("script") or ""))
    found = _ENTER_BOOK.search(script)
    if found:
        script = script[:found.end()] + _push_lines(name) + script[found.end():]
    else:
        if script and not script.endswith("\n"):
            script += "\n"
        script += "to handle enterBook\n" + _push_lines(name) + "end\n"
    book["script"] = script


def clear_system(book: dict) -> None:
    book.pop("system", None)
    script = _without_push(str(book.get("script") or ""))
    if script.strip():
        book["script"] = script
    else:
        book.pop("script", None)


def handler_names(book: dict) -> list[str]:
    """`to handle` and `to get` names in the book script and page scripts, in order."""
    import re
    header = re.compile(r"(?im)^[ \t]*to[ \t]+(?:handle|get)[ \t]+([A-Za-z_]\w*)")
    scripts = [book.get("script") or ""]
    scripts += [page.get("script") or "" for page in book.get("pages") or []]
    names = [m.group(1) for script in scripts for m in header.finditer(str(script))]
    names += [str(h.get("name")) for h in book.get("handlers") or [] if isinstance(h, dict) and h.get("name")]
    return list(dict.fromkeys(names))
