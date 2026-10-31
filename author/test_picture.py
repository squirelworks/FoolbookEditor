"""A picture is embedded as PNG, linked when asked, and refused when too large."""

from __future__ import annotations

import base64
import tempfile
import unittest
from pathlib import Path

from author.picture import LIMIT, PictureRefused, picture_fields


class PictureTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_a_gif_is_embedded_as_png(self):
        from PIL import Image
        gif = self.dir / "dot.gif"
        Image.new("RGB", (4, 3), (200, 10, 10)).save(gif)
        fields = picture_fields(gif)
        raw = base64.b64decode(fields["data"])
        self.assertTrue(raw.startswith(b"\x89PNG\r\n\x1a\n"))
        self.assertNotIn("src", fields)

    def test_linking_keeps_the_path_beside_the_book(self):
        from PIL import Image
        (self.dir / "art").mkdir()
        png = self.dir / "art" / "dot.png"
        Image.new("RGB", (2, 2)).save(png)
        fields = picture_fields(png, embed=False, book=self.dir / "course.fbk")
        self.assertEqual(fields, {"src": "art/dot.png"})

    def test_a_picture_over_the_limit_is_refused_with_a_sentence(self):
        big = self.dir / "huge.png"
        with open(big, "wb") as handle:
            handle.truncate(LIMIT + 1)
        with self.assertRaises(PictureRefused) as caught:
            picture_fields(big)
        self.assertIn("huge.png", str(caught.exception))
        self.assertIn("20 MB", str(caught.exception))

    def test_a_file_that_is_not_a_picture_is_refused(self):
        text = self.dir / "notes.png"
        text.write_text("not a picture")
        with self.assertRaises(PictureRefused):
            picture_fields(text)


if __name__ == "__main__":
    unittest.main()
