"""Foolbook editor.

Foolbook opens a book. This writes one.

  python3 -m foolbookeditor
  python3 -m foolbookeditor path/to/book.fbk
  python3 -m foolbookeditor --desktop path/to/book.fbk
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
    if "--export-exe" in args:
        rest = [a for a in args if a != "--export-exe" and a != "--desktop"]
        from author.executable import export_executable
        try:
            export_executable(rest[0] if rest else None)
        except NotImplementedError as exc:
            print(exc)
            return 2
        return 0
    if "--desktop" in args:
        args = [a for a in args if a != "--desktop"]
        from author.gui import main as desktop
        return desktop(args)
    from author.web import main as browser
    return browser(args)


if __name__ == "__main__":
    raise SystemExit(main())
