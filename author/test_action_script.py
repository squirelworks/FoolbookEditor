"""The editor writes the script an action list stands for, and keeps the list."""

import unittest

from author.actions import script_for, write_script

SHAPES = [
    {"kind": "text", "name": "Answer"},
    {"kind": "text", "name": "Note"},
    {"kind": "rect", "name": "Mark"},
]


class ActionScript(unittest.TestCase):
    def test_each_action_becomes_one_line(self):
        script = script_for([
            {"do": "show", "shape": "Answer"},
            {"do": "hide", "shape": "Mark"},
            {"do": "settext", "shape": "Note", "text": "Well done"},
            {"do": "goto", "page": "P2"},
            {"do": "next"},
            {"do": "previous"},
        ], SHAPES)
        self.assertEqual(script.splitlines(), [
            "to handle buttonClick",
            '  show field "Answer"',
            '  hide rectangle "Mark"',
            '  set text of field "Note" to "Well done"',
            '  go to page "P2"',
            "  send next",
            "  send previous",
            "end",
        ])

    def test_play_has_no_script_line_and_says_so(self):
        line = script_for([{"do": "play", "shape": "Clip"}], []).splitlines()[1]
        self.assertTrue(line.strip().startswith("-- play"))

    def test_writing_the_script_keeps_the_action_list(self):
        shape = {"kind": "button", "actions": [{"do": "next"}]}
        write_script(shape, SHAPES)
        self.assertEqual(shape["script"], "to handle buttonClick\n  send next\nend")
        self.assertEqual(shape["actions"], [{"do": "next"}])


if __name__ == "__main__":
    unittest.main()
