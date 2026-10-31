"""The book dict, written down.

Foolbook reads this dict. The Tk editor and the web editor write it.
This module is the field list both editors follow; ``schema.md`` says
the same thing in sentences. Until the web editor can import anything,
it copies this list in a pull request that changes both.
"""

from __future__ import annotations

# The kinds of shape the editor draws and Foolbook paints.
SHAPE_KINDS = (
    "rect", "roundrect", "ellipse", "line", "curve", "polygon", "arc", "pie", "chord",
    "text", "button", "image", "hotspot", "check", "radio", "list", "combo",
)

# Shape fields that must survive a save and a load. Any kind may carry
# any of them; ``schema.md`` says which kinds read which.
SHAPE_FIELDS = (
    # every shape
    "kind", "name", "x", "y", "w", "h", "visible", "layer", "script", "item",
    # paint
    "fill", "outline", "stroke", "tile",
    # points and curves
    "points", "ends", "radius", "start", "sweep",
    # words
    "text", "font", "size", "bold", "italic", "underline", "align", "border", "editable", "preset",
    # pictures
    "src", "data", "pixels", "fit",
    # controls
    "value", "group", "choices",
)
