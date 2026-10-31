"""Every tool the window offers has a README section Help can open."""

from __future__ import annotations

import unittest

from author.help import readme_section

TOOLS = ("Select", "Button", "Field", "Rectangle", "Line", "Ellipse", "Polygon", "Arc", "Picture")


class ReadmeSections(unittest.TestCase):
    def test_each_tool_has_a_section(self):
        for tool in TOOLS:
            with self.subTest(tool=tool):
                self.assertTrue(readme_section(tool), f"README has no ### {tool}")

    def test_a_section_stops_at_the_next_heading(self):
        text = "# A\n\n### One\n\nfirst\n\n### Two\n\nsecond\n"
        self.assertEqual(readme_section("One", text), "first")
        self.assertIsNone(readme_section("Three", text))


if __name__ == "__main__":
    unittest.main()
