"""The menu bar, as data. The window builds it. Tests read it.

Each item is (label, command, shortcut). The command is the name of an
Editor method, `tool:<name>` to pick a drawing tool, or `layer:<name>` to
pick the layer. The shortcut is a key such as `Ctrl+S`, or the word
`none`, said on purpose. None is a separator.

Delete page has no key, so a slip cannot drop a page. The layers have
none because the toolbar radio buttons are one click.
"""

from __future__ import annotations

MENUS = (
    ("File", (
        ("New", "_new", "Ctrl+N"),
        ("Open...", "_open", "Ctrl+O"),
        ("Save", "_save", "Ctrl+S"),
        ("Save as...", "_save_as", "Ctrl+Shift+S"),
        None,
        ("Import .tbk...", "_import", "Ctrl+I"),
        ("Export...", "_export", "Ctrl+E"),
        ("Proof PNGs...", "_proof", "Ctrl+P"),
        None,
        ("Quit", "_close", "Ctrl+Q"),
    )),
    ("Edit", (
        ("Apply page text", "_apply", "Ctrl+Return"),
        ("Apply object script", "_apply_script", "Ctrl+Shift+Return"),
    )),
    ("Insert", (
        ("Button", "tool:button", "Ctrl+1"),
        ("Field", "tool:text", "Ctrl+2"),
        ("Rectangle", "tool:box", "Ctrl+3"),
        ("Line", "tool:line", "Ctrl+4"),
        ("Ellipse", "tool:ellipse", "Ctrl+5"),
        ("Polygon", "tool:polygon", "Ctrl+6"),
        ("Arc", "tool:arc", "Ctrl+7"),
        ("Picture", "tool:picture", "Ctrl+8"),
    )),
    ("Arrange", (
        ("Bring to front", "_front", "Ctrl+]"),
        ("Send to back", "_back", "Ctrl+["),
        None,
        ("Work on the page", "layer:page", "none"),
        ("Work on the background", "layer:background", "none"),
    )),
    ("Book", (
        ("Add page", "_add_page", "Ctrl+M"),
        ("Delete page", "_del_page", "none"),
        ("New background", "_add_background", "Ctrl+Shift+M"),
    )),
    ("Help", (
        ("Help for this tool", "_help_tool", "F1"),
        ("Keyboard map", "_help_keys", "none"),
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
    """Every (menu, label, command, shortcut), separators left out."""
    for menu, entries in MENUS:
        for entry in entries:
            if entry is not None:
                yield menu, entry[0], entry[1], entry[2]


_KEYS = {"]": "bracketright", "[": "bracketleft", "Return": "Return"}


def tk_sequence(shortcut: str) -> str | None:
    """`Ctrl+Shift+S` as the Tk event `<Control-S>`. `none` has no event."""
    if not shortcut or shortcut == "none":
        return None
    parts = shortcut.split("+")
    key = parts[-1]
    mods = parts[:-1]
    shift = "Shift" in mods
    name = _KEYS.get(key, key)
    if len(name) == 1 and name.isalpha():
        name = name.upper() if shift else name.lower()
        shift = False
    elif name.isdigit():
        # <Control-3> is the third mouse button. The key is Key-3.
        name = "Key-" + name
    out = []
    if "Ctrl" in mods:
        out.append("Control")
    if shift:
        out.append("Shift")
    out.append(name)
    return "<" + "-".join(out) + ">"


def keymap_text() -> str:
    """The keyboard map Help prints, one line per menu item."""
    lines = []
    for menu, label, _command, shortcut in items():
        lines.append(f"{shortcut:<20} {menu} > {label.rstrip('.')}")
    return "\n".join(lines) + "\n"


def tool_help(tool: str) -> str:
    """The README section for the tool, or a sentence saying there is none."""
    from author.help import readme_section
    title = TOOL_TITLES.get(tool, tool.title())
    return readme_section(title) or f"The README has no section for {title}."
