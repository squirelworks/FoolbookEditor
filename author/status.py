"""The line at the bottom of the window. Built from data, so it is tested without a window."""

from __future__ import annotations


def status_text(tool: str, page_id: str | None, shape_name: str | None, zoom: str, dirty: bool) -> str:
    """Tool, page id, shape name, zoom, and whether there are unsaved changes.

    `shape_name` None is nothing selected. An empty name is an unnamed shape.
    """
    shape = "none" if shape_name is None else (shape_name or "(unnamed)")
    return "   ".join((
        f"Tool: {tool}",
        f"Page: {page_id or 'none'}",
        f"Shape: {shape}",
        f"Zoom: {zoom}",
        "Unsaved changes" if dirty else "Saved",
    ))
