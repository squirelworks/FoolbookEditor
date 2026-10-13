"""Self-running book. Scaffold only. Not implemented.

ToolBook could save a book as an executable that carried its own
runtime, so the reader did not need ToolBook installed. FoolbookEditor
will do the same: one file that opens this book and nothing else.

The file would hold the Foolbook reader and the book. It would not be
an author, and it would not be a .tbk. This module only names that
export. It does not build a binary.
"""

from __future__ import annotations

from pathlib import Path


class ExecutableNotBuilt(NotImplementedError):
    """Raised until a self-running export exists."""


def plan(book: str | Path | None = None, dest: str | Path | None = None) -> dict:
    """Describe an export that has not been built. Writes nothing."""
    return {
        "status": "scaffold",
        "book": str(book) if book else None,
        "dest": str(dest) if dest else None,
        "contains": ["foolbook-reader", "book"],
        "note": "A self-running file is not built yet.",
    }


def export_executable(book: str | Path | None = None, dest: str | Path | None = None) -> None:
    """The future self-running export. It does not write a file."""
    plan(book, dest)
    raise ExecutableNotBuilt(
        "Self-running export is scaffolded and not implemented. "
        "FoolbookEditor will later write one file that carries the Foolbook reader and this book."
    )
