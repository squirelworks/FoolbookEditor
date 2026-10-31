"""Import a .tbk as a book the editor can save.

Foolbook reads the file. What it can see (pages, field text, polygons,
button bitmaps) arrives as shapes. What it cannot see is listed in a
report, so nothing is dropped without a line saying so. The .tbk is
only read. Export .tbk is still the shell writer.
"""

from __future__ import annotations

from pathlib import Path

from foolbookeditor.core import read

# Kinds the reader draws as themselves.
DRAWN = {"rect", "ellipse", "line", "polygon", "text", "image", "button"}

# Not read from any .tbk today. Foolbook's knownbugs.md is where these are kept.
ALWAYS = (
    "Fonts, indents, and bevels are not read from a .tbk. Text uses the reader's face.",
    "Pattern tiles are not read. A patterned fill is the record's colour.",
    "A script that is only bytecode is not kept as source.",
)


def import_book(path: str | Path) -> tuple[dict, list[str]]:
    """The book dict and the report. Saving it is the caller's choice."""
    src = Path(path)
    book = read(src)
    book["imported_from"] = src.name
    return book, report(book)


def report(book: dict) -> list[str]:
    """One line per thing the reader left behind, page by page, then the general limits."""
    lines = []
    for page in book.get("pages") or []:
        pid = page.get("id") or "?"
        groups: dict[str, int] = {}
        for shape in page.get("shapes") or []:
            kind = (shape.get("kind") or "").lower()
            name = shape.get("name") or "(unnamed)"
            for group in shape.get("groups") or []:
                groups[group] = groups.get(group, 0) + 1
            if kind == "arc":
                lines.append(f"{pid}: arc {name} is drawn as the ellipse of its bounds.")
            elif kind in ("curve", "pie", "chord", "roundrect"):
                lines.append(f"{pid}: {kind} {name} is not drawn by the reader.")
            elif kind and kind not in DRAWN:
                lines.append(f"{pid}: {kind} {name} is a kind the reader does not draw.")
        for group, count in groups.items():
            lines.append(f"{pid}: group {group} is not kept as a group. Its {count} objects are on the page, loose.")
        for handler in page.get("handlers") or []:
            if handler.get("name") and not (handler.get("source") or "").strip():
                lines.append(f"{pid}: handler {handler['name']} has no source.")
    return lines + list(ALWAYS)


def report_text(lines: list[str]) -> str:
    return "Left behind by the import:\n\n" + "\n".join(f"- {line}" for line in lines) + "\n"
