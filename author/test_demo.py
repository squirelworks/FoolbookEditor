"""The demo book is made by a script, and the start window opens it as a copy."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

from author.start import DEMO, first_book
from foolbookeditor.core import load

ROOT = Path(__file__).resolve().parents[1]
STAMPS = ("fbk", "foolbook", "format", "format_version")


def _script():
    spec = importlib.util.spec_from_file_location("demo_script", ROOT / "examples" / "demo.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _content(book: dict) -> dict:
    return {key: value for key, value in book.items() if key not in STAMPS}


class DemoBook(unittest.TestCase):
    def test_the_shipped_file_is_what_the_script_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            made = _script().write(Path(tmp) / "garden.fbk")
            self.assertEqual(_content(load(made)), _content(load(DEMO)))
            again = _script().write(Path(tmp) / "again.fbk")
            self.assertEqual(made.read_bytes(), again.read_bytes())

    def test_it_has_a_background_a_picture_a_quiz_and_a_next_button(self):
        book = load(DEMO)
        pages = [p for p in book["pages"] if not p.get("background")]
        backgrounds = [p for p in book["pages"] if p.get("background")]
        self.assertEqual(len(pages), 3)
        self.assertEqual(len(backgrounds), 1)
        self.assertTrue(all(p.get("uses") == backgrounds[0]["id"] for p in pages))
        shapes = [s for p in pages for s in p.get("shapes") or []]
        self.assertTrue(any(s["kind"] == "image" and s.get("data") for s in shapes))
        self.assertTrue(any(p.get("quiz") for p in pages))
        self.assertTrue(any(s["kind"] == "button" and (s.get("item") or {}).get("label") == "Next" for s in shapes))

    def test_no_path_opens_the_demo_as_an_unsaved_copy(self):
        book, path = first_book(None)
        self.assertEqual(book["title"], "A Small Garden")
        self.assertIsNone(path)

    def test_a_path_is_opened_as_usual(self):
        self.assertEqual(first_book("x.fbk"), (None, Path("x.fbk")))


if __name__ == "__main__":
    unittest.main()
