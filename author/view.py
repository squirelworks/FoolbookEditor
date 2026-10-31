"""Zoom and scroll on the stage. View-only: stored coordinates never change.

Fit is the old behaviour, the page scaled into the pane. 50, 100, and 200
draw the page at that size. A page smaller than the pane sits in its
middle. A larger one scrolls. `to_page` turns a stage pixel back into a
page coordinate. It belongs with the geometry functions and moves there
once `author/geometry.py` has landed.
"""

from __future__ import annotations

ZOOMS = {"Fit": None, "50%": 0.5, "100%": 1.0, "200%": 2.0}
MARGIN = 12


def to_page(x: float, y: float, zoom: float, ox: float = 0.0, oy: float = 0.0, x0: float = 0.0, y0: float = 0.0) -> tuple[float, float]:
    """A stage pixel as a page coordinate. (ox, oy) is where page point (x0, y0) is drawn."""
    zoom = zoom or 1.0
    return (float(x) - ox) / zoom + x0, (float(y) - oy) / zoom + y0


def to_window(x: float, y: float, zoom: float, ox: float = 0.0, oy: float = 0.0, x0: float = 0.0, y0: float = 0.0) -> tuple[float, float]:
    zoom = zoom or 1.0
    return (float(x) - x0) * zoom + ox, (float(y) - y0) * zoom + oy


def placed(box, zoom: float | None, pane_w: int, pane_h: int):
    """(scale, dx, dy, ox, oy, region_w, region_h) for `place_window` and the scroll region."""
    x0, y0, x1, y1 = box
    if zoom is None:
        from engine.place import fit_view
        scale, dx, dy, ox, oy = fit_view(box, pane_w, pane_h, MARGIN)
        return scale, dx, dy, ox, oy, pane_w, pane_h
    wide = (x1 - x0) * zoom
    tall = (y1 - y0) * zoom
    region_w = max(pane_w, int(round(wide + 2 * MARGIN)))
    region_h = max(pane_h, int(round(tall + 2 * MARGIN)))
    ox = (region_w - wide) / 2
    oy = (region_h - tall) / 2
    return zoom, ox - x0, oy - y0, ox, oy, region_w, region_h
