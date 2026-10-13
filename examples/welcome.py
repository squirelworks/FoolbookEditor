"""Write the two books a new Foolbook install opens.

  python3 examples/welcome.py /path/to/Foolbook/foolbook/books
"""

from __future__ import annotations

import sys
from pathlib import Path

from foolbookeditor.core import save_book


INK = "#0b1c3d"
GOLD = "#e6b325"
CREAM = "#f6f1e7"
CORAL = "#e36b4a"
SKY = "#8ecae6"
SUN = "#ffb703"
HILL = "#2a9d8f"
HILL2 = "#1b6b5a"
GRASS = "#40916c"
DOOR = "#6b3a2a"
GLASS = "#ffd166"
NIGHT = "#071428"
SEA = "#123055"
DAWN = "#f4a261"
DAY = "#5fa8d3"


def _cover() -> list[dict]:
    return [
        {"kind": "rect", "x": 0, "y": 0, "w": 700, "h": 280, "fill": INK, "outline": INK},
        {"kind": "rect", "x": 0, "y": 0, "w": 14, "h": 280, "fill": GOLD, "outline": GOLD},
        {"kind": "ellipse", "x": 520, "y": 36, "w": 150, "h": 150, "fill": GOLD, "outline": GOLD},
        {"kind": "ellipse", "x": 558, "y": 24, "w": 130, "h": 130, "fill": INK, "outline": INK},
        {"kind": "text", "x": 44, "y": 78, "text": "Foolbook", "fill": "#ffffff", "size": 42, "bold": True},
        {"kind": "text", "x": 48, "y": 138, "text": "A book that draws.", "fill": GOLD, "size": 18},
        {"kind": "rect", "x": 48, "y": 188, "w": 36, "h": 36, "fill": CORAL, "outline": CORAL},
        {"kind": "ellipse", "x": 100, "y": 188, "w": 36, "h": 36, "fill": "#ffffff", "outline": "#ffffff"},
        {"kind": "polygon", "points": [[152, 224], [170, 188], [188, 224]], "fill": GOLD, "outline": GOLD},
    ]


def _house() -> list[dict]:
    return [
        {"kind": "rect", "x": 0, "y": 0, "w": 700, "h": 168, "fill": SKY, "outline": SKY},
        {"kind": "ellipse", "x": 560, "y": 22, "w": 72, "h": 72, "fill": SUN, "outline": SUN},
        {"kind": "polygon", "points": [[0, 168], [160, 96], [320, 168]], "fill": HILL, "outline": HILL},
        {"kind": "polygon", "points": [[220, 168], [420, 72], [640, 168]], "fill": HILL2, "outline": HILL2},
        {"kind": "rect", "x": 0, "y": 168, "w": 700, "h": 112, "fill": GRASS, "outline": GRASS},
        {"kind": "rect", "x": 86, "y": 150, "w": 150, "h": 88, "fill": CREAM, "outline": "#c4b8a4"},
        {"kind": "polygon", "points": [[72, 152], [161, 86], [250, 152]], "fill": CORAL, "outline": CORAL},
        {"kind": "rect", "x": 140, "y": 184, "w": 34, "h": 54, "fill": DOOR, "outline": DOOR},
        {"kind": "rect", "x": 104, "y": 168, "w": 28, "h": 24, "fill": GLASS, "outline": "#ffffff"},
        {"kind": "rect", "x": 186, "y": 168, "w": 28, "h": 24, "fill": GLASS, "outline": "#ffffff"},
        {"kind": "text", "x": 300, "y": 196, "text": "Rects, ellipses, polygons.", "fill": "#ffffff", "size": 16, "bold": True},
    ]


def _night() -> list[dict]:
    stars = []
    for x, y in ((80, 36), (140, 80), (220, 28), (300, 64), (380, 24), (460, 70), (40, 100), (520, 40)):
        stars.append({"kind": "ellipse", "x": x, "y": y, "w": 4, "h": 4, "fill": "#ffffff", "outline": "#ffffff"})
    return [
        {"kind": "rect", "x": 0, "y": 0, "w": 700, "h": 190, "fill": NIGHT, "outline": NIGHT},
        *stars,
        {"kind": "ellipse", "x": 540, "y": 28, "w": 84, "h": 84, "fill": CREAM, "outline": CREAM},
        {"kind": "ellipse", "x": 564, "y": 20, "w": 72, "h": 72, "fill": NIGHT, "outline": NIGHT},
        {"kind": "rect", "x": 0, "y": 190, "w": 700, "h": 90, "fill": SEA, "outline": SEA},
        {"kind": "line", "points": [[80, 214], [200, 214]], "outline": "#8ecae6"},
        {"kind": "line", "points": [[360, 230], [520, 230]], "outline": "#8ecae6"},
        {"kind": "text", "x": 36, "y": 120, "text": "First light", "fill": "#ffffff", "size": 32, "bold": True},
    ]


def _dawn() -> list[dict]:
    return [
        {"kind": "rect", "x": 0, "y": 0, "w": 700, "h": 90, "fill": "#1d3557", "outline": "#1d3557"},
        {"kind": "rect", "x": 0, "y": 90, "w": 700, "h": 70, "fill": "#e76f51", "outline": "#e76f51"},
        {"kind": "rect", "x": 0, "y": 160, "w": 700, "h": 40, "fill": DAWN, "outline": DAWN},
        {"kind": "ellipse", "x": 300, "y": 150, "w": 100, "h": 100, "fill": SUN, "outline": SUN},
        {"kind": "rect", "x": 0, "y": 200, "w": 700, "h": 80, "fill": "#1d4e89", "outline": "#1d4e89"},
        {"kind": "polygon", "points": [[0, 200], [120, 150], [240, 200]], "fill": "#264653", "outline": "#264653"},
        {"kind": "polygon", "points": [[180, 200], [360, 130], [540, 200]], "fill": "#1d3557", "outline": "#1d3557"},
        {"kind": "text", "x": 36, "y": 28, "text": "The sky changes color.", "fill": "#ffffff", "size": 20, "bold": True},
    ]


def _day() -> list[dict]:
    return [
        {"kind": "rect", "x": 0, "y": 0, "w": 700, "h": 160, "fill": DAY, "outline": DAY},
        {"kind": "ellipse", "x": 48, "y": 24, "w": 64, "h": 64, "fill": SUN, "outline": SUN},
        {"kind": "rect", "x": 0, "y": 160, "w": 700, "h": 120, "fill": "#1b7f9e", "outline": "#1b7f9e"},
        {"kind": "polygon", "points": [[420, 168], [470, 70], [520, 168]], "fill": "#ffffff", "outline": "#ffffff"},
        {"kind": "rect", "x": 455, "y": 168, "w": 8, "h": 36, "fill": DOOR, "outline": DOOR},
        {"kind": "polygon", "points": [[430, 200], [500, 200], [490, 214], [440, 214]], "fill": CREAM, "outline": "#c4b8a4"},
        {"kind": "text", "x": 36, "y": 100, "text": "A sail is a polygon.", "fill": INK, "size": 20, "bold": True},
    ]


def welcome() -> dict:
    return {
        "id": "using_foolbook",
        "title": "Using Foolbook",
        "subject": "Foolbook",
        "module": "Start here",
        "pages": [
            {
                "id": "P0",
                "text": [
                    "You opened Foolbook.",
                    "The picture is part of the book. It is not a separate file.",
                    "Next is another page. First Light is a second book.",
                ],
                "items": [
                    {"label": "Next", "page": "P100"},
                    {"label": "First Light", "page": "P0", "book": "first_light"},
                ],
                "shapes": _cover(),
            },
            {
                "id": "P100",
                "text": [
                    "A page can be a picture.",
                    "This one is rectangles, ellipses, and polygons. The words underneath are the page text.",
                ],
                "items": [
                    {"label": "Back", "page": "P0"},
                    {"label": "First Light", "page": "P0", "book": "first_light"},
                ],
                "shapes": _house(),
            },
        ],
    }


def first_light() -> dict:
    return {
        "id": "first_light",
        "title": "First Light",
        "subject": "Foolbook",
        "module": "Examples",
        "pages": [
            {
                "id": "P0",
                "text": [
                    "Night. The moon is two circles. The stars are small ellipses.",
                ],
                "items": [{"label": "Next", "page": "P100"}],
                "shapes": _night(),
            },
            {
                "id": "P100",
                "text": [
                    "Dawn. Three bands of color, then the sun on the water.",
                ],
                "items": [
                    {"label": "Next", "page": "P200"},
                    {"label": "Back", "page": "P0"},
                ],
                "shapes": _dawn(),
            },
            {
                "id": "P200",
                "text": [
                    "Day. The sail is a triangle. The hull is a polygon.",
                    "That is the whole trick. A Foolbook page can draw.",
                ],
                "items": [{"label": "Back", "page": "P100"}],
                "shapes": _day(),
            },
        ],
    }


def main(argv: list[str] | None = None) -> int:
    argv = list(argv if argv is not None else sys.argv[1:])
    dest = Path(argv[0]) if argv else Path.cwd()
    dest.mkdir(parents=True, exist_ok=True)
    save_book(dest / "using_foolbook.fbk", welcome())
    save_book(dest / "first_light.fbk", first_light())
    print(f"Wrote using_foolbook and first_light in {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
