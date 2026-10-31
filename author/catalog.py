"""What Author shows of a book Foolbook already read.

Reader hides the field named correct. Author does not. The list is the
page's shapes, in the order the book stored them. A shape with no name
is still a row.
"""

from __future__ import annotations


def page_ids(book: dict) -> list[str]:
    """Page ids in book order. Author does not sort them."""
    return [str(page.get("id") or "") for page in book.get("pages") or []]


def objects_of(page: dict, layer: str | None = None) -> list[dict]:
    """One row per shape on that layer. Hidden objects stay in the list.

    A shape with no layer is on the page. That is the older file.
    """
    rows = []
    for index, shape in enumerate(page.get("shapes") or []):
        if not isinstance(shape, dict):
            continue
        if layer and (shape.get("layer") or "page") != layer:
            continue
        rows.append({
            "index": index,
            "kind": shape.get("kind") or "",
            "name": shape.get("name") or "",
            "bounds": _bounds(shape),
            "script": shape.get("script") or "",
            "text": shape.get("text") or "",
            "hidden": shape.get("visible") is False,
            "locked": shape.get("locked") is True,
            "layer": shape.get("layer") or "page",
        })
    return rows


def place_shape(page: dict, shape: dict) -> int:
    """Put a shape on its own layer. Background stays under the page."""
    shapes = page.setdefault("shapes", [])
    layer = shape.get("layer") or "page"
    shape["layer"] = layer
    if layer == "page":
        shapes.append(shape)
        return len(shapes) - 1
    for index, existing in enumerate(shapes):
        if isinstance(existing, dict) and (existing.get("layer") or "page") == "page":
            shapes.insert(index, shape)
            return index
    shapes.append(shape)
    return len(shapes) - 1


def restack(page: dict, index: int, direction: str) -> int:
    """Change one object's place in paint order, within its own layer.

    Array order is paint order, so later is in front. ``forward`` and
    ``backward`` swap with the next object on the same layer; ``front`` and
    ``back`` go past every object on that layer. Objects on the other layer
    keep their places. Returns the object's new index.
    """
    shapes = page.get("shapes") or []
    if not (0 <= index < len(shapes)) or not isinstance(shapes[index], dict):
        return index
    layer = shapes[index].get("layer") or "page"
    same = [
        at for at, shape in enumerate(shapes)
        if isinstance(shape, dict) and (shape.get("layer") or "page") == layer
    ]
    pos = same.index(index)
    target = {
        "forward": min(pos + 1, len(same) - 1),
        "backward": max(pos - 1, 0),
        "front": len(same) - 1,
        "back": 0,
    }.get(direction)
    if target is None:
        raise ValueError(f"unknown direction {direction}")
    if target == pos:
        return index
    # Take the layer's objects out in order, move one, and put them back in the same slots.
    order = [shapes[at] for at in same]
    order.insert(target, order.pop(pos))
    for slot, shape in zip(same, order):
        shapes[slot] = shape
    return same[target]


def page_script(page: dict) -> str:
    """The page script. Handlers are used when the page has no script field."""
    source = page.get("script") or ""
    if source:
        return source if str(source).endswith("\n") else str(source) + "\n"
    parts = []
    for handler in page.get("handlers") or []:
        if not isinstance(handler, dict):
            continue
        text = handler.get("source") or ""
        if text:
            parts.append(text if str(text).endswith("\n") else str(text) + "\n")
    return "".join(parts)


def set_page_script(page: dict, source: str) -> bool:
    """Write the page script when the pane changed it. Not compiled. True when it was written.

    A page that came with handlers and no script keeps its handlers until
    the author actually edits what the pane shows.
    """
    if source.strip() == page_script(page).strip():
        return False
    source = source.strip()
    if source:
        page["script"] = source + "\n"
    else:
        page.pop("script", None)
    return True


def set_object_script(page: dict, index: int, source: str) -> None:
    """Write the script back onto that shape. Author does not compile it."""
    shapes = page.get("shapes") or []
    if not (0 <= index < len(shapes)) or not isinstance(shapes[index], dict):
        return
    source = source.strip()
    if source:
        shapes[index]["script"] = source if source.endswith("\n") else source + "\n"
    else:
        shapes[index]["script"] = ""


def set_object_text(page: dict, index: int, raw: str) -> None:
    """The words typed into a field. Lines stay lines. Tk's own last newline is not the author's."""
    shapes = page.get("shapes") or []
    if not (0 <= index < len(shapes)) or not isinstance(shapes[index], dict):
        return
    if raw.endswith("\n"):
        raw = raw[:-1]
    shapes[index]["text"] = raw


def _bounds(shape: dict) -> list[int]:
    bounds = shape.get("bounds")
    if isinstance(bounds, (list, tuple)) and len(bounds) >= 4:
        return [int(bounds[0]), int(bounds[1]), int(bounds[2]), int(bounds[3])]
    return [
        int(shape.get("x") or 0),
        int(shape.get("y") or 0),
        int(shape.get("w") or 0),
        int(shape.get("h") or 0),
    ]
