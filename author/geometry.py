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

# The grid is off until the author turns it on. Snapping happens on release.
GRID = 8

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
    """Move one shape, its points, arc ends, and a group's children included.

    Size does not change.
    """
    if "x" in shape or shape.get("w"):
        shape["x"] = int(round(float(shape.get("x") or 0) + dx))
        shape["y"] = int(round(float(shape.get("y") or 0) + dy))
    for key in ("points", "ends"):
        if shape.get(key):
            shape[key] = [[pt[0] + dx, pt[1] + dy] + list(pt[2:]) for pt in shape[key]]
    for child in shape.get("children") or []:
        if isinstance(child, dict):
            offset(child, dx, dy)


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
    if (shape.get("kind") or "") == "group":
        # Resizing a group, and everything in it, is not done yet. It only moves.
        return {}
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


def constrain_box(x0: float, y0: float, x1: float, y1: float) -> tuple[float, float]:
    """Shift while drawing a box: the far corner moves so the box is a square.

    The side is the longer of the two drags. The drag direction is kept.
    """
    side = max(abs(x1 - x0), abs(y1 - y0))
    return x0 + math.copysign(side, (x1 - x0) or 1), y0 + math.copysign(side, (y1 - y0) or 1)


def constrain_line(x0: float, y0: float, x1: float, y1: float) -> tuple[float, float]:
    """Shift while drawing a line: the end snaps to horizontal, vertical, or 45 degrees.

    The nearest of the eight directions wins. The length along it is kept
    for horizontal and vertical, and is the longer leg for a diagonal.
    """
    dx, dy = x1 - x0, y1 - y0
    if not dx and not dy:
        return x1, y1
    angle = math.degrees(math.atan2(dy, dx)) % 180
    if angle < 22.5 or angle >= 157.5:
        return x1, y0
    if 67.5 <= angle < 112.5:
        return x0, y1
    leg = max(abs(dx), abs(dy))
    return x0 + math.copysign(leg, dx or 1), y0 + math.copysign(leg, dy or 1)


def snap(value: float, grid: int = GRID) -> int:
    """The nearest grid line. A half-way value goes up."""
    if grid <= 0:
        return int(round(value))
    return int(math.floor(value / grid + 0.5) * grid)


def snap_point(x: float, y: float, grid: int = GRID) -> tuple[int, int]:
    return snap(x, grid), snap(y, grid)


def snap_move(shapes: list[dict], indices: list[int], grid: int = GRID) -> None:
    """After a move, shift the selection so the first shape's top-left is on the grid.

    The others move by the same amount, so their spacing is kept.
    """
    chosen = [i for i in dict.fromkeys(indices) if 0 <= i < len(shapes) and isinstance(shapes[i], dict)]
    if not chosen:
        return
    x, y, _w, _h = bounds(shapes[chosen[0]])
    dx, dy = snap(x, grid) - x, snap(y, grid) - y
    if dx or dy:
        nudge(shapes, chosen, dx, dy)


# Align choices, in the order the menu lists them.
ALIGN = ("left", "right", "top", "bottom", "center horizontal", "center vertical")


def align(shapes: list[dict], indices: list[int], how: str) -> None:
    """Line the selection up with the first selected shape, which does not move.

    ``center horizontal`` puts every centre on the first shape's vertical
    centre line (they share an x centre). ``center vertical`` shares a y centre.
    """
    chosen = [i for i in dict.fromkeys(indices) if 0 <= i < len(shapes) and isinstance(shapes[i], dict)]
    if len(chosen) < 2:
        return
    rx, ry, rw, rh = bounds(shapes[chosen[0]])
    for index in chosen[1:]:
        x, y, w, h = bounds(shapes[index])
        dx = dy = 0.0
        if how == "left":
            dx = rx - x
        elif how == "right":
            dx = (rx + rw) - (x + w)
        elif how == "top":
            dy = ry - y
        elif how == "bottom":
            dy = (ry + rh) - (y + h)
        elif how == "center horizontal":
            dx = (rx + rw / 2) - (x + w / 2)
        elif how == "center vertical":
            dy = (ry + rh / 2) - (y + h / 2)
        else:
            raise ValueError(f"unknown alignment {how}")
        if dx or dy:
            offset(shapes[index], dx, dy)


def distribute(shapes: list[dict], indices: list[int], axis: str) -> None:
    """Equal gaps between the selected shapes' bounds, ``horizontal`` or ``vertical``.

    The two outermost shapes stay where they are; the ones between them move.
    Shapes are taken in the order they sit along the axis, not the order chosen.
    Fewer than three shapes is a no-op.
    """
    chosen = [i for i in dict.fromkeys(indices) if 0 <= i < len(shapes) and isinstance(shapes[i], dict)]
    if len(chosen) < 3:
        return
    if axis not in ("horizontal", "vertical"):
        raise ValueError(f"unknown axis {axis}")
    pos, size = (0, 2) if axis == "horizontal" else (1, 3)
    boxes = {i: bounds(shapes[i]) for i in chosen}
    order = sorted(chosen, key=lambda i: (boxes[i][pos], i))
    first, last = boxes[order[0]], boxes[order[-1]]
    span = (last[pos] + last[size]) - first[pos]
    filled = sum(boxes[i][size] for i in order)
    gap = (span - filled) / (len(order) - 1)
    at = first[pos] + first[size] + gap
    for index in order[1:-1]:
        move = at - boxes[index][pos]
        if move:
            offset(shapes[index], move if pos == 0 else 0, move if pos == 1 else 0)
        at += boxes[index][size] + gap


def group(shapes: list[dict], indices: list[int], names: set[str] | None = None) -> int | None:
    """Put the selected shapes in one ``group`` shape. Returns the group's index.

    The children keep their page order and their absolute bounds. The group
    takes the place of the front-most child, so nothing moves in paint order
    relative to what was not grouped. Its ``x, y, w, h`` are the children's
    bounds. Fewer than two shapes, or shapes on two layers, is not a group.
    The reader paints a group by painting its children (Foolbook#48).
    """
    chosen = sorted(i for i in set(indices) if 0 <= i < len(shapes) and isinstance(shapes[i], dict))
    if len(chosen) < 2:
        return None
    layers = {shapes[i].get("layer") or "page" for i in chosen}
    if len(layers) != 1:
        return None
    children = [shapes[i] for i in chosen]
    boxes = [bounds(child) for child in children]
    left = min(b[0] for b in boxes)
    top = min(b[1] for b in boxes)
    right = max(b[0] + b[2] for b in boxes)
    bottom = max(b[1] + b[3] for b in boxes)
    taken = set(names or ()) | {s.get("name") or "" for s in shapes if isinstance(s, dict)}
    name, n = "Group", 2
    while name in taken:
        name, n = f"Group{n}", n + 1
    made = {
        "kind": "group",
        "name": name,
        "x": int(left),
        "y": int(top),
        "w": int(right - left),
        "h": int(bottom - top),
        "layer": layers.pop(),
        "visible": True,
        "children": children,
    }
    at = chosen[-1] - (len(chosen) - 1)
    for index in reversed(chosen):
        del shapes[index]
    shapes.insert(at, made)
    return at


def flatten(shapes: list) -> list:
    """What the stage paints: a group is its children, in its place.

    A hidden group hides its children, as in the reader.
    """
    out = []
    for shape in shapes or []:
        if not isinstance(shape, dict) or (shape.get("kind") or "") != "group":
            out.append(shape)
            continue
        for child in flatten(shape.get("children") or []):
            if shape.get("visible") is False and isinstance(child, dict):
                child = {**child, "visible": False}
            out.append(child)
    return out
