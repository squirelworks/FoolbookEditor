"""Every line in the README's script table is one the reader runs."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

from engine.engine import follow, run_handler, split_handlers
from foolbook.model import Book, Page, RuntimeState

README = Path(__file__).resolve().parent.parent / "README.md"


def table_scripts() -> list[str]:
    text = README.read_text(encoding="utf-8")
    start = text.find("## Scripts the reader runs")
    if start < 0:
        return []
    section = text[start:]
    stop = section.find("\n## ", 4)
    if stop > 0:
        section = section[:stop]
    return re.findall(r"^\| `([^`]+)` \|", section, re.MULTILINE)


def _run(line: str) -> tuple[RuntimeState, list[dict]]:
    pages = [Page(id="P1"), Page(id="P2"), Page(id="P3")]
    state = RuntimeState(book=Book(path="book.fbk", pages=pages), index=1)
    source = split_handlers("to handle buttonClick\n  %s\nend\n" % line)[0].source
    return state, run_handler(state, source)


class ScriptTableTests(unittest.TestCase):
    def test_the_readme_has_the_table(self):
        self.assertGreaterEqual(len(table_scripts()), 4)

    def test_every_line_in_the_table_runs(self):
        for line in table_scripts():
            with self.subTest(line=line):
                _, actions = _run(line)
                kinds = [a["kind"] for a in actions]
                self.assertNotIn("note", kinds)
                self.assertTrue(set(kinds) & {"goto", "send"})

    def test_next_and_previous_move_the_page(self):
        state, actions = _run("send next")
        self.assertTrue(follow(state, actions))
        self.assertEqual(state.page.id, "P3")
        state, actions = _run("send previous")
        self.assertTrue(follow(state, actions))
        self.assertEqual(state.page.id, "P1")


if __name__ == "__main__":
    unittest.main()
