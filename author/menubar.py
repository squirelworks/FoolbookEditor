"""The book's own menu bar, written as an outline.

A menu is a line at the left margin. Its items are indented under it:

    Go
      Contents -> P0
      Glossary: go to page "Glossary"

`Label -> P` goes to page P. `Label: line` runs that one line of
OpenScript, stored as the item's buttonClick handler. The reader shows
the bar from `book["menubar"]`.
"""

from __future__ import annotations

HANDLER = "to handle buttonClick\n  {}\nend"


def parse(text: str) -> list[dict]:
    bar: list[dict] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if raw[:1] not in (" ", "\t"):
            bar.append({"label": line, "items": []})
            continue
        if not bar:
            raise ValueError(f"An item comes before any menu: {line}")
        mark = "->" if "->" in line else ":" if ":" in line else None
        if mark is None:
            raise ValueError(f"An item needs -> page or : script: {line}")
        label, where = (part.strip() for part in line.split(mark, 1))
        if not label or not where:
            raise ValueError(f"An item needs a label and somewhere to go: {line}")
        if mark == "->":
            bar[-1]["items"].append({"label": label, "page": where})
        else:
            bar[-1]["items"].append({"label": label, "script": HANDLER.format(where)})
    return bar


def render(bar: list[dict]) -> str:
    lines = []
    for menu in bar or []:
        lines.append(str(menu.get("label") or ""))
        for item in menu.get("items") or []:
            if item.get("page"):
                lines.append(f"  {item['label']} -> {item['page']}")
            else:
                lines.append(f"  {item['label']}: {_body(item.get('script') or '')}")
    return "\n".join(lines)


def _body(script: str) -> str:
    rows = [row.strip() for row in script.strip().splitlines()]
    if len(rows) >= 3 and rows[0].lower().startswith("to handle") and rows[-1].lower().startswith("end"):
        rows = rows[1:-1]
    return " ".join(row for row in rows if row)


def set_menubar(book: dict, text: str) -> None:
    bar = parse(text)
    if bar:
        book["menubar"] = bar
    else:
        book.pop("menubar", None)
