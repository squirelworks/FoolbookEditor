"""A small spellcheck that shells out to nothing.

`words.txt` holds a few hundred ordinary English words, written for this
editor. A word in a text shape that is not there, and not in the book's
own `words`, is flagged. Numbers and single letters are not words to check.
"""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

_WORD = re.compile(r"[A-Za-z][A-Za-z']*")


@lru_cache(maxsize=1)
def known() -> frozenset[str]:
    lines = (Path(__file__).with_name("words.txt")).read_text(encoding="utf-8").splitlines()
    return frozenset(w.lower() for line in lines if not line.startswith("#") for w in line.split())


def _text_of(shape: dict) -> str:
    text = shape.get("text")
    return "\n".join(map(str, text)) if isinstance(text, list) else str(text or "")


def unknown(text: str, extra: set[str] = frozenset()) -> list[str]:
    seen, out = set(), []
    for raw in _WORD.findall(text or ""):
        word = raw.strip("'").lower()
        if word.endswith("'s"):
            word = word[:-2]
        if len(word) < 2 or word in known() or word in extra or word in seen:
            continue
        seen.add(word)
        out.append(word)
    return out


def check(book: dict) -> list[tuple[str, str, str]]:
    """(page id, shape name, word) for each unknown word in a text shape or the page text."""
    extra = {str(w).lower() for w in book.get("words") or []}
    found = []
    for page in book.get("pages") or []:
        pid = str(page.get("id") or "")
        for word in unknown("\n".join(map(str, page.get("text") or [])), extra):
            found.append((pid, "", word))
        for shape in page.get("shapes") or []:
            if isinstance(shape, dict) and shape.get("kind") in ("text", "button"):
                for word in unknown(_text_of(shape), extra):
                    found.append((pid, str(shape.get("name") or ""), word))
    return found


def add_word(book: dict, word: str) -> None:
    words = book.setdefault("words", [])
    word = word.strip().lower()
    if word and word not in words:
        words.append(word)
