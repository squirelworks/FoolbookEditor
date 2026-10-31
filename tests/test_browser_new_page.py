"""The older --browser window gives a new page `shapes`, not `widgets`.

The reader draws `shapes` and never reads `widgets` (schema.md). The Tk
window was fixed for this; the page the browser window makes is written
as a JavaScript literal in `author.web.HTML`, so the test reads that.
"""

from __future__ import annotations

import re
import unittest

from author.schema import PAGE_FIELDS


def _new_pages(html: str) -> list[str]:
    """Every page literal the browser script makes: `{id: ..., text: [...] ...}`."""
    return re.findall(r"\{id: [^{}]*text: \[\"New slide\"\][^{}]*\}", html)


class BrowserNewPage(unittest.TestCase):
    def setUp(self):
        from author.web import HTML
        self.pages = _new_pages(HTML)

    def test_the_browser_window_makes_pages(self):
        self.assertGreaterEqual(len(self.pages), 2, "Add page and the empty-book page")

    def test_every_new_page_has_shapes(self):
        for page in self.pages:
            self.assertIn("shapes: []", page, page)

    def test_no_new_page_has_widgets(self):
        for page in self.pages:
            self.assertNotIn("widgets", page, page)

    def test_every_key_is_a_page_field(self):
        for page in self.pages:
            keys = re.findall(r"(\w+):", page)
            self.assertTrue(set(keys) <= set(PAGE_FIELDS), f"{keys} not all in schema")


if __name__ == "__main__":
    unittest.main()
