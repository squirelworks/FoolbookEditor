"""Find and replace reaches page text and shape text, as plain text, with case optional."""

import unittest

from author.findreplace import find, replace_all


def _book():
    return {"pages": [
        {"id": "P0", "text": ["Cats are fine.", "A cat (or two)."], "shapes": [
            {"kind": "text", "name": "Q", "text": "Which CAT?"},
            {"kind": "button", "name": "Go", "text": "Next"},
            {"kind": "rect", "name": "R"},
        ]},
        {"id": "P1", "shapes": [{"kind": "text", "name": "End", "text": "cat.cat"}]},
    ]}


class FindReplace(unittest.TestCase):
    def test_find_counts_matches_in_page_text_and_shapes_ignoring_case(self):
        self.assertEqual(find(_book(), "cat"), [
            ("P0", "page text", 1), ("P0", "page text", 1), ("P0", "Q", 1), ("P1", "End", 2)])

    def test_match_case_narrows_it(self):
        self.assertEqual(find(_book(), "CAT", case=True), [("P0", "Q", 1)])

    def test_the_needle_is_plain_text_not_a_pattern(self):
        self.assertEqual(find(_book(), "t."), [("P1", "End", 1)])
        self.assertEqual(find(_book(), "(or two)"), [("P0", "page text", 1)])

    def test_replace_all_changes_every_match_and_says_how_many(self):
        book = _book()
        self.assertEqual(replace_all(book, "cat", "dog"), 5)
        self.assertEqual(book["pages"][0]["text"], ["dogs are fine.", "A dog (or two)."])
        self.assertEqual(book["pages"][0]["shapes"][0]["text"], "Which dog?")
        self.assertEqual(book["pages"][1]["shapes"][0]["text"], "dog.dog")

    def test_a_replacement_with_backslashes_is_written_as_is(self):
        book = _book()
        replace_all(book, "Next", r"\1 \g<0>", case=True)
        self.assertEqual(book["pages"][0]["shapes"][1]["text"], r"\1 \g<0>")


if __name__ == "__main__":
    unittest.main()
