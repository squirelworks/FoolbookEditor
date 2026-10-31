"""An action dropped on the page lands on the topmost object under the pointer."""

import unittest

from author.actions import drop, make


def _page():
    return {"shapes": [
        {"kind": "rect", "name": "Back", "x": 0, "y": 0, "w": 400, "h": 300, "layer": "background"},
        {"kind": "button", "name": "Low", "x": 10, "y": 10, "w": 100, "h": 40},
        {"kind": "button", "name": "High", "x": 50, "y": 20, "w": 100, "h": 40},
    ]}


class Drop(unittest.TestCase):
    def test_the_topmost_object_gets_the_action(self):
        page = _page()
        self.assertEqual(drop(page, 60, 30, make("next"), "page"), 2)
        self.assertEqual(page["shapes"][2]["actions"], [{"do": "next"}])
        self.assertNotIn("actions", page["shapes"][1])

    def test_a_drop_on_bare_page_adds_nothing(self):
        page = _page()
        self.assertIsNone(drop(page, 300, 250, make("next"), "page"))
        self.assertFalse(any("actions" in s for s in page["shapes"]))

    def test_actions_pile_up_in_drop_order(self):
        page = _page()
        drop(page, 20, 20, make("show", "Answer"), "page")
        drop(page, 20, 20, make("goto", "P2"), "page")
        self.assertEqual([a["do"] for a in page["shapes"][1]["actions"]], ["show", "goto"])


if __name__ == "__main__":
    unittest.main()
