"""A book keeps at least one page. Deleting the only one is refused."""

from __future__ import annotations

import unittest
from pathlib import Path

from author.document import LastPage, delete_page

README = Path(__file__).resolve().parents[1] / "README.md"


def book(*ids: str) -> dict:
    return {"pages": [{"id": i} for i in ids]}


class DeletePageTests(unittest.TestCase):
    def test_the_only_page_is_refused(self):
        b = book("A")
        with self.assertRaises(LastPage):
            delete_page(b, 0)
        self.assertEqual([p["id"] for p in b["pages"]], ["A"])

    def test_a_page_of_two_is_deleted(self):
        b = book("A", "B")
        self.assertEqual(delete_page(b, 1), 0)
        self.assertEqual([p["id"] for p in b["pages"]], ["A"])

    def test_the_readme_says_the_rule(self):
        self.assertIn("Deleting the only page is refused", README.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
