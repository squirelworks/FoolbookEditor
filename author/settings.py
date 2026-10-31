"""The editor's own settings, in the user's config directory.

Nothing here is written into the repository or into a book. One JSON file:
`$XDG_CONFIG_HOME/foolbookeditor/settings.json`, `~/.config/...` when that
is not set, and `%APPDATA%\\foolbookeditor` on Windows.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

LEFT = 180      # page list
RIGHT = 280     # properties
STAGE = 300     # the narrowest the stage may get
EDGE = 120      # the narrowest the properties pane may get


def directory() -> Path:
    if sys.platform.startswith("win") and os.environ.get("APPDATA"):
        return Path(os.environ["APPDATA"]) / "foolbookeditor"
    base = os.environ.get("XDG_CONFIG_HOME") or str(Path.home() / ".config")
    return Path(base) / "foolbookeditor"


def path() -> Path:
    return directory() / "settings.json"


def load() -> dict:
    try:
        found = json.loads(path().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return found if isinstance(found, dict) else {}


def update(**values) -> dict:
    """Merge these values into the file. A write that fails is not an error."""
    found = load()
    found.update(values)
    try:
        path().parent.mkdir(parents=True, exist_ok=True)
        path().write_text(json.dumps(found, indent=2) + "\n", encoding="utf-8")
    except OSError:
        pass
    return found


def sashes(saved, width: int) -> list[int]:
    """Where the two sashes go in a window this wide. The stage keeps room."""
    if isinstance(saved, (list, tuple)) and len(saved) == 2:
        left, right = int(saved[0]), int(saved[1])
    else:
        left, right = LEFT, width - RIGHT
    right = min(right, width - EDGE)
    left = max(40, min(left, right - STAGE))
    return [left, right]


# Recent books: the last five opened or saved, newest first, under "recent".
RECENT_KEEP = 5


def recent() -> list[str]:
    found = load().get("recent")
    return [p for p in found if isinstance(p, str)][:RECENT_KEEP] if isinstance(found, list) else []


def remember(book: str | Path) -> list[str]:
    """Put this book first. The list keeps five and no copies."""
    book = str(Path(book).resolve())
    kept = ([book] + [p for p in recent() if p != book])[:RECENT_KEEP]
    update(recent=kept)
    return kept


def forget(book: str | Path) -> list[str]:
    kept = [p for p in recent() if p != str(book)]
    update(recent=kept)
    return kept


def pick(book: str) -> tuple[Path | None, str]:
    """The book to open, or None and the sentence to show when it is gone."""
    if Path(book).is_file():
        return Path(book), ""
    forget(book)
    return None, f"{Path(book).name} is not there any more. It was taken off the recent list."
