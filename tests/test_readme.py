"""The README says how to install the editor and run it."""

from __future__ import annotations

import unittest
from pathlib import Path

README = Path(__file__).resolve().parents[1] / "README.md"


class ReadmeTests(unittest.TestCase):
    def test_says_which_repository_is_the_window(self):
        text = README.read_text(encoding="utf-8")
        self.assertIn("Foolbook is the reader", text)
        self.assertIn("this repository is the window", text)

    def test_install_is_a_venv_and_an_editable_install(self):
        text = README.read_text(encoding="utf-8")
        for line in ("python3 -m venv .venv", "python3 -m pip install -e .", "python3 -m foolbookeditor"):
            self.assertIn(line, text)


if __name__ == "__main__":
    unittest.main()
