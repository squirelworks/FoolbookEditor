"""Find and replace across page text and shape text.

The search is plain text, never a regular expression. Case is ignored
unless the author asks to match it.
"""

from __future__ import annotations

import re


def _pattern(needle: str, case: bool) -> re.Pattern | None:
    if not needle:
        return None
    return re.compile(re.escape(needle), 0 if case else re.IGNORECASE)


def _places(book: dict):
    """(page, holder, key, label) for every text the author wrote."""
    for page in book.get("pages") or []:
        pid = str(page.get("id") or "")
        text = page.get("text")
        if isinstance(text, list):
            for n in range(len(text)):
                yield pid, text, n, "page text"
        for shape in page.get("shapes") or []:
            if isinstance(shape, dict) and isinstance(shape.get("text"), str) and shape["text"]:
                yield pid, shape, "text", str(shape.get("name") or shape.get("kind") or "")


def find(book: dict, needle: str, case: bool = False) -> list[tuple[str, str, int]]:
    """(page id, where, how many) for each text that holds the needle."""
    pattern = _pattern(needle, case)
    if pattern is None:
        return []
    hits = []
    for pid, holder, key, label in _places(book):
        count = len(pattern.findall(str(holder[key])))
        if count:
            hits.append((pid, label, count))
    return hits


def replace_all(book: dict, needle: str, replacement: str, case: bool = False) -> int:
    """Replace every match. Returns how many were replaced."""
    pattern = _pattern(needle, case)
    if pattern is None:
        return 0
    total = 0
    for _pid, holder, key, _label in _places(book):
        changed, count = pattern.subn(lambda _m: replacement, str(holder[key]))
        if count:
            holder[key] = changed
            total += count
    return total
