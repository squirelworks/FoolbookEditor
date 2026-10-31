"""The property pane, as data.

Each row is a key on the shape dict, a label, and how the typed text is
read. ``write`` changes the shape only when the text is good. Bad text
leaves the old value, and the pane shows it again.
"""

from __future__ import annotations

import re

# key, label, kind. The window builds one row per entry, in this order.
ROWS = [
    ("name", "Name", "name"),
    ("text", "Text", "text"),
    ("fill", "Fill", "color"),
    ("outline", "Outline", "color"),
    ("stroke", "Line width", "width"),
    ("font", "Font", "face"),
    ("size", "Size", "points"),
    ("bold", "Bold", "flag"),
    ("italic", "Italic", "flag"),
    ("underline", "Underline", "flag"),
    ("align", "Align", "choice"),
    ("visible", "Visible", "flag"),
    ("x", "Left", "place"),
    ("y", "Top", "place"),
    ("w", "Width", "extent"),
    ("h", "Height", "extent"),
    ("points", "Points", "pointlist"),
]

# The fewest points a shape of that kind keeps. Others need two.
FEWEST_POINTS = {"polygon": 3}

# The smallest width or height a typed size may give.
MIN_EXTENT = 4

# The values a choice row offers.
CHOICES = {"align": ("left", "center", "right")}

# The colour well: eight plain colours. Each is named by its hex value.
WELL = (
    "#000000",
    "#ffffff",
    "#808080",
    "#c00000",
    "#e0c000",
    "#008000",
    "#0040c0",
    "#f7f4ee",
)

# What Tab puts into a script pane.
SCRIPT_TAB = "  "

# What a shape with no stroke is drawn at.
STROKE = 1

_HEX = re.compile(r"^#[0-9a-fA-F]{6}$")


def read(shape: dict, key: str) -> str:
    """The value as the pane shows it."""
    if key == "stroke":
        return str(shape.get("stroke", STROKE))
    if key == "points":
        return "\n".join(f"{int(pt[0])}, {int(pt[1])}" for pt in shape.get("points") or [] if len(pt) >= 2)
    if _kind(key) in ("place", "extent"):
        from author.tools import bounds_of
        return str(int(dict(zip("xywh", bounds_of(shape)))[key]))
    if key == "visible":
        # Missing is shown. Only an explicit false hides the object.
        return "false" if shape.get("visible") is False else "true"
    if _kind(key) == "flag":
        return "true" if shape.get(key) else "false"
    if key == "align":
        return _align_name(shape.get("align"))
    value = shape.get(key)
    return "" if value is None else str(value)


def write(shape: dict, key: str, raw: str, page: dict | None = None) -> bool:
    """Set one property from typed text. False, and nothing changed, when the text is not usable."""
    kind = _kind(key)
    raw = raw if kind == "text" else raw.strip()
    if kind == "name":
        if not raw or _name_taken(page, shape, raw):
            return False
        shape["name"] = raw
    elif kind == "text":
        shape["text"] = raw
    elif kind == "color":
        if key == "fill" and raw == "":
            # No fill. The reader draws nothing inside the outline.
            shape["fill"] = ""
            return True
        if not _HEX.match(raw):
            return False
        shape[key] = raw.lower()
    elif kind == "width":
        try:
            width = int(raw)
        except ValueError:
            return False
        if width < 0:
            return False
        shape["stroke"] = width
    elif kind == "face":
        # Empty means the reader's own face.
        if raw:
            shape["font"] = raw
        else:
            shape.pop("font", None)
    elif kind == "points":
        try:
            size = int(raw)
        except ValueError:
            return False
        if not 1 <= size <= 288:
            return False
        shape["size"] = size
    elif kind == "flag":
        if raw.lower() not in ("true", "false", "1", "0"):
            return False
        shape[key] = raw.lower() in ("true", "1")
    elif kind == "choice":
        if raw.lower() not in CHOICES[key]:
            return False
        shape[key] = raw.lower()
    elif kind == "pointlist":
        points = _parse_points(raw)
        if points is None or len(points) < FEWEST_POINTS.get(shape.get("kind") or "", 2):
            return False
        shape["points"] = points
        xs = [pt[0] for pt in points]
        ys = [pt[1] for pt in points]
        shape["x"], shape["y"] = min(xs), min(ys)
        shape["w"], shape["h"] = max(xs) - min(xs), max(ys) - min(ys)
    elif kind in ("place", "extent"):
        try:
            number = int(raw)
        except ValueError:
            return False
        if kind == "extent" and number < MIN_EXTENT:
            return False
        _set_bounds(shape, key, number)
    else:
        return False
    return True


def _parse_points(raw: str) -> list[list[int]] | None:
    """One "x, y" pair per line. A comma or spaces between. Blank lines are skipped."""
    points = []
    for line in raw.splitlines():
        parts = line.replace(",", " ").split()
        if not parts:
            continue
        if len(parts) != 2:
            return None
        try:
            points.append([int(parts[0]), int(parts[1])])
        except ValueError:
            return None
    return points


def _set_bounds(shape: dict, key: str, number: int) -> None:
    """Move or size by one number. Points and arc ends go with the box."""
    from author.tools import bounds_of
    x, y, w, h = bounds_of(shape)
    box = {"x": x, "y": y, "w": w, "h": h}
    box[key] = number
    sx = box["w"] / w if w else 1
    sy = box["h"] / h if h else 1
    for field in ("points", "ends"):
        if shape.get(field):
            shape[field] = [
                [int(round(box["x"] + (pt[0] - x) * sx)), int(round(box["y"] + (pt[1] - y) * sy))]
                for pt in shape[field]
            ]
    for field in ("x", "y", "w", "h"):
        shape[field] = int(box[field])


def _align_name(value) -> str:
    """A .tbk stores 0, 1, 2 for left, right, center. The pane shows the word."""
    if isinstance(value, str) and value.lower() in CHOICES["align"]:
        return value.lower()
    try:
        code = int(value or 0)
    except (TypeError, ValueError):
        code = 0
    return {1: "right", 2: "center"}.get(code, "left")


def _kind(key: str) -> str:
    for name, _label, kind in ROWS:
        if name == key:
            return kind
    return ""


def _name_taken(page: dict | None, shape: dict, name: str) -> bool:
    """Another object on the page already has that name. Case does not make it different."""
    for other in (page or {}).get("shapes") or []:
        if other is shape or not isinstance(other, dict):
            continue
        if str(other.get("name") or "").lower() == name.lower():
            return True
    return False
