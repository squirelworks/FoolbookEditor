"""The menu bar is File, Edit, Insert, Arrange, Book, Help, and every item does something."""

from __future__ import annotations

import unittest

from author.gui import Editor
from author.commands import SHORTCUTS
from author.menus import ALREADY_BOUND, MENUS, items, keymap_text, tk_sequence, tool_help
from author.tools import _KIND


class MenuBar(unittest.TestCase):
    def test_the_six_menus_in_order(self):
        self.assertEqual([name for name, _ in MENUS], ["File", "Edit", "Insert", "Arrange", "Book", "Help"])

    def test_every_item_names_a_command_the_window_has(self):
        for menu, label, command, _key in items():
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


class KeyboardMap(unittest.TestCase):
    def test_every_item_has_a_shortcut_or_says_none(self):
        for menu, label, _command, key in items():
            with self.subTest(menu=menu, label=label):
                self.assertTrue(key, "say none on purpose")
                if key != "none":
                    self.assertIsNotNone(tk_sequence(key))

    def test_no_two_items_share_a_key(self):
        keys = [key for *_rest, key in items() if key != "none"]
        self.assertEqual(len(keys), len(set(keys)))

    def test_keys_become_tk_events(self):
        self.assertEqual(tk_sequence("Ctrl+S"), "<Control-s>")
        self.assertEqual(tk_sequence("Ctrl+Shift+S"), "<Control-S>")
        self.assertEqual(tk_sequence("Ctrl+]"), "<Control-bracketright>")
        self.assertEqual(tk_sequence("Ctrl+Shift+Return"), "<Control-Shift-Return>")
        self.assertEqual(tk_sequence("Ctrl+3"), "<Control-Key-3>")
        self.assertEqual(tk_sequence("F1"), "<F1>")
        self.assertIsNone(tk_sequence("none"))

    def test_help_prints_the_map(self):
        text = keymap_text()
        self.assertIn("Ctrl+S", text)
        self.assertIn("File > Save", text)
        self.assertIn("none                 Arrange > Work on the page", text)

    def test_keys_the_window_already_binds_are_shown_as_they_are(self):
        for _menu, _label, command, key in items():
            if command in ALREADY_BOUND:
                with self.subTest(command=command):
                    self.assertEqual(key, SHORTCUTS[ALREADY_BOUND[command]][0])

    def test_no_menu_key_runs_another_command_already_bound(self):
        taken = {event for keys in SHORTCUTS.values() for event in keys[1:]}
        for _menu, label, command, key in items():
            if command not in ALREADY_BOUND and key != "none":
                with self.subTest(label=label):
                    self.assertNotIn(tk_sequence(key), taken)


if __name__ == "__main__":
    unittest.main()
