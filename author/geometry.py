"""Geometry for the Author stage, in page coordinates.

Pure functions over the shape dicts the reader draws. Nothing here knows
about Tk, so the web editor can be checked against the same numbers.
"""

from __future__ import annotations

import math

# How close, in page pixels, a click must be to a line to hit it.
LINE_SLOP = 3.0

_LINES = {"line", "curve"}


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
