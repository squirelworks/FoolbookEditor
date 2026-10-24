"""Foolbook editor.

Foolbook opens a book. This writes one.

  python3 -m foolbookeditor
  python3 -m foolbookeditor path/to/book.tbk
  python3 -m foolbookeditor --browser path/to/book.fbk
  python3 -m foolbookeditor --fbk path/to/book.tbk       # write book.fbk; an .sbk writes an .fsk
  python3 -m foolbookeditor --export-exe path/to/book.fbk   # scaffold, writes nothing
"""

from __future__ import annotations

import sys
from pathlib import Path

_root = Path(__file__).resolve().parents[1]
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))


def main() -> int:
    from foolbookeditor.core import require
    require()
    args = sys.argv[1:]
    if "--fbk" in args:
        rest = [a for a in args if a != "--fbk"]
        from author.convert import main as convert
        return convert(rest)
    if "--export-exe" in args:
        rest = [a for a in args if a != "--export-exe" and a != "--desktop"]
        from author.executable import export_executable
        try:
            export_executable(rest[0] if rest else None)
        except NotImplementedError as exc:
            print(exc)
            return 2
        return 0
    if "--browser" in args:
        rest = [a for a in args if a != "--browser"]
        from author.web import main as browser
        return browser(rest)
    args = [a for a in args if a != "--desktop"]
    from author.gui import main as desktop
    return desktop(args)


if __name__ == "__main__":
    raise SystemExit(main())
