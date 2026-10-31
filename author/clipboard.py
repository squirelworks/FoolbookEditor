"""Cut, copy, and paste inside the editor.

The clipboard is the editor's own. Nothing goes to the system clipboard yet.
It holds either shapes from one page or one whole page, always as copies.
"""

from __future__ import annotations

import copy

from author import document
from author.catalog import place_shape
from author.geometry import offset

# A pasted shape lands this far right and down of what was copied.
PASTE_OFFSET = (8, 8)


class Clipboard:
    def __init__(self):
        self.kind: str | None = None
        self._held = None

    def copy_shapes(self, page: dict, indices: list[int]) -> int:
        """Hold copies of those shapes, in page order. Returns how many."""
        shapes = page.get("shapes") or []
        chosen = sorted(i for i in set(indices) if 0 <= i < len(shapes) and isinstance(shapes[i], dict))
        if not chosen:
            return 0
        self.kind = "shapes"
        self._held = [copy.deepcopy(shapes[i]) for i in chosen]
        return len(chosen)

    def cut_shapes(self, page: dict, indices: list[int]) -> int:
        """Copy, then take them off the page."""
        count = self.copy_shapes(page, indices)
        shapes = page.get("shapes") or []
        for index in sorted(set(indices), reverse=True):
            if 0 <= index < len(shapes):
                del shapes[index]
        return count

    def copy_page(self, book: dict, index: int) -> bool:
        found = book.get("pages") or []
        if not (0 <= index < len(found)):
            return False
        self.kind = "page"
        self._held = copy.deepcopy(found[index])
        return True

    def paste_shapes(self, page: dict) -> list[int]:
        """Put copies on the page, 8 right and 8 down. Returns where they landed.

        A name another shape on the page already has gets a number. Each paste
        lands 8 further on, so pasting twice does not stack two on one spot.
        """
        if self.kind != "shapes":
            return []
        dx, dy = PASTE_OFFSET
        for held in self._held:
            offset(held, dx, dy)
        taken = {s.get("name") or "" for s in page.get("shapes") or [] if isinstance(s, dict)}
        made = []
        for held in self._held:
            shape = copy.deepcopy(held)
            name = shape.get("name") or ""
            if name and name in taken:
                stem = name.rstrip("0123456789") or name
                n = 2
                while f"{stem}{n}" in taken:
                    n += 1
                shape["name"] = f"{stem}{n}"
            taken.add(shape.get("name") or "")
            place_shape(page, shape)
            made.append(shape)
        # A background shape goes in under the page ones, which can shift the
        # index of one placed before it, so find them all again at the end.
        shapes = page.get("shapes") or []
        return [i for i, s in enumerate(shapes) if any(s is m for m in made)]

    def paste_page(self, book: dict, current: int) -> int | None:
        """Put a copy of the held page after the current one. Its id is renamed when taken."""
        if self.kind != "page":
            return None
        twin = copy.deepcopy(self._held)
        taken = {str(p.get("id") or "").casefold() for p in book.get("pages") or []}
        if str(twin.get("id") or "").casefold() in taken:
            twin["id"] = document.fresh_id(book)
        found = document.pages(book)
        at = current + 1 if 0 <= current < len(found) else len(found)
        found.insert(at, twin)
        return at

