"""The Properties pane undocks into its own window and docks back. It is the same pane."""

from __future__ import annotations

import os
import unittest

try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:  # no Tk in this Python
    tk = None


@unittest.skipIf(tk is None or not os.environ.get("DISPLAY"), "needs tkinter and a display")
class SheetTests(unittest.TestCase):
    def setUp(self):
        from author.sheet import Sheet
        self.root = tk.Tk()
        self.parent = ttk.Frame(self.root)
        self.parent.pack()
        # Tk only hands a classic frame to the window manager, so the ttk pane sits in one.
        self.pane = tk.Frame(self.parent)
        inner = ttk.LabelFrame(self.pane, text="Properties")
        inner.pack(fill="both", expand=True)
        self.entry = ttk.Entry(inner)
        self.entry.pack()
        self.pane.pack(fill="x", pady=4)
        self.sheet = Sheet(self.root, self.pane, "Properties")
        self.root.update()

    def tearDown(self):
        self.root.destroy()

    def test_undock_makes_the_same_pane_a_window(self):
        self.sheet.undock()
        self.root.update()
        self.assertFalse(self.sheet.docked)
        self.assertEqual(self.root.tk.call("wm", "title", self.pane), "Properties")
        self.assertEqual(self.pane.winfo_manager(), "wm")
        # The same widgets, not a copy.
        self.assertIs(self.entry.master.master, self.pane)

    def test_dock_puts_it_back_where_it_was(self):
        self.sheet.undock()
        self.root.update()
        self.sheet.dock()
        self.root.update()
        self.assertTrue(self.sheet.docked)
        self.assertEqual(self.pane.winfo_manager(), "pack")
        self.assertEqual(str(self.pane.pack_info()["in"]), str(self.parent))

    def test_toggle_goes_back_and_forth(self):
        self.assertFalse(self.sheet.toggle())
        self.assertTrue(self.sheet.toggle())


if __name__ == "__main__":
    unittest.main()
