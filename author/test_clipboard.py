"""Cut, copy and paste, without the window."""

from __future__ import annotations

import unittest

from author.clipboard import PASTE_OFFSET, Clipboard


def _page():
    return {"id": "P0", "shapes": [
        {"kind": "rect", "name": "paper", "x": 0, "y": 0, "w": 640, "h": 480, "layer": "background"},
        {"kind": "button", "name": "Next", "x": 10, "y": 20, "w": 90, "h": 28, "script": "go to next page\n"},
        {"kind": "line", "name": "Rule", "points": [[0, 100], [100, 100]]},
    ]}


class ShapeClipboardTests(unittest.TestCase):
    def test_paste_lands_eight_right_and_eight_down_with_a_new_name(self):
        self.assertEqual(PASTE_OFFSET, (8, 8))
        page = _page()
        board = Clipboard()
        self.assertEqual(board.copy_shapes(page, [1, 2]), 2)
        landed = board.paste_shapes(page)
        self.assertEqual(landed, [3, 4])
        pasted = page["shapes"][3]
        self.assertEqual((pasted["x"], pasted["y"]), (18, 28))
        self.assertEqual(pasted["name"], "Next2")
        self.assertEqual(pasted["script"], "go to next page\n")
        self.assertEqual(page["shapes"][4]["points"], [[8, 108], [108, 108]])
        self.assertEqual(page["shapes"][4]["name"], "Rule2")

    def test_a_second_paste_lands_further_on(self):
        page = _page()
        board = Clipboard()
        board.copy_shapes(page, [1])
        board.paste_shapes(page)
        board.paste_shapes(page)
        self.assertEqual([(s["name"], s["x"]) for s in page["shapes"][3:]], [("Next2", 18), ("Next3", 26)])

    def test_the_copy_is_not_the_original(self):
        page = _page()
        board = Clipboard()
        board.copy_shapes(page, [1])
        page["shapes"][1]["x"] = 500
        board.paste_shapes(page)
        self.assertEqual(page["shapes"][3]["x"], 18)

    def test_cut_takes_them_off_and_paste_puts_them_back(self):
        page = _page()
        board = Clipboard()
        self.assertEqual(board.cut_shapes(page, [2, 1]), 2)
        self.assertEqual([s["name"] for s in page["shapes"]], ["paper"])
        board.paste_shapes(page)
        self.assertEqual([s["name"] for s in page["shapes"]], ["paper", "Next", "Rule"])

    def test_a_background_shape_pastes_under_the_page(self):
        page = _page()
        board = Clipboard()
        board.copy_shapes(page, [0])
        self.assertEqual(board.paste_shapes(page), [1])
        self.assertEqual([s["name"] for s in page["shapes"]], ["paper", "paper2", "Next", "Rule"])


class PageClipboardTests(unittest.TestCase):
    def test_a_pasted_page_with_a_taken_id_is_renamed(self):
        book = {"pages": [_page(), {"id": "P100"}]}
        board = Clipboard()
        board.copy_page(book, 0)
        at = board.paste_page(book, 0)
        self.assertEqual(at, 1)
        ids = [p["id"] for p in book["pages"]]
        self.assertEqual(ids[0], "P0")
        self.assertNotIn(ids[1], ("P0", "P100"))
        self.assertEqual(len(book["pages"][1]["shapes"]), 3)

    def test_a_page_whose_id_is_free_keeps_it(self):
        book = {"pages": [{"id": "Intro"}, {"id": "P100"}]}
        other = {"pages": [{"id": "P0"}]}
        board = Clipboard()
        board.copy_page(book, 0)
        board.paste_page(other, 0)
        self.assertEqual([p["id"] for p in other["pages"]], ["P0", "Intro"])

    def test_shapes_do_not_paste_as_a_page(self):
        board = Clipboard()
        board.copy_shapes(_page(), [1])
        self.assertIsNone(board.paste_page({"pages": []}, 0))
        self.assertEqual(board.paste_shapes({"shapes": []}), [0])


if __name__ == "__main__":
    unittest.main()
