"""Objects Author can place, move, and resize.

A drag with Button, Field, or Rectangle places one shape. A drag with
Select moves the object under the pointer. A drag on a corner changes
the size, and the opposite corner stays where it was.
"""

from __future__ import annotations


# The tool Author starts with, and the one Escape returns to.
DEFAULT_TOOL = "select"

# A new rectangle is paper with an ink outline until the property pane says otherwise.
PAPER = "#f7f4ee"
INK = "#071428"

# Radios placed one after another answer the same question until the property pane renames the group.
RADIO_GROUP = "choice"

_SIZE = {
    "button": (90, 28),
    "text": (160, 36),
    "label": (120, 24),
    "check": (120, 22),
    "radio": (120, 22),
    "box": (100, 60),
    "line": (80, 8),
    "ellipse": (80, 60),
    "polygon": (80, 60),
    "arc": (80, 60),
    "picture": (120, 80),
}

_KIND = {
    "button": "button",
    "text": "text",
    "label": "text",
    "check": "check",
    "radio": "radio",
    "box": "rect",
    "line": "line",
    "ellipse": "ellipse",
    "polygon": "polygon",
    "arc": "arc",
    "picture": "image",
}
_LABEL = {
    "button": "Button",
    "text": "Field",
    "label": "Label",
    "check": "Check",
    "radio": "Radio",
    "box": "Rectangle",
    "line": "Line",
    "ellipse": "Ellipse",
    "polygon": "Polygon",
    "arc": "Arc",
    "picture": "Picture",
}


def after_escape(tool: str) -> str:
    """Escape puts the pointer back to Select, whatever tool was chosen."""
    return DEFAULT_TOOL


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


def new_shape(tool: str, x0: float, y0: float, x1: float, y1: float, names: set[str], layer: str = "page") -> dict:
    """One new object. ``tool`` is one Foolbook already draws."""
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
    shape = {
        "kind": _KIND[tool],
        "name": name,
        "x": int(left),
        "y": int(top),
        "w": int(width),
        "h": int(height),
        "text": label if tool in ("button", "text", "label", "check", "radio") else "",
        "script": "",
        "fill": "#c0c0c0" if tool == "button" else "",
        "outline": "#000000",
        "visible": True,
        "layer": layer or "page",
    }
    if tool == "line":
        if abs(x1 - x0) < 8 and abs(y1 - y0) < 8:
            shape["points"] = [[int(left), int(top)], [int(left + width), int(top + height)]]
        else:
            shape["points"] = [[int(x0), int(y0)], [int(x1), int(y1)]]
    elif tool == "text":
        # The reader gives an editable field the keyboard and keeps the typing as value.
        shape["editable"] = True
    elif tool == "label":
        # A label is a preset of the text shape, not a kind of its own.
        shape["preset"] = "label"
        shape["border"] = 1
        shape["editable"] = False
    elif tool in ("check", "radio"):
        # The reader turns value over on a click. A radio turns off the others in its group.
        shape["value"] = False
        shape["outline"] = INK
        if tool == "radio":
            shape["group"] = RADIO_GROUP
    elif tool == "box":
        shape["fill"] = PAPER
        shape["outline"] = INK
    elif tool == "polygon":
        shape["points"] = [
            [int(left), int(top)],
            [int(left + width), int(top)],
            [int(left + width), int(top + height)],
            [int(left), int(top + height)],
        ]
        shape["fill"] = "#c0c0c0"
    elif tool == "arc":
        shape["ends"] = [[int(left), int(top + height / 2)], [int(left + width), int(top + height / 2)]]
    return shape


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
