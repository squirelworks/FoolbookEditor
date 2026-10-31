"""The book stores the viewer the reader shows."""

from __future__ import annotations

import unittest

from author.document import blank_book, set_viewer, viewer_of
from foolbookeditor.core import pack, unpack


class ViewerRecord(unittest.TestCase):
    def test_a_viewer_round_trips(self):
        book = blank_book()
        set_viewer(book, "Main", [800, 600], ["next", "previous", "page"])
        again = unpack(pack(book, compress=False))
        self.assertEqual(again["viewers"], [{"name": "Main", "size": [800, 600], "buttons": ["previous", "next", "page"]}])
        self.assertEqual(viewer_of(again)["name"], "Main")

    def test_an_unknown_button_is_refused(self):
        book = blank_book()
        with self.assertRaises(ValueError):
            set_viewer(book, "Main", [640, 480], ["next", "zoom"])
        self.assertNotIn("viewers", book)

    def test_setting_it_again_replaces_the_first(self):
        book = blank_book()
        set_viewer(book, "Main", [640, 480], ["next"])
        book["viewers"].append({"name": "Other", "size": [10, 10], "buttons": []})
        set_viewer(book, "Main", [640, 480], ["page"])
        self.assertEqual([v["name"] for v in book["viewers"]], ["Main", "Other"])
        self.assertEqual(book["viewers"][0]["buttons"], ["page"])

    def test_a_book_with_no_viewer_has_none(self):
        self.assertIsNone(viewer_of(blank_book()))


if __name__ == "__main__":
    unittest.main()
