"""Export one PNG per page for proofing, drawn by Foolbook's draw, with no window."""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from author.proof import export_pngs


def _book() -> dict:
    return {"id": "proof", "title": "Proof", "pages": [
        {"id": "Paper", "background": True, "shapes": [
            {"kind": "rect", "name": "band", "x": 0, "y": 0, "w": 640, "h": 40, "fill": "#0000ff", "outline": ""},
        ]},
        {"id": "P0", "uses": "Paper", "shapes": [
            {"kind": "rect", "name": "box", "x": 100, "y": 100, "w": 50, "h": 50, "fill": "#ff0000", "outline": ""},
            {"kind": "text", "name": "t", "x": 20, "y": 200, "w": 200, "h": 30, "text": "Hello"},
            {"kind": "button", "name": "Next", "x": 400, "y": 400, "w": 90, "h": 28, "src": "face.png"},
        ]},
        {"id": "P100", "size": [320, 240], "shapes": [
            {"kind": "ellipse", "name": "dot", "x": 10, "y": 10, "w": 40, "h": 40, "fill": "#00ff00", "outline": ""},
            {"kind": "rect", "name": "hid", "x": 200, "y": 200, "w": 20, "h": 20, "fill": "#ff0000", "visible": False},
        ]},
    ]}


class ProofPages(unittest.TestCase):
    def test_one_png_per_page_and_none_for_a_background(self):
        from PIL import Image
        os.environ.pop("DISPLAY", None)
        with tempfile.TemporaryDirectory() as tmp:
            Image.new("RGB", (90, 28), (255, 255, 0)).save(Path(tmp) / "face.png")
            written = export_pngs(_book(), Path(tmp) / "proof", base=tmp)
            self.assertEqual([p.name for p in written], ["001_P0.png", "002_P100.png"])
            first = Image.open(written[0]).convert("RGB")
            second = Image.open(written[1]).convert("RGB")
            self.assertEqual(first.size, (640, 480))
            self.assertEqual(second.size, (320, 240))
            self.assertEqual(first.getpixel((120, 120)), (255, 0, 0))
            self.assertEqual(first.getpixel((300, 20)), (0, 0, 255))
            self.assertEqual(first.getpixel((600, 300)), (255, 255, 255))
            self.assertEqual(first.getpixel((440, 410)), (255, 255, 0))
            self.assertEqual(second.getpixel((30, 30)), (0, 255, 0))
            self.assertEqual(second.getpixel((210, 210)), (255, 255, 255))
            dark = [px for px in first.crop((20, 200, 220, 230)).getdata() if sum(px) < 200]
            self.assertTrue(dark, "the text drew no ink")


if __name__ == "__main__":
    unittest.main()
