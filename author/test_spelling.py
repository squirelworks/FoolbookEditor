"""The small spellcheck flags words it does not know in text shapes, and the book can teach it more."""

import unittest

from author.spelling import add_word, check, known


class Spelling(unittest.TestCase):
    def test_the_list_is_small_and_ordinary(self):
        self.assertLess(len(known()), 1000)
        self.assertGreater(len(known()), 300)
        self.assertIn("the", known())

    def test_unknown_words_in_text_shapes_and_page_text_are_flagged_once(self):
        book = {"pages": [{"id": "P0", "text": ["The quik answer"], "shapes": [
            {"kind": "text", "name": "Q", "text": "What is the anser? The anser is 4."},
            {"kind": "rect", "name": "R", "text": "zzzz"},
        ]}]}
        self.assertEqual(check(book), [("P0", "", "quik"), ("P0", "Q", "anser")])

    def test_a_word_added_to_the_book_is_no_longer_flagged(self):
        book = {"pages": [{"id": "P0", "shapes": [{"kind": "text", "name": "Q", "text": "Foolbook's photosynthesis"}]}]}
        self.assertEqual([w for _p, _s, w in check(book)], ["foolbook", "photosynthesis"])
        add_word(book, "Photosynthesis")
        add_word(book, "foolbook")
        self.assertEqual(check(book), [])
        self.assertEqual(book["words"], ["photosynthesis", "foolbook"])


if __name__ == "__main__":
    unittest.main()
