"""Browser editor.

  python3 -m foolbookeditor
  python3 -m foolbookeditor path/to/book.fbk
"""

from __future__ import annotations

import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from author.document import blank_book
from foolbookeditor.core import (
    compile_script,
    export_book,
    is_office,
    load as load_book,
    save_book,
    to_book,
    write_office,
)


_OFFICE = {".pdf", ".ppt", ".pptx", ".doc", ".docx", ".odt"}
_OPEN = {".fbk", ".fsk", ".fsc", ".json", ".tbk", ".sbk", ".xml"} | _OFFICE
_EXPORT = {".docx", ".doc", ".pptx", ".ppt", ".odt", ".pdf", ".fbk", ".fsk", ".fsc", ".tbk", ".sbk", ".tbx"}

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Foolbook Editor</title>
<style>
  body { margin: 0; height: 100vh; display: flex; flex-direction: column;
    font-family: "MS Sans Serif", Tahoma, sans-serif; font-size: 11px; background: #c0c0c0; }
  #bar { display: flex; gap: 4px; align-items: center; padding: 4px; border-bottom: 2px solid #808080; }
  button, select { font: inherit; background: #c0c0c0; border: 2px outset #fff; padding: 2px 8px; }
  #status { margin-left: auto; }
  #body { flex: 1; display: flex; min-height: 0; }
  #side { width: 160px; display: flex; flex-direction: column; border-right: 2px solid #808080; }
  #side h1 { margin: 0; padding: 4px 6px; background: #000080; color: #fff; font-size: 12px; }
  #pages { list-style: none; padding: 0; margin: 0; overflow-y: auto; flex: 1; }
  #pages li { padding: 2px 6px; cursor: pointer; border-bottom: 1px solid #dfdfdf; }
  #pages li.active { background: #000080; color: #fff; }
  #work { flex: 1; display: flex; min-width: 0; }
  #form { flex: 1; overflow: auto; padding: 8px; display: flex; flex-direction: column; gap: 6px; }
  #preview { width: 280px; background: #fff; border-left: 2px solid #808080; padding: 8px; overflow: auto; }
  label { display: block; }
  input[type="text"], textarea { font: inherit; width: 100%; box-sizing: border-box; }
  textarea { min-height: 80px; }
  .row { display: flex; gap: 6px; }
  .row label { flex: 1; }
  .jump, .choice { display: flex; gap: 4px; margin-top: 2px; }
  .jump input, .choice input[type="text"] { flex: 1; }
  h2 { font-size: 12px; margin: 8px 0 4px; }
  #preview p { margin: 0 0 8px; }
  #preview button { display: block; margin: 2px 0; }
</style>
</head>
<body>
  <div id="bar">
    <button type="button" id="save">Save</button>
    <label>Open <input id="open" type="file" accept=".fbk,.fsk,.json,.pdf,.ppt,.pptx,.doc,.docx,.odt"></label>
    <label>Export
      <select id="export">
        <option value="">…</option>
        <option value=".fbk">Foolbook .fbk</option>
        <option value=".fsk">System .fsk</option>
        <option value=".fsc">Course .fsc</option>
        <option value=".tbx">TBX folder .tbx</option>
        <option value=".tbk">ToolBook shell .tbk</option>
        <option value=".sbk">System shell .sbk</option>
        <option value=".docx">Word .docx</option>
        <option value=".doc">Word .doc</option>
        <option value=".pptx">PowerPoint .pptx</option>
        <option value=".ppt">PowerPoint .ppt</option>
        <option value=".odt">OpenDocument .odt</option>
        <option value=".pdf">PDF</option>
        <option value="exe">Self-running (not built)</option>
      </select>
    </label>
    <span id="status"></span>
  </div>
  <div id="body">
    <div id="side">
      <h1>Pages</h1>
      <ul id="pages"></ul>
      <div style="padding:4px">
        <button type="button" id="add">Add</button>
        <button type="button" id="del">Delete</button>
        <button type="button" id="up">Up</button>
        <button type="button" id="down">Down</button>
      </div>
    </div>
    <div id="work">
      <div id="form">
        <div class="row">
          <label>Title <input id="title" type="text"></label>
          <label>Subject <input id="subject" type="text"></label>
          <label>Module <input id="module" type="text"></label>
        </div>
        <label>Page id <input id="pid" type="text"></label>
        <label>Text. A blank line starts a paragraph.
          <textarea id="text"></textarea>
        </label>
        <h2>Jumps</h2>
        <div id="jumps"></div>
        <button type="button" id="add-jump">Add jump</button>
        <h2>Script</h2>
        <textarea id="script"></textarea>
        <h2>Quiz</h2>
        <label><input id="quiz-on" type="checkbox"> This page is a quiz</label>
        <div class="row">
          <label>Correct goes to <input id="quiz-next" type="text"></label>
          <label>Wrong goes to <input id="quiz-again" type="text"></label>
        </div>
        <div id="choices"></div>
        <button type="button" id="add-choice">Add choice</button>
      </div>
      <div id="preview"></div>
    </div>
  </div>
<script>
let book = null;
let index = 0;

function freshId() {
  const used = new Set((book.pages || []).map(p => p.id));
  let n = 0;
  while (true) {
    const id = n === 0 ? "P0" : "P" + (n * 100);
    if (!used.has(id)) return id;
    n++;
  }
}

function field(id) { return document.getElementById(id); }

function readJumps() {
  const items = [];
  document.querySelectorAll("#jumps .jump").forEach(row => {
    const label = row.querySelector(".j-label").value.trim();
    const page = row.querySelector(".j-page").value.trim();
    if (label || page) items.push({label: label || page, page: page});
  });
  return items;
}

function readChoices() {
  const choices = [];
  document.querySelectorAll("#choices .choice").forEach(row => {
    const label = row.querySelector(".c-label").value.trim();
    if (!label) return;
    choices.push({label: label, correct: row.querySelector(".c-ok").checked});
  });
  return choices;
}

function readForm() {
  const page = book.pages[index];
  if (!page) return;
  book.title = field("title").value;
  const subject = field("subject").value.trim();
  const module = field("module").value.trim();
  if (subject) book.subject = subject; else delete book.subject;
  if (module) book.module = module; else delete book.module;
  page.id = field("pid").value.trim() || page.id || "P0";
  const raw = field("text").value.trim();
  page.text = raw ? raw.split(/\n\n/).map(b => b.trim()).filter(Boolean) : [];
  page.items = readJumps();
  const script = field("script").value;
  if (script.trim()) page.script = script.endsWith("\n") ? script : script + "\n";
  else delete page.script;
  if (field("quiz-on").checked) {
    const quiz = Object.assign({}, page.quiz || {});
    quiz.choices = readChoices();
    const next = field("quiz-next").value.trim();
    const again = field("quiz-again").value.trim();
    if (next) quiz.next = next; else delete quiz.next;
    if (again) quiz.again = again; else delete quiz.again;
    page.quiz = quiz;
  } else {
    delete page.quiz;
  }
}

function jumpRow(item) {
  const row = document.createElement("div");
  row.className = "jump";
  row.innerHTML = '<input class="j-label" type="text" placeholder="Label"><input class="j-page" type="text" placeholder="Page id"><button type="button">Remove</button>';
  row.querySelector(".j-label").value = item.label || "";
  row.querySelector(".j-page").value = item.page || "";
  row.querySelector("button").onclick = () => { row.remove(); preview(); };
  row.querySelectorAll("input").forEach(el => el.oninput = preview);
  return row;
}

function choiceRow(choice) {
  const row = document.createElement("div");
  row.className = "choice";
  row.innerHTML = '<input class="c-label" type="text" placeholder="Choice"><label><input class="c-ok" type="checkbox"> Correct</label><button type="button">Remove</button>';
  row.querySelector(".c-label").value = choice.label || "";
  row.querySelector(".c-ok").checked = !!choice.correct;
  row.querySelector("button").onclick = () => { row.remove(); preview(); };
  row.querySelector(".c-label").oninput = preview;
  return row;
}

function fillJumps(page) {
  const box = field("jumps");
  box.innerHTML = "";
  (page.items || []).forEach(item => box.appendChild(jumpRow(item)));
}

function fillQuiz(page) {
  const quiz = page.quiz || {};
  field("quiz-on").checked = !!page.quiz;
  field("quiz-next").value = quiz.next || "";
  field("quiz-again").value = quiz.again || "";
  const box = field("choices");
  box.innerHTML = "";
  (quiz.choices || []).forEach(choice => box.appendChild(choiceRow(choice)));
}

function preview() {
  const box = field("preview");
  box.innerHTML = "";
  const page = book.pages[index];
  if (!page) return;
  const raw = field("text").value.trim();
  const blocks = raw ? raw.split(/\n\n/).map(b => b.trim()).filter(Boolean) : (page.text || []);
  blocks.forEach(text => {
    const p = document.createElement("p");
    p.textContent = text;
    box.appendChild(p);
  });
  readJumps().forEach(item => {
    const b = document.createElement("button");
    b.type = "button";
    b.textContent = item.label || item.page || "Go";
    b.onclick = () => {
      readForm();
      const at = book.pages.findIndex(p => (p.id || "").toLowerCase() === (item.page || "").toLowerCase());
      if (at >= 0) show(at, false);
    };
    box.appendChild(b);
  });
  if (field("quiz-on").checked) {
    readChoices().forEach(choice => {
      const b = document.createElement("button");
      b.type = "button";
      b.textContent = choice.label + (choice.correct ? " *" : "");
      box.appendChild(b);
    });
  }
}

function show(i, flush) {
  if (flush && book.pages[index]) readForm();
  index = i;
  const page = book.pages[i];
  field("title").value = book.title || "";
  field("subject").value = book.subject || "";
  field("module").value = book.module || "";
  field("pid").value = page.id || "";
  field("text").value = (page.text || []).join("\n\n");
  field("script").value = page.script || "";
  fillJumps(page);
  fillQuiz(page);
  const ul = field("pages");
  ul.innerHTML = "";
  book.pages.forEach((p, j) => {
    const li = document.createElement("li");
    li.textContent = p.id || "?";
    li.className = j === index ? "active" : "";
    li.onclick = () => show(j, true);
    ul.appendChild(li);
  });
  preview();
}

function status(text) { field("status").textContent = text; }

async function openBook() {
  const r = await fetch("/api/book");
  book = await r.json();
  if (!book.pages || !book.pages.length) book.pages = [{id: "P0", text: ["New slide"], items: []}];
  show(0, false);
  status(book.path || "New book");
}

field("add").onclick = () => {
  readForm();
  book.pages.push({id: freshId(), text: ["New slide"], items: [], widgets: []});
  show(book.pages.length - 1, false);
};
field("del").onclick = () => {
  if (book.pages.length <= 1) return;
  readForm();
  book.pages.splice(index, 1);
  show(Math.min(index, book.pages.length - 1), false);
};
field("up").onclick = () => {
  if (index < 1) return;
  readForm();
  const page = book.pages.splice(index, 1)[0];
  book.pages.splice(index - 1, 0, page);
  show(index - 1, false);
};
field("down").onclick = () => {
  if (index + 1 >= book.pages.length) return;
  readForm();
  const page = book.pages.splice(index, 1)[0];
  book.pages.splice(index + 1, 0, page);
  show(index + 1, false);
};
field("add-jump").onclick = () => {
  field("jumps").appendChild(jumpRow({label: "", page: ""}));
};
field("add-choice").onclick = () => {
  field("choices").appendChild(choiceRow({label: "", correct: false}));
  field("quiz-on").checked = true;
};
["title", "subject", "module", "pid", "text", "script", "quiz-next", "quiz-again"].forEach(id => {
  field(id).oninput = preview;
});

field("save").onclick = async () => {
  readForm();
  const r = await fetch("/api/book", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(book),
  });
  const data = await r.json();
  status(r.ok ? ("Saved " + data.path) : (data.error || "Save failed"));
  if (data.path) book.path = data.path;
};

field("open").onchange = async (ev) => {
  const file = ev.target.files[0];
  ev.target.value = "";
  if (!file) return;
  const r = await fetch("/api/open", {
    method: "POST",
    headers: {"X-Filename": file.name, "Content-Type": "application/octet-stream"},
    body: file,
  });
  const data = await r.json();
  if (!r.ok) { status(data.error || "Open failed"); return; }
  book = data;
  show(0, false);
  status(book.path || file.name);
};

field("export").onchange = async () => {
  const kind = field("export").value;
  field("export").value = "";
  if (!kind) return;
  readForm();
  const r = await fetch("/api/export", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({kind: kind, book: book}),
  });
  const data = await r.json();
  status(r.ok ? ("Exported " + data.path) : (data.error || "Export failed"));
};

openBook();
</script>
</body>
</html>
"""


def _prepare(path: Path) -> dict:
    book = to_book(path) if is_office(path) else load_book(path)
    pages = book.setdefault("pages", [])
    if not pages:
        pages.append(blank_book()["pages"][0])
    return book


def _dest_for(state: dict, suffix: str) -> Path:
    current = state["path"] or (Path.cwd() / "new-book.fbk")
    if current.suffix.lower() in _OFFICE:
        current = current.with_suffix(".fbk")
    return current.with_suffix(suffix)


def serve(path: Path | None, port: int = 6767) -> None:
    state = {"book": blank_book(), "path": None}
    if path is not None:
        state["book"] = _prepare(path)
        state["path"] = Path(path).resolve()

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            pass

        def _send(self, code: int, body: bytes, content_type: str) -> None:
            self.send_response(code)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _json(self, code: int, payload: dict) -> None:
            self._send(code, json.dumps(payload).encode("utf-8"), "application/json")

        def _read_json(self) -> dict | None:
            length = int(self.headers.get("Content-Length") or 0)
            try:
                data = json.loads(self.rfile.read(length).decode("utf-8"))
            except Exception:
                self._json(400, {"error": "not json"})
                return None
            if not isinstance(data, dict):
                self._json(400, {"error": "not a book"})
                return None
            return data

        def do_GET(self):
            u = urlparse(self.path)
            if u.path in ("/", "/index.html"):
                self._send(200, HTML.encode("utf-8"), "text/html; charset=utf-8")
                return
            if u.path == "/api/book":
                payload = dict(state["book"])
                if state["path"]:
                    payload["path"] = str(state["path"])
                self._json(200, payload)
                return
            self.send_response(404)
            self.end_headers()

        def do_POST(self):
            u = urlparse(self.path)
            if u.path == "/api/book":
                self._save()
                return
            if u.path == "/api/open":
                self._open()
                return
            if u.path == "/api/export":
                self._export()
                return
            self.send_response(404)
            self.end_headers()

        def _save(self) -> None:
            data = self._read_json()
            if data is None:
                return
            if not isinstance(data.get("pages"), list) or not data["pages"]:
                self._json(400, {"error": "book needs pages"})
                return
            data.pop("path", None)
            dest = state["path"] or Path.cwd() / "new-book.fbk"
            saved = save_book(dest, data)
            state["book"] = data
            state["path"] = saved.with_suffix(".fbk").resolve()
            self._json(200, {"ok": True, "path": str(state["path"])})

        def _open(self) -> None:
            name = Path(self.headers.get("X-Filename") or "upload.fbk").name
            if Path(name).suffix.lower() not in _OPEN:
                self._json(400, {"error": "open an .fbk, .json, .fsk, or an office file"})
                return
            length = int(self.headers.get("Content-Length") or 0)
            dest = (Path.cwd() / name).resolve()
            dest.write_bytes(self.rfile.read(length))
            try:
                book = _prepare(dest)
            except Exception as exc:
                self._json(400, {"error": str(exc)})
                return
            state["book"] = book
            state["path"] = dest
            payload = dict(book)
            payload["path"] = str(dest)
            self._json(200, payload)

        def _export(self) -> None:
            data = self._read_json()
            if data is None:
                return
            kind = str(data.get("kind") or "")
            book = data.get("book") if isinstance(data.get("book"), dict) else state["book"]
            book = dict(book)
            book.pop("path", None)
            if not isinstance(book.get("pages"), list) or not book["pages"]:
                self._json(400, {"error": "book needs pages"})
                return
            if kind == "exe":
                self._json(501, {"error": "Self-running export is scaffolded and not implemented."})
                return
            try:
                if kind == "exe":
                    self._json(501, {"error": "Self-running export is scaffolded and not implemented."})
                    return
                if kind not in _EXPORT:
                    self._json(400, {"error": "unknown export"})
                    return
                dest = _dest_for(state, kind)
                export_book(dest, book, compile_script)
            except Exception as exc:
                self._json(400, {"error": str(exc)})
                return
            self._json(200, {"ok": True, "path": str(dest)})

    try:
        server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    except OSError as exc:
        if getattr(exc, "errno", None) in (98, 48):
            print("Editor already running, cannot start a new instance")
            raise SystemExit(1)
        raise
    url = f"http://127.0.0.1:{port}/"
    name = state["path"].name if state["path"] else "New book"
    print(f"Foolbook Editor  {name}")
    print(f"Open {url}")
    _open_browser(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print()
        server.shutdown()


def _open_browser(url: str) -> None:
    import shutil
    import subprocess
    import webbrowser
    for cmd in ("xdg-open", "gio"):
        if shutil.which(cmd):
            try:
                args = [cmd, url] if cmd == "xdg-open" else [cmd, "open", url]
                subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return
            except Exception:
                continue
    try:
        webbrowser.open(url, new=2)
    except Exception:
        print(f"Browser did not open. Go to {url}")


def main(argv: list[str] | None = None) -> int:
    argv = list(argv if argv is not None else sys.argv[1:])
    port = 6767
    if "--port" in argv:
        i = argv.index("--port")
        if i + 1 >= len(argv):
            print("--port needs a number")
            return 2
        try:
            port = int(argv[i + 1])
        except ValueError:
            print(f"--port needs a number, got {argv[i + 1]}")
            return 2
        del argv[i:i + 2]
    path = None
    if argv:
        path = Path(argv[0].replace("\\", "/")).expanduser()
        if path.suffix.lower() not in _OPEN:
            print("The editor opens .fbk, .fsk, .json, .pdf, .ppt, .pptx, .doc, .docx, and .odt.")
            return 2
        if not path.exists():
            print(f"not found: {path}")
            return 1
    serve(path, port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
