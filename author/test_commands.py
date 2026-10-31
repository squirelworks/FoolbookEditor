"""Commands the window binds, run without the window."""

from __future__ import annotations

import unittest

from author import commands


def _book(*ids):
    return {"id": "b", "pages": [{"id": i, "shapes": []} for i in ids]}


class AddPageTests(unittest.TestCase):
    def test_the_new_page_follows_the_current_one(self):
        book = _book("P0", "P100", "P200")
        at = commands.add_page(book, 0)
        self.assertEqual(at, 1)
        self.assertEqual([p["id"] for p in book["pages"]][0], "P0")
        self.assertNotIn(book["pages"][1]["id"], ("P0", "P100", "P200"))
        self.assertEqual([p["id"] for p in book["pages"]][2:], ["P100", "P200"])

    def test_after_the_last_page_it_is_the_end(self):
        book = _book("P0", "P100")
        self.assertEqual(commands.add_page(book, 1), 2)

    def test_an_empty_book_gets_its_first_page(self):
        book = {"pages": []}
        self.assertEqual(commands.add_page(book, -1), 0)
        self.assertEqual(len(book["pages"]), 1)

    def test_the_shortcut_is_written_down(self):
        label, event = commands.SHORTCUTS["add_page"]
        self.assertEqual(label, "Ctrl+M")
        self.assertEqual(event, "<Control-m>")


class DuplicatePageTests(unittest.TestCase):
    def _book(self):
        return {"pages": [
            {"id": "P0", "shapes": []},
            {"id": "P100", "script": "to handle enterPage\nend\n", "shapes": [
                {"kind": "button", "name": "Next", "x": 1, "y": 2, "w": 3, "h": 4,
                 "script": "to handle buttonClick\n  go to next page\nend\n",
                 "points": [[1, 2], [3, 4]]},
            ]},
            {"id": "P200", "shapes": []},
        ]}

    def test_the_copy_is_the_next_page_with_a_new_id(self):
        book = self._book()
        at = commands.duplicate_page(book, 1)
        self.assertEqual(at, 2)
        ids = [p["id"] for p in book["pages"]]
        self.assertEqual(ids[:2], ["P0", "P100"])
        self.assertEqual(ids[3], "P200")
        self.assertNotIn(ids[2], ("P0", "P100", "P200"))
        self.assertEqual(len(set(ids)), 4)

    def test_shapes_and_scripts_come_along_but_are_not_shared(self):
        book = self._book()
        commands.duplicate_page(book, 1)
        source, twin = book["pages"][1], book["pages"][2]
        self.assertEqual(twin["script"], source["script"])
        self.assertEqual(twin["shapes"], source["shapes"])
        twin["shapes"][0]["x"] = 99
        twin["shapes"][0]["points"][0][0] = 99
        self.assertEqual(source["shapes"][0]["x"], 1)
        self.assertEqual(source["shapes"][0]["points"][0][0], 1)

    def test_no_page_no_copy(self):
        book = self._book()
        self.assertEqual(commands.duplicate_page(book, 7), 7)
        self.assertEqual(len(book["pages"]), 3)


class DeletePageTests(unittest.TestCase):
    def test_the_window_asks_with_the_page_id_and_object_count(self):
        book = {"pages": [{"id": "P0"}, {"id": "Quiz", "shapes": [{"kind": "rect"}, {"kind": "button"}]}]}
        self.assertEqual(commands.delete_question(book, 1), "Delete page Quiz and its 2 objects?")
        book["pages"][1]["shapes"].pop()
        self.assertEqual(commands.delete_question(book, 1), "Delete page Quiz and its 1 object?")

    def test_nothing_to_ask_about_the_last_page(self):
        self.assertIsNone(commands.delete_question({"pages": [{"id": "P0"}]}, 0))

    def test_the_command_deletes_without_asking(self):
        book = {"pages": [{"id": "P0"}, {"id": "P100"}, {"id": "P200"}]}
        self.assertEqual(commands.delete_page(book, 1), 1)
        self.assertEqual([p["id"] for p in book["pages"]], ["P0", "P200"])


class ReorderTests(unittest.TestCase):
    def test_up_and_down_move_the_current_page_and_follow_it(self):
        book = _book("P0", "P100", "P200")
        self.assertEqual(commands.page_up(book, 2), 1)
        self.assertEqual([p["id"] for p in book["pages"]], ["P0", "P200", "P100"])
        self.assertEqual(commands.page_down(book, 0), 1)
        self.assertEqual([p["id"] for p in book["pages"]], ["P200", "P0", "P100"])

    def test_the_ends_do_not_move_past_the_book(self):
        book = _book("P0", "P100")
        self.assertEqual(commands.page_up(book, 0), 0)
        self.assertEqual(commands.page_down(book, 1), 1)
        self.assertEqual([p["id"] for p in book["pages"]], ["P0", "P100"])

    def test_a_one_page_book_stays(self):
        book = _book("P0")
        self.assertEqual(commands.page_up(book, 0), 0)
        self.assertEqual(commands.page_down(book, 0), 0)


if __name__ == "__main__":
    unittest.main()
