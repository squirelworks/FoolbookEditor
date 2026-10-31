"""A pane that can leave the main window and come back.

Undock hands the pane itself to the window manager (Tk's `wm manage`),
so the widgets, their variables, and their bindings are the ones the
main window already had. Dock packs it back where it was. Closing the
undocked window docks it. Tk only manages a classic tk.Frame this way,
so a ttk pane goes inside one.
"""

from __future__ import annotations


class Sheet:
    def __init__(self, root, pane, title: str):
        self.root = root
        self.pane = pane
        self.title = title
        self.docked = True
        self._pack = {k: v for k, v in pane.pack_info().items() if k != "in"}
        self._parent = pane.pack_info().get("in") or pane.master

    def undock(self) -> None:
        if not self.docked:
            return
        self.pane.pack_forget()
        call = self.root.tk.call
        call("wm", "manage", self.pane)
        call("wm", "title", self.pane, self.title)
        call("wm", "protocol", self.pane, "WM_DELETE_WINDOW", self.root.register(self.dock))
        self.docked = False

    def dock(self) -> None:
        if self.docked:
            return
        self.root.tk.call("wm", "forget", self.pane)
        self.pane.pack(in_=self._parent, **self._pack)
        self.docked = True

    def toggle(self) -> bool:
        """Undock if docked, dock if not. Returns whether it is docked now."""
        if self.docked:
            self.undock()
        else:
            self.dock()
        return self.docked
