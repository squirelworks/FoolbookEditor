"""Geometry for the Author stage, in page coordinates.

Pure functions over the shape dicts the reader draws. Nothing here knows
about Tk, so the web editor can be checked against the same numbers.
"""

from __future__ import annotations

import math

# How close, in page pixels, a click must be to a line to hit it.
LINE_SLOP = 3.0

_LINES = {"line", "curve"}

# Arrow keys move the selection by NUDGE page pixels, Shift+arrow by NUDGE_BIG.
NUDGE = 1
NUDGE_BIG = 8

# No resize makes a shape smaller than this, in page pixels, either way.
MIN_SIZE = 4

# Box handles: which edges each one pulls. l/r/t/b = left, right, top, bottom.
BOX_HANDLES = {
    "nw": "lt", "n": "t", "ne": "rt", "e": "r",
    "se": "rb", "s": "b", "sw": "lb", "w": "l",
}


def bounds(shape: dict) -> tuple[float, float, float, float]:
    """``(x, y, w, h)``. A shape with no width and height uses its points."""
    x = float(shape.get("x") or 0)
    y = float(shape.get("y") or 0)
    w = float(shape.get("w") or 0)
    h = float(shape.get("h") or 0)
    points = [pt for pt in list(shape.get("points") or []) + list(shape.get("ends") or []) if len(pt) >= 2]
    if (w and h) or not points:
        return x, y, w, h
    xs = [float(pt[0]) for pt in points]
    ys = [float(pt[1]) for pt in points]
    return min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)


def _near_segment(px: float, py: float, ax: float, ay: float, bx: float, by: float, slop: float) -> bool:
    dx, dy = bx - ax, by - ay
    length = dx * dx + dy * dy
    t = 0.0 if not length else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / length))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy)) <= slop


def contains(shape: dict, x: float, y: float) -> bool:
    """Is the page point on the shape. A line is hit near its stroke, not its box."""
    points = [pt for pt in shape.get("points") or [] if len(pt) >= 2]
    if (shape.get("kind") or "") in _LINES and len(points) >= 2:
        return any(
            _near_segment(x, y, float(a[0]), float(a[1]), float(b[0]), float(b[1]), LINE_SLOP)
            for a, b in zip(points, points[1:])
        )
    left, top, w, h = bounds(shape)
    return left <= x <= left + w and top <= y <= top + h


def hit(shapes: list[dict], x: float, y: float, layer: str | None = None) -> int | None:
    """Index of the topmost shape under the point, or None for the page.

    Array order is paint order, so the last match wins. When ``layer`` is
    named, only shapes on that layer can be hit: background shapes are hit
    only when the background is what the tools work on.
    """
    for index in range(len(shapes) - 1, -1, -1):
        shape = shapes[index]
        if not isinstance(shape, dict):
            continue
        if layer and (shape.get("layer") or "page") != layer:
            continue
        if contains(shape, x, y):
            return index
    return None


def intersects(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> bool:
    """Do two ``(x, y, w, h)`` boxes touch or overlap."""
    return a[0] <= b[0] + b[2] and b[0] <= a[0] + a[2] and a[1] <= b[1] + b[3] and b[1] <= a[1] + a[3]


def marquee(shapes: list[dict], x0: float, y0: float, x1: float, y1: float, layer: str | None = None) -> list[int]:
    """Indices, in array order, of every shape whose bounds meet the dragged box.

    The box may be dragged in any direction. A line uses its points' bounds.
    """
    box = (min(x0, x1), min(y0, y1), abs(x1 - x0), abs(y1 - y0))
    found = []
    for index, shape in enumerate(shapes):
        if not isinstance(shape, dict):
            continue
        if layer and (shape.get("layer") or "page") != layer:
            continue
        if intersects(box, bounds(shape)):
            found.append(index)
    return found


def offset(shape: dict, dx: float, dy: float) -> None:
    """Move one shape, its points and arc ends included. Size does not change."""
    if "x" in shape or shape.get("w"):
        shape["x"] = int(round(float(shape.get("x") or 0) + dx))
        shape["y"] = int(round(float(shape.get("y") or 0) + dy))
    for key in ("points", "ends"):
        if shape.get(key):
            shape[key] = [[pt[0] + dx, pt[1] + dy] + list(pt[2:]) for pt in shape[key]]


def nudge(shapes: list[dict], indices: list[int], dx: float, dy: float) -> None:
    """Move every selected shape by the same amount."""
    for index in dict.fromkeys(indices):
        if 0 <= index < len(shapes) and isinstance(shapes[index], dict):
            offset(shapes[index], dx, dy)


def arrow_step(key: str, shift: bool) -> tuple[int, int]:
    """``(dx, dy)`` for an arrow key name: Left, Right, Up, Down."""
    step = NUDGE_BIG if shift else NUDGE
    return {"Left": (-step, 0), "Right": (step, 0), "Up": (0, -step), "Down": (0, step)}.get(key, (0, 0))


def is_line(shape: dict) -> bool:
    points = [pt for pt in shape.get("points") or [] if len(pt) >= 2]
    return (shape.get("kind") or "") in _LINES and len(points) >= 2


def handles(shape: dict) -> dict[str, tuple[float, float]]:
    """Where the resize handles sit. A line's ends are its handles, ``p0`` and ``p1``.

    Any other shape has eight: the corners and the middle of each side.
    """
    if is_line(shape):
        points = [pt for pt in shape.get("points") or [] if len(pt) >= 2]
        ends = {0: points[0], len(points) - 1: points[-1]}
        return {f"p{i}": (float(pt[0]), float(pt[1])) for i, pt in ends.items()}
    x, y, w, h = bounds(shape)
    mx, my = x + w / 2, y + h / 2
    return {
        "nw": (x, y), "n": (mx, y), "ne": (x + w, y), "e": (x + w, my),
        "se": (x + w, y + h), "s": (mx, y + h), "sw": (x, y + h), "w": (x, my),
    }


def resize(shape: dict, before: dict, handle: str, px: float, py: float) -> None:
    """Pull one handle to the page point ``(px, py)``.

    ``before`` is a copy of the shape from the start of the drag. The edges the
    handle does not pull stay put. Neither side gets smaller than MIN_SIZE. A
    line end moves on its own, and cannot come within MIN_SIZE of the other end.
    Points inside a box shape are scaled with it.
    """
    if handle.startswith("p"):
        at = int(handle[1:])
        points = [list(pt) for pt in before.get("points") or []]
        if not (0 <= at < len(points)):
            return
        other = points[-1] if at == 0 else points[0]
        if math.hypot(px - float(other[0]), py - float(other[1])) < MIN_SIZE:
            return
        points[at] = [px, py] + points[at][2:]
        shape["points"] = points
        if "x" in before or before.get("w"):
            x, y, w, h = bounds({"points": points})
            shape["x"], shape["y"], shape["w"], shape["h"] = int(x), int(y), int(w), int(h)
        return
    pulls = BOX_HANDLES.get(handle)
    if not pulls:
        return
    x, y, w, h = bounds(before)
    left, top, right, bottom = x, y, x + w, y + h
    if "l" in pulls:
        left = min(px, right - MIN_SIZE)
    if "r" in pulls:
        right = max(px, left + MIN_SIZE)
    if "t" in pulls:
        top = min(py, bottom - MIN_SIZE)
    if "b" in pulls:
        bottom = max(py, top + MIN_SIZE)
    nw, nh = right - left, bottom - top
    shape["x"], shape["y"], shape["w"], shape["h"] = int(round(left)), int(round(top)), int(round(nw)), int(round(nh))
    for key in ("points", "ends"):
        if before.get(key) and w and h:
            shape[key] = [
                [left + (float(pt[0]) - x) * nw / w, top + (float(pt[1]) - y) * nh / h] + list(pt[2:])
                for pt in before[key]
            ]
