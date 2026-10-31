"""Small drawings of each page for the page list.

Not a screenshot. Each shape becomes one rectangle, oval, line, or polygon,
scaled to fit the page into the thumbnail. Hidden shapes are left out,
because the reader leaves them out. Tk draws the result; nothing else is needed.
"""

from __future__ import annotations

from author.stage import page_size
from author.tools import bounds_of

SIZE = (96, 72)

_OVAL = {"ellipse", "arc", "pie", "chord"}
_LINE = {"line", "curve"}
_POLY = {"polygon"}


def miniature(page: dict, width: int = SIZE[0], height: int = SIZE[1]) -> list[tuple]:
    """``(kind, coords, fill, outline)`` in thumbnail pixels, in paint order.

    ``kind`` is ``page``, ``rect``, ``oval``, ``line``, or ``polygon``. The first
    item is always the page itself.
    """
    pw, ph = page_size(page)
    scale = min(width / pw, height / ph)
    ops: list[tuple] = [("page", (0.0, 0.0, pw * scale, ph * scale), "#ffffff", "#7f7f7f")]
    from author.geometry import flatten

    for shape in flatten(page.get("shapes") or []):
        if not isinstance(shape, dict) or shape.get("visible") is False:
            continue
        kind = shape.get("kind") or ""
        fill = shape.get("fill") or ""
        outline = shape.get("outline") or "#000000"
        points = [pt for pt in shape.get("points") or [] if len(pt) >= 2]
        if kind in _LINE and len(points) >= 2:
            coords = tuple(float(v) * scale for pt in points for v in pt[:2])
            ops.append(("line", coords, "", outline))
            continue
        if kind in _POLY and len(points) >= 3:
            coords = tuple(float(v) * scale for pt in points for v in pt[:2])
            ops.append(("polygon", coords, fill, outline))
            continue
        x, y, w, h = bounds_of(shape)
        if not (w or h):
            continue
        box = (x * scale, y * scale, (x + w) * scale, (y + h) * scale)
        ops.append(("oval" if kind in _OVAL else "rect", box, fill, outline))
    return ops


def draw(canvas, ops: list[tuple], left: float, top: float, tag: str) -> None:
    """Put one miniature on a Tk canvas with its top-left at ``(left, top)``."""
    for kind, coords, fill, outline in ops:
        moved = [v + (left if i % 2 == 0 else top) for i, v in enumerate(coords)]
        if kind == "line":
            canvas.create_line(*moved, fill=outline, tags=(tag,))
        elif kind == "polygon":
            canvas.create_polygon(*moved, fill=fill, outline=outline, tags=(tag,))
        elif kind == "oval":
            canvas.create_oval(*moved, fill=fill, outline=outline, tags=(tag,))
        else:
            canvas.create_rectangle(*moved, fill=fill, outline=outline, tags=(tag,))
