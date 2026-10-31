"""A hotword is stored as the range of a word in a field's text, with a page to go to."""

from __future__ import annotations

import unittest

from author.hotwords import add_hotword


def _field(text="See the glossary or go on."):
    return {"kind": "text", "name": "Body", "text": text}


class HotwordTests(unittest.TestCase):
    def test_the_word_becomes_a_range_with_a_jump(self):
        shape = _field()
        add_hotword(shape, "glossary", "P900")
        self.assertEqual(shape["hotwords"], [{"start": 8, "end": 16, "item": {"page": "P900"}}])

    def test_the_second_one_is_added_after_the_first(self):
        shape = _field()
        add_hotword(shape, "glossary", "P900")
        add_hotword(shape, "go on", "P100")
        self.assertEqual([w["start"] for w in shape["hotwords"]], [8, 20])

    def test_a_word_that_is_not_in_the_text_is_refused_by_name(self):
        with self.assertRaisesRegex(ValueError, "index"):
            add_hotword(_field(), "index", "P1")

    def test_a_hotword_needs_a_page(self):
        with self.assertRaises(ValueError):
            add_hotword(_field(), "glossary", " ")

    def test_a_word_already_hot_is_refused(self):
        shape = _field()
        add_hotword(shape, "glossary", "P900")
        with self.assertRaises(ValueError):
            add_hotword(shape, "gloss", "P1")

    def test_only_text_shapes_take_hotwords(self):
        with self.assertRaises(ValueError):
            add_hotword({"kind": "button", "text": "Go"}, "Go", "P1")

    def test_the_count_is_in_the_text_the_reader_draws(self):
        shape = _field("Line one\r\nthe glossary")
        add_hotword(shape, "glossary", "P9")
        self.assertEqual(shape["hotwords"][0]["start"], len("Line one\nthe "))


if __name__ == "__main__":
    unittest.main()
