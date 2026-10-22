"""Turn a ToolBook file into the book Foolbook saves.

A .tbk becomes an .fbk. An .sbk becomes an .fsk. A TBKX does the same.
Foolbook reads the file. This module only writes the result.
"""

from __future__ import annotations

from pathlib import Path

from foolbookeditor.core import pack, read


def convert(src: str | Path) -> Path:
    src = Path(src)
    data = read(src)
    kind = "fsk" if src.suffix.lower() == ".sbk" else "fbk"
    dest = src.with_suffix(".fsk" if kind == "fsk" else ".fbk")
    dest.write_bytes(pack({**data, "format": kind}, kind, compress=True))
    return dest


def sources(raw: str) -> list[Path]:
    path = Path(raw)
    if path.is_dir():
        return [
            p for p in sorted(path.rglob("*"))
            if p.suffix.lower() in {".tbk", ".sbk", ".xml", ".zip", ".tbkx"}
            or p.name.lower().endswith(".tbkx.zip")
        ]
    return [path]


def main(args: list[str]) -> int:
    if not args:
        print("python3 -m foolbookeditor --fbk book.tbk")
        return 2
    failed = 0
    for raw in args:
        for src in sources(raw):
            try:
                dest = convert(src)
                print(dest)
            except Exception as exc:
                failed += 1
                print(f"{src.name}: {exc}")
    return 1 if failed else 0
