"""The status line names the tool, the page, the shape, the zoom, and unsaved changes."""

from __future__ import annotations

import unittest

from author.status import status_text


class StatusLine(unittest.TestCase):
    def test_every_part_is_shown(self):
        self.assertEqual(
            status_text("rectangle", "P100", "box", "200%", True),
            "Tool: rectangle   Page: P100   Shape: box   Zoom: 200%   Unsaved changes",
        )

    def test_nothing_selected_and_saved(self):
        self.assertEqual(
            status_text("select", "P0", None, "Fit", False),
            "Tool: select   Page: P0   Shape: none   Zoom: Fit   Saved",
        )

    def test_an_unnamed_shape_and_no_page(self):
        self.assertEqual(
            status_text("select", None, "", "100%", False),
            "Tool: select   Page: none   Shape: (unnamed)   Zoom: 100%   Saved",
        )


if __name__ == "__main__":
    unittest.main()
