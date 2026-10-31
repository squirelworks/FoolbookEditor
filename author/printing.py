"""Print is the PNG proof export, sent to the printer when the platform has one call for it.

Windows prints a file with `os.startfile(path, "print")`. A Mac or Linux
machine with `lpr` on the PATH prints the pages with one `lpr`. Anywhere
else the folder of PNG pages is the print, and the editor says so.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


def printer(platform: str = sys.platform, which=shutil.which, run=subprocess.run, start=None):
    """A function that sends a list of files to the printer, or None."""
    if platform.startswith("win"):
        start = start or getattr(os, "startfile", None)
        if start is None:
            return None
        return lambda paths: [start(str(p), "print") for p in paths]
    lpr = which("lpr")
    if lpr:
        return lambda paths: run([lpr, *map(str, paths)], check=True)
    return None


def print_book(book: dict, folder: str | Path, base=None, send=None) -> tuple[list[Path], bool]:
    """Write the PNG pages, then print them if `send` can. Returns the pages and whether they were sent."""
    from author.proof import export_pngs
    written = export_pngs(book, folder, base=base)
    if send is None or not written:
        return written, False
    send(written)
    return written, True
