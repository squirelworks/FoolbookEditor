"""The script pane warns about words the reader does not run."""

from __future__ import annotations

import unittest

from author.scripts import warning


class ScriptWarningTests(unittest.TestCase):
    def test_a_script_the_reader_runs_has_no_warning(self):
        self.assertEqual(warning('to handle buttonClick\n  go to page "P2"\nend\n'), "")

    def test_an_unknown_word_is_a_warning_with_its_line(self):
        text = warning('to handle buttonClick\n  flash button "x"\n  wobble\nend\n')
        self.assertTrue(text.startswith("Warning: line 2:"))
        self.assertIn("'flash'", text)
        self.assertIn("1 more", text)

    def test_the_list_is_foolbooks(self):
        from engine.subset import COMMANDS
        for word in COMMANDS:
            self.assertEqual(warning(word), "", word)


if __name__ == "__main__":
    unittest.main()
