"""The palette offers the colours the book already uses, most used first."""

import unittest

from author.palette import used_colours


class Palette(unittest.TestCase):
    def test_colours_come_from_every_page_most_used_first(self):
        book = {"pages": [
            {"shapes": [{"fill": "#FF0000", "outline": "#000000"}, {"fill": "#00ff00"}]},
            {"shapes": [{"fill": "#ff0000", "outline": "#000000"}, {"fill": "#ff0000"}]},
        ]}
        self.assertEqual(used_colours(book), ["#ff0000", "#000000", "#00ff00"])

    def test_names_and_blanks_are_left_out(self):
        book = {"pages": [{"shapes": [{"fill": "", "outline": None}, {"fill": "red"}, {"fill": "#123"}]}]}
        self.assertEqual(used_colours(book), [])

    def test_the_palette_is_capped(self):
        shapes = [{"fill": f"#0000{i:02x}"} for i in range(40)]
        self.assertEqual(len(used_colours({"pages": [{"shapes": shapes}]})), 16)


if __name__ == "__main__":
    unittest.main()
