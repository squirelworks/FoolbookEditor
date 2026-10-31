"""A golden uncompressed FBK1 book loads to its dict and saves to its bytes."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from author.files import ENVELOPE, open_book, save
from tests.fixtures.make_fixtures import TINY

FIXTURES = Path(__file__).resolve().parent / "fixtures"


class GoldenTests(unittest.TestCase):
    def test_the_file_is_uncompressed_fbk1(self):
        blob = (FIXTURES / "tiny.fbk").read_bytes()
        self.assertEqual(blob[:5], b"FBK1\x00")

    def test_loading_it_yields_the_dict(self):
        book = open_book(FIXTURES / "tiny.fbk")
        self.assertEqual({k: v for k, v in book.items() if k not in ENVELOPE}, TINY)

    def test_saving_it_uncompressed_yields_the_same_bytes(self):
        golden = (FIXTURES / "tiny.fbk").read_bytes()
        book = open_book(FIXTURES / "tiny.fbk")
        with tempfile.TemporaryDirectory() as tmp:
            out = save(Path(tmp) / "again.fbk", book, compress=False)
            self.assertEqual(out.read_bytes(), golden)


if __name__ == "__main__":
    unittest.main()
