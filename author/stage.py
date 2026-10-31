"""The page picture in the middle of Author.

Foolbook draws it. The editor only chooses the page and the scale.
An object Reader hides is still drawn, so Author can select it.
A hotspot is drawn as its outline for the same reason.
"""

from __future__ import annotations


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


def paint(canvas, page: dict, book: dict | None = None) -> None:
    """Draw one page into the editor's canvas, fitted to that canvas.

    Only the page's own shapes can be hit. A shared background is drawn under them.
    """
    from engine.graphics import draw
    from engine.place import content_box, fit_view, place_window

    canvas.delete("all")
    shapes = shown(page)
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    if width < 20 or height < 20:
        canvas.after(50, lambda: paint(canvas, page, book))
        return
    drawn = shown(page, book)
    box = content_box(drawn) if drawn else (0.0, 0.0, 640.0, 480.0)
    scale, dx, dy, ox, oy = fit_view(box, width, height)
    draw(canvas, place_window(drawn, scale, box[0], box[1], dx, dy))
    canvas._author_view = {
        "scale": scale,
        "ox": ox,
        "oy": oy,
        "x0": box[0],
        "y0": box[1],
        "shapes": shapes,
    }
