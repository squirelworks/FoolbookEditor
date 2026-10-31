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
