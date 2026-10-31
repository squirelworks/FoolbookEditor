"""Foolbook comes from its main branch or a release tag, never one commit.

A commit pin freezes the editor on a reader that main has already moved
past. Main, or a tag the reader cut, is a reader that exists.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PinTests(unittest.TestCase):
    def test_foolbook_follows_main_or_a_tag(self):
        text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        found = re.search(r'"foolbook @ (git\+[^"]+)"', text)
        self.assertIsNotNone(found, "no foolbook dependency")
        self.assertRegex(found.group(1), r"\.git@(main|v\d[\w.]*)$")


if __name__ == "__main__":
    unittest.main()
