# FoolbookEditor

The editor. [Foolbook](https://github.com/squirelworks/Foolbook) is the reader and the core. Foolbook is the reader, and this repository is the window. It does not keep its own copy of loading, saving, office files, or OpenScript. Those calls go through `foolbookeditor.core`, which calls `foolbook.core`.

## Install

```bash
git clone https://github.com/squirelworks/FoolbookEditor.git
cd FoolbookEditor
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -U pip
python3 -m pip install -e .
python3 -m foolbookeditor
```

`pip install -e .` brings Foolbook with it, at the commit `pyproject.toml` pins. A pull request that needs a newer reader function bumps that pin and says which function. The window needs Tk. On Debian and Ubuntu that is `sudo apt install python3-tk`.

```bash
python3 -m foolbookeditor --selftest    # save and load a book, no window
```

Every pull request runs the self test before it goes up.

## Use

```bash
python3 -m foolbookeditor --fbk path/to/book.tbk    # write book.fbk beside it
python3 -m foolbookeditor --fbk path/to/book.sbk    # write book.fsk
python3 -m foolbookeditor --fbk path/to/courses     # every book in the folder
```

The Author window is the outside. Pages are on the left, the object and its script are on the right, and the middle is the page Foolbook draws. A click on that picture selects the object. Foolbook's own window still has its page list. That list is for development. It is not how Author is arranged.

```bash
python3 -m foolbookeditor path/to/book.tbk          # desktop Author
python3 -m foolbookeditor --browser path/to/book.fbk
python3 -m foolbookeditor --fbk path/to/book.tbk    # write book.fbk beside it
```

The desktop window is Author. Select is the tool it starts with, and Escape goes back to it. Select moves an object and pulls its corners. Button, Field, Rectangle, Rounded, Line, Ellipse, Arc, Pie, Chord, Picture, and Hotspot place one where you drag. A new Field opens for typing where it was placed, and a double-click with Select types into a field already there. Return makes a new line. Escape or a click elsewhere keeps the words. Picture asks whether to keep the picture inside the book. Yes stores it as base64 PNG in `data`, so the book stays one file. No stores `src`, the path beside the book. A file over 20 MB is refused with a sentence that says so. A hotspot (`kind: hotspot`) has no fill. Author shows its outline, Foolbook draws nothing, and a click there follows its item. Polygon and Curve are clicked out one point at a time. A curve stays open (`kind: curve`), and Foolbook draws it as straight segments through its points for now. An arc is stored as `start` and `sweep` in degrees (zero east, counterclockwise). A new one is the top half of its bounds. Pie places a filled slice the same way, a quarter to start. Chord places the half closed by a straight line. Double-click or Enter closes it, and Escape drops it without leaving a piece on the page. A new rectangle is filled `#f7f4ee` with a `#071428` outline. Rounded is the same with corners of radius 8 (`kind: roundrect`). Page and Background choose the layer. Fill and Line colour the selected object. The Properties pane, under the object list, sets Name, Text, Fill, Outline, and Line width (`stroke`, 1 when missing), then Font, Size, Bold, Italic, Underline, and Align (left, center, right). Under them is a well of eight plain colours, each named by its hex value. A click sets the fill and a right-click sets the outline. Any other colour is typed as `#rrggbb`. No fill, or an empty Fill, means no fill: Foolbook draws nothing inside the outline. Visible off stores `visible: false`. Foolbook skips that object, and Author draws it ghosted, washed toward white, so it can still be found. Left, Top, Width, and Height are numbers. Typing one moves or sizes the object, points included. Text that is not a whole number, or a size under 4, keeps the old value. Points lists a line, polygon, or curve one `x, y` pair per line. Leaving the box applies it, and a polygon needs three. The script pane is monospace, and Tab puts in two spaces. It holds the selected object's script, or the page's script when no object is chosen. A script is stored as the string you typed. It is not compiled as you type. Return or leaving a box applies it. A name another object on the page has, a colour that is not `#rrggbb`, or a width that is not a whole number leaves the old value. Front and Back reorder it on that layer. `--browser` is the older window.

Pages: Add (Ctrl+M) puts a blank page right after the current page. Duplicate (Ctrl+Shift+D) copies the current page, shapes and scripts included, under a new id, and the copy is the next page. Delete (Ctrl+Shift+Delete) asks first, naming the page and how many objects go with it. The last page cannot be deleted. Up and Down (Ctrl+Shift+Up, Ctrl+Shift+Down) move the current page one place; page order is reading order.

Size under the stage sets the page's `size`. A page with none is 640 by 480. The stage draws a dashed line at the page edge. A shape that hangs past it stays in the file as it is and is drawn past the line.

A page's Transition is stored as `transition` and ignored. Foolbook changes pages with no animation. The field is there so a later reader can honour it without changing the format.
Under the page list, each page has a small drawing of its shapes. A click on one shows that page.

Go to (Ctrl+G) takes a page id. Case does not matter, as in the reader. An unknown id leaves the page where it is and the status line says it is unknown. The |< < > >| buttons (Ctrl+Home, Ctrl+Page Up, Ctrl+Page Down, Ctrl+End) show the first, previous, next, and last page in book order. They move the editor, not the reader: the book's own Next button and scripts are not run.

Select picks the topmost object under the pointer. A line is picked within 3 page pixels of its stroke. With Page chosen, background objects cannot be picked; with Background chosen, only they can. Stage geometry lives in `author/geometry.py` so the web editor can be checked against the same numbers.

A drag that starts on empty page draws a box and selects every object whose bounds meet it; a line counts by its points' bounds. Ctrl-click and Shift-click in the object list also select more than one. The first selected object is the one whose script and handles are shown.

Arrow keys move the selection 1 page pixel; Shift+arrow moves it 8 (`geometry.NUDGE`, `geometry.NUDGE_BIG`). While a text box has the keyboard, arrows stay in the text. Dragging one of several selected objects moves them all.

A selected object has eight handles: four corners and the middle of each side. A side handle pulls only that side; a corner keeps the opposite corner. A line's handles are its two ends. Nothing resizes below 4 by 4 page pixels (`geometry.MIN_SIZE`).

Hold Shift while drawing: a box, ellipse, button, or field comes out square, and a line snaps to horizontal, vertical, or 45 degrees.

Export writes `.fbk`, `.fsk`, `.fsc`, a `.tbx` folder, a `.tbk` or `.sbk` shell, or `.pdf`, `.doc`, `.docx`, `.ppt`, `.pptx`, and `.odt`. A `.tbx` folder is `Book.xml` with `Book.Pages` in reading order, then one folder per page. Fields and buttons are written with bounds. The ToolBook shells are what Foolbook can open. ToolBook itself has not been shown to open one.

```bash
python3 examples/welcome.py /path/to/Foolbook/foolbook/books
```

That writes the two books a new Foolbook install opens: Using Foolbook and First Light.


## Quizzes

A quiz is data on the page, `page["quiz"]`: `version` (1), `question`, `choices` (each `{"label", "correct"}`, exactly one right), `feedback_right`, `feedback_wrong`, and optional `next` and `again` pages. `author/quiz.py` makes and checks one. The `choices` list is the shape Foolbook already reads, so an older quiz still opens.
## Scripts the reader runs

Foolbook runs a small part of OpenScript. These are the lines a script in this editor can count on today. Anything else is kept in the file and shown in the script pane, but the reader does not act on it.

| Script | What the reader does |
|---|---|
| `go to page "P2"` | Shows page P2. Page ids are compared without case. |
| `go to page "P2" of book "other"` | Opens the book `other` beside this one and shows its page P2. |
| `send next` | Shows the next page, or the page the current page's Next item names. |
| `send previous` | Shows the previous page, or the page the Back item names. `send back` is the same. |

A button's script is read as `to handle buttonClick`, then these lines, then `end`. A script with no `to handle buttonClick` line is not run by the reader yet.

Self-running export is scaffolded and not built. The Export menu and `--export-exe` name it and write nothing.

