# Changelog

## 2026-10-31

- Pattern steps the selected rectangle through 8 by 8 fills (checks, horizontal, vertical, diagonal, dots) and back to none. It is stored as `tile`. A `.tbk` export keeps the plain fill colour.
## Unreleased — 2026-10-31

- Author starts on Select, and Escape goes back to Select from any tool.
- A new rectangle is filled `#f7f4ee` with a `#071428` outline. It had no fill and a black outline.
- Rounded places a rounded rectangle (`kind: roundrect`, `radius: 8`). Foolbook draws it from Foolbook#23 on.
- Polygon is clicked out: each click is a point, double-click or Enter closes it, and Escape drops it with nothing left on the page. It used to be a rectangle you dragged.
- Curve is clicked out like Polygon and stays open. It stores `kind: curve` and its points. Foolbook draws it from Foolbook#26 on.
- A new arc stores `start: 0` and `sweep: 180`, the top half of its bounds, instead of two endpoints. Foolbook draws it from Foolbook#28 on. An arc read from a `.tbk` keeps its endpoints.
- Pie places a filled slice (`kind: pie`, `start: 0`, `sweep: 90`). Foolbook draws it from Foolbook#29 on.
- Chord places a filled chord (`kind: chord`, `start: 0`, `sweep: 180`). Foolbook draws it from Foolbook#30 on.
- Type into a field on the page. A new Field opens for typing, and a double-click with Select reopens one. Several lines are kept as lines. Escape or a click away keeps them.
- Picture embeds the file as base64 PNG by default, or links it beside the book as `src`. A file over 20 MB, or one that is not a picture, is refused with a sentence instead of a crash.
- Hotspot places a `kind: hotspot` with no fill. Author draws its outline so it can be found. Foolbook does not draw it, from Foolbook#31 on, and follows its item.
- A Properties pane sets the selected object's name, text, fill, outline, and line width (`stroke`, default 1). Bad input keeps the old value. Foolbook draws `stroke` from Foolbook#25 on.
- The Properties pane sets font face, size, bold, italic, underline, and alignment (left, center, right). Foolbook reads underline and named alignment from Foolbook#32 and #35 on.
- A colour well of eight plain colours sits under the Properties pane. A click sets the fill and a right-click sets the outline. Typed `#rrggbb` still works.
- No fill, or an empty Fill box, stores `fill: ""` and the object is drawn with nothing inside. A button with no fill saves and draws that way.
- A Visible check box in the Properties pane. An object with `visible: false` is drawn ghosted on the stage, its colours washed toward white, and Foolbook still skips it.
- Left, Top, Width, and Height in the Properties pane move and size the object by number, points included. Bad input keeps the old value.
- Points in the Properties pane lists a polygon, line, or curve as one `x, y` pair per line. Editing it reshapes the object. A line that is not two numbers, or too few points, keeps the old outline.
- The script pane is monospace, and Tab puts in two spaces. With no object chosen it edits the page script, which is stored as typed. A page that came with handlers keeps them until its script is actually edited.
- Undock under the Properties pane moves that same pane into its own window. Dock, or closing the window, puts it back. There is still one property system.
## 2026-10-31

- The page form has a Background list. It names the shared backgrounds in the book (pages with `"background": true`) and `(none)`. Picking one sets the page's `uses`, and the stage draws that background under the page. `(none)` clears it. The model refuses a name that is not a background. Test: `author/test_backgrounds.py`.
- The README lists the script lines the reader runs: `go to page`, `go to page of book`, `send next`, `send previous`. `author/test_script_subset.py` runs every line in that table through Foolbook.
- `instructor-map.md` lists the fourteen Instructor jobs, where each one stands, and the work order items that cover it. `author/test_instructor_map.py` keeps every job listed once with a status.
## Unreleased — 2026-10-31

- Add puts the new page right after the current page, not at the end. Ctrl+M does the same.
- With no book named, Author opens a start window: New book, Open book, and up to five recent books that are still on disk.
- New book asks for a page size, 640 by 480 unless changed, and a background colour, then opens the stage. The colour is a page-sized `paper` rect on the background layer, which the reader already paints first.
- Template starts a new book from a copy of `blank`, `title-and-button`, or `question-and-four-choices` in `templates/`. `python3 -m author.templates` writes those three files. Save asks for a new name, so a template is never written over.
- Catalog lists the `.fbk` and `.fsk` books in a folder you pick: title, page count, and file name. A book that will not open is listed and says so. Double-click opens a book.
- The README says how to install the editor: a venv, `pip install -e .`, and `python3 -m foolbookeditor`.
- Foolbook is pinned to commit 031e8d8, not to a floating main. A pull request that needs a newer reader bumps the pin and names the function.
- `python3 -m foolbookeditor --selftest` builds a book in memory, saves it, loads it, and checks the page id, one shape, and one script. No window.
- The self test also opens the saved book and Using Foolbook through the reader, so an editor change that breaks the reader fails it.
- A book the editor opens and saves again, uncompressed, is the same bytes. The editor drops the envelope keys the reader stamps (`format`, `format_version`, `fbk`, `foolbook`) before a save, so they come back in the reader's order. `tests/fixtures/tiny.fbk` is the golden file.
- The compressed form has a golden file too, `tests/fixtures/tiny_z.fbk`: flags byte 1, then a zlib stream the reader decompresses. Opened and saved compressed, it is the same bytes.
- Duplicate copies the current page, with its shapes and scripts, under a new id. The copy is the next page. Ctrl+Shift+D does the same.
- Delete asks before it removes a page, and names the page and how many objects go with it. Ctrl+Shift+Delete does the same.
- Up and Down beside the page list move the current page one place earlier or later. Ctrl+Shift+Up and Ctrl+Shift+Down do the same.

## 0.4.0 — 2026-10-24

- Page and Background are separate. The list and a new object follow the one that is selected. The picture still shows both, background first.
- Line, Ellipse, Polygon, Arc, and Picture place a shape Foolbook draws. Fill and Line set the colour of the selected object. Front and Back move it within its own layer.

## 0.3.5 — 2026-10-24

- Select drags the object under the pointer. The four squares on a selected object pull its corners, and the opposite corner stays put.

## 0.3.4 — 2026-10-24

- The Author window opens large enough for three panes. The picture is the middle one. The page list and the object list cannot push it off the screen.

## 0.3.3 — 2026-10-24

- The desktop window is what opens. `--browser` is the other one.
- Button, Field, and Rectangle place an object where you drag on the picture. Select still picks the object under the pointer.

## 0.3.2 — 2026-10-24

- The browser editor, which is what starts with no `--desktop` flag, now has the page in the middle. Pages stay on the left. Objects and the object script stay on the right. A `.tbk` is read through Foolbook, so the picture is the book's objects.

## 0.3.1 — 2026-10-24

- The middle of Author is the page Foolbook draws. Pages stay on the left and the object script stays on the right. A click on the picture selects the object. Opening a `.tbk` reads it through Foolbook.

## 0.3.0 — 2026-10-24

- Author lists the objects on the selected page, in book order. A field Reader hides is still in the list. The selected object's script can be edited. Save still writes an `.fbk`.

## 0.2.3 — 2026-10-22

- The conversion note that said bitmaps are missing is gone. A button picture is in the `.fbk` once Foolbook 1.0.5r15 has read it.

## 0.2.2 — 2026-10-22

- No loader of its own. A `.tbk` converted after Foolbook 1.0.5r13 keeps the object store: page order, field text, polygon outlines, the background colour, and button bitmaps.
