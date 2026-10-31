"""The Icon tool places a 32 by 32 picture, whatever the drag."""

import unittest

from author.tools import ICON, new_shape


class IconPreset(unittest.TestCase):
    def test_a_click_places_a_32_square_picture(self):
        shape = new_shape("icon", 100, 50, 100, 50, set())
        self.assertEqual((shape["kind"], shape["w"], shape["h"], shape["preset"]), ("image", 32, 32, "icon"))
        self.assertEqual((shape["x"], shape["y"]), (100, 50))

    def test_a_drag_does_not_size_an_icon(self):
        shape = new_shape("icon", 10, 10, 200, 150, {"Icon"})
        self.assertEqual((shape["w"], shape["h"]), (ICON, ICON))
        self.assertEqual(shape["name"], "Icon2")


if __name__ == "__main__":
    unittest.main()
