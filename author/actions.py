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


# The OpenScript class Foolbook matches for each kind of shape.
CLASS = {
    "text": "field",
    "button": "button",
    "rect": "rectangle",
    "ellipse": "ellipse",
    "image": "picture",
    "line": "line",
    "polygon": "polygon",
    "arc": "arc",
}


def _quote(text: str) -> str:
    return '"' + str(text).replace('"', "'") + '"'


def script_for(actions: list[dict], shapes: list[dict]) -> str:
    """The buttonClick handler that does what the action list does."""
    kinds = {(s.get("name") or "").strip().lower(): s.get("kind") or "" for s in shapes or [] if isinstance(s, dict)}

    def cls(name) -> str:
        return CLASS.get(kinds.get(str(name or "").strip().lower(), ""), "button")

    lines = []
    for action in actions or []:
        do = action.get("do")
        if do == "goto":
            lines.append(f"go to page {_quote(action.get('page'))}")
        elif do in ("next", "previous"):
            lines.append(f"send {do}")
        elif do in ("show", "hide"):
            lines.append(f"{do} {cls(action.get('shape'))} {_quote(action.get('shape'))}")
        elif do == "settext":
            lines.append(f"set text of {cls(action.get('shape'))} {_quote(action.get('shape'))} to {_quote(action.get('text') or '')}")
        elif do == "play":
            lines.append(f"-- play {_quote(action.get('shape'))}: no script line plays a clip, only the action does")
    return "to handle buttonClick\n" + "".join(f"  {line}\n" for line in lines) + "end"


def write_script(shape: dict, shapes: list[dict]) -> str:
    """Put the equivalent script on the shape. The action list stays."""
    shape["script"] = script_for(shape.get("actions") or [], shapes)
    return shape["script"]
