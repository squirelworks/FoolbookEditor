"""Write the demo book that opens when the editor is started with no path.

  python3 examples/demo.py            # rewrites foolbookeditor/demo/garden.fbk

The book is made with the editor's own model calls, so the file is what
the editor makes. It is original: a shared background, a picture, a
quiz, and a Next button, on three pages. A test regenerates it and
compares the bytes with the copy that ships.
"""

from __future__ import annotations

import base64
import struct
import sys
import zlib
from pathlib import Path

_root = Path(__file__).resolve().parents[1]
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from author.catalog import place_shape  # noqa: E402
from author.document import add_background, add_page, set_background, set_id, set_viewer  # noqa: E402
from author.tools import new_shape  # noqa: E402
from foolbookeditor.core import save_book  # noqa: E402

SHIPPED = _root / "foolbookeditor" / "demo" / "garden.fbk"

SOIL = (122, 82, 48)
LEAF = (64, 145, 108)
SKY = (142, 202, 230)
# Light enough that the reader writes button words in black.
PALE = "#e3ece5"


def sprout_png(width: int = 96, height: int = 72) -> bytes:
    """A small picture of a sprout, drawn pixel by pixel. No image file is read."""
    rows = []
    for y in range(height):
        row = bytearray([0])
        for x in range(width):
            colour = SKY
            if y >= height * 2 // 3:
                colour = SOIL
            elif abs(x - width // 2) <= 1 and y >= height // 3:
                colour = LEAF
            elif (x - width // 2 + 12) ** 2 + 4 * (y - height // 3) ** 2 <= 90 and x < width // 2:
                colour = LEAF
            elif (x - width // 2 - 12) ** 2 + 4 * (y - height // 3) ** 2 <= 90 and x > width // 2:
                colour = LEAF
            row.extend(colour)
        rows.append(bytes(row))

    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)

    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(b"IDAT", zlib.compress(b"".join(rows), 9)) + chunk(b"IEND", b"")


def _place(page: dict, tool: str, x: int, y: int, w: int, h: int, **values) -> dict:
    names = {shape.get("name") for shape in page.get("shapes") or []}
    shape = new_shape(tool, x, y, x + w, y + h, names, values.pop("layer", "page"))
    shape.update(values)
    place_shape(page, shape)
    return shape


def _quiz(page: dict, question: str, choices: list[str], right: int, yes: str, no: str, next_page: str) -> None:
    """The quiz schema of item 81: the quiz on the page, one button per choice, hidden feedback."""
    page["quiz"] = {
        "version": 1,
        "question": question,
        "choices": [{"label": label, "correct": i == right} for i, label in enumerate(choices)],
        "feedback_right": yes,
        "feedback_wrong": no,
        "next": next_page,
    }
    _place(page, "text", 40, 70, 560, 48, name="Question", text=question)
    top = 130
    for i, label in enumerate(choices):
        _place(page, "button", 40, top, 320, 28, name=f"Choice {i + 1}", text=label, choice=i, fill=PALE)
        top += 40
    for side, words in (("right", yes), ("wrong", no)):
        _place(page, "text", 40, top, 560, 40, name=f"Feedback {side}", text=words, feedback=side, visible=False)


def demo() -> dict:
    book = {"id": "garden", "title": "A Small Garden", "pages": []}
    first = book["pages"]
    add_page(book)
    set_id(first[0], "P0")
    add_page(book)
    set_id(first[1], "P100")
    add_page(book)
    set_id(first[2], "P200")
    for page in first:
        page["text"] = []
        page.pop("widgets", None)

    paper = add_background(book)
    set_id(paper, "Garden")
    _place(paper, "box", 0, 0, 640, 480, name="Paper", fill="#f6f1e7", outline="#f6f1e7", layer="background")
    _place(paper, "box", 0, 0, 640, 48, name="Band", fill="#2d6a4f", outline="#2d6a4f", layer="background")
    _place(paper, "text", 16, 8, 400, 32, name="Title", text="A Small Garden", outline="#ffffff", layer="background")
    for page in book["pages"]:
        if not page.get("background"):
            set_background(book, page, "Garden")

    p0, p100, p200 = book["pages"][:3]
    _place(p0, "text", 40, 70, 560, 60, name="Intro", text="A seed is a small plant waiting. Give it water and warmth and it sends up a sprout.")
    _place(p0, "picture", 40, 150, 96, 72, name="Sprout", data=base64.b64encode(sprout_png()).decode("ascii"))
    _place(p0, "button", 500, 420, 90, 28, name="Next", text="Next", fill=PALE, item={"label": "Next", "page": "P100"})

    _quiz(p100, "What does a seed need to sprout?", ["Water and warmth", "Only darkness", "Salt"], 0,
          "Yes. Water and warmth wake it up.", "Not that one. Try another.", "P200")

    _place(p200, "text", 40, 70, 560, 60, name="Done", text="That is the last page. The sprout is on its way.")

    set_viewer(book, "Main", [640, 480], ["page"])
    return book


def write(path: Path = SHIPPED) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    return save_book(path, demo())


if __name__ == "__main__":
    print(write(Path(sys.argv[1]) if len(sys.argv) > 1 else SHIPPED))
