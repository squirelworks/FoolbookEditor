"""Foolbook author.

Slide editor. Produces .fbk (and .fsk). Export .tbk writes a shell with compiled OpenScript.

  python3 -m author.gui
  python3 -m author.gui path/to/book.fbk
"""

from __future__ import annotations

import sys
from pathlib import Path

from .files import open_book as load_book, save as save_book

try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox
except ImportError:
    print("Tkinter is required for the authoring GUI.")
    print("On Windows it ships with Python. On Linux install python3-tk.")
    raise SystemExit(1)


class Editor:
    def __init__(self, path: Path | None = None):
        self.root = tk.Tk()
        self.root.title("Foolbook Author")
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        self.root.geometry(f"{max(1280, screen_w - 40)}x{max(800, screen_h - 80)}")
        self.book: dict = {"id": "new", "title": "New book", "pages": []}
        self.path: Path | None = path
        self.current = 0
        from author.tools import DEFAULT_TOOL
        self.tool = tk.StringVar(value=DEFAULT_TOOL)
        self._build()
        if path and path.exists():
            self._load(path)
        else:
            self._new(ask=False)
            if path is None:
                self._start([])
        self.root.mainloop()

    def _start(self, recent: list[str]):
        """The start window. New book keeps the blank book already showing."""
        from author.start import OPEN, start_choices
        win = tk.Toplevel(self.root)
        win.title("Foolbook Author")
        win.transient(self.root)
        frame = ttk.Frame(win, padding=16)
        frame.pack(fill="both", expand=True)

        def pick(label: str, chosen: Path | None):
            win.destroy()
            if chosen is not None:
                self._load(chosen)
            elif label == OPEN:
                self._open()
            else:
                self._new()

        for label, chosen in start_choices(recent):
            text = label if chosen is None else f"{label}: {chosen.name}"
            ttk.Button(frame, text=text, command=lambda l=label, c=chosen: pick(l, c)).pack(fill="x", pady=2)
        win.bind("<Escape>", lambda _e: win.destroy())
        win.grab_set()

    def _build(self):
        # toolbar
        bar = ttk.Frame(self.root, padding=4)
        bar.pack(fill="x")
        ttk.Button(bar, text="New", command=self._new).pack(side="left")
        ttk.Button(bar, text="Template", command=self._template).pack(side="left", padx=(2, 0))
        ttk.Button(bar, text="Open", command=self._open).pack(side="left", padx=2)
        ttk.Button(bar, text="Catalog", command=self._catalog).pack(side="left")
        ttk.Button(bar, text="Save", command=self._save).pack(side="left")
        ttk.Button(bar, text="Save as", command=self._save_as).pack(side="left", padx=2)
        ttk.Button(bar, text="Export", command=self._export).pack(side="left", padx=2)
        ttk.Button(bar, text="Export executable", command=self._export_executable).pack(side="left", padx=2)
        ttk.Button(bar, text="Publish", command=self._publish).pack(side="left", padx=2)
        ttk.Separator(bar, orient="vertical").pack(side="left", fill="y", padx=6)
        for name, label in (("select", "Select"), ("button", "Button"), ("text", "Field"), ("box", "Rectangle"), ("roundrect", "Rounded")):
            ttk.Radiobutton(bar, text=label, value=name, variable=self.tool).pack(side="left", padx=2)
        ttk.Separator(bar, orient="vertical").pack(side="left", fill="y", padx=6)
        ttk.Button(bar, text="Bold", command=lambda: self._wrap("**")).pack(side="left")
        ttk.Button(bar, text="List", command=self._make_list).pack(side="left", padx=2)
        self.status = ttk.Label(bar, text="")
        self.status.pack(side="right")

        tools = ttk.Frame(self.root, padding=4)
        tools.pack(fill="x")
        self.layer = tk.StringVar(value="page")
        for name, label in (
            ("line", "Line"),
            ("ellipse", "Ellipse"),
            ("polygon", "Polygon"),
            ("curve", "Curve"),
            ("arc", "Arc"),
            ("chord", "Chord"),
            ("pie", "Pie"),
            ("picture", "Picture"),
            ("hotspot", "Hotspot"),
        ):
            ttk.Radiobutton(tools, text=label, value=name, variable=self.tool).pack(side="left", padx=2)
        ttk.Separator(tools, orient="vertical").pack(side="left", fill="y", padx=6)
        ttk.Radiobutton(tools, text="Page", value="page", variable=self.layer, command=self._relayer).pack(side="left")
        ttk.Radiobutton(tools, text="Background", value="background", variable=self.layer, command=self._relayer).pack(side="left", padx=2)
        ttk.Separator(tools, orient="vertical").pack(side="left", fill="y", padx=6)
        ttk.Button(tools, text="Fill", command=lambda: self._color("fill")).pack(side="left")
        ttk.Button(tools, text="Line", command=lambda: self._color("outline")).pack(side="left", padx=2)
        ttk.Button(tools, text="Pattern", command=self._pattern).pack(side="left")
        ttk.Button(tools, text="Front", command=lambda: self._restack("front")).pack(side="left", padx=(8, 2))
        ttk.Button(tools, text="Back", command=lambda: self._restack("back")).pack(side="left")

        body = ttk.PanedWindow(self.root, orient="horizontal")
        body.pack(fill="both", expand=True, padx=4, pady=4)
        self.body = body

        # page list
        left = ttk.Frame(body, width=160)
        body.add(left, weight=0)
        ttk.Label(left, text="Pages").pack(anchor="w")
        self.pages = tk.Listbox(left, exportselection=False, width=18)
        self.pages.pack(fill="both", expand=True)
        self.pages.bind("<<ListboxSelect>>", self._on_select)
        row = ttk.Frame(left)
        row.pack(fill="x", pady=4)
        ttk.Button(row, text="Add", command=self._add_page).pack(side="left")
        from author.commands import SHORTCUTS
        self.root.bind(SHORTCUTS["add_page"][1], lambda _e: self._add_page())
        self.root.bind(SHORTCUTS["duplicate_page"][1], lambda _e: self._duplicate_page())
        self.root.bind(SHORTCUTS["delete_page"][1], lambda _e: self._del_page())
        self.root.bind(SHORTCUTS["page_up"][1], lambda _e: self._reorder("page_up"))
        self.root.bind(SHORTCUTS["page_down"][1], lambda _e: self._reorder("page_down"))
        ttk.Button(row, text="Duplicate", command=self._duplicate_page).pack(side="left", padx=4)
        ttk.Button(row, text="Delete", command=self._del_page).pack(side="left")
        order = ttk.Frame(left)
        order.pack(fill="x")
        ttk.Button(order, text="Up", command=lambda: self._reorder("page_up")).pack(side="left")
        ttk.Button(order, text="Down", command=lambda: self._reorder("page_down")).pack(side="left", padx=4)
        ttk.Button(left, text="New background", command=self._add_background).pack(anchor="w")

        # The page picture. Foolbook draws it. The editor only holds the panes.
        center = ttk.Frame(body)
        body.add(center, weight=3)
        self.canvas = tk.Canvas(center, bg="white", width=640, height=480, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<ButtonPress-1>", self._on_press)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)
        self.canvas.bind("<Configure>", self._on_canvas_resize)

        # objects on the selected page. Author shows them. Reader may hide some.
        objects = ttk.Frame(body, width=260)
        body.add(objects, weight=0)
        ttk.Label(objects, text="Objects").pack(anchor="w")
        self.objects = tk.Listbox(objects, exportselection=False, width=28)
        self.objects.pack(fill="both", expand=True)
        self.objects.bind("<<ListboxSelect>>", self._on_object)
        self.object_meta = ttk.Label(objects, text="", wraplength=200)
        self.object_meta.pack(anchor="w", pady=4)
        self._build_properties(objects)
        ttk.Label(objects, text="Script (the object's, or the page's when no object is chosen)").pack(anchor="w")
        self.oscript = tk.Text(objects, height=12, wrap="none", font="TkFixedFont", undo=True)
        self.oscript.pack(fill="both", expand=True)
        self.oscript.bind("<Tab>", self._script_tab)
        ttk.Button(objects, text="Apply script", command=self._apply_script).pack(anchor="e", pady=4)
        self._rows: list[dict] = []
        self._object = None
        self._drag = None

        form = ttk.Frame(center)
        form.pack(fill="x")
        ttk.Label(form, text="Page id").grid(row=0, column=0, sticky="w")
        self.pid = ttk.Entry(form, width=12)
        self.pid.grid(row=0, column=1, sticky="w", padx=4)
        ttk.Label(form, text="Next").grid(row=0, column=2, sticky="w")
        self.next = ttk.Entry(form, width=10)
        self.next.grid(row=0, column=3, sticky="w", padx=4)
        ttk.Label(form, text="Back").grid(row=0, column=4, sticky="w")
        self.back = ttk.Entry(form, width=10)
        self.back.grid(row=0, column=5, sticky="w", padx=4)
        ttk.Label(form, text="Background").grid(row=0, column=6, sticky="w")
        self.uses = ttk.Combobox(form, width=14, state="readonly")
        self.uses.grid(row=0, column=7, sticky="w", padx=4)
        self.uses.bind("<<ComboboxSelected>>", self._on_uses)

        ttk.Label(center, text="Text  (blank line = new paragraph; lines starting with - or * are a list)").pack(anchor="w", pady=(6, 0))
        self.text = tk.Text(center, height=4, wrap="word")
        self.text.pack(fill="x")
        self.text.bind("<KeyRelease>", lambda e: self._preview())

        ttk.Button(center, text="Apply", command=self._apply).pack(anchor="e", pady=4)
        self.root.bind("<Escape>", self._on_escape)
        self.canvas.bind("<Double-Button-1>", self._finish_draft)
        self.root.bind("<Return>", self._finish_draft)
        self._draft = None
        # Choosing another tool drops a polygon that was not closed.
        self.tool.trace_add("write", lambda *_args: setattr(self, "_draft", None))
        self.root.after_idle(self._split)

    def _build_properties(self, parent):
        """One row per property. Return or leaving the box applies it. Bad text puts the old value back."""
        from author.properties import CHOICES, ROWS
        # A classic frame holds the pane so Undock can hand it to the window manager.
        self.props_holder = tk.Frame(parent)
        self.props_holder.pack(fill="x", pady=4)
        self.props = ttk.LabelFrame(self.props_holder, text="Properties", padding=4)
        self.props.pack(fill="both", expand=True)
        ttk.Button(self.props_holder, text="Undock", command=self._toggle_properties).pack(anchor="e")
        self.props.columnconfigure(1, weight=1)
        self._prop_vars: dict[str, tk.StringVar] = {}
        self._prop_texts: dict[str, tk.Text] = {}
        for row, (key, label, kind) in enumerate(ROWS):
            ttk.Label(self.props, text=label).grid(row=row, column=0, sticky="w")
            var = tk.StringVar()
            if kind == "flag":
                box = ttk.Checkbutton(self.props, variable=var, onvalue="true", offvalue="false",
                                      command=lambda k=key: self._set_property(k))
                box.grid(row=row, column=1, sticky="w", padx=4, pady=1)
            elif kind == "pointlist":
                text = tk.Text(self.props, height=4, width=18, font="TkFixedFont", wrap="none")
                text.grid(row=row, column=1, sticky="we", padx=4, pady=1)
                text.bind("<FocusOut>", lambda _e, k=key: self._set_property(k))
                self._prop_texts[key] = text
            elif kind == "choice":
                pick = ttk.Combobox(self.props, textvariable=var, values=CHOICES[key], state="readonly", width=16)
                pick.grid(row=row, column=1, sticky="we", padx=4, pady=1)
                pick.bind("<<ComboboxSelected>>", lambda _e, k=key: self._set_property(k))
            else:
                entry = ttk.Entry(self.props, textvariable=var, width=18)
                entry.grid(row=row, column=1, sticky="we", padx=4, pady=1)
                entry.bind("<Return>", lambda _e, k=key: self._set_property(k))
                entry.bind("<FocusOut>", lambda _e, k=key: self._set_property(k))
            self._prop_vars[key] = var
        self._build_well(len(ROWS))
        from author.sheet import Sheet
        self.sheet = Sheet(self.root, self.props_holder, "Properties")

    def _toggle_properties(self):
        """The same Properties pane, in its own window or back in Author."""
        docked = self.sheet.toggle()
        for child in self.props_holder.winfo_children():
            if isinstance(child, ttk.Button):
                child.config(text="Undock" if docked else "Dock")

    def _build_well(self, row: int):
        """Eight plain colours. A click sets the fill, a right-click the outline."""
        from author.properties import WELL
        ttk.Label(self.props, text="Colours").grid(row=row, column=0, sticky="w")
        well = ttk.Frame(self.props)
        well.grid(row=row, column=1, sticky="w", padx=4, pady=2)
        for at, color in enumerate(WELL):
            swatch = tk.Label(well, bg=color, width=2, relief="solid", borderwidth=1, name=f"well{color[1:]}")
            swatch.grid(row=0, column=at, padx=1)
            swatch.bind("<Button-1>", lambda _e, c=color: self._pick_color("fill", c))
            swatch.bind("<Button-3>", lambda _e, c=color: self._pick_color("outline", c))
        ttk.Button(well, text="No fill", width=7, command=lambda: self._pick_color("fill", "")).grid(
            row=0, column=len(WELL), padx=(4, 0)
        )

    def _pick_color(self, key: str, color: str):
        self._prop_vars[key].set(color)
        self._set_property(key)

    def _show_properties(self):
        from author.properties import read
        shape, _index = self._selected()
        for key, var in self._prop_vars.items():
            var.set(read(shape, key) if shape is not None else "")
        for key, text in self._prop_texts.items():
            text.delete("1.0", "end")
            text.insert("1.0", read(shape, key) if shape is not None else "")

    def _set_property(self, key: str):
        shape, index = self._selected()
        if shape is None:
            return
        from author.properties import read, write
        page = (self.book.get("pages") or [])[self.current]
        if key in self._prop_texts:
            text = self._prop_texts[key]
            changed = write(shape, key, text.get("1.0", "end"), page)
            text.delete("1.0", "end")
            text.insert("1.0", read(shape, key))
        else:
            changed = write(shape, key, self._prop_vars[key].get(), page)
            self._prop_vars[key].set(read(shape, key))
        if not changed:
            self.status.config(text=f"{key} kept: that value cannot be used")
            return
        if key == "name" and self._object is not None:
            row = self._rows[self._object]
            row["name"] = shape.get("name") or ""
            self.objects.delete(self._object)
            self.objects.insert(self._object, f"{row['kind']}  {row['name']}{' hidden' if row['hidden'] else ''}")
            self.objects.selection_set(self._object)
        self._preview()

    def _split(self):
        """Keep the picture on screen. The side panes do not take the window."""
        width = self.body.winfo_width()
        if width < 400:
            self.root.after(50, self._split)
            return
        try:
            self.body.sashpos(0, 180)
            self.body.sashpos(1, width - 280)
        except tk.TclError:
            return

    def _new(self, ask: bool = True):
        from author.document import new_book
        if not ask:
            self._open_new(new_book())
            return
        self._ask_new()

    def _ask_new(self):
        """Page size and background colour, then the stage."""
        from author.document import PAGE_SIZE, new_book
        win = tk.Toplevel(self.root)
        win.title("New book")
        win.transient(self.root)
        form = ttk.Frame(win, padding=12)
        form.pack(fill="both", expand=True)
        fields = {}
        for row, (label, value) in enumerate((
            ("Width", PAGE_SIZE[0]),
            ("Height", PAGE_SIZE[1]),
            ("Background", "#ffffff"),
        )):
            ttk.Label(form, text=label).grid(row=row, column=0, sticky="w")
            var = tk.StringVar(value=str(value))
            ttk.Entry(form, textvariable=var, width=10).grid(row=row, column=1, sticky="w", pady=2)
            fields[label] = var
        error = ttk.Label(form, text="", foreground="#a00000", wraplength=240)
        error.grid(row=3, column=0, columnspan=2, sticky="w")

        def make():
            try:
                size = (int(fields["Width"].get()), int(fields["Height"].get()))
            except ValueError:
                error.config(text="Width and height are whole numbers.")
                return
            try:
                book = new_book(size, fields["Background"].get())
            except ValueError as exc:
                error.config(text=str(exc))
                return
            win.destroy()
            self._open_new(book)

        buttons = ttk.Frame(form)
        buttons.grid(row=4, column=0, columnspan=2, sticky="e", pady=(8, 0))
        ttk.Button(buttons, text="Cancel", command=win.destroy).pack(side="right")
        ttk.Button(buttons, text="Create", command=make).pack(side="right", padx=4)
        win.bind("<Return>", lambda _e: make())
        win.bind("<Escape>", lambda _e: win.destroy())
        win.grab_set()

    def _template(self):
        """A new book copied from a template. The template file is not opened."""
        from author.templates import from_template, names
        win = tk.Toplevel(self.root)
        win.title("New from template")
        win.transient(self.root)
        frame = ttk.Frame(win, padding=12)
        frame.pack(fill="both", expand=True)
        found = names()
        listing = tk.Listbox(frame, height=max(3, len(found)), exportselection=False)
        for name in found:
            listing.insert("end", name)
        listing.pack(fill="both", expand=True)

        def make():
            sel = listing.curselection()
            if not sel:
                return
            book = from_template(found[sel[0]])
            win.destroy()
            self._open_new(book)

        ttk.Button(frame, text="Create", command=make).pack(anchor="e", pady=(8, 0))
        listing.bind("<Double-Button-1>", lambda _e: make())
        win.bind("<Escape>", lambda _e: win.destroy())
        win.grab_set()

    def _catalog(self):
        """The books in a folder. Double-click opens one."""
        from author.shelf import list_books
        folder = filedialog.askdirectory(title="Catalog folder")
        if not folder:
            return
        rows = list_books(folder)
        win = tk.Toplevel(self.root)
        win.title(f"Catalog: {Path(folder).name}")
        tree = ttk.Treeview(win, columns=("title", "pages", "file"), show="headings", height=min(20, max(4, len(rows))))
        for column, label, width in (("title", "Title", 260), ("pages", "Pages", 60), ("file", "File", 200)):
            tree.heading(column, text=label)
            tree.column(column, width=width, anchor="e" if column == "pages" else "w")
        for index, row in enumerate(rows):
            title = row["error"] or row["title"]
            tree.insert("", "end", iid=str(index), values=(title, row["pages"], row["file"]))
        tree.pack(fill="both", expand=True, padx=8, pady=8)

        def open_row(_evt=None):
            sel = tree.selection()
            if not sel or rows[int(sel[0])]["error"]:
                return
            win.destroy()
            self._load(rows[int(sel[0])]["path"])

        tree.bind("<Double-Button-1>", open_row)
        tree.bind("<Return>", open_row)

    def _open_new(self, book: dict):
        self.book = book
        self.path = None
        self.current = 0
        self._refresh_list()
        self.status.config(text="New book")

    def _open(self):
        p = filedialog.askopenfilename(
            title="Open book",
            filetypes=[
                ("Foolbook", "*.fbk *.json *.tbk *.sbk"),
                ("Office", "*.pdf *.ppt *.pptx *.doc *.docx *.odt"),
                ("All", "*.*"),
            ],
        )
        if p:
            self._load(Path(p))

    def _load(self, path: Path):
        from foolbookeditor.core import is_office, read, to_book
        suffix = path.suffix.lower()
        if is_office(path):
            self.book = to_book(path)
        elif suffix in {".tbk", ".sbk"}:
            self.book = read(path)
        else:
            self.book = load_book(path)
        self.path = path
        self.current = 0
        self._refresh_list()
        self.status.config(text=str(path.name))

    def _save(self):
        self._apply()
        if not self.path:
            self._save_as()
            return
        save_book(self.path, self.book)
        self.status.config(text=f"Saved {self.path.with_suffix('.json').name} and .fbk")

    def _save_as(self):
        self._apply()
        p = filedialog.asksaveasfilename(
            title="Save book",
            defaultextension=".fbk",
            filetypes=[("Foolbook book", "*.fbk"), ("JSON", "*.json")],
        )
        if not p:
            return
        self.path = Path(p)
        save_book(self.path, self.book)
        self.status.config(text=f"Saved {self.path.with_suffix('.json').name} and .fbk")


    def _publish(self):
        """A folder with the .fbk, its linked files, and a README. No installer."""
        self._apply()
        folder = filedialog.askdirectory(title="Publish into this folder")
        if not folder:
            return
        from author.publish import publish
        source = self.path.parent if self.path else None
        name = self.path.with_suffix(".fbk").name if self.path else ""
        written, missing = publish(self.book, folder, source=source, name=name)
        note = f"Published {len(written)} files to {folder}"
        if missing:
            note += f". Not found: {', '.join(missing)}"
        self.status.config(text=note)

    def _export(self):
        """Save as a book, a TBX folder, a ToolBook shell, or an office file."""
        self._apply()
        p = filedialog.asksaveasfilename(
            title="Export",
            defaultextension=".fbk",
            filetypes=[
                ("Foolbook book", "*.fbk"),
                ("System book", "*.fsk"),
                ("Course", "*.fsc"),
                ("TBX folder", "*.tbx"),
                ("ToolBook shell", "*.tbk"),
                ("System shell", "*.sbk"),
                ("PDF", "*.pdf"),
                ("Word", "*.docx"),
                ("Word (legacy)", "*.doc"),
                ("PowerPoint", "*.pptx"),
                ("PowerPoint (legacy)", "*.ppt"),
                ("OpenDocument", "*.odt"),
            ],
        )
        if not p:
            return
        from foolbookeditor.core import compile_script, export_book
        dest = export_book(p, self.book, compile_script)
        note = "folder" if dest.is_dir() else dest.name
        self.status.config(text=f"Exported {note}")

    def _export_executable(self):
        """ToolBook-style self-running book. Scaffold only."""
        from author.executable import export_executable
        try:
            export_executable(self.path)
        except NotImplementedError as exc:
            messagebox.showinfo("Foolbook Editor", str(exc))

    def _refresh_list(self):
        self.pages.delete(0, "end")
        from author.document import page_label
        for p in self.book.get("pages") or []:
            self.pages.insert("end", page_label(p))
        if self.book.get("pages"):
            self.pages.selection_set(self.current)
            self._show(self.current)

    def _on_select(self, _evt=None):
        sel = self.pages.curselection()
        if not sel:
            return
        self._apply()
        self._apply_script()
        self.current = sel[0]
        self._show(self.current)

    def _show(self, idx: int):
        pages = self.book.get("pages") or []
        if not (0 <= idx < len(pages)):
            return
        p = pages[idx]
        self.pid.delete(0, "end")
        self.pid.insert(0, p.get("id") or "")
        items = { (i.get("label") or "").lower(): i.get("page") for i in p.get("items") or [] }
        self.next.delete(0, "end")
        self.next.insert(0, items.get("next") or "")
        self.back.delete(0, "end")
        self.back.insert(0, items.get("back") or "")
        self.text.delete("1.0", "end")
        self.text.insert("1.0", "\n\n".join(p.get("text") or []))
        self._fill_uses(p)
        self._fill_objects(p)
        self._preview()

    def _fill_uses(self, page: dict):
        from author.document import background_of
        names = [str(p.get("id") or "") for p in self.book.get("pages") or [] if p.get("background")]
        self.uses.config(values=["(none)"] + names, state="disabled" if page.get("background") else "readonly")
        found = background_of(self.book, page)
        self.uses.set(found.get("id") if found else "(none)")

    def _on_uses(self, _evt=None):
        pages = self.book.get("pages") or []
        if not (0 <= self.current < len(pages)):
            return
        from author.document import clear_background, set_background
        page = pages[self.current]
        chosen = self.uses.get()
        if chosen == "(none)":
            clear_background(page)
        else:
            set_background(self.book, page, chosen)
        self._fitted = None
        self._preview()

    def _fill_objects(self, page: dict):
        from author.catalog import objects_of, page_script
        self._rows = objects_of(page, self.layer.get())
        self._object = None
        self.objects.delete(0, "end")
        for row in self._rows:
            name = row["name"] or "(unnamed)"
            mark = " hidden" if row["hidden"] else ""
            self.objects.insert("end", f"{row['kind']}  {name}{mark}")
        script = page_script(page)
        self.oscript.delete("1.0", "end")
        self.oscript.insert("1.0", script)
        self.object_meta.config(text="Page script" if script else "No objects" if not self._rows else "")

    def _on_object(self, _evt=None):
        sel = self.objects.curselection()
        if not sel or not self._rows:
            return
        self._apply_script()
        self._object = sel[0]
        row = self._rows[self._object]
        left, top, right, bottom = row["bounds"]
        self.object_meta.config(text=f"{row['kind']}  {row['name'] or '(unnamed)'}  {left}, {top}, {right}, {bottom}")
        self.oscript.delete("1.0", "end")
        self.oscript.insert("1.0", row["script"])
        self._show_properties()

    def _script_tab(self, _evt=None):
        from author.properties import SCRIPT_TAB
        self.oscript.insert("insert", SCRIPT_TAB)
        return "break"

    def _apply_script(self):
        pages = self.book.get("pages") or []
        if not (0 <= self.current < len(pages)):
            return
        if self._object is None:
            from author.catalog import set_page_script
            set_page_script(pages[self.current], self.oscript.get("1.0", "end"))
            return
        from author.catalog import set_object_script
        set_object_script(pages[self.current], self._rows[self._object]["index"], self.oscript.get("1.0", "end"))
        self._rows[self._object]["script"] = pages[self.current]["shapes"][self._rows[self._object]["index"]].get("script") or ""

    def _apply(self):
        pages = self.book.get("pages") or []
        if not (0 <= self.current < len(pages)):
            return
        p = pages[self.current]
        from author.document import set_id, set_nav, set_text, text_from_editor
        set_id(p, self.pid.get())
        set_text(p, text_from_editor(self.text.get("1.0", "end")))
        set_nav(p, self.next.get(), self.back.get())
        from author.document import page_label
        self.pages.delete(self.current)
        self.pages.insert(self.current, page_label(p))
        self.pages.selection_set(self.current)
        self._preview()

    def _add_page(self):
        self._apply()
        from author.commands import add_page
        self.current = add_page(self.book, self.current)
        self._refresh_list()

    def _duplicate_page(self):
        self._apply()
        self._apply_script()
        from author.commands import duplicate_page
        self.current = duplicate_page(self.book, self.current)
        self._refresh_list()

    def _reorder(self, command: str):
        self._apply()
        self._apply_script()
        from author import commands
        self.current = getattr(commands, command)(self.book, self.current)
        self._refresh_list()

    def _add_background(self):
        self._apply()
        from author.document import add_background
        add_background(self.book)
        self.current = len(self.book["pages"]) - 1
        self._refresh_list()

    def _del_page(self):
        from author.commands import delete_page, delete_question
        question = delete_question(self.book, self.current)
        if question is None:
            self.status.config(text="A book keeps its last page")
            return
        if not messagebox.askyesno("Delete page", question, parent=self.root):
            return
        self.current = delete_page(self.book, self.current)
        self._refresh_list()

    def _preview(self):
        if getattr(self, "_typing", None) is not None:
            # A field is being typed into. Redrawing now would take the box away.
            return
        page = None
        pages = self.book.get("pages") or []
        if 0 <= self.current < len(pages):
            page = pages[self.current]
        from author.stage import paint
        paint(self.canvas, page or {}, self.book)
        self._draw_handles()
        self._draw_draft()

    def _draw_handles(self):
        if self.tool.get() != "select" or self._object is None:
            return
        pages = self.book.get("pages") or []
        if not (0 <= self.current < len(pages)):
            return
        from author.tools import corners, window_point
        shape, _index = self._selected()
        view = getattr(self.canvas, "_author_view", None)
        if shape is None or not view:
            return
        for x, y in corners(shape).values():
            sx, sy = window_point(view, x, y)
            self.canvas.create_rectangle(sx - 4, sy - 4, sx + 4, sy + 4, fill="#ffffff", outline="#000000")

    def _on_canvas_resize(self, event):
        if event.widget is not self.canvas or event.width < 20 or event.height < 20:
            return
        if getattr(self, "_fitted", None) == (event.width, event.height):
            return
        self._fitted = (event.width, event.height)
        self._preview()

    def _on_press(self, evt):
        self._down = (evt.x, evt.y)
        self._drag = None
        if self.tool.get() != "select":
            return
        pages = self.book.get("pages") or []
        page = pages[self.current] if 0 <= self.current < len(pages) else None
        view = getattr(self.canvas, "_author_view", None)
        if page is None or not view or not view.get("scale"):
            return
        from author.tools import handle_at, opposite, page_point, snapshot
        if self._object is not None:
            current, index = self._selected()
            corner = handle_at(view, current, evt.x, evt.y) if current else None
            if corner and current is not None:
                ax, ay = opposite(current, corner)
                self._drag = {"mode": "size", "index": index, "ax": ax, "ay": ay, "snap": snapshot(current)}
                return
        self._select_at(evt.x, evt.y)
        current, index = self._selected()
        if current is None:
            return
        px, py = page_point(view, evt.x, evt.y)
        from author.stage import hit
        if hit(view["shapes"], px, py, self.layer.get()) != index:
            return
        self._drag = {"mode": "move", "index": index, "px": px, "py": py, "snap": snapshot(current)}

    def _on_drag(self, evt):
        drag = self._drag
        if not drag or self.tool.get() != "select":
            return
        view = getattr(self.canvas, "_author_view", None)
        pages = self.book.get("pages") or []
        if not view or not (0 <= self.current < len(pages)):
            return
        from author.tools import move_shape, page_point, resize_shape
        shapes = pages[self.current].get("shapes") or []
        if not (0 <= drag["index"] < len(shapes)):
            return
        shape = shapes[drag["index"]]
        px, py = page_point(view, evt.x, evt.y)
        if drag["mode"] == "move":
            move_shape(shape, drag["snap"], px - drag["px"], py - drag["py"])
        else:
            resize_shape(shape, drag["snap"], drag["ax"], drag["ay"], px, py)
        self._preview()

    def _on_release(self, evt):
        tool = self.tool.get()
        down = getattr(self, "_down", None)
        self._down = None
        if tool == "select":
            if self._drag:
                self._show_properties()
            self._drag = None
            return
        self._drag = None
        if down is None:
            return
        view = getattr(self.canvas, "_author_view", None)
        if not view or not view.get("scale"):
            return
        from author.tools import POINT_TOOLS, PointDraft, new_shape, page_point
        x0, y0 = page_point(view, down[0], down[1])
        x1, y1 = page_point(view, evt.x, evt.y)
        pages = self.book.get("pages") or []
        if not (0 <= self.current < len(pages)):
            return
        page = pages[self.current]
        if tool in POINT_TOOLS:
            if self._draft is None or self._draft.tool != tool:
                self._draft = PointDraft(tool)
            self._draft.add(x1, y1)
            self._preview()
            return
        names = {shape.get("name") or "" for shape in page.get("shapes") or [] if isinstance(shape, dict)}
        shape = new_shape(tool, x0, y0, x1, y1, names, self.layer.get())
        if tool == "picture":
            chosen = filedialog.askopenfilename(
                title="Picture",
                filetypes=[("Pictures", "*.png *.gif *.bmp *.jpg *.jpeg"), ("All", "*.*")],
            )
            if not chosen:
                return
            from author.picture import PictureRefused, picture_fields
            embed = messagebox.askyesno(
                "Picture",
                "Keep the picture inside the book?\n\nNo links the file beside the book instead.",
                parent=self.root,
            )
            try:
                shape.update(picture_fields(chosen, embed=embed, book=self.path))
            except PictureRefused as exc:
                messagebox.showinfo("Picture", str(exc), parent=self.root)
                return
        self._place(page, shape)

    def _place(self, page: dict, shape: dict):
        from author.catalog import place_shape
        placed = place_shape(page, shape)
        self._fill_objects(page)
        for row, item in enumerate(self._rows):
            if item["index"] == placed:
                self.objects.selection_clear(0, "end")
                self.objects.selection_set(row)
                self.objects.see(row)
                self._on_object()
                break
        self._fitted = None
        self._preview()
        if (shape.get("kind") or "") == "text":
            self._edit_text(placed)

    def _on_escape(self, _evt=None):
        from author.tools import after_escape
        self.tool.set(after_escape(self.tool.get(), self._draft))
        self._draft = None
        self._preview()

    def _finish_draft(self, _evt=None):
        """Close the polygon or curve being clicked out. Too few points leaves nothing."""
        draft = self._draft
        if draft is None:
            if _evt is not None and getattr(_evt, "widget", None) is self.canvas and self.tool.get() == "select":
                self._type_into(_evt.x, _evt.y)
            return None
        self._draft = None
        pages = self.book.get("pages") or []
        if not (0 <= self.current < len(pages)):
            return "break"
        page = pages[self.current]
        names = {shape.get("name") or "" for shape in page.get("shapes") or [] if isinstance(shape, dict)}
        shape = draft.finish(names, self.layer.get())
        if shape is None:
            self._preview()
            return "break"
        self._place(page, shape)
        return "break"

    def _type_into(self, wx: float, wy: float):
        """Double-click a field with Select and type into it, on the page. Several lines are fine."""
        view = getattr(self.canvas, "_author_view", None)
        if not view or not view.get("scale"):
            return
        from author.stage import hit
        from author.tools import page_point
        px, py = page_point(view, wx, wy)
        index = hit(view["shapes"], px, py, self.layer.get())
        pages = self.book.get("pages") or []
        if index is None or not (0 <= self.current < len(pages)):
            return
        shape = (pages[self.current].get("shapes") or [])[index]
        if (shape.get("kind") or "") != "text":
            return
        self._edit_text(index)

    def _edit_text(self, index: int):
        view = getattr(self.canvas, "_author_view", None)
        pages = self.book.get("pages") or []
        if not view or not (0 <= self.current < len(pages)):
            return
        page = pages[self.current]
        shape = page["shapes"][index]
        from author.tools import bounds_of, window_point
        x, y, w, h = bounds_of(shape)
        left, top = window_point(view, x, y)
        right, bottom = window_point(view, x + w, y + h)
        box = tk.Text(self.canvas, wrap="word", undo=True, borderwidth=1, relief="solid")
        box.insert("1.0", str(shape.get("text") or ""))
        window = self.canvas.create_window(left, top, anchor="nw", window=box,
                                           width=max(40, right - left), height=max(24, bottom - top))

        def done(_evt=None):
            if not box.winfo_exists():
                return
            from author.catalog import set_object_text
            set_object_text(page, index, box.get("1.0", "end"))
            self.canvas.delete(window)
            box.destroy()
            self._typing = None
            self._preview()

        box.bind("<FocusOut>", done)
        box.bind("<Escape>", done)
        box.focus_set()
        self._typing = box

    def _draw_draft(self):
        draft = self._draft
        view = getattr(self.canvas, "_author_view", None)
        if draft is None or not draft.points or not view:
            return
        from author.tools import window_point
        flat = []
        for x, y in draft.points:
            flat.extend(window_point(view, x, y))
        if len(flat) >= 4:
            self.canvas.create_line(*flat, fill="#071428", dash=(4, 2))
        for x, y in draft.points:
            sx, sy = window_point(view, x, y)
            self.canvas.create_rectangle(sx - 2, sy - 2, sx + 2, sy + 2, outline="#071428")

    def _selected(self):
        pages = self.book.get("pages") or []
        if self._object is None or not self._rows or not (0 <= self.current < len(pages)):
            return None, None
        if not (0 <= self._object < len(self._rows)):
            return None, None
        index = self._rows[self._object]["index"]
        shapes = pages[self.current].get("shapes") or []
        if not (0 <= index < len(shapes)):
            return None, None
        return shapes[index], index

    def _relayer(self):
        pages = self.book.get("pages") or []
        if 0 <= self.current < len(pages):
            self._fill_objects(pages[self.current])
        self._preview()

    def _color(self, which: str):
        shape, _index = self._selected()
        if shape is None:
            return
        from tkinter import colorchooser
        _rgb, color = colorchooser.askcolor(color=shape.get(which) or None, parent=self.root)
        if not color:
            return
        shape[which] = color
        self._preview()

    def _pattern(self):
        shape, _index = self._selected()
        if shape is None:
            return
        from author.patterns import next_pattern
        name = next_pattern(shape)
        if name is None:
            self.status.config(text="Only a rectangle takes a pattern")
            return
        self.status.config(text=f"Pattern: {name}")
        self._preview()

    def _restack(self, direction: str):
        _shape, index = self._selected()
        pages = self.book.get("pages") or []
        if index is None or not (0 <= self.current < len(pages)):
            return
        from author.catalog import restack
        moved = restack(pages[self.current], index, direction)
        self._fill_objects(pages[self.current])
        for row, item in enumerate(self._rows):
            if item["index"] == moved:
                self.objects.selection_set(row)
                self.objects.see(row)
                self._on_object()
                break
        self._preview()

    def _select_at(self, x: float, y: float):
        view = getattr(self.canvas, "_author_view", None)
        if not view or not view.get("scale"):
            return
        from author.stage import hit
        from author.tools import page_point
        px, py = page_point(view, x, y)
        found = hit(view["shapes"], px, py, self.layer.get())
        if found is None:
            return
        for row, item in enumerate(self._rows):
            if item["index"] == found:
                self.objects.selection_clear(0, "end")
                self.objects.selection_set(row)
                self.objects.see(row)
                self._on_object()
                return

    def _wrap(self, mark: str):
        try:
            sel = self.text.get("sel.first", "sel.last")
            self.text.delete("sel.first", "sel.last")
            self.text.insert("insert", f"{mark}{sel}{mark}")
        except tk.TclError:
            pass
        self._preview()

    def _make_list(self):
        try:
            sel = self.text.get("sel.first", "sel.last")
        except tk.TclError:
            return
        lines = ["- " + ln.strip() if ln.strip() and not ln.strip().startswith(("-", "*")) else ln for ln in sel.split("\n")]
        self.text.delete("sel.first", "sel.last")
        self.text.insert("insert", "\n".join(lines))
        self._preview()


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    path = Path(argv[0]) if argv else None
    Editor(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
