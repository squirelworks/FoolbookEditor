"""The menu bar is File, Edit, Insert, Arrange, Book, Help, and every item does something."""

from __future__ import annotations

import unittest

from author.gui import Editor
from author.menus import MENUS, items, tool_help
from author.tools import _KIND


class MenuBar(unittest.TestCase):
    def test_the_six_menus_in_order(self):
        self.assertEqual([name for name, _ in MENUS], ["File", "Edit", "Insert", "Arrange", "Book", "Help"])

    def test_every_item_names_a_command_the_window_has(self):
        for menu, label, command in items():
            with self.subTest(menu=menu, label=label):
                if command.startswith("tool:"):
                    self.assertIn(command[5:], _KIND)
                elif command.startswith("layer:"):
                    self.assertIn(command[6:], ("page", "background"))
                else:
                    self.assertTrue(callable(getattr(Editor, command, None)), command)

    def test_help_opens_the_readme_section_for_the_tool(self):
        sections = {"Select": "Drag the corner squares.", "Picture": "PNG, or converted to PNG."}
        self.assertEqual(tool_help("select", sections.get), "Drag the corner squares.")
        self.assertEqual(tool_help("picture", sections.get), "PNG, or converted to PNG.")

    def test_a_tool_with_no_section_says_so(self):
        self.assertEqual(tool_help("sprocket", {}.get), "The README has no section for Sprocket.")

    def test_help_works_with_or_without_the_readme_sections(self):
        self.assertTrue(tool_help("select"))


if __name__ == "__main__":
    unittest.main()
