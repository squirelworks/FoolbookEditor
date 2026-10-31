"""The Pattern button steps a rectangle through 8 by 8 fills and back to none."""

import unittest

from author.patterns import PRESETS, next_pattern, pattern_name


class Patterns(unittest.TestCase):
    def test_every_preset_is_eight_rows_of_eight_bits(self):
        for name, rows in PRESETS[1:]:
            self.assertEqual(len(rows), 8, name)
            self.assertTrue(all(len(r) == 8 and set(r) <= {"0", "1"} for r in rows), name)

    def test_a_rectangle_steps_through_every_pattern_and_back_to_none(self):
        shape = {"kind": "rect"}
        seen = [next_pattern(shape) for _ in PRESETS]
        self.assertEqual(seen, [name for name, _ in PRESETS[1:]] + ["none"])
        self.assertNotIn("tile", shape)

    def test_the_tile_is_stored_on_the_shape(self):
        shape = {"kind": "rect"}
        next_pattern(shape)
        self.assertEqual(shape["tile"], ["10101010", "01010101"] * 4)
        self.assertEqual(pattern_name(shape), "checks")

    def test_other_shapes_get_no_pattern(self):
        shape = {"kind": "button"}
        self.assertIsNone(next_pattern(shape))
        self.assertNotIn("tile", shape)

    def test_a_custom_tile_steps_to_none(self):
        shape = {"kind": "rect", "tile": ["11110000"] * 8}
        self.assertEqual(pattern_name(shape), "custom")
        self.assertEqual(next_pattern(shape), "none")


if __name__ == "__main__":
    unittest.main()
