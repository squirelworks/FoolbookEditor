"""What the editor opens.

A path opens that book. No path opens the demo book that ships with the
editor, as an unsaved copy, so Save asks where to put it and the shipped
file is never written.
"""

from __future__ import annotations

from pathlib import Path

DEMO = Path(__file__).resolve().parents[1] / "foolbookeditor" / "demo" / "garden.fbk"


def first_book(path: str | Path | None) -> tuple[dict | None, Path | None]:
    """(book, path to save to). (None, path) means open the path as usual."""
    if path is not None:
        return None, Path(path)
    from foolbookeditor.core import load
    if DEMO.is_file():
        return load(DEMO), None
    return None, None
