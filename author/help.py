"""Help is the README beside the editor, not a website."""

from __future__ import annotations

import re
from pathlib import Path

README = Path(__file__).resolve().parents[1] / "README.md"


def readme_section(title: str, text: str | None = None) -> str | None:
    """The body under `### title`, up to the next heading. None when the README has no such section."""
    if text is None:
        try:
            text = README.read_text(encoding="utf-8")
        except OSError:
            return None
    found = re.search(rf"(?m)^###\s+{re.escape(title)}\s*$", text)
    if not found:
        return None
    rest = text[found.end():]
    stop = re.search(r"(?m)^#{1,3}\s", rest)
    return (rest[:stop.start()] if stop else rest).strip() or None
