"""Pane widths are kept in the user's config, not in the repository."""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from author import settings


class Settings(unittest.TestCase):
    def test_the_file_is_under_the_user_config_directory(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(os.environ, {"XDG_CONFIG_HOME": tmp}):
            self.assertEqual(settings.path(), Path(tmp) / "foolbookeditor" / "settings.json")

    def test_widths_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(os.environ, {"XDG_CONFIG_HOME": tmp}):
            self.assertEqual(settings.load(), {})
            settings.update(panes=[200, 900])
            self.assertEqual(settings.load()["panes"], [200, 900])
            settings.update(other=1)
            self.assertEqual(settings.load(), {"panes": [200, 900], "other": 1})

    def test_a_broken_file_is_ignored(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(os.environ, {"XDG_CONFIG_HOME": tmp}):
            settings.path().parent.mkdir(parents=True)
            settings.path().write_text("{not json")
            self.assertEqual(settings.load(), {})


class Sashes(unittest.TestCase):
    def test_no_saved_widths_uses_the_defaults(self):
        self.assertEqual(settings.sashes(None, 1400), [180, 1120])

    def test_saved_widths_are_used(self):
        self.assertEqual(settings.sashes([220, 1000], 1400), [220, 1000])

    def test_the_stage_keeps_room_when_the_window_is_smaller(self):
        left, right = settings.sashes([220, 1300], 900)
        self.assertLessEqual(left, 220)
        self.assertGreaterEqual(right - left, 300)
        self.assertLessEqual(right, 900 - 120)


if __name__ == "__main__":
    unittest.main()
