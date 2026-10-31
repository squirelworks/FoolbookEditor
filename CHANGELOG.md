# Changelog

## 2026-10-31

- A question bank is `name.bank.json` beside the book: `{"bank": 1, "questions": [...]}`, the quiz schema as an array. `author/bank.py` loads, checks, and saves it, refuses a newer bank version and names it, and `pick` puts one question on a page. Tested in `author/test_bank.py`, with questions written for the test.
- `author.quiz.insert_quiz` puts a quiz on the page as shapes: the question, one button per choice with its `choice` index, and the right and wrong feedback hidden. Foolbook grades the saved page by that index. Tested in `author/test_quiz_insert.py`.
- Apply script shows the first error Foolbook's check finds, with its line number, in the status line, ahead of any warning. The script is saved anyway. Tested in `author/test_script_check.py`.
- Save from the window keeps a system book a system book again. The safe save, which writes beside the file and then replaces it, saved `.fsk` as `.fbk` and an `.sbk` import as `.fbk`; it now writes where `save_target` says, through `save_system` for `.fsk`. Test: `tests/test_safe_save_kind.py`.
- A book dropped on the program's icon or shortcut opens: the first file among the arguments is opened, and flags, folders and missing paths are skipped. A packaged macOS app answers `::tk::mac::OpenDocument`. The README says that a drop on the open window does nothing on any platform, since stock Tk has no drop target. Test: `tests/test_drop.py`.
- The older `--browser` window gives a new page `shapes: []`, as the Author window does since the page fields were written down. It gave Add page `widgets: []`, which the reader never reads, and an empty book's first page no shapes list at all. Test: `tests/test_browser_new_page.py`.
- Recent, beside Open, lists the last five books opened or saved, and the start window offers them; before, nothing recorded them and the start window was always handed an empty list. The list lives under `recent` in the editor's existing settings file in the user's config folder. Choosing one that is gone drops it and the status line says so. Test: `tests/test_recent.py`.
- `schema.md` and `author/schema.py` write down the 34 shape fields and 17 kinds the editor writes, with the drawing tools' `radius`, `start`/`sweep`, `stroke`, text style, `item`, and `data`/`pixels`/`src`. A test fails when a Tk tool or a property-pane row writes a key that is not listed, and saves, opens and reads a shape with every field. Test: `tests/test_schema_shape.py`.
- A book the web editor downloaded (`FBK1`, a zero flags byte, plain JSON) opens under its own name and saves again with the same shapes. An `FBK1` or `FSK1` file that holds only zero bytes after the header, which the web Download wrote before the site fixed it, is refused with a message saying to download it again; the window shows that message and keeps the book it had. Test: `tests/test_web_download.py`.
- A new page gets `shapes: []`, not `widgets: []`; the reader draws `shapes` and never reads `widgets`. `schema.md` and `author/schema.py` write down the twelve page fields, and a test saves, opens and reads a page with every one of them. The three shipped templates are rebuilt by `python -m author.templates`. Test: `tests/test_schema_page.py`.
- `move_page` is tested at the ends: the first page, the last page, and a one-page book. Moving past an end does nothing. No behavior changed.
- Page ids are unique in a book, without regard to case, as the reader finds them. `rename_page` refuses a rename onto another page's id and the status line says so. The casing typed is kept. A new page's id no longer collides with an id in another case.
- `schema.md` and `author/schema.py` write the book dict down, starting with the book fields `id`, `title`, and `pages`. `_magic` is the web editor's envelope state and is not written into the payload; the reader opens a book with or without it.
- A generated 200-page book with 20 shapes a page opens in the editor in about 0.012 s and in the reader in about 0.02 s, well under two seconds. A test holds it under two seconds. No optimization.
- The title bar shows a star while the book differs from its file. Close, New, and Open ask before dropping changes. The flag is `is_dirty(saved, current)`, which compares what Save would write, so envelope keys do not count.
- Save writes compressed or uncompressed. Compressed stays the default, matching Foolbook's `pack`. A Compress box turns it off, and a book opened from an uncompressed file saves uncompressed.
- Open sniffs the bytes. A ToolBook file renamed `.fbk` opens as ToolBook, and an `.fbk` named `.tbk` opens as a Foolbook book. Save after opening a renamed ToolBook file asks for a name instead of writing over it. A file that will not open says why instead of stopping the window.
- Save writes a page's background shapes ahead of its page shapes. The reader paints in array order, so a background shape added after a page shape (a web editor book) was drawn on top of it. Backgrounds stay on the page, tagged `layer: background`; `schema.md` says why.
- Deleting the only page is refused with a sentence, in the model (`LastPage`), not silently ignored. No blank page is made. The README says so.
- Record lays its rows out as pages: the fields go on this page with the first row, and the page is copied once for each further row with that row in the fields. Previous record and Next record go to the page before and after; the first page has no Previous and the last no Next. Nothing is stored as `records`, so the reader needs no change (Foolbook#53 is closed). `author/test_records.py`.
- Print writes the PNG proof pages and sends them to the printer when the machine has one call for it: `os.startfile(path, "print")` on Windows, one `lpr` on a Mac or Linux. Anywhere else the folder of pages is the print, and the status line says so.
- Save is not Export. Save writes `.fbk`, `.fsk`, or `.json`. A book opened from a `.tbk`, an `.sbk`, or an office file is saved beside it as `.fbk` (or `.fsk`), and the original is not written. Saving an `.fsk` keeps it a system book; it was written as an `.fbk`. The status line names the file written. Export stays its own button. The extension picks the kind whatever its case, no extension saves as `.fbk`, a system book saved as `.fbk` becomes a book, and an empty system book is still a valid `FSK1` file. Tests: `tests/test_save_target.py`, `tests/test_save_as_kind.py`.
- Apply script on an object shows a warning in the status line when a line uses a word Foolbook does not run, with the line number. The script is still kept. The words come from Foolbook's `engine/subset.py` table through `foolbook.core.unknown_words`. Tested in `author/test_scripts.py`.
- Foolbook comes from its main branch, not commit 031e8d8. The pin froze the editor on a reader main has moved past: at that commit the system-book test fails, and at the v1.0.8 tag eight tests fail. A release tag is the other allowed form. Test: `tests/test_pin.py`.

## 2026-10-31

- Naming a system book writes OpenScript the reader runs: the book script's `enterBook` gets `if "shared.fsk" is not in sysBooks` / `push "shared.fsk" onto sysBooks` / `end if`, as a ToolBook course does. Before, only a `system` key was stored, and Foolbook does not read it, so the system book's handlers never ran. A new name replaces the push, and clearing it takes the push out and leaves the rest of the script. `system` stays as the editor's own record. Test: `author/test_system_book.py`.
- Find lists every page text and shape text that holds a word or phrase, with how many times, and Replace all changes them and says how many. The search is plain text, never a regular expression. Match case is off unless ticked.
- - The property pane has Go to page, In book, and Jump label rows. They write the shape's `item`, which Foolbook follows on a click with no script. An empty page takes the jump off, and a book or label needs a page first. Test: `author/test_properties.py` ItemTests.

## 2026-10-31

- Zoom: Fit (as before), 50%, 100%, 200%. At a fixed zoom, a page smaller than the stage sits in the middle and a larger one scrolls. A click on a scrolled stage still lands on the right object. Zoom is view-only and stored coordinates never change. Test: `author/test_view.py` (`to_page(x, y, zoom)`).
- Spelling lists words in page text, fields, and buttons that are not in a small list of ordinary English words (`author/words.txt`, written for this editor, under 600 words). Selecting one goes to its page. Add to book stores the word in the book's `words` so it is not flagged again. Nothing is shelled out to.

## 2026-10-31

- A status line at the bottom of the window shows the tool, page id, selected shape, and Saved or Unsaved changes, and the zoom once the stage has a zoom control. Unsaved changes reads the dirty flag from item 22 once that has landed, and says Saved until then. Test: `author/test_status.py`.
- A page's Transition is stored as `transition` and ignored. Foolbook changes pages with no animation, and the README says so. "none" stores nothing.

## 2026-10-31

- The README has a Tools section with one `###` heading per tool (Select, Button, Field, Rectangle, Line, Ellipse, Polygon, Arc, Picture), so Help can open the local section for the tool in use. Test: `author/test_help.py`.
- A picture is stored as PNG. GIF, BMP, and JPEG are converted when Pillow is installed. The picture's size in pixels shows when it comes in and when it is selected, and a click without a drag places it at that size. A file that is not a picture is refused.
- Book sets the book's title, author, default page size (`pageSize`), and first page (`firstPage`). A bad size or a page that does not exist is refused and changes nothing. Foolbook opens the book at its first page.

## 2026-10-31

- A menu bar: File, Edit, Insert, Arrange, Book, Help. It is built from `author/menus.py`, and every item runs a command the window already has. Help for this tool opens the tool's README section in a window, not a website. Test: `author/test_menus.py`.
- Drag an action from the Actions pane onto an object on the page and it is added to that object's list. Goto, show, hide, set text, and play take their page or shape from the box beside the list, or ask.
- Write script puts the script an action list stands for into the object script, so the author can see it and edit it. The action list stays. A play action has no script line and the script says so in a comment.
- The Actions pane builds an action list on the selected object (go to page, next, previous, show, hide, set text, play), one `do` plus its arguments each. Foolbook runs them on a click. When the object also has a script, the pane says the script runs, not the actions.

## 2026-10-31

- Save writes the book to a temporary file beside it (`.name.saving.fbk`) and only then replaces the old file in one step. If the write or the replace fails, the temporary file is removed and the previous book is untouched. Test: `author/test_safesave.py`, which makes the replace step fail. A book from a newer Foolbook is still refused, and an opened book still saves back to the same bytes.
- The Icon tool places a picture at 32 by 32, whatever the drag or the picture's own size, and marks it `preset: "icon"`. The reader stretches the picture to fit.

## 2026-10-31

- Every menu item has a keyboard shortcut, or `none` on purpose (the two layer items). Add page and Delete page show the keys the window already had and are not bound twice. The menus show the keys, and Help > Keyboard map prints the whole map. Ctrl+1 to Ctrl+8 pick the drawing tools. Test: `author/test_menus.py` `KeyboardMap`.
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

- Every five minutes, a book with unsaved changes gets a recovery copy in the user config directory (`foolbookeditor/recovery/`), never beside the book. Saving removes it. Opening a book whose recovery copy is newer than the file asks which one to open. Test: `author/test_recovery.py` checks the copy's contents.
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
