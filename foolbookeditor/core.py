"""Foolbook is the core of this editor.

Editor modules call this file. They do not import engine, viewer, or menu.
Foolbook does the work. This file only asks it to.

The editor still holds its own window, page list, and the unfinished
self-running export. Those are not the core.
"""

from __future__ import annotations

from pathlib import Path


def require():
    """Fail early when Foolbook is not installed."""
    try:
        from foolbook import core as core
    except ImportError as exc:
        raise SystemExit(
            "FoolbookEditor needs Foolbook. Foolbook is the core. This program only edits."
        ) from exc
    return core


def format_version() -> int:
    """The newest book generation the installed reader writes (the ``fbk`` key)."""
    require()
    from engine.formats import FORMAT_VERSION
    return FORMAT_VERSION


def load(path: str | Path) -> dict:
    return require().load(path)


def read(path: str | Path) -> dict:
    """What Foolbook loaded, as a dict. The editor decides where to save it."""
    return require().read(path)


def shipped_book(name: str) -> Path | None:
    """A sample book that ships with Foolbook, such as ``using_foolbook``.

    Found beside the installed reader. None when the install does not
    carry the sample books.
    """
    import foolbook
    where = getattr(foolbook, "__file__", None)
    if not where:
        return None
    path = Path(where).resolve().parents[1] / "_books" / name / f"{name}.fbk"
    return path if path.exists() else None


def save_book(path: str | Path, book: dict, compress: bool = True) -> Path:
    return require().save_book(path, book, compress=compress)


def save_system(path: str | Path, system: dict, compress: bool = True) -> Path:
    return require().save_system(path, system, compress=compress)


def pack(data: dict, kind: str = "fbk", compress: bool = True) -> bytes:
    return require().pack(data, kind, compress=compress)


def unpack(blob: bytes) -> dict:
    return require().unpack(blob)


def is_toolbook(path: str | Path) -> bool:
    """True when the bytes are ToolBook, whatever the name says."""
    require()
    from toolbook.format import is_toolbook as sniff
    return sniff(path)


def is_office(path: str | Path) -> bool:
    return require().is_office(path)


def to_book(path: str | Path) -> dict:
    return require().to_book(path)


def write_office(path: str | Path, book: dict) -> Path:
    return require().write_office(path, book)


def export_book(path: str | Path, book: dict, compile_script=None) -> Path:
    return require().export_book(path, book, compile_script)


def compile_script(source: str, keywords: list[str] | None = None) -> bytes:
    return require().compile_script(source, keywords)


def click(path: str | Path, page_id: str, x: float, y: float) -> str:
    """The page the reader shows after a click at (x, y) on that page.

    Headless. The same steps Foolbook's window takes: the object under
    the point runs its click script, and when that does not move the
    page, its ``item`` is followed. Returns the page id after the click.
    """
    require()
    from engine.engine import click_script, follow, press, run_handler
    from engine.loader import load as load_book
    from engine.place import click_target
    from foolbook.model import RuntimeState

    book = load_book(Path(path))
    state = RuntimeState(book=book)
    ids = [page.id.lower() for page in book.pages]
    state.index = ids.index(page_id.lower())
    obj = click_target(state.page.shapes, x, y)
    if obj is None:
        return state.page.id
    moved = False
    script = click_script(obj)
    if script:
        moved = follow(state, run_handler(state, script))
    item = obj.get("item") or {}
    if not moved and (item.get("page") or item.get("label")):
        press(state, item.get("label") or obj.get("text") or "", item.get("page") or "")
    return state.page.id
