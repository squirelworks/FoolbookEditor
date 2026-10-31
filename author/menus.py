"""The menu bar, as data. The window builds it. Tests read it.

Each item is (label, command). The command is the name of an Editor
method, `tool:<name>` to pick a drawing tool, or `layer:<name>` to pick
the layer. None is a separator.
"""

from __future__ import annotations

MENUS = (
    ("File", (
        ("New", "_new"),
        ("Open...", "_open"),
        ("Save", "_save"),
        ("Save as...", "_save_as"),
        None,
        ("Import .tbk...", "_import"),
        ("Export...", "_export"),
        ("Proof PNGs...", "_proof"),
        None,
        ("Quit", "_close"),
    )),
    ("Edit", (
        ("Apply page text", "_apply"),
        ("Apply object script", "_apply_script"),
    )),
    ("Insert", (
        ("Button", "tool:button"),
        ("Field", "tool:text"),
        ("Rectangle", "tool:box"),
        ("Line", "tool:line"),
        ("Ellipse", "tool:ellipse"),
        ("Polygon", "tool:polygon"),
        ("Arc", "tool:arc"),
        ("Picture", "tool:picture"),
    )),
    ("Arrange", (
        ("Bring to front", "_front"),
        ("Send to back", "_back"),
        None,
        ("Work on the page", "layer:page"),
        ("Work on the background", "layer:background"),
    )),
    ("Book", (
        ("Add page", "_add_page"),
        ("Delete page", "_del_page"),
        ("New background", "_add_background"),
    )),
    ("Help", (
        ("Help for this tool", "_help_tool"),
    )),
)

TOOL_TITLES = {
    "select": "Select",
    "button": "Button",
    "text": "Field",
    "box": "Rectangle",
    "line": "Line",
    "ellipse": "Ellipse",
    "polygon": "Polygon",
    "arc": "Arc",
    "picture": "Picture",
}


def items():
    """Every (menu, label, command), separators left out."""
    for menu, entries in MENUS:
        for entry in entries:
            if entry is not None:
                yield menu, entry[0], entry[1]


def tool_help(tool: str, section=None) -> str:
    """The README section for the tool, or a sentence saying there is none.

    `section` finds a README section by title. By default it is
    `author.help.readme_section`; an editor without that module has no sections.
    """
    if section is None:
        try:
            from author.help import readme_section as section
        except ImportError:
            def section(_title):
                return None
    title = TOOL_TITLES.get(tool, tool.title())
    return section(title) or f"The README has no section for {title}."
