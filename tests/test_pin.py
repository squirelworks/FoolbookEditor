"""Foolbook is pinned to a commit, not to a floating main."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PinTests(unittest.TestCase):
    def test_foolbook_is_pinned_to_a_commit(self):
        text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        found = re.search(r'"foolbook @ (git\+[^"]+)"', text)
        self.assertIsNotNone(found, "no foolbook dependency")
        self.assertRegex(found.group(1), r"\.git@[0-9a-f]{40}$")


if __name__ == "__main__":
    unittest.main()
