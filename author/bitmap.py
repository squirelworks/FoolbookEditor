"""Pictures come into a book as PNG.

A PNG is kept as it is. Its size is read from the header, so no library
is needed. A GIF, BMP, or JPEG is turned into PNG with Pillow when Pillow
is installed, the same optional Pillow the reader uses to fit pictures.
Without Pillow those are refused with a note to save as PNG. Anything
that is not a picture is refused.
"""

from __future__ import annotations

import io
import struct

PNG = b"\x89PNG\r\n\x1a\n"
_OTHER = (b"GIF87a", b"GIF89a", b"BM", b"\xff\xd8\xff")


def png_size(data: bytes) -> tuple[int, int]:
    if not data.startswith(PNG) or data[12:16] != b"IHDR":
        raise ValueError("Not a PNG.")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def import_bitmap(data: bytes) -> tuple[bytes, tuple[int, int]]:
    """PNG bytes and the size in pixels, or ValueError for a non-picture."""
    if data.startswith(PNG):
        return data, png_size(data)
    if not data.startswith(_OTHER):
        raise ValueError("That file is not a picture. Use PNG, GIF, BMP, or JPEG.")
    try:
        from PIL import Image
    except ImportError:
        raise ValueError("Save the picture as PNG first. Other formats need Pillow.") from None
    try:
        image = Image.open(io.BytesIO(data))
        image.load()
    except Exception as exc:
        raise ValueError(f"That picture cannot be read: {exc}") from None
    out = io.BytesIO()
    image.save(out, "PNG")
    return out.getvalue(), image.size
