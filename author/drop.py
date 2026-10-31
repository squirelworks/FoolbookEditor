"""Files handed to the editor from outside: a drop on the program, or the command line.

Stock Tk has no drop target for a window. tkinterdnd2 would add one,
and it is a dependency this editor does not take for one gesture. What
works without it:

  Windows, Linux   dropping a book on the program's icon or shortcut
                   starts it with that path, which is the command line.
  macOS            dropping a book on the Dock icon of a packaged app
                   calls ``::tk::mac::OpenDocument``. The editor answers it.

Dropping onto the open window does nothing on any platform. The README
says so.
"""

from __future__ import annotations

from pathlib import Path


def paths_from(raw: list[str] | tuple[str, ...]) -> list[Path]:
    """The files among what was handed over, in order. Folders, flags, and
    paths that are not there are left out."""
    found = []
    for item in raw:
        if not item or item.startswith("-"):
            continue
        path = Path(item)
        if path.is_file():
            found.append(path)
    return found


def install(root, open_path) -> bool:
    """Answer the macOS open-document event. False where Tk has none."""
    if root.tk.call("tk", "windowingsystem") != "aqua":
        return False

    def opened(*names):
        found = paths_from(list(names))
        if found:
            open_path(found[0])

    root.createcommand("::tk::mac::OpenDocument", opened)
    return True
