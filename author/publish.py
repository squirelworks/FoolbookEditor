"""Publish a course as a folder, not an installer.

The folder holds the book as .fbk, every file a shape links by `src`
(a picture or clip beside the book, not embedded), and a one-line README
that says to open it with Foolbook. Linked files keep their path relative
to the book, so the book finds them in the folder the same way.
"""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

README = "Open {name} with Foolbook.\n"
CATALOG = "books.json"


def _slug(title: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]+", "-", title).strip("-") or "book"


def linked(book: dict) -> list[str]:
    """The relative `src` paths the book's shapes name, once each, in page order."""
    seen: list[str] = []
    for page in book.get("pages") or []:
        for shape in page.get("shapes") or []:
            src = str((shape or {}).get("src") or "").strip() if isinstance(shape, dict) else ""
            if src and not Path(src).is_absolute() and ".." not in Path(src).parts and src not in seen:
                seen.append(src)
    return seen


def publish(book: dict, folder: str | Path, source: str | Path | None = None, name: str = "") -> tuple[list[Path], list[str]]:
    """Write the folder. Returns the files written and the linked files that were not found."""
    from author.formats import save_book
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    name = name or f"{_slug(str(book.get('title') or 'book'))}.fbk"
    written = [save_book(folder / name, book)]
    missing = []
    for src in linked(book):
        origin = Path(source) / src if source else None
        if origin is None or not origin.is_file():
            missing.append(src)
            continue
        dest = folder / src
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(origin, dest)
        written.append(dest)
    written.append(write_catalog(folder, book, name))
    readme = folder / "README.txt"
    readme.write_text(README.format(name=name), encoding="utf-8")
    written.append(readme)
    return written, missing


def write_catalog(folder: str | Path, book: dict, name: str) -> Path:
    """Add or update this book's line in the folder's books.json: title, file, page count.

    Other books already listed stay, so several books can be published
    into one folder. A books.json that cannot be read is replaced.
    """
    path = Path(folder) / CATALOG
    try:
        books = json.loads(path.read_text(encoding="utf-8")).get("books") or []
    except (OSError, ValueError, AttributeError):
        books = []
    books = [b for b in books if isinstance(b, dict) and b.get("file") != name]
    books.append({"title": str(book.get("title") or ""), "file": name, "pages": len(book.get("pages") or [])})
    path.write_text(json.dumps({"books": books}, indent=2) + "\n", encoding="utf-8")
    return path
