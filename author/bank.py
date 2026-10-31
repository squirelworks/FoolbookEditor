"""A question bank: the quiz schema as an array, in a JSON file beside the book.

    {"bank": 1, "questions": [quiz, quiz, ...]}

``bank`` is the bank format's version. Each question is a quiz dict as
``author.quiz`` writes it. The editor picks a question from the bank onto a
page with ``insert_quiz``. The bank file itself is never put inside the book.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

from author.quiz import insert_quiz, validate

VERSION = 1


def new_bank(questions: list[dict] | None = None) -> dict:
    return {"bank": VERSION, "questions": list(questions or [])}


def check(bank: dict) -> list[str]:
    """What is wrong with a bank, in sentences. Empty when it is whole."""
    if not isinstance(bank, dict) or not isinstance(bank.get("questions"), list):
        return ["a bank is {\"bank\": 1, \"questions\": [...]}"]
    version = bank.get("bank")
    if not isinstance(version, int) or version < 1:
        return ["a bank has no version"]
    if version > VERSION:
        return [f"bank version {version} is newer than this editor knows ({VERSION})"]
    problems = []
    for i, quiz in enumerate(bank["questions"], 1):
        problems.extend(f"question {i}: {problem}" for problem in validate(quiz))
    return problems


def load_bank(path: str | Path) -> dict:
    bank = json.loads(Path(path).read_text(encoding="utf-8"))
    problems = check(bank)
    if problems:
        raise ValueError(f"{Path(path).name}: {problems[0]}")
    return bank


def save_bank(path: str | Path, bank: dict) -> Path:
    problems = check(bank)
    if problems:
        raise ValueError(problems[0])
    path = Path(path)
    path.write_text(json.dumps(bank, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def bank_path(book_path: str | Path) -> Path:
    """Where a book's bank sits: beside it, ``name.bank.json``."""
    book_path = Path(book_path)
    return book_path.with_name(book_path.stem + ".bank.json")


def pick(page: dict, bank: dict, index: int, x: int = 40, y: int = 40) -> list[dict]:
    """Put question ``index`` of the bank on the page. The bank is not changed."""
    questions = bank.get("questions") or []
    if not 0 <= index < len(questions):
        raise IndexError(f"the bank has {len(questions)} questions, not {index + 1}")
    return insert_quiz(page, copy.deepcopy(questions[index]), x, y)
