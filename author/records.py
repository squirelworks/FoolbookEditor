"""A record: rows of data, one page each.

Record places a text field per field name on the page, then copies the
page once for each further row, with that row in the fields. Previous
record and Next record are buttons that go to the page before and after.
The reader needs nothing new: these are pages, fields, and page jumps.
"""

from __future__ import annotations

from author.document import duplicate_page
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


def place_record(book: dict, index: int, fields: list[str], rows: list[list[str]], x: int, y: int) -> int:
    """Lay the record out from page `index`. Returns how many pages it takes."""
    pages = book.get("pages") or []
    page = pages[index]
    shapes = page.setdefault("shapes", [])
    taken = {(s.get("name") or "").lower() for s in shapes if isinstance(s, dict)}
    for name in fields:
        if name.lower() in taken:
            raise ValueError(f"The page already has an object named {name}.")
    top = y
    for name in fields:
        shapes.append({
            "kind": "text", "name": name, "text": "",
            "x": x, "y": top, "w": FIELD_W, "h": ROW_H - 4,
            "fill": "#ffffff", "outline": INK, "border": 0, "script": "", "visible": True, "layer": "page",
        })
        top += ROW_H
    # Not named Next: the reader treats a button named Next as the quiz's Next.
    for label, left in (("Previous", x), ("Next", x + 100)):
        shapes.append({
            "kind": "button", "name": f"{label} record", "text": label,
            "x": left, "y": top + GAP, "w": 90, "h": 28,
            "fill": "#c0c0c0", "outline": "#000000",
            "script": "", "visible": True, "layer": "page",
        })
    count = max(1, len(rows))
    for n in range(1, count):
        duplicate_page(book, index + n - 1)
    run = pages[index:index + count]
    for n, each in enumerate(run):
        row = rows[n] if n < len(rows) else []
        for shape in each["shapes"]:
            name = shape.get("name") or ""
            if shape.get("kind") == "text" and name in fields:
                cell = fields.index(name)
                shape["text"] = str(row[cell]) if cell < len(row) else ""
        before = run[n - 1]["id"] if n > 0 else None
        after = run[n + 1]["id"] if n + 1 < len(run) else None
        kept = []
        for shape in each["shapes"]:
            target = {"Previous record": before, "Next record": after}.get(shape.get("name"), "")
            if target is None:
                continue  # no page that way
            if target:
                shape["item"] = {"page": target}
            kept.append(shape)
        each["shapes"] = kept
    return count
