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
