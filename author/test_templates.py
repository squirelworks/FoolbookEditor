"""Three original templates ship with the editor, and opening one copies it."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

from author import templates

HAVE_FOOLBOOK = importlib.util.find_spec("foolbook") is not None


@unittest.skipUnless(HAVE_FOOLBOOK, "Foolbook is the core; install it to load and save books")
class TemplateTests(unittest.TestCase):
    def test_the_three_templates_ship(self):
        self.assertEqual(
            templates.names(),
            ["blank", "question-and-four-choices", "title-and-button"],
        )

    def test_each_shipped_file_is_what_the_module_makes(self):
        with tempfile.TemporaryDirectory() as tmp:
            templates.write_all(Path(tmp))
            for name in templates.BUILDERS:
                self.assertEqual(
                    templates.from_template(name),
                    templates.from_template(name, Path(tmp)),
                    name,
                )

    def test_a_template_is_copied_not_opened_in_place(self):
        path = templates.TEMPLATE_DIR / "title-and-button.fbk"
        before = path.read_bytes()
        book = templates.from_template("title-and-button")
        book["pages"][0]["text"] = ["Changed"]
        self.assertEqual(path.read_bytes(), before)
        self.assertNotEqual(templates.from_template("title-and-button")["pages"][0]["text"], ["Changed"])

    def test_the_question_has_four_choices_and_one_is_right(self):
        quiz = templates.from_template("question-and-four-choices")["pages"][0]["quiz"]
        self.assertEqual(len(quiz["choices"]), 4)
        self.assertEqual(sum(1 for c in quiz["choices"] if c["correct"]), 1)

    def test_an_unknown_template_is_refused_by_name(self):
        with self.assertRaisesRegex(ValueError, "nothing-here"):
            templates.from_template("nothing-here")


if __name__ == "__main__":
    unittest.main()
