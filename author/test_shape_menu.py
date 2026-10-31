"""Right click on a shape: properties, script, forward, backward, cut, copy, delete."""

from __future__ import annotations

import unittest

from author import commands


class ShapeMenuTests(unittest.TestCase):
    def test_the_shape_menu_order(self):
        self.assertEqual(
            [label for label, _command, _key in commands.shape_menu()],
            ["Properties", "Script", "Forward", "Backward", "Cut", "Copy", "Delete"],
        )

    def test_cut_and_copy_show_the_keys_they_already_have(self):
        keys = {command: key for _label, command, key in commands.shape_menu()}
        self.assertEqual(keys["cut"], commands.SHORTCUTS["cut"][0])
        self.assertEqual(keys["copy"], commands.SHORTCUTS["copy"][0])
        self.assertEqual(keys["delete_shapes"], commands.SHORTCUTS["delete_shapes"][0])

    def test_delete_removes_the_chosen_shapes_and_keeps_the_rest_in_order(self):
        page = {"shapes": [{"name": "A"}, {"name": "B"}, {"name": "C"}, {"name": "D"}]}
        self.assertEqual(commands.delete_shapes(page, [2, 0]), 2)
        self.assertEqual([s["name"] for s in page["shapes"]], ["B", "D"])

    def test_delete_ignores_an_index_that_is_not_there(self):
        page = {"shapes": [{"name": "A"}]}
        self.assertEqual(commands.delete_shapes(page, [5]), 0)
        self.assertEqual(len(page["shapes"]), 1)


if __name__ == "__main__":
    unittest.main()
