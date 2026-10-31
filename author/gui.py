"""Foolbook author.

Slide editor. Produces .fbk (and .fsk). Export .tbk writes a shell with compiled OpenScript.

  python3 -m author.gui
  python3 -m author.gui path/to/book.fbk
"""

from __future__ import annotations

import sys
from pathlib import Path

from .formats import save_book, load as load_book

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
        self.tool = tk.StringVar(value="select")
        self._build()
        if path and path.exists():
            self._load(path)
        else:
            self._new()
        self.root.mainloop()

    def _build(self):
        # toolbar
        bar = ttk.Frame(self.root, padding=4)
        bar.pack(fill="x")
        ttk.Button(bar, text="New", command=self._new).pack(side="left")
        ttk.Button(bar, text="Open", command=self._open).pack(side="left", padx=2)
        ttk.Button(bar, text="Save", command=self._save).pack(side="left")
        ttk.Button(bar, text="Save as", command=self._save_as).pack(side="left", padx=2)
        ttk.Button(bar, text="Export", command=self._export).pack(side="left", padx=2)
        ttk.Button(bar, text="Export executable", command=self._export_executable).pack(side="left", padx=2)
        ttk.Separator(bar, orient="vertical").pack(side="left", fill="y", padx=6)
        for name, label in (("select", "Select"), ("button", "Button"), ("text", "Field"), ("box", "Rectangle")):
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
            ("arc", "Arc"),
            ("picture", "Picture"),
        ):
            ttk.Radiobutton(tools, text=label, value=name, variable=self.tool).pack(side="left", padx=2)
        ttk.Separator(tools, orient="vertical").pack(side="left", fill="y", padx=6)
        ttk.Radiobutton(tools, text="Page", value="page", variable=self.layer, command=self._relayer).pack(side="left")
        ttk.Radiobutton(tools, text="Background", value="background", variable=self.layer, command=self._relayer).pack(side="left", padx=2)
        ttk.Separator(tools, orient="vertical").pack(side="left", fill="y", padx=6)
        ttk.Button(tools, text="Fill", command=lambda: self._color("fill")).pack(side="left")
        ttk.Button(tools, text="Line", command=lambda: self._color("outline")).pack(side="left", padx=2)
        self.grid = tk.BooleanVar(value=False)
        ttk.Checkbutton(tools, text="Grid 8", variable=self.grid, command=self._preview).pack(side="left", padx=(8, 0))
        aligner = ttk.Menubutton(tools, text="Align")
        menu = tk.Menu(aligner, tearoff=False)
        menu.add_command(label="To the first selected object", state="disabled")
        from author.geometry import ALIGN
        for how in ALIGN:
            menu.add_command(label=how.capitalize(), command=lambda h=how: self._align(h))
        menu.add_separator()
        menu.add_command(label="Distribute across (3 or more)", command=lambda: self._distribute("horizontal"))
        menu.add_command(label="Distribute down (3 or more)", command=lambda: self._distribute("vertical"))
        aligner["menu"] = menu
        aligner.pack(side="left", padx=(8, 0))
        locker = ttk.Menubutton(tools, text="Lock")
        lock_menu = tk.Menu(locker, tearoff=False)
        lock_menu.add_command(label="Lock selected", command=lambda: self._lock(True))
        lock_menu.add_command(label="Unlock selected (pick it in the object list)", command=lambda: self._lock(False))
        lock_menu.add_command(label="Unlock all on this page", command=self._unlock_all)
        locker["menu"] = lock_menu
        locker.pack(side="left", padx=(8, 0))
        ttk.Button(tools, text="Group", command=self._group).pack(side="left", padx=(8, 0))
        ttk.Button(tools, text="Ungroup", command=self._ungroup).pack(side="left", padx=2)
        ttk.Button(tools, text="Front", command=lambda: self._restack("front")).pack(side="left", padx=(8, 2))
        ttk.Button(tools, text="Forward", command=lambda: self._restack("forward")).pack(side="left")
        ttk.Button(tools, text="Backward", command=lambda: self._restack("backward")).pack(side="left", padx=2)
        ttk.Button(tools, text="Back", command=lambda: self._restack("back")).pack(side="left")

        body = ttk.PanedWindow(self.root, orient="horizontal")
        body.pack(fill="both", expand=True, padx=4, pady=4)
        self.body = body

        # page list
        left = ttk.Frame(body, width=160)
        body.add(left, weight=0)
        ttk.Label(left, text="Pages").pack(anchor="w")
        self.pages = tk.Listbox(left, exportselection=False, width=18, height=8)
        self.pages.pack(fill="both", expand=True)
        self.pages.bind("<<ListboxSelect>>", self._on_select)
        # One small drawing per page. A click on one shows that page.
        strip = ttk.Frame(left)
        strip.pack(fill="both", expand=True, pady=(4, 0))
        self.thumbs = tk.Canvas(strip, width=120, height=200, bg="#e8e8e8", highlightthickness=0)
        thumb_bar = ttk.Scrollbar(strip, orient="vertical", command=self.thumbs.yview)
        self.thumbs.configure(yscrollcommand=thumb_bar.set)
        thumb_bar.pack(side="right", fill="y")
        self.thumbs.pack(side="left", fill="both", expand=True)
        self.thumbs.bind("<ButtonRelease-1>", self._on_thumb)
        row = ttk.Frame(left)
        row.pack(fill="x", pady=4)
        ttk.Button(row, text="Add", command=self._add_page).pack(side="left")
        from author.commands import SHORTCUTS
        self.root.bind(SHORTCUTS["add_page"][1], lambda _e: self._add_page())
        self.root.bind(SHORTCUTS["duplicate_page"][1], lambda _e: self._duplicate_page())
        self.root.bind(SHORTCUTS["delete_page"][1], lambda _e: self._del_page())
        self.root.bind(SHORTCUTS["go_to_page"][1], lambda _e: (self.goto.focus_set(), self.goto.select_range(0, "end")))
        for key in ("Left", "Right", "Up", "Down"):
            self.root.bind(f"<{key}>", lambda e, k=key: self._nudge(e, k, False))
            self.root.bind(f"<Shift-{key}>", lambda e, k=key: self._nudge(e, k, True))
        for command in ("first_page", "previous_page", "next_page", "last_page"):
            self.root.bind(SHORTCUTS[command][1], lambda _e, c=command: self._browse(c))
        self.root.bind(SHORTCUTS["page_up"][1], lambda _e: self._reorder("page_up"))
        self.root.bind(SHORTCUTS["page_down"][1], lambda _e: self._reorder("page_down"))
        ttk.Button(row, text="Duplicate", command=self._duplicate_page).pack(side="left", padx=4)
        ttk.Button(row, text="Delete", command=self._del_page).pack(side="left")
        order = ttk.Frame(left)
        order.pack(fill="x")
        browse = ttk.Frame(left)
        browse.pack(fill="x", pady=(4, 0))
        for command, label in (("first_page", "|<"), ("previous_page", "<"), ("next_page", ">"), ("last_page", ">|")):
            ttk.Button(browse, text=label, width=3, command=lambda c=command: self._browse(c)).pack(side="left")
        goto = ttk.Frame(left)
        goto.pack(fill="x", pady=(4, 0))
        ttk.Label(goto, text="Go to").pack(side="left")
        self.goto = ttk.Entry(goto, width=10)
        self.goto.pack(side="left", padx=4, fill="x", expand=True)
        self.goto.bind("<Return>", lambda _e: self._go_to())
        ttk.Button(order, text="Up", command=lambda: self._reorder("page_up")).pack(side="left")
        ttk.Button(order, text="Down", command=lambda: self._reorder("page_down")).pack(side="left", padx=4)

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
        self.objects = tk.Listbox(objects, exportselection=False, width=28, selectmode="extended")
        self.objects.pack(fill="both", expand=True)
        self.objects.bind("<<ListboxSelect>>", self._on_object)
        self.object_meta = ttk.Label(objects, text="", wraplength=200)
        self.object_meta.pack(anchor="w", pady=4)
        ttk.Label(objects, text="Object script").pack(anchor="w")
        self.oscript = tk.Text(objects, height=12, wrap="word")
        self.oscript.pack(fill="both", expand=True)
        ttk.Button(objects, text="Apply script", command=self._apply_script).pack(anchor="e", pady=4)
        self._rows: list[dict] = []
        self._object = None
        # Shape indices that are selected, in the order they were chosen.
        self._chosen: list[int] = []
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
        ttk.Label(form, text="Size").grid(row=0, column=6, sticky="w")
        self.page_w = ttk.Entry(form, width=5)
        self.page_w.grid(row=0, column=7, sticky="w", padx=(4, 0))
        ttk.Label(form, text="x").grid(row=0, column=8)
        self.page_h = ttk.Entry(form, width=5)
        self.page_h.grid(row=0, column=9, sticky="w")

        ttk.Label(center, text="Text  (blank line = new paragraph; lines starting with - or * are a list)").pack(anchor="w", pady=(6, 0))
        self.text = tk.Text(center, height=4, wrap="word")
        self.text.pack(fill="x")
        self.text.bind("<KeyRelease>", lambda e: self._preview())

        ttk.Button(center, text="Apply", command=self._apply).pack(anchor="e", pady=4)
        self.root.after_idle(self._split)

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

    def _new(self):
        self.book = {
            "id": "new",
            "title": "New book",
            "pages": [{"id": "P0", "text": ["New slide"], "items": [], "widgets": []}],
        }
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
        for p in self.book.get("pages") or []:
            self.pages.insert("end", p.get("id") or "?")
        self._draw_thumbs()
        if self.book.get("pages"):
            self.pages.selection_set(self.current)
            self._show(self.current)

    _THUMB_STEP = 96

    def _draw_thumbs(self):
        from author.thumbs import draw, miniature
        self.thumbs.delete("all")
        pages = self.book.get("pages") or []
        for index, page in enumerate(pages):
            top = 4 + index * self._THUMB_STEP
            if index == self.current:
                self.thumbs.create_rectangle(2, top - 2, 102, top + 90, fill="#a8c4e0", outline="")
            draw(self.thumbs, miniature(page), 4, top, f"thumb{index}")
            self.thumbs.create_text(4, top + 74, text=page.get("id") or "?", anchor="nw", font=("TkDefaultFont", 8))
        self.thumbs.configure(scrollregion=(0, 0, 110, 8 + len(pages) * self._THUMB_STEP))

    def _on_thumb(self, evt):
        index = int(self.thumbs.canvasy(evt.y) - 4) // self._THUMB_STEP
        if not (0 <= index < len(self.book.get("pages") or [])) or index == self.current:
            return
        self.pages.selection_clear(0, "end")
        self.pages.selection_set(index)
        self._on_select()

    def _on_select(self, _evt=None):
        sel = self.pages.curselection()
        if not sel:
            return
        self._apply()
        self._apply_script()
        self.current = sel[0]
        self._show(self.current)
        self._draw_thumbs()

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
        from author.stage import page_size
        width, height = page_size(p)
        self.page_w.delete(0, "end")
        self.page_w.insert(0, str(width))
        self.page_h.delete(0, "end")
        self.page_h.insert(0, str(height))
        self.text.delete("1.0", "end")
        self.text.insert("1.0", "\n\n".join(p.get("text") or []))
        self._fill_objects(p)
        self._preview()

    def _fill_objects(self, page: dict):
        from author.catalog import objects_of, page_script
        self._rows = objects_of(page, self.layer.get())
        self._object = None
        self._chosen = []
        self.objects.delete(0, "end")
        for row in self._rows:
            name = row["name"] or "(unnamed)"
            mark = (" hidden" if row["hidden"] else "") + (" locked" if row.get("locked") else "")
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
        # Keep the order things were chosen in. The first one is the reference.
        picked = [self._rows[at]["index"] for at in sel]
        self._chosen = [i for i in self._chosen if i in picked] + [i for i in picked if i not in self._chosen]
        self._object = next(at for at, row in enumerate(self._rows) if row["index"] == self._chosen[0])
        row = self._rows[self._object]
        left, top, right, bottom = row["bounds"]
        self.object_meta.config(text=f"{row['kind']}  {row['name'] or '(unnamed)'}  {left}, {top}, {right}, {bottom}")
        self.oscript.delete("1.0", "end")
        self.oscript.insert("1.0", row["script"])

    def _apply_script(self):
        if self._object is None:
            return
        pages = self.book.get("pages") or []
        if not (0 <= self.current < len(pages)):
            return
        from author.catalog import set_object_script
        set_object_script(pages[self.current], self._rows[self._object]["index"], self.oscript.get("1.0", "end"))
        self._rows[self._object]["script"] = pages[self.current]["shapes"][self._rows[self._object]["index"]].get("script") or ""

    def _apply(self):
        pages = self.book.get("pages") or []
        if not (0 <= self.current < len(pages)):
            return
        p = pages[self.current]
        from author.document import set_id, set_nav, set_size, set_text, text_from_editor
        from author.stage import page_size
        if (self.page_w.get().strip(), self.page_h.get().strip()) != tuple(str(n) for n in page_size(p)):
            if not set_size(p, self.page_w.get().strip(), self.page_h.get().strip()):
                width, height = page_size(p)
                self.page_w.delete(0, "end")
                self.page_w.insert(0, str(width))
                self.page_h.delete(0, "end")
                self.page_h.insert(0, str(height))
                self.status.config(text="Size is two whole numbers above zero")
        set_id(p, self.pid.get())
        set_text(p, text_from_editor(self.text.get("1.0", "end")))
        set_nav(p, self.next.get(), self.back.get())
        self.pages.delete(self.current)
        self.pages.insert(self.current, p["id"])
        self.pages.selection_set(self.current)
        self._preview()
        self._draw_thumbs()

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

    def _browse(self, command: str):
        from author import commands
        index = getattr(commands, command)(self.book, self.current)
        if index == self.current:
            return
        self.pages.selection_clear(0, "end")
        self.pages.selection_set(index)
        self.pages.see(index)
        self._on_select()

    def _go_to(self):
        from author.commands import go_to_page
        index, note = go_to_page(self.book, self.current, self.goto.get())
        if note:
            self.status.config(text=note)
        if index == self.current:
            return
        self.pages.selection_clear(0, "end")
        self.pages.selection_set(index)
        self.pages.see(index)
        self._on_select()

    def _reorder(self, command: str):
        self._apply()
        self._apply_script()
        from author import commands
        self.current = getattr(commands, command)(self.book, self.current)
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
        page = None
        pages = self.book.get("pages") or []
        if 0 <= self.current < len(pages):
            page = pages[self.current]
        from author.stage import paint
        paint(self.canvas, page or {})
        if self.grid.get():
            self._draw_grid(page or {})
        self._draw_handles()

    def _draw_grid(self, page: dict):
        """A dot at every grid crossing on the page, under the handles."""
        view = getattr(self.canvas, "_author_view", None)
        if not view or not view.get("scale"):
            return
        from author.geometry import GRID
        from author.stage import page_size
        from author.tools import window_point
        width, height = page_size(page)
        step = GRID
        while step * view["scale"] < 6:
            step *= 2
        for gx in range(0, width + 1, step):
            for gy in range(0, height + 1, step):
                sx, sy = window_point(view, gx, gy)
                self.canvas.create_line(sx, sy, sx + 1, sy, fill="#9a9a9a", tags=("grid",))

    def _draw_handles(self):
        if self.tool.get() != "select" or self._object is None:
            return
        pages = self.book.get("pages") or []
        if not (0 <= self.current < len(pages)):
            return
        from author.geometry import bounds, handles
        from author.tools import window_point
        shape, _index = self._selected()
        view = getattr(self.canvas, "_author_view", None)
        if shape is None or not view:
            return
        shapes = pages[self.current].get("shapes") or []
        for index in self._chosen:
            if 0 <= index < len(shapes) and len(self._chosen) > 1:
                x, y, w, h = bounds(shapes[index])
                sx0, sy0 = window_point(view, x, y)
                sx1, sy1 = window_point(view, x + w, y + h)
                self.canvas.create_rectangle(sx0 - 2, sy0 - 2, sx1 + 2, sy1 + 2, outline="#3070c0", dash=(3, 2))
        for x, y in handles(shape).values():
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
        import copy
        from author.geometry import handles
        from author.tools import page_point, snapshot, window_point
        if self._object is not None:
            current, index = self._selected()
            grabbed = None
            for name, (hx, hy) in (handles(current).items() if current else ()):
                sx, sy = window_point(view, hx, hy)
                if abs(sx - evt.x) <= 6 and abs(sy - evt.y) <= 6:
                    grabbed = name
                    break
            if grabbed and current is not None:
                self._drag = {"mode": "size", "index": index, "handle": grabbed, "before": copy.deepcopy(current)}
                return
        px, py = page_point(view, evt.x, evt.y)
        from author.stage import hit
        self.canvas.focus_set()
        under = hit(view["shapes"], px, py, self.layer.get())
        if under is not None and under in self._chosen and len(self._chosen) > 1:
            # Pressing on one of several selected objects drags them all.
            shapes = page.get("shapes") or []
            snaps = {i: snapshot(shapes[i]) for i in self._chosen if 0 <= i < len(shapes)}
            self._drag = {"mode": "move-all", "px": px, "py": py, "snaps": snaps}
            return
        if under is None:
            # Empty page under the pointer: drag a box to choose.
            self._choose([])
            self._drag = {"mode": "marquee", "wx": evt.x, "wy": evt.y}
            return
        self._select_at(evt.x, evt.y)
        current, index = self._selected()
        if current is None:
            return
        if hit(view["shapes"], px, py, self.layer.get()) != index:
            return
        self.canvas.focus_set()
        self._drag = {"mode": "move", "index": index, "px": px, "py": py, "snap": snapshot(current)}

    def _on_drag(self, evt):
        drag = self._drag
        if not drag or self.tool.get() != "select":
            return
        view = getattr(self.canvas, "_author_view", None)
        pages = self.book.get("pages") or []
        if not view or not (0 <= self.current < len(pages)):
            return
        if drag["mode"] == "marquee":
            self.canvas.delete("marquee")
            self.canvas.create_rectangle(drag["wx"], drag["wy"], evt.x, evt.y, outline="#3070c0", dash=(4, 2), tags=("marquee",))
            return
        from author.tools import move_shape, page_point
        shapes = pages[self.current].get("shapes") or []
        if drag["mode"] == "move-all":
            px, py = page_point(view, evt.x, evt.y)
            for index, snap in drag["snaps"].items():
                move_shape(shapes[index], snap, px - drag["px"], py - drag["py"])
            self._preview()
            return
        if not (0 <= drag["index"] < len(shapes)):
            return
        shape = shapes[drag["index"]]
        px, py = page_point(view, evt.x, evt.y)
        if drag["mode"] == "move":
            move_shape(shape, drag["snap"], px - drag["px"], py - drag["py"])
        else:
            from author.geometry import resize
            resize(shape, drag["before"], drag["handle"], px, py)
        self._preview()

    def _on_release(self, evt):
        tool = self.tool.get()
        down = getattr(self, "_down", None)
        self._down = None
        if tool == "select":
            drag, self._drag = self._drag, None
            if drag and drag["mode"] == "marquee":
                self.canvas.delete("marquee")
                view = getattr(self.canvas, "_author_view", None)
                if view and view.get("scale"):
                    from author.geometry import marquee
                    from author.tools import page_point
                    x0, y0 = page_point(view, drag["wx"], drag["wy"])
                    x1, y1 = page_point(view, evt.x, evt.y)
                    self._choose(marquee(view["shapes"], x0, y0, x1, y1, self.layer.get()))
            elif drag:
                if self.grid.get():
                    self._snap_drag(drag, evt)
                self._draw_thumbs()
            return
        self._drag = None
        if down is None:
            return
        view = getattr(self.canvas, "_author_view", None)
        if not view or not view.get("scale"):
            return
        from author.catalog import place_shape
        from author.tools import new_shape, page_point
        x0, y0 = page_point(view, down[0], down[1])
        x1, y1 = page_point(view, evt.x, evt.y)
        if self.grid.get():
            from author.geometry import snap_point
            x0, y0 = snap_point(x0, y0)
            x1, y1 = snap_point(x1, y1)
        if evt.state & 0x0001:
            # Shift: a square box, or a line at 0, 45, or 90 degrees.
            from author.geometry import constrain_box, constrain_line
            x1, y1 = (constrain_line if tool == "line" else constrain_box)(x0, y0, x1, y1)
        pages = self.book.get("pages") or []
        if not (0 <= self.current < len(pages)):
            return
        page = pages[self.current]
        names = {shape.get("name") or "" for shape in page.get("shapes") or [] if isinstance(shape, dict)}
        shape = new_shape(tool, x0, y0, x1, y1, names, self.layer.get())
        if tool == "picture":
            chosen = filedialog.askopenfilename(
                title="Picture",
                filetypes=[("Pictures", "*.png *.gif *.bmp *.jpg *.jpeg"), ("All", "*.*")],
            )
            if not chosen:
                return
            import base64
            shape["data"] = base64.b64encode(Path(chosen).read_bytes()).decode("ascii")
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
        self._draw_thumbs()

    def _nudge(self, event, key: str, shift: bool):
        """Arrow keys move the selection, unless a text box has the keys."""
        if isinstance(event.widget, (tk.Entry, ttk.Entry, tk.Text, tk.Listbox)):
            return None
        pages = self.book.get("pages") or []
        if not self._chosen or not (0 <= self.current < len(pages)):
            return None
        from author.geometry import arrow_step, nudge
        dx, dy = arrow_step(key, shift)
        nudge(pages[self.current].get("shapes") or [], self._chosen, dx, dy)
        self._preview()
        self._draw_thumbs()
        return "break"

    def _align(self, how: str):
        pages = self.book.get("pages") or []
        if len(self._chosen) < 2 or not (0 <= self.current < len(pages)):
            self.status.config(text="Align needs two or more selected objects")
            return
        from author.geometry import align
        align(pages[self.current].get("shapes") or [], self._chosen, how)
        self._preview()
        self._draw_thumbs()

    def _lock(self, locked: bool):
        pages = self.book.get("pages") or []
        if not self._chosen or not (0 <= self.current < len(pages)):
            self.status.config(text="Select an object in the object list first")
            return
        from author.geometry import set_locked
        page = pages[self.current]
        chosen = list(self._chosen)
        set_locked(page.get("shapes") or [], chosen, locked)
        self._fill_objects(page)
        self._choose([] if locked else chosen)
        self.status.config(text="Locked" if locked else "Unlocked")

    def _unlock_all(self):
        pages = self.book.get("pages") or []
        if not (0 <= self.current < len(pages)):
            return
        from author.geometry import set_locked
        page = pages[self.current]
        shapes = page.get("shapes") or []
        set_locked(shapes, list(range(len(shapes))), False)
        self._fill_objects(page)
        self._preview()
        self.status.config(text="Nothing on this page is locked")

    def _group(self):
        pages = self.book.get("pages") or []
        if len(self._chosen) < 2 or not (0 <= self.current < len(pages)):
            self.status.config(text="Group needs two or more selected objects")
            return
        self._apply_script()
        from author.geometry import group
        page = pages[self.current]
        at = group(page.get("shapes") or [], self._chosen)
        if at is None:
            self.status.config(text="Group needs objects on one layer")
            return
        self._fill_objects(page)
        self._choose([at])
        self._draw_thumbs()

    def _ungroup(self):
        shape, index = self._selected()
        pages = self.book.get("pages") or []
        if shape is None or (shape.get("kind") or "") != "group":
            self.status.config(text="Ungroup needs a selected group")
            return
        self._apply_script()
        from author.geometry import ungroup
        page = pages[self.current]
        back = ungroup(page.get("shapes") or [], index)
        self._fill_objects(page)
        self._choose(back)
        self._draw_thumbs()

    def _distribute(self, axis: str):
        pages = self.book.get("pages") or []
        if len(self._chosen) < 3 or not (0 <= self.current < len(pages)):
            self.status.config(text="Distribute needs three or more selected objects")
            return
        from author.geometry import distribute
        distribute(pages[self.current].get("shapes") or [], self._chosen, axis)
        self._preview()
        self._draw_thumbs()

    def _choose(self, indices: list[int]):
        """Select these shapes in the object list. The first one is the one edited."""
        self.objects.selection_clear(0, "end")
        self._chosen = list(indices)
        rows = [row for row, item in enumerate(self._rows) if item["index"] in indices]
        for row in rows:
            self.objects.selection_set(row)
        if rows:
            self.objects.see(rows[0])
            self._on_object()
            self._preview()
        else:
            self._apply_script()
            self._object = None
            self._chosen = []
            self._preview()

    def _snap_drag(self, drag: dict, evt):
        """The grid applies once, when the button comes up, so a drag does not jitter."""
        pages = self.book.get("pages") or []
        view = getattr(self.canvas, "_author_view", None)
        if not view or not (0 <= self.current < len(pages)):
            return
        shapes = pages[self.current].get("shapes") or []
        from author.geometry import resize, snap_move, snap_point
        from author.tools import page_point
        if drag["mode"] == "move-all":
            snap_move(shapes, list(drag["snaps"]))
        elif drag["mode"] == "move":
            snap_move(shapes, [drag["index"]])
        elif drag["mode"] == "size" and 0 <= drag["index"] < len(shapes):
            px, py = snap_point(*page_point(view, evt.x, evt.y))
            resize(shapes[drag["index"]], drag["before"], drag["handle"], px, py)
        self._preview()

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
