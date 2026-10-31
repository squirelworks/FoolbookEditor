"""What the script pane says about a script. A warning, never an error.

The words come from Foolbook's table of what the reader runs. They are not
typed here a second time.
"""

from __future__ import annotations


def warning(source: str) -> str:
    """One line for the status bar, or "" when the reader runs every word."""
    from foolbookeditor.core import unknown_words
    found = unknown_words(source or "")
    if not found:
        return ""
    line, word = found[0]
    more = f" (and {len(found) - 1} more)" if len(found) > 1 else ""
    return f"Warning: line {line}: the reader does not run '{word}'{more}. The script is kept."
