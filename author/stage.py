"""The page picture in the middle of Author.

Foolbook draws it. The editor only chooses the page and the scale.
An object Reader hides is still drawn, so Author can select it.
A hotspot is drawn as its outline for the same reason.
"""

from __future__ import annotations

# The page an author sees when the book does not say. The web editor uses it too.
DEFAULT_SIZE = (640, 480)


def page_size(page: dict | None) -> tuple[int, int]:
    """The page's ``size`` as ``(w, h)``, or the default when it is missing or bad."""
    size = (page or {}).get("size")
    if isinstance(size, (list, tuple)) and len(size) >= 2:
        try:
            w, h = int(size[0]), int(size[1])
        except (TypeError, ValueError):
            return DEFAULT_SIZE
        if w > 0 and h > 0:
            return w, h
    return DEFAULT_SIZE


def view_box(page: dict | None, shapes: list[dict]) -> tuple[float, float, float, float]:
    """What the stage fits: the whole page, grown to take in shapes that hang off it."""
    from author.tools import bounds_of

    w, h = page_size(page)
    left, top, right, bottom = 0.0, 0.0, float(w), float(h)
    for shape in shapes:
        x, y, sw, sh = bounds_of(shape)
        if not (sw or sh or x or y):
            continue
        left, top = min(left, x), min(top, y)
        right, bottom = max(right, x + sw), max(bottom, y + sh)
    return left, top, right, bottom


def shown(page: dict, book: dict | None = None) -> list[dict]:
    """Shapes in book order. A hidden one is drawn, not dropped.

    Given the book, the shared background the page uses comes first. Those
    shapes are copies. They are edited on the background page.
    """
    rows = []
    if book is not None:
        from author.document import background_of
        under = background_of(book, page)
        for shape in shown(under) if under else []:
            item = dict(shape)
            item.setdefault("layer", "background")
            rows.append(item)
    for shape in page.get("shapes") or []:
        if not isinstance(shape, dict):
            continue
        if (shape.get("kind") or "") == "hotspot":
            # Reader does not draw a hotspot. Author draws its outline so it can be found.
            shape = dict(shape, kind="rect", fill="", outline=shape.get("outline") or "#071428")
        if shape.get("visible") is False:
            # Ghosted: the same object, its colours washed toward white.
            item = dict(shape)
            item["visible"] = True
            item["outline"] = ghost(item.get("outline") or "#606060")
            if item.get("fill"):
                item["fill"] = ghost(item["fill"])
            item["ghost"] = True
            rows.append(item)
        else:
            rows.append(shape)
    return rows


def ghost(color: str, amount: float = 0.7) -> str:
    """A ``#rrggbb`` colour moved most of the way to white. Anything else is a light grey."""
    text = str(color or "")
    if len(text) != 7 or not text.startswith("#"):
        return "#c8c8c8"
    try:
        parts = [int(text[at:at + 2], 16) for at in (1, 3, 5)]
    except ValueError:
        return "#c8c8c8"
    return "#" + "".join(f"{int(round(part + (255 - part) * amount)):02x}" for part in parts)


def hit(shapes: list[dict], x: float, y: float, layer: str | None = None) -> int | None:
    """The topmost object under a page coordinate. None is the page itself.

    ``author.geometry.hit`` does the work.
    """
    from author.geometry import hit as geometry_hit

    return geometry_hit(shapes, x, y, layer)


def paint(canvas, page: dict, book: dict | None = None, zoom: float | None = None) -> None:
    """Draw one page into the editor's canvas, fitted to that canvas.

    Only the page's own shapes can be hit. A shared background is drawn under them.
    A zoom of None fits the page to the canvas. A number draws it at that size and scrolls.
    """
    from engine.graphics import draw
    from engine.place import place_window
    from author.view import placed

    canvas.delete("all")
    shapes = shown(page)
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    if width < 20 or height < 20:
        canvas.after(50, lambda: paint(canvas, page, book, zoom))
        return
    # A group is painted as its children. Hit tests still see the group.
    from author.geometry import flatten
    drawn = shown(dict(page, shapes=flatten(page.get("shapes") or [])), book)
    box = view_box(page, drawn)
    scale, dx, dy, ox, oy, region_w, region_h = placed(box, zoom, width, height)
    canvas.configure(scrollregion=(0, 0, region_w, region_h))
    draw(canvas, place_window(drawn, scale, box[0], box[1], dx, dy))
    # The page edge. A shape past it is kept in the file and drawn past the line.
    pw, ph = page_size(page)
    left = (0 - box[0]) * scale + ox
    top = (0 - box[1]) * scale + oy
    canvas.create_rectangle(left, top, left + pw * scale, top + ph * scale, outline="#7f7f7f", dash=(4, 3), tags=("page-edge",))
    canvas._author_view = {
        "scale": scale,
        "ox": ox,
        "oy": oy,
        "x0": box[0],
        "y0": box[1],
        "shapes": shapes,
    }
