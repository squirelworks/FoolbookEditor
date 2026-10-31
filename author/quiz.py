"""A quiz is data on the page, in ``page["quiz"]``.

    {
      "version": 1,
      "question": "Which file starts with FBK1?",
      "choices": [
        {"label": "A Foolbook book", "correct": true},
        {"label": "A picture", "correct": false}
      ],
      "feedback_right": "Yes. FBK1 is the book envelope.",
      "feedback_wrong": "Not that one. Try again.",
      "next": "P3",
      "again": ""
    }

``choices`` keeps the shape Foolbook already reads: ``label`` and ``correct``.
Exactly one choice is right. ``next`` and ``again`` are optional pages for a
right and a wrong answer. A book with an older quiz that has no ``version``
or ``question`` still opens; ``validate`` says what it is missing.
"""

from __future__ import annotations

VERSION = 1
FIELDS = ("version", "question", "choices", "feedback_right", "feedback_wrong", "next", "again")


def make_quiz(question: str, choices: list[str], right: int,
              feedback_right: str = "", feedback_wrong: str = "",
              next_page: str = "", again: str = "") -> dict:
    """A quiz dict. ``right`` is the index of the right choice."""
    if not 0 <= right < len(choices):
        raise ValueError(f"right choice {right} is not one of {len(choices)} choices")
    quiz = {
        "version": VERSION,
        "question": question.strip(),
        "choices": [{"label": str(label).strip(), "correct": i == right} for i, label in enumerate(choices)],
        "feedback_right": feedback_right.strip(),
        "feedback_wrong": feedback_wrong.strip(),
    }
    if next_page.strip():
        quiz["next"] = next_page.strip()
    if again.strip():
        quiz["again"] = again.strip()
    problems = validate(quiz)
    if problems:
        raise ValueError(problems[0])
    return quiz


def right_index(quiz: dict) -> int:
    """The index of the right choice, or -1."""
    for i, choice in enumerate((quiz or {}).get("choices") or []):
        if isinstance(choice, dict) and choice.get("correct"):
            return i
    return -1


def validate(quiz: dict) -> list[str]:
    """What is wrong with a quiz, in sentences. Empty when it is whole."""
    problems = []
    if not isinstance(quiz, dict):
        return ["a quiz is a dict"]
    version = quiz.get("version", VERSION)
    if not isinstance(version, int) or version > VERSION:
        problems.append(f"quiz version {version} is newer than this editor knows ({VERSION})")
    if not str(quiz.get("question") or "").strip():
        problems.append("the quiz has no question")
    choices = quiz.get("choices") or []
    if len(choices) < 2:
        problems.append("a quiz needs at least two choices")
    if any(not str((c or {}).get("label") or "").strip() for c in choices):
        problems.append("a choice has no words")
    right = sum(1 for c in choices if isinstance(c, dict) and c.get("correct"))
    if right != 1:
        problems.append(f"a quiz has exactly one right choice, not {right}")
    return problems
