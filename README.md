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

## Tools

Help in the editor opens the section below for the tool in use.

### Select

The pointer. Click an object to select it, drag it to move it, or drag one of its corner squares to resize it. The opposite corner stays where it was. Only objects on the layer chosen with Page and Background can be picked.

### Button

Drag to place a button, or click to place one at 90 by 28. It starts out labelled with its name. Its script is edited in the object pane.

### Field

Drag to place a text field, or click to place one at 160 by 36. The words come from the object's text.

### Rectangle

Drag to place a rectangle, or click to place one at 100 by 60. Fill and Line set its colours.

### Line

Drag from one end to the other.

### Ellipse

Drag the box the ellipse fits in, or click to place one at 80 by 60.

### Polygon

Drag to place a polygon in the box you drag.

### Arc

Drag the box the arc's ellipse fits in.

### Picture

Drag the box, then choose a PNG, GIF, BMP, or JPEG. The picture is stored in the book, so the book stays one file.

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

