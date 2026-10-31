"""Recent files: five paths in the user config folder. A missing one is dropped."""

from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from author import recent

ROOT = Path(__file__).resolve().parents[1]


class RecentTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.store = self.tmp / "config" / "recent.json"

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def book(self, name: str) -> Path:
        path = self.tmp / name
        path.write_bytes(b"FBK1\x00{}")
        return path

    def test_newest_first_and_five_kept(self):
        for i in range(7):
            recent.remember(self.store, self.book(f"b{i}.fbk"))
        names = [Path(p).name for p in recent.load(self.store)]
        self.assertEqual(names, ["b6.fbk", "b5.fbk", "b4.fbk", "b3.fbk", "b2.fbk"])

    def test_opening_again_moves_it_to_the_top_without_a_copy(self):
        a, b = self.book("a.fbk"), self.book("b.fbk")
        recent.remember(self.store, a)
        recent.remember(self.store, b)
        recent.remember(self.store, a)
        self.assertEqual([Path(p).name for p in recent.load(self.store)], ["a.fbk", "b.fbk"])

    def test_a_missing_path_is_dropped_and_said(self):
        a = self.book("a.fbk")
        recent.remember(self.store, a)
        a.unlink()
        found, said = recent.pick(self.store, recent.load(self.store)[0])
        self.assertIsNone(found)
        self.assertIn("a.fbk", said)
        self.assertEqual(recent.load(self.store), [])

    def test_the_list_lives_in_the_user_config_folder(self):
        linux = recent.config_dir({"HOME": "/home/u"}, "linux")
        self.assertEqual(linux, Path("/home/u/.config/foolbookeditor"))
        self.assertEqual(recent.config_dir({"XDG_CONFIG_HOME": "/x"}, "linux"), Path("/x/foolbookeditor"))
        self.assertEqual(recent.config_dir({"APPDATA": "C:/A"}, "win32"), Path("C:/A/foolbookeditor"))
        self.assertNotIn(str(ROOT), str(recent.recent_file()))

    def test_a_broken_list_reads_as_empty(self):
        self.store.parent.mkdir(parents=True)
        self.store.write_text("not json", encoding="utf-8")
        self.assertEqual(recent.load(self.store), [])


if __name__ == "__main__":
    unittest.main()
