"""The page picture in the middle of Author.

Foolbook draws it. The editor only chooses the page and the scale.
An object Reader hides is still drawn, so Author can select it.
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


def shown(page: dict) -> list[dict]:
    """Shapes in book order. A hidden one is drawn, not dropped."""
    rows = []
    for shape in page.get("shapes") or []:
        if not isinstance(shape, dict):
            continue
        if shape.get("visible") is False:
            item = dict(shape)
            item["visible"] = True
            item["outline"] = item.get("outline") or "#606060"
            rows.append(item)
        else:
            rows.append(shape)
    return rows


def hit(shapes: list[dict], x: float, y: float, layer: str | None = None) -> int | None:
    """The topmost object under a page coordinate. None is the page itself.

    ``author.geometry.hit`` does the work.
    """
    from author.geometry import hit as geometry_hit

    return geometry_hit(shapes, x, y, layer)


def paint(canvas, page: dict) -> None:
    """Draw one page into the editor's canvas, fitted to that canvas."""
    from engine.graphics import draw
    from engine.place import fit_view, place_window

    canvas.delete("all")
    shapes = shown(page)
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    if width < 20 or height < 20:
        canvas.after(50, lambda: paint(canvas, page))
        return
    box = view_box(page, shapes)
    scale, dx, dy, ox, oy = fit_view(box, width, height)
    # A group is painted as its children. Hit tests still see the group.
    from author.geometry import flatten
    painted = shown({"shapes": flatten(page.get("shapes") or [])})
    draw(canvas, place_window(painted, scale, box[0], box[1], dx, dy))
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
