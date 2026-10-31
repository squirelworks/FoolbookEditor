"""Action lists, so a book can do things without a script.

A shape's `actions` is a list of dicts, each a `do` and its arguments.
Foolbook runs them in order on a click when the shape has no script.
When it has a script, the script wins, and the editor says so.
"""

from __future__ import annotations

ARGS: dict[str, tuple[str, ...]] = {
    "goto": ("page",),
    "next": (),
    "previous": (),
    "show": ("shape",),
    "hide": ("shape",),
    "settext": ("shape", "text"),
    "play": ("shape",),
}
DOS = tuple(ARGS)


def make(do: str, target: str = "", text: str = "") -> dict:
    """One action. `target` is the page for goto and the shape for the rest."""
    if do not in ARGS:
        raise ValueError(f"Unknown action: {do}")
    action: dict = {"do": do}
    for arg in ARGS[do]:
        value = text if arg == "text" else target.strip()
        if arg != "text" and not value:
            raise ValueError(f"{do} needs a {arg}")
        action[arg] = value
    return action


def describe(action: dict) -> str:
    do = action.get("do")
    if do == "goto":
        return f"Go to page {action.get('page')}"
    if do == "next":
        return "Go to next page"
    if do == "previous":
        return "Go to previous page"
    if do in ("show", "hide", "play"):
        return f"{do.capitalize()} {action.get('shape')}"
    if do == "settext":
        return f"Set text of {action.get('shape')} to \"{action.get('text') or ''}\""
    return f"Unknown: {do}"


def add(shape: dict, action: dict) -> None:
    shape.setdefault("actions", []).append(action)


def remove(shape: dict, index: int) -> None:
    actions = shape.get("actions") or []
    if 0 <= index < len(actions):
        del actions[index]
    if not actions:
        shape.pop("actions", None)


def note(shape: dict) -> str:
    """What the status line says about this shape's actions."""
    if not shape.get("actions"):
        return ""
    if str(shape.get("script") or "").strip():
        return "This object has a script. The script runs, not these actions."
    return f"{len(shape['actions'])} action(s) run on a click."
