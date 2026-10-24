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
    """Move one object in front of or behind its neighbour on the same layer."""
    shapes = page.get("shapes") or []
    if not (0 <= index < len(shapes)) or not isinstance(shapes[index], dict):
        return index
    layer = shapes[index].get("layer") or "page"
    same = [
        at for at, shape in enumerate(shapes)
        if isinstance(shape, dict) and (shape.get("layer") or "page") == layer
    ]
    pos = same.index(index)
    if direction == "front" and pos + 1 < len(same):
        other = same[pos + 1]
    elif direction == "back" and pos > 0:
        other = same[pos - 1]
    else:
        return index
    shapes[index], shapes[other] = shapes[other], shapes[index]
    return other


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
