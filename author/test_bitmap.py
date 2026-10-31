"""A picture comes in as PNG with its size in pixels, and a file that is not a picture is refused."""

import base64
import struct
import unittest
import zlib

from author.bitmap import PNG, import_bitmap


def _png(width: int, height: int) -> bytes:
    def chunk(kind: bytes, body: bytes) -> bytes:
        return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body))
    rows = b"".join(b"\x00" + b"\xff\x00\x00" * width for _ in range(height))
    return PNG + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)) \
        + chunk(b"IDAT", zlib.compress(rows)) + chunk(b"IEND", b"")


# A 2x1 GIF.
GIF = base64.b64decode("R0lGODlhAgABAIAAAP8AAAAAACwAAAAAAgABAAACAoRRADs=")


class Bitmap(unittest.TestCase):
    def test_a_png_is_kept_and_its_size_read(self):
        data = _png(7, 3)
        self.assertEqual(import_bitmap(data), (data, (7, 3)))

    def test_text_is_refused(self):
        with self.assertRaises(ValueError):
            import_bitmap(b"to handle buttonClick\nend\n")

    def test_a_gif_becomes_png(self):
        try:
            import PIL  # noqa: F401
        except ImportError:
            self.skipTest("Pillow turns other formats into PNG")
        data, size = import_bitmap(GIF)
        self.assertTrue(data.startswith(PNG))
        self.assertEqual(size, (2, 1))


if __name__ == "__main__":
    unittest.main()
