"""Objects Author can place on a page.

A drag on the picture becomes one shape Foolbook already knows how to draw.
The corner that is up and to the left is the origin, whichever way the drag went.
A click with no drag still places the object, at that tool's ordinary size.
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
    shape = {
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
    return shape
