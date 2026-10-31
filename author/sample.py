"""Generated books for timing and tests. Original content only."""

from __future__ import annotations


def large_book(pages: int = 200, shapes: int = 20) -> dict:
    """A book of ``pages`` pages with ``shapes`` shapes each, every kind used."""
    kinds = ("rect", "ellipse", "line", "polygon", "text", "button")
    book = {"id": "large", "title": "Large book", "pages": []}
    for p in range(pages):
        found = []
        for s in range(shapes):
            kind = kinds[s % len(kinds)]
            x, y = 10 + (s % 5) * 120, 10 + (s // 5) * 110
            shape = {"kind": kind, "name": f"{kind}{s}", "x": x, "y": y, "w": 100, "h": 90,
                     "fill": "#f7f4ee", "outline": "#071428", "layer": "page"}
            if kind in ("line", "polygon"):
                shape["points"] = [[x, y], [x + 100, y], [x + 50, y + 90]][: 2 if kind == "line" else 3]
            if kind in ("text", "button"):
                shape["text"] = f"Page {p} shape {s}"
            if kind == "button":
                shape["item"] = {"page": f"P{(p + 1) % pages}"}
            found.append(shape)
        book["pages"].append({"id": f"P{p}", "text": [f"Page {p}"], "items": [], "shapes": found})
    return book
