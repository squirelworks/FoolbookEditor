"""The page picture in the middle of Author.

Foolbook draws it. The editor only chooses the page and the scale.
An object Reader hides is still drawn, so Author can select it.
A hotspot is drawn as its outline for the same reason.
"""

from __future__ import annotations


def shown(page: dict) -> list[dict]:
    """Shapes in book order. A hidden one is drawn, not dropped."""
    rows = []
    for shape in page.get("shapes") or []:
        if not isinstance(shape, dict):
            continue
        if (shape.get("kind") or "") == "hotspot":
            # Reader does not draw a hotspot. Author draws its outline so it can be found.
            shape = dict(shape, kind="rect", fill="", outline=shape.get("outline") or "#071428")
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

    When a layer is named, an object on the other layer cannot be selected.
    """
    for index in range(len(shapes) - 1, -1, -1):
        shape = shapes[index]
        if layer and (shape.get("layer") or "page") != layer:
            continue
        left = float(shape.get("x") or 0)
        top = float(shape.get("y") or 0)
        if left <= x <= left + float(shape.get("w") or 0) and top <= y <= top + float(shape.get("h") or 0):
            return index
    return None


def paint(canvas, page: dict) -> None:
    """Draw one page into the editor's canvas, fitted to that canvas."""
    from engine.graphics import draw
    from engine.place import content_box, fit_view, place_window

    canvas.delete("all")
    shapes = shown(page)
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    if width < 20 or height < 20:
        canvas.after(50, lambda: paint(canvas, page))
        return
    box = content_box(shapes) if shapes else (0.0, 0.0, 640.0, 480.0)
    scale, dx, dy, ox, oy = fit_view(box, width, height)
    draw(canvas, place_window(shapes, scale, box[0], box[1], dx, dy))
    canvas._author_view = {
        "scale": scale,
        "ox": ox,
        "oy": oy,
        "x0": box[0],
        "y0": box[1],
        "shapes": shapes,
    }
