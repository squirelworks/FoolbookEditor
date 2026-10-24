"""Objects Author can place, move, and resize.

A drag with Button, Field, or Rectangle places one shape. A drag with
Select moves the object under the pointer. A drag on a corner changes
the size, and the opposite corner stays where it was.
"""

from __future__ import annotations


_SIZE = {
    "button": (90, 28),
    "text": (160, 36),
    "box": (100, 60),
}

_KIND = {"button": "button", "text": "text", "box": "rect"}
_LABEL = {"button": "Button", "text": "Field", "box": "Rectangle"}


def page_point(view: dict, x: float, y: float) -> tuple[float, float]:
    """A pixel in the picture, turned back into a page coordinate."""
    scale = view.get("scale") or 1
    return (
        (x - view.get("ox", 0)) / scale + view.get("x0", 0),
        (y - view.get("oy", 0)) / scale + view.get("y0", 0),
    )


def window_point(view: dict, x: float, y: float) -> tuple[float, float]:
    """A page coordinate, turned into a pixel in the picture."""
    scale = view.get("scale") or 1
    return (
        (x - view.get("x0", 0)) * scale + view.get("ox", 0),
        (y - view.get("y0", 0)) * scale + view.get("oy", 0),
    )


def new_shape(tool: str, x0: float, y0: float, x1: float, y1: float, names: set[str]) -> dict:
    """One new object. ``tool`` is button, text, or box."""
    if tool not in _KIND:
        raise ValueError(f"unknown tool {tool}")
    left, top = min(x0, x1), min(y0, y1)
    width, height = abs(x1 - x0), abs(y1 - y0)
    ordinary = _SIZE[tool]
    if width < 8:
        width = ordinary[0]
    if height < 8:
        height = ordinary[1]
    label = _LABEL[tool]
    name = label
    n = 2
    while name in names:
        name = f"{label}{n}"
        n += 1
    return {
        "kind": _KIND[tool],
        "name": name,
        "x": int(left),
        "y": int(top),
        "w": int(width),
        "h": int(height),
        "text": label if tool != "box" else "",
        "script": "",
        "fill": "#c0c0c0" if tool == "button" else "",
        "outline": "#000000",
        "visible": True,
    }


def shape_at(page: dict, index: int) -> dict | None:
    """The shape at that row. Hidden ones count. Non-shapes do not."""
    seen = 0
    for shape in page.get("shapes") or []:
        if not isinstance(shape, dict):
            continue
        if seen == index:
            return shape
        seen += 1
    return None


def bounds_of(shape: dict) -> tuple[float, float, float, float]:
    x = float(shape.get("x") or 0)
    y = float(shape.get("y") or 0)
    w = float(shape.get("w") or 0)
    h = float(shape.get("h") or 0)
    if w and h:
        return x, y, w, h
    points = list(shape.get("points") or []) + list(shape.get("ends") or [])
    xs = [float(pt[0]) for pt in points if len(pt) >= 2]
    ys = [float(pt[1]) for pt in points if len(pt) >= 2]
    if not xs:
        return x, y, w, h
    return min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)


def corners(shape: dict) -> dict[str, tuple[float, float]]:
    x, y, w, h = bounds_of(shape)
    return {
        "nw": (x, y),
        "ne": (x + w, y),
        "sw": (x, y + h),
        "se": (x + w, y + h),
    }


def opposite(shape: dict, corner: str) -> tuple[float, float]:
    across = {"nw": "se", "ne": "sw", "sw": "ne", "se": "nw"}
    return corners(shape)[across[corner]]


def snapshot(shape: dict) -> dict:
    return {
        "x": float(shape.get("x") or 0),
        "y": float(shape.get("y") or 0),
        "w": float(shape.get("w") or 0),
        "h": float(shape.get("h") or 0),
        "points": [list(pt) for pt in shape.get("points") or []],
        "ends": [list(pt) for pt in shape.get("ends") or []],
    }


def move_shape(shape: dict, snap: dict, dx: float, dy: float) -> None:
    """Shift the object by the drag. The start of the drag is ``snap``."""
    shape["x"] = int(snap["x"] + dx)
    shape["y"] = int(snap["y"] + dy)
    shape["w"] = int(snap["w"])
    shape["h"] = int(snap["h"])
    if snap["points"]:
        shape["points"] = [[pt[0] + dx, pt[1] + dy] for pt in snap["points"]]
    if snap["ends"]:
        shape["ends"] = [[pt[0] + dx, pt[1] + dy] for pt in snap["ends"]]


def resize_shape(shape: dict, snap: dict, ax: float, ay: float, px: float, py: float) -> None:
    """Pull one corner. ``(ax, ay)`` is the corner that stays put."""
    if abs(px - ax) < 8:
        px = ax + 8 if px >= ax else ax - 8
    if abs(py - ay) < 8:
        py = ay + 8 if py >= ay else ay - 8
    left, right = (ax, px) if ax <= px else (px, ax)
    top, bottom = (ay, py) if ay <= py else (py, ay)
    width, height = right - left, bottom - top
    shape["x"] = int(left)
    shape["y"] = int(top)
    shape["w"] = int(width)
    shape["h"] = int(height)
    if snap["w"] and snap["h"] and snap["points"]:
        sx, sy = width / snap["w"], height / snap["h"]
        ox, oy = snap["x"], snap["y"]
        shape["points"] = [
            [left + (pt[0] - ox) * sx, top + (pt[1] - oy) * sy] for pt in snap["points"]
        ]
    if snap["w"] and snap["h"] and snap["ends"]:
        sx, sy = width / snap["w"], height / snap["h"]
        ox, oy = snap["x"], snap["y"]
        shape["ends"] = [
            [left + (pt[0] - ox) * sx, top + (pt[1] - oy) * sy] for pt in snap["ends"]
        ]


def handle_at(view: dict, shape: dict, wx: float, wy: float, radius: float = 8) -> str | None:
    """Which corner square the pointer is on, or none."""
    for name, (x, y) in corners(shape).items():
        sx, sy = window_point(view, x, y)
        if abs(sx - wx) <= radius and abs(sy - wy) <= radius:
            return name
    return None
