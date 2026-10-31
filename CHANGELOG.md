# Changelog

## 2026-10-31

- Hotword asks for a word in the selected field and a page, and stores the word's range and the jump in `hotwords`. The range is counted in the text as the reader draws it. Needs Foolbook#57 and #58.
- Naming a system book writes OpenScript the reader runs: the book script's `enterBook` gets `if "shared.fsk" is not in sysBooks` / `push "shared.fsk" onto sysBooks` / `end if`, as a ToolBook course does. Before, only a `system` key was stored, and Foolbook does not read it, so the system book's handlers never ran. A new name replaces the push, and clearing it takes the push out and leaves the rest of the script. `system` stays as the editor's own record. Test: `author/test_system_book.py`.
- Find lists every page text and shape text that holds a word or phrase, with how many times, and Replace all changes them and says how many. The search is plain text, never a regular expression. Match case is off unless ticked.

## 2026-10-31

- Spelling lists words in page text, fields, and buttons that are not in a small list of ordinary English words (`author/words.txt`, written for this editor, under 600 words). Selecting one goes to its page. Add to book stores the word in the book's `words` so it is not flagged again. Nothing is shelled out to.

## 2026-10-31

- A page's Transition is stored as `transition` and ignored. Foolbook changes pages with no animation, and the README says so. "none" stores nothing.

## 2026-10-31

- A picture is stored as PNG. GIF, BMP, and JPEG are converted when Pillow is installed. The picture's size in pixels shows when it comes in and when it is selected, and a click without a drag places it at that size. A file that is not a picture is refused.
- Book sets the book's title, author, default page size (`pageSize`), and first page (`firstPage`). A bad size or a page that does not exist is refused and changes nothing. Foolbook opens the book at its first page.

## 2026-10-31

- Drag an action from the Actions pane onto an object on the page and it is added to that object's list. Goto, show, hide, set text, and play take their page or shape from the box beside the list, or ask.
- Write script puts the script an action list stands for into the object script, so the author can see it and edit it. The action list stays. A play action has no script line and the script says so in a comment.
- The Actions pane builds an action list on the selected object (go to page, next, previous, show, hide, set text, play), one `do` plus its arguments each. Foolbook runs them on a click. When the object also has a script, the pane says the script runs, not the actions.

## 2026-10-31

- The Icon tool places a picture at 32 by 32, whatever the drag or the picture's own size, and marks it `preset: "icon"`. The reader stretches the picture to fit.

## 2026-10-31

- The tool row shows the colours the book already uses, most used first. Click a swatch to fill the selected object with it, right-click to use it for the line.
- The pages, stage, and properties panes reopen at the widths you left them. The sashes are kept in `settings.json` under the user config directory (`$XDG_CONFIG_HOME` or `~/.config/foolbookeditor`, `%APPDATA%` on Windows), not in the book. A smaller window still leaves the stage at least 300 pixels. Test: `author/test_settings.py`.
- Proof PNGs writes one picture per page (`001_P0.png`, ...) into a folder, the shared background first, using Foolbook's `draw` as the stage does. It needs no window, and backgrounds are not pages. Text uses Pillow's built-in face. PDF was already in Export, through Foolbook. Test: `author/test_proof.py`.
- Import .tbk reads a ToolBook book through Foolbook into a book the editor saves as an `.fbk` beside it. The `.tbk` is not written. A report window lists what the reader left behind: groups kept as loose objects, arcs drawn as their ellipse, curves and other kinds it does not draw, handlers with no source, and the limits no `.tbk` import has yet. Test: `author/test_import.py`.
- The quiz schema is written down: `version`, `question`, `choices` (`label`, `correct`, exactly one right), `feedback_right`, `feedback_wrong`, optional `next` and `again`. `author/quiz.py` has `make_quiz`, `right_index`, and `validate`. Tested in `author/test_quiz.py`, with questions written for the test.
- System book: a page book names one `.fsk` in the toolbar, stored as `system`. Foolbook runs that book's handlers first once squirelworks/Foolbook#40 lands. Open takes an `.fsk`, which opens as its handlers (the status line counts them) plus any pages it has. Test: `author/test_system_book.py`.
- Viewer: Previous, Next, and Page number checkboxes store the book's first viewer (`viewers[0]`: name, size, buttons). Foolbook shows those buttons under the page once squirelworks/Foolbook#34 lands. Test: `author/test_viewers.py`.
- New background adds an empty shared background at the end of the book (`Background`, `Background 2`, ...). The page list marks each one `(background)`, and the Background list on every page offers all of them. Test: `author/test_backgrounds.py` `SeveralBackgrounds`.
- Publish also writes `books.json` in the folder: each book's title, file, and page count. Publishing another book into the same folder adds its line and keeps the rest.
- Publish writes a folder: the book as `.fbk`, every picture or clip a shape links by a relative `src`, and a one-line `README.txt` that says to open it with Foolbook. A linked file that is not found is named in the status line. No installer.
- Pattern steps the selected rectangle through 8 by 8 fills (checks, horizontal, vertical, diagonal, dots) and back to none. It is stored as `tile`. A `.tbk` export keeps the plain fill colour.
## Unreleased — 2026-10-31

- Author starts on Select, and Escape goes back to Select from any tool.
- A new rectangle is filled `#f7f4ee` with a `#071428` outline. It had no fill and a black outline.
- Label places a text shape with no border and no fill. It is the text kind with `preset: label`, not a new kind, so the reader draws it today.
- A new Field is `editable: true`, so the student can type into it in Foolbook and the typing is kept as `value`. A Label is `editable: false`. Needs the reader change in Foolbook#42.
- Check and Radio place a checkbox and a radio button, off, with a caption. Radios share the group `choice`, so the reader turns the others off when one is clicked. Needs Foolbook#49.
- List places a list box with three choices and none chosen. The reader picks a row into `value` and scrolls a long list. Needs Foolbook#50.
- Combo places a one-row combo box with three choices. The reader opens it on a click and closes it on the row picked. Needs Foolbook#51.
- Fit steps the selected picture through `fill`, `contain`, and `none`, which is how the reader sits it in its frame. A picture with no `fit` is `fill`. Needs Foolbook#52.
- Record asks for field names and rows, then places one text field per name and Previous and Next buttons, and stores the rows on the page as `records`. The reader shows one row at a time. Needs Foolbook#53.
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
- A new book carries `"fbk": 1`, the book version Foolbook already stamps. The editor refuses to save a book whose version is newer than the installed reader writes, and says the number. A book with no version key still opens and saves.
- Duplicate copies the current page, with its shapes and scripts, under a new id. The copy is the next page. Ctrl+Shift+D does the same.
- Delete asks before it removes a page, and names the page and how many objects go with it. Ctrl+Shift+Delete does the same.
- Up and Down beside the page list move the current page one place earlier or later. Ctrl+Shift+Up and Ctrl+Shift+Down do the same.
- Size under the stage sets the page size, 640 by 480 when the book does not say. The stage shows the whole page with a dashed edge, and a shape past the edge is kept and drawn past it.
- Each page has a small drawing of its shapes under the page list. A click on one shows that page.
- Go to, or Ctrl+G, shows the page whose id you type. An unknown id stays put and the status line says so.
- First, previous, next, and last buttons under the page list move the editor through the pages in book order. They do not follow the book's Next button.
- Right click on a page in the list opens Add page, Duplicate page, Delete page, and Properties. They run the same commands as the buttons and keys, and show the key. Properties moves to the page id field.
- A click selects the topmost shape under it. A line is picked near its stroke, a shape stored as points is picked inside its points' bounds, and background shapes are picked only while Background is chosen.
- A drag on empty page draws a box and selects every object whose bounds meet it. The object list can select more than one.
- Arrow keys move the selected objects by 1, and Shift+arrow by 8. Dragging one of several selected objects moves them all.
- A selected object has eight handles, and a line has its two ends. A side handle pulls one side. Nothing resizes below 4 by 4.
- Shift while drawing makes a box square, and makes a line horizontal, vertical, or 45 degrees.
- Grid 8 snaps a drawn, moved, or resized object to an 8-pixel grid when the mouse button comes up. It is off by default.
- Align lines up the selection by left, right, top, bottom, or centre, against the first selected object.
- Distribute spaces three or more selected objects with equal gaps, across or down.
- Front and Back now go all the way on the object's layer. Forward and Backward move it one place.
- Group puts the selected objects into one group object that moves as one. Foolbook paints its children (Foolbook#48).
- Ungroup puts a group's objects back on the page where it was, in order. A group inside it stays a group.
- Lock keeps an object from being picked on the stage. The object list can still select it, and the Lock menu unlocks it. locked: true is kept in the file.
- Undo and Redo, Ctrl+Z and Ctrl+Y, step through the last 50 changes. Typing in a box is one step when the box loses focus.
- Cut, Copy and Paste work on the selected objects, or on the page when the page list has focus. A paste lands 8 right and 8 down, and a taken name or page id is renamed.
- Right click on an object on the stage chooses it and opens Properties, Script, Forward, Backward, Cut, Copy, and Delete. Delete, or the Delete key, removes the chosen objects as one undo step. Properties and Script move to the panes that hold them.

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
