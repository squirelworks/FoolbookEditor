"""The author builds an action list on a shape, and the editor says when a script wins over it."""

import unittest

from author import actions


class ActionList(unittest.TestCase):
    def test_each_action_is_do_plus_its_arguments(self):
        self.assertEqual(actions.make("goto", "P2"), {"do": "goto", "page": "P2"})
        self.assertEqual(actions.make("next"), {"do": "next"})
        self.assertEqual(actions.make("settext", "Note", "Well done"),
                         {"do": "settext", "shape": "Note", "text": "Well done"})
        self.assertEqual(actions.make("play", " Clip "), {"do": "play", "shape": "Clip"})

    def test_a_missing_target_or_unknown_action_is_refused(self):
        for do, target in (("goto", ""), ("show", " "), ("explode", "x")):
            with self.assertRaises(ValueError):
                actions.make(do, target)

    def test_actions_are_added_in_order_and_removing_the_last_drops_the_list(self):
        shape = {"kind": "button"}
        actions.add(shape, actions.make("show", "Answer"))
        actions.add(shape, actions.make("goto", "P1"))
        self.assertEqual([actions.describe(a) for a in shape["actions"]], ["Show Answer", "Go to page P1"])
        actions.remove(shape, 0)
        actions.remove(shape, 0)
        self.assertNotIn("actions", shape)

    def test_the_status_says_a_script_wins(self):
        shape = {"actions": [{"do": "next"}]}
        self.assertEqual(actions.note(shape), "1 action(s) run on a click.")
        shape["script"] = "to handle buttonClick\n  send next\nend"
        self.assertIn("script runs", actions.note(shape))
        self.assertEqual(actions.note({"script": "x"}), "")


if __name__ == "__main__":
    unittest.main()


class ActionsPane(unittest.TestCase):
    def test_choosing_an_object_lists_its_actions(self):
        try:
            import tkinter as tk
            from unittest import mock
            from author import gui
        except ImportError:
            self.skipTest("no tkinter")
        with mock.patch.object(tk.Tk, "mainloop", lambda self: None), \
                mock.patch.object(gui.Editor, "_start", lambda self, recent: None):
            try:
                ed = gui.Editor(None)
            except tk.TclError:
                self.skipTest("no display")
        try:
            page = ed.book["pages"][ed.current]
            page.setdefault("shapes", []).append(
                {"kind": "button", "name": "Go", "x": 10, "y": 10, "w": 60, "h": 20,
                 "actions": [{"do": "next"}]})
            ed._fill_objects(page)
            ed.objects.selection_set(len(ed._rows) - 1)
            ed._on_object()
            self.assertEqual(ed.action_list.get(0, "end"), ("Go to next page",))
        finally:
            ed.root.destroy()
