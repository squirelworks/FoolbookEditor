"""A record on a page: rows of data shown one at a time.

The page stores `records` with `fields`, `rows`, and `at`. Each field is
a text shape of that name. Previous and Next are buttons whose `item`
steps the row. The reader fills the fields and steps the rows. This is
data on the page, not a database. One record per page.
"""

from __future__ import annotations

from author.tools import INK

ROW_H = 28
GAP = 10
FIELD_W = 200


def parse_rows(fields_text: str, rows_text: str) -> tuple[list[str], list[list[str]]]:
    """Field names split on commas, and one row per non-blank line."""
    fields = [name.strip() for name in fields_text.split(",") if name.strip()]
    if not fields:
        raise ValueError("A record needs at least one field name.")
    rows = [[cell.strip() for cell in line.split(",")] for line in rows_text.splitlines() if line.strip()]
    return fields, rows


def place_record(page: dict, fields: list[str], rows: list[list[str]], x: int, y: int) -> None:
    if page.get("records"):
        raise ValueError("This page already has a record.")
    shapes = page.setdefault("shapes", [])
    taken = {(s.get("name") or "").lower() for s in shapes if isinstance(s, dict)}
    for name in fields:
        if name.lower() in taken:
            raise ValueError(f"The page already has an object named {name}.")
    first = rows[0] if rows else []
    page["records"] = {"fields": list(fields), "rows": [list(r) for r in rows], "at": 0}
    top = y
    for n, name in enumerate(fields):
        shapes.append({
            "kind": "text", "name": name, "text": str(first[n]) if n < len(first) else "",
            "x": x, "y": top, "w": FIELD_W, "h": ROW_H - 4,
            "fill": "#ffffff", "outline": INK, "border": 0, "script": "", "visible": True, "layer": "page",
        })
        top += ROW_H
    # Not named Next: the reader treats a button named Next as the quiz's Next.
    for label, step, left in (("Previous", "previous", x), ("Next", "next", x + 100)):
        shapes.append({
            "kind": "button", "name": f"{label} record", "text": label,
            "x": left, "y": top + GAP, "w": 90, "h": 28,
            "fill": "#c0c0c0", "outline": "#000000", "item": {"record": step},
            "script": "", "visible": True, "layer": "page",
        })
