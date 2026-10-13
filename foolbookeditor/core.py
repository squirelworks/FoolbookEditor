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


def load(path: str | Path) -> dict:
    return require().load(path)


def save_book(path: str | Path, book: dict, compress: bool = True) -> Path:
    return require().save_book(path, book, compress=compress)


def save_system(path: str | Path, system: dict, compress: bool = True) -> Path:
    return require().save_system(path, system, compress=compress)


def pack(data: dict, kind: str = "fbk", compress: bool = True) -> bytes:
    return require().pack(data, kind, compress=compress)


def unpack(blob: bytes) -> dict:
    return require().unpack(blob)


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
