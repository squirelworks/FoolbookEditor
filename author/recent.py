"""Recent files. Five paths, newest first, kept in the user's config folder.

Not in the repository and not beside the book. A path that is gone when
it is opened is dropped from the list, and the caller says so.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

KEEP = 5


def config_dir(env: dict | None = None, platform: str | None = None) -> Path:
    """Where the editor keeps its settings for this user."""
    env = os.environ if env is None else env
    platform = sys.platform if platform is None else platform
    if platform.startswith("win") and env.get("APPDATA"):
        base = Path(env["APPDATA"])
    elif platform == "darwin":
        base = Path(env.get("HOME") or Path.home()) / "Library" / "Application Support"
    elif env.get("XDG_CONFIG_HOME"):
        base = Path(env["XDG_CONFIG_HOME"])
    else:
        base = Path(env.get("HOME") or Path.home()) / ".config"
    return base / "foolbookeditor"


def recent_file(env: dict | None = None) -> Path:
    return config_dir(env) / "recent.json"


def load(store: Path) -> list[str]:
    try:
        found = json.loads(store.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    return [p for p in found if isinstance(p, str)][:KEEP] if isinstance(found, list) else []


def _write(store: Path, paths: list[str]) -> list[str]:
    store.parent.mkdir(parents=True, exist_ok=True)
    store.write_text(json.dumps(paths, indent=1) + "\n", encoding="utf-8")
    return paths


def remember(store: Path, path: str | Path) -> list[str]:
    """Put ``path`` first. The list keeps five."""
    path = str(Path(path).resolve())
    paths = [path] + [p for p in load(store) if p != path]
    return _write(store, paths[:KEEP])


def forget(store: Path, path: str | Path) -> list[str]:
    path = str(path)
    return _write(store, [p for p in load(store) if p != path])


def pick(store: Path, path: str) -> tuple[Path | None, str]:
    """The path to open, or None and the sentence to show when it is gone."""
    if Path(path).exists():
        return Path(path), ""
    forget(store, path)
    return None, f"{Path(path).name} is not there any more. It was taken off the recent list."
