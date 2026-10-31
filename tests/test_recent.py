"""Recent books: five paths in the user's settings file. A missing one is dropped."""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from author import settings
from author.files import save

ROOT = Path(__file__).resolve().parents[1]
BOOK = {"id": "r", "title": "R", "pages": [{"id": "P0", "text": ["x"], "items": [], "shapes": []}]}


class RecentTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self._env = mock.patch.dict(os.environ, {"XDG_CONFIG_HOME": str(self.tmp / "config")})
        self._env.start()

    def tearDown(self):
        self._env.stop()
        self._tmp.cleanup()

    def book(self, name: str) -> Path:
        return save(self.tmp / name, BOOK)

    def test_newest_first_and_five_kept(self):
        for i in range(7):
            settings.remember(self.book(f"b{i}.fbk"))
        names = [Path(p).name for p in settings.recent()]
        self.assertEqual(names, ["b6.fbk", "b5.fbk", "b4.fbk", "b3.fbk", "b2.fbk"])

    def test_opening_again_moves_it_to_the_top_without_a_copy(self):
        a, b = self.book("a.fbk"), self.book("b.fbk")
        for path in (a, b, a):
            settings.remember(path)
        self.assertEqual([Path(p).name for p in settings.recent()], ["a.fbk", "b.fbk"])

    def test_a_missing_book_is_dropped_and_said(self):
        a = self.book("a.fbk")
        settings.remember(a)
        a.unlink()
        found, said = settings.pick(settings.recent()[0])
        self.assertIsNone(found)
        self.assertIn("a.fbk", said)
        self.assertEqual(settings.recent(), [])

    def test_the_list_shares_the_settings_file_and_keeps_the_panes(self):
        settings.update(panes=[200, 900])
        settings.remember(self.book("a.fbk"))
        self.assertEqual(settings.load()["panes"], [200, 900])
        self.assertEqual(settings.path(), self.tmp / "config" / "foolbookeditor" / "settings.json")
        self.assertNotIn(str(ROOT), str(settings.path()))

    def test_the_window_remembers_what_it_opens_and_saves_and_offers_it_at_start(self):
        try:
            import tkinter as tk
            from author import gui
        except ImportError:
            self.skipTest("no tkinter")
        opened, saved_as = self.book("opened.fbk"), self.tmp / "saved.fbk"
        offered = []
        with mock.patch.object(tk.Tk, "mainloop", lambda self: None), \
                mock.patch.object(gui.Editor, "_start", lambda self, recent: offered.append(recent)):
            try:
                ed = gui.Editor(None)
            except tk.TclError:
                self.skipTest("no display")
        try:
            self.assertEqual(offered, [[]])
            ed._load(opened)
            with mock.patch.object(gui.filedialog, "asksaveasfilename", return_value=str(saved_as)):
                ed._save_as()
            self.assertEqual([Path(p).name for p in settings.recent()], ["saved.fbk", "opened.fbk"])
            labels = [ed.recent_menu.entrycget(i, "label") for i in range(ed.recent_menu.index("end") + 1)]
            self.assertEqual([Path(p).name for p in labels], ["saved.fbk", "opened.fbk"])
            saved_as.unlink()
            ed._open_recent(settings.recent()[0])
            self.assertIn("saved.fbk is not there any more", ed.status.cget("text"))
            self.assertEqual(ed.recent_menu.index("end"), 0)
        finally:
            ed.root.destroy()
        with mock.patch.object(tk.Tk, "mainloop", lambda self: None), \
                mock.patch.object(gui.Editor, "_start", lambda self, recent: offered.append(recent)):
            gui.Editor(None).root.destroy()
        self.assertEqual([Path(p).name for p in offered[-1]], ["opened.fbk"])


if __name__ == "__main__":
    unittest.main()
