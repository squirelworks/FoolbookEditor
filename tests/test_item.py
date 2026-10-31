"""A button's item is the jump. With no script, the reader still follows it."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from author.document import set_item
from author.files import save
from foolbookeditor.core import click


def book_with(button: dict) -> dict:
    page = lambda pid, shapes: {"id": pid, "text": [pid], "items": [], "shapes": shapes}
    return {"id": "jump", "title": "Jump", "pages": [
        page("P0", [button]), page("P100", []), page("P200", []),
    ]}


def button() -> dict:
    return {"kind": "button", "name": "Go", "text": "Go", "x": 10, "y": 10, "w": 90, "h": 28}


class ItemTests(unittest.TestCase):
    def test_set_item_writes_page_book_and_label(self):
        shape = button()
        set_item(shape, " P200 ", book="other.fbk", label="Next")
        self.assertEqual(shape["item"], {"page": "P200", "book": "other.fbk", "label": "Next"})

    def test_an_empty_page_clears_the_item(self):
        shape = button()
        set_item(shape, "P200")
        set_item(shape, "")
        self.assertNotIn("item", shape)

    def test_the_reader_follows_an_item_with_no_script(self):
        shape = button()
        set_item(shape, "P200")
        with tempfile.TemporaryDirectory() as tmp:
            path = save(Path(tmp) / "jump.fbk", book_with(shape))
            self.assertEqual(click(path, "P0", 20, 20), "P200")

    def test_a_click_off_the_button_stays(self):
        shape = button()
        set_item(shape, "P200")
        with tempfile.TemporaryDirectory() as tmp:
            path = save(Path(tmp) / "jump.fbk", book_with(shape))
            self.assertEqual(click(path, "P0", 300, 300), "P0")

    def test_a_script_that_moves_wins_over_the_item(self):
        shape = button()
        set_item(shape, "P200")
        shape["script"] = 'to handle buttonClick\n  go to page "P100"\nend\n'
        with tempfile.TemporaryDirectory() as tmp:
            path = save(Path(tmp) / "jump.fbk", book_with(shape))
            self.assertEqual(click(path, "P0", 20, 20), "P100")


if __name__ == "__main__":
    unittest.main()
