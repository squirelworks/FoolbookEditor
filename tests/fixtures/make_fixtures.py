"""Write the golden books in this folder.

Run it again when the Foolbook pin moves to a reader with a new version
string, because the reader stamps that string into every file.

    python3 tests/fixtures/make_fixtures.py
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

TINY = {
    "id": "tiny",
    "title": "Tiny",
    "pages": [{
        "id": "P0",
        "text": ["A tiny book."],
        "items": [],
        "shapes": [{"kind": "rect", "name": "Box", "x": 20, "y": 20, "w": 100, "h": 60}],
    }],
}


def main() -> None:
    from author.files import save
    save(HERE / "tiny.fbk", TINY, compress=False)


if __name__ == "__main__":
    main()
