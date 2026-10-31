"""The colours a book already uses, most used first.

The author picks from these to keep a book's colours consistent.
"""

from __future__ import annotations

import re
from collections import Counter

LIMIT = 16
_HEX = re.compile(r"^#[0-9a-fA-F]{6}$")


def used_colours(book: dict, limit: int = LIMIT) -> list[str]:
    counts: Counter[str] = Counter()
    first: dict[str, int] = {}
    for page in book.get("pages") or []:
        for shape in page.get("shapes") or []:
            for key in ("fill", "outline"):
                colour = str(shape.get(key) or "")
                if _HEX.match(colour):
                    colour = colour.lower()
                    counts[colour] += 1
                    first.setdefault(colour, len(first))
    return sorted(counts, key=lambda c: (-counts[c], first[c]))[:limit]
