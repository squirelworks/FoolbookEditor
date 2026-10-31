"""Eight by eight pattern fills for rectangles.

The reader repeats `tile` across a rectangle: a 1 in the outline colour,
a 0 in the fill colour. These are the patterns the Pattern button steps
through. They are drawn here, not taken from anywhere.
"""

from __future__ import annotations

PRESETS: list[tuple[str, list[str] | None]] = [
    ("none", None),
    ("checks", ["10101010", "01010101"] * 4),
    ("horizontal", ["11111111", "00000000"] * 4),
    ("vertical", ["10101010"] * 8),
    ("diagonal", [format(0x80 >> i, "08b") for i in range(8)]),
    ("dots", ["10001000", "00000000", "00100010", "00000000"] * 2),
]


def pattern_name(shape: dict) -> str:
    tile = shape.get("tile")
    for name, rows in PRESETS:
        if rows == tile:
            return name
    return "custom" if tile else "none"


def next_pattern(shape: dict) -> str | None:
    """Step a rectangle to the next pattern. Other shapes are left alone."""
    if (shape.get("kind") or "rect") != "rect":
        return None
    names = [name for name, _rows in PRESETS]
    current = pattern_name(shape)
    name = names[(names.index(current) + 1) % len(names)] if current in names else "none"
    rows = dict(PRESETS)[name]
    if rows is None:
        shape.pop("tile", None)
    else:
        shape["tile"] = list(rows)
    return name
