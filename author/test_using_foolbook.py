"""Using Foolbook in Foolbook's sample folder is what the editor's script writes."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

from foolbookeditor.core import load

ROOT = Path(__file__).resolve().parents[1]
STAMPS = ("fbk", "foolbook", "format", "format_version")


def _script():
    spec = importlib.util.spec_from_file_location("using_foolbook_script", ROOT / "examples" / "using_foolbook.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _sample() -> Path:
    import foolbook
    return Path(foolbook.__file__).resolve().parents[1] / "_books" / "using_foolbook" / "using_foolbook.fbk"


def _content(book: dict) -> dict:
    return {key: value for key, value in book.items() if key not in STAMPS}


class UsingFoolbook(unittest.TestCase):
    def test_the_sample_is_what_the_script_writes(self):
        sample = _sample()
        if not sample.is_file():
            self.skipTest(f"Foolbook's sample folder is not installed beside the package ({sample})")
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(_script().main([tmp]), 0)
            made = Path(tmp) / "using_foolbook.fbk"
            self.assertEqual(_content(load(made)), _content(load(sample)))

    def test_two_runs_write_the_same_bytes(self):
        with tempfile.TemporaryDirectory() as one, tempfile.TemporaryDirectory() as two:
            _script().main([one])
            _script().main([two])
            self.assertEqual((Path(one) / "using_foolbook.fbk").read_bytes(), (Path(two) / "using_foolbook.fbk").read_bytes())

    def test_the_manual_has_its_twenty_three_pages(self):
        book = _script().using_foolbook()
        self.assertEqual(len(book["pages"]), 23)
        self.assertEqual(book["pages"][0]["id"], "P0")
        self.assertEqual(book["pages"][-1]["id"], "P180")


if __name__ == "__main__":
    unittest.main()
