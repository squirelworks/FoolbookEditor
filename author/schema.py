"""The book dict, written down.

Foolbook reads this dict. The Tk editor and the web editor write it.
This module is the field list both editors follow; ``schema.md`` says
the same thing in sentences. Until the web editor can import anything,
it copies this list in a pull request that changes both.
"""

from __future__ import annotations

# Page fields that must survive a save and a load. ``text`` is a list of
# strings. ``size`` is [w, h]; a page without it is the book's size.
PAGE_FIELDS = (
    "id", "text", "items", "shapes", "script", "name", "size",
    "background", "uses", "transition", "quiz", "records",
)
