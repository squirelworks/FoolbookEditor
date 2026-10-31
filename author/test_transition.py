"""A page transition is stored and ignored, and the README says so."""

import unittest
from pathlib import Path

from author.document import set_transition


class Transition(unittest.TestCase):
    def test_a_named_transition_is_stored_and_none_removes_it(self):
        page = {"id": "P0"}
        set_transition(page, " dissolve ")
        self.assertEqual(page["transition"], "dissolve")
        set_transition(page, "none")
        self.assertNotIn("transition", page)
        set_transition(page, "")
        self.assertNotIn("transition", page)

    def test_the_readme_says_it_is_ignored(self):
        readme = (Path(__file__).resolve().parents[1] / "README.md").read_text(encoding="utf-8")
        line = next((ln for ln in readme.splitlines() if "`transition`" in ln), "")
        self.assertIn("ignored", line)


if __name__ == "__main__":
    unittest.main()
