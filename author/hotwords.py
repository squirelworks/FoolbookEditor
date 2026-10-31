"""Hotwords in a field: a word in the text that jumps to a page.

The reader counts characters in the text as it draws it: CRLF becomes a
newline, runs of three or more spaces become one, and trailing newlines
go. The range is counted the same way here, so the two agree.
"""

from __future__ import annotations

import re


def drawn_text(shape: dict) -> str:
    text = str(shape.get("text") or "").replace("\r\n", "\n").replace("\r", "\n").rstrip("\n")
    return re.sub(r" {3,}", " ", text)


def add_hotword(shape: dict, word: str, page: str) -> dict:
    """Make the first free occurrence of word jump to page."""
    if (shape.get("kind") or "") != "text":
        raise ValueError("Only a field or label has hotwords.")
    word, page = word.strip(), page.strip()
    if not page:
        raise ValueError("A hotword needs a page to go to.")
    text = drawn_text(shape)
    taken = shape.get("hotwords") or []
    at = text.find(word) if word else -1
    while at >= 0:
        end = at + len(word)
        if not any(at < int(w["end"]) and int(w["start"]) < end for w in taken):
            hot = {"start": at, "end": end, "item": {"page": page}}
            shape["hotwords"] = sorted(taken + [hot], key=lambda w: int(w["start"]))
            return hot
        at = text.find(word, at + 1)
    if word and word in text:
        raise ValueError(f"{word} is already a hotword.")
    raise ValueError(f"The text does not have {word or 'that word'} in it.")
