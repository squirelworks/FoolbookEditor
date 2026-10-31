"""What a drop on the program hands over, and what the README promises."""

from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from author.drop import paths_from

README = Path(__file__).resolve().parents[1] / "README.md"


class DropTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_files_are_kept_in_order_and_the_rest_left_out(self):
        a = self.tmp / "a.fbk"
        b = self.tmp / "b.tbk"
        a.write_bytes(b"x")
        b.write_bytes(b"x")
        raw = ["--desktop", str(self.tmp), str(self.tmp / "gone.fbk"), str(b), str(a), ""]
        self.assertEqual(paths_from(raw), [b, a])

    def test_the_readme_says_which_platforms_work(self):
        text = README.read_text(encoding="utf-8")
        self.assertIn("Dropping a book onto the open window does nothing anywhere", text)
        for platform in ("Windows", "Linux", "macOS"):
            self.assertIn(platform, text)

    def test_the_program_opens_the_first_file_it_is_handed(self):
        from unittest import mock
        from author import gui
        book = self.tmp / "dropped.fbk"
        book.write_bytes(b"x")
        with mock.patch.object(gui, "Editor") as editor:
            gui.main(["-psn_0_1234", str(self.tmp), str(book)])
        editor.assert_called_once_with(book)

    def test_the_window_answers_the_macos_open_event_only_on_macos(self):
        from unittest import mock
        from author.drop import install
        opened = []
        root = mock.Mock()
        root.tk.call.return_value = "x11"
        self.assertFalse(install(root, opened.append))
        root.tk.call.return_value = "aqua"
        self.assertTrue(install(root, opened.append))
        name, handler = root.createcommand.call_args[0]
        self.assertEqual(name, "::tk::mac::OpenDocument")
        book = self.tmp / "a.fbk"
        book.write_bytes(b"x")
        handler(str(self.tmp / "gone.fbk"), str(book))
        self.assertEqual(opened, [book])


if __name__ == "__main__":
    unittest.main()
