"""What the script pane says about a script. It never stops a save.

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


def first_error(source: str) -> str:
    """The first error Foolbook's check finds, for the status bar, or ""."""
    from foolbookeditor.core import check_script
    errors = check_script(source or "")
    if not errors:
        return ""
    line, message = errors[0]
    return f"Error: line {line}: {message}. Saved anyway."


def status(source: str) -> str:
    """An error first, then a warning, then nothing."""
    return first_error(source) or warning(source)


def apply(page: dict, index: int | None, source: str) -> str:
    """Write the pane's script onto the shape at ``index``, or onto the page
    when ``index`` is None, and return what the status line says about it.

    A page script is checked the same way as an object script. It is kept
    whatever the check finds.
    """
    from author.catalog import set_object_script, set_page_script
    if index is None:
        set_page_script(page, source)
    else:
        set_object_script(page, index, source)
    return status(source)
