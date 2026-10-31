"""The books New from template starts from.

A template is an ordinary .fbk in templates/ at the top of the editor
repository. Opening one copies it: the book has no path, so Save asks
where the new book goes and the template file is never written.

The three files are made by this module, not drawn by hand:

  python3 -m author.templates
"""

from __future__ import annotations

import copy
from pathlib import Path

from author import document

TEMPLATE_DIR = Path(__file__).resolve().parents[1] / "templates"

# The envelope stamps these on save. They name the writer, not the book.
_STAMPS = ("fbk", "foolbook")


def blank() -> dict:
    book = document.new_book()
    book["id"] = book["title"] = "blank"
    return book


def title_and_button() -> dict:
    book = document.blank_book()
    book["id"], book["title"] = "title-and-button", "Title and button"
    first = book["pages"][0]
    document.set_text(first, ["Title", "One line under the title."])
    second = book["pages"][document.add_page(book)]
    document.set_text(second, ["The next page"])
    document.set_nav(first, second["id"], "")
    document.set_nav(second, "", first["id"])
    return book


def question_and_four_choices() -> dict:
    book = document.blank_book()
    book["id"], book["title"] = "question-and-four-choices", "Question and four choices"
    question = book["pages"][0]
    done = book["pages"][document.add_page(book)]
    document.set_text(question, ["Question", "Which of these is a colour of the rainbow?"])
    document.set_quiz(question, {
        "choices": [
            {"label": "Green", "correct": True},
            {"label": "Grey", "correct": False},
            {"label": "Brown", "correct": False},
            {"label": "Black", "correct": False},
        ],
        "next": done["id"],
        "again": question["id"],
    })
    document.set_text(done, ["Right", "Green is in the rainbow."])
    document.set_nav(done, "", question["id"])
    return book


BUILDERS = {
    "blank": blank,
    "title-and-button": title_and_button,
    "question-and-four-choices": question_and_four_choices,
}


def names(directory: Path = TEMPLATE_DIR) -> list[str]:
    """Template names, from the files that are there."""
    return sorted(path.stem for path in Path(directory).glob("*.fbk"))


def from_template(name: str, directory: Path = TEMPLATE_DIR) -> dict:
    """A new book that starts as a copy of the template. It has no path."""
    from foolbookeditor.core import load
    path = Path(directory) / f"{name}.fbk"
    if not path.is_file():
        raise ValueError(f"There is no template named {name!r}.")
    book = copy.deepcopy(load(path))
    for key in _STAMPS:
        book.pop(key, None)
    return book


def write_all(directory: Path = TEMPLATE_DIR) -> list[Path]:
    from foolbookeditor.core import save_book
    Path(directory).mkdir(parents=True, exist_ok=True)
    return [save_book(Path(directory) / f"{name}.fbk", build()) for name, build in BUILDERS.items()]


if __name__ == "__main__":
    for written in write_all():
        print(written)
