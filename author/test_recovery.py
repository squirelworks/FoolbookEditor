"""The recovery copy holds the unsaved book, and only when there is something unsaved."""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from author import recovery
from foolbookeditor.core import load, save_book


def _book(title: str) -> dict:
    return {"id": "r", "title": title, "pages": [{"id": "P0", "text": [title]}]}


class Recovery(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self._env = mock.patch.dict(os.environ, {"XDG_CONFIG_HOME": str(self.tmp / "config")})
        self._env.start()

    def tearDown(self):
        self._env.stop()
        self._tmp.cleanup()

    def test_every_five_minutes(self):
        self.assertEqual(recovery.INTERVAL_MS, 300000)

    def test_an_unchanged_book_writes_nothing(self):
        book = _book("Same")
        self.assertIsNone(recovery.tick(book, recovery.snapshot(book), self.tmp / "r.fbk"))
        self.assertFalse(recovery.recovery_path(self.tmp / "r.fbk").exists())

    def test_a_changed_book_is_written_to_the_config_directory(self):
        path = self.tmp / "r.fbk"
        book = _book("Before")
        saved = recovery.snapshot(book)
        book["title"] = "After"
        copy = recovery.tick(book, saved, path)
        self.assertTrue(str(copy).startswith(str(self.tmp / "config" / "foolbookeditor" / "recovery")))
        self.assertEqual(load(copy)["title"], "After")
        self.assertEqual(load(copy)["pages"], book["pages"])

    def test_a_newer_copy_is_found_and_clearing_removes_it(self):
        path = self.tmp / "r.fbk"
        save_book(path, _book("Saved"))
        old = path.stat().st_mtime - 60
        os.utime(path, (old, old))
        recovery.tick(_book("Unsaved"), None, path)
        self.assertEqual(recovery.newer(path), recovery.recovery_path(path))
        recovery.clear(path)
        self.assertIsNone(recovery.newer(path))

    def test_an_older_copy_is_not_offered(self):
        path = self.tmp / "r.fbk"
        recovery.tick(_book("Unsaved"), None, path)
        save_book(path, _book("Saved"))
        later = recovery.recovery_path(path).stat().st_mtime + 60
        os.utime(path, (later, later))
        self.assertIsNone(recovery.newer(path))


if __name__ == "__main__":
    unittest.main()
