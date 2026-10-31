"""A question bank beside the book. The questions are written for this test."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from author.bank import bank_path, check, load_bank, new_bank, pick, save_bank
from author.quiz import make_quiz


def _bank():
    return new_bank([
        make_quiz("Which month has the fewest days?", ["March", "February", "June"], 1, "Yes.", "No."),
        make_quiz("What does a thermometer measure?", ["Weight", "Temperature"], 1, "Right.", "Try again."),
    ])


class BankTests(unittest.TestCase):
    def test_round_trip_beside_the_book(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = bank_path(Path(tmp) / "weather.fbk")
            self.assertEqual(path.name, "weather.bank.json")
            save_bank(path, _bank())
            self.assertEqual(load_bank(path), _bank())
            self.assertEqual(json.loads(path.read_text())["bank"], 1)

    def test_pick_puts_one_question_on_the_page(self):
        bank = _bank()
        page = {"id": "P1"}
        added = pick(page, bank, 1)
        self.assertEqual(page["quiz"]["question"], "What does a thermometer measure?")
        self.assertEqual([s.get("choice") for s in added if s["kind"] == "button"], [0, 1])
        page["quiz"]["question"] = "changed"
        self.assertEqual(bank["questions"][1]["question"], "What does a thermometer measure?")

    def test_a_question_that_is_not_there(self):
        with self.assertRaises(IndexError):
            pick({"id": "P1"}, _bank(), 5)

    def test_a_future_bank_is_refused_with_its_number(self):
        self.assertEqual(check({"bank": 3, "questions": []}), ["bank version 3 is newer than this editor knows (1)"])
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "x.bank.json"
            path.write_text(json.dumps({"bank": 3, "questions": []}))
            with self.assertRaises(ValueError) as caught:
                load_bank(path)
        self.assertIn("3", str(caught.exception))

    def test_a_bad_question_is_named(self):
        bank = new_bank([{"question": "", "choices": []}])
        self.assertTrue(check(bank)[0].startswith("question 1:"))
        with self.assertRaises(ValueError):
            save_bank(Path("unused.json"), bank)


if __name__ == "__main__":
    unittest.main()
