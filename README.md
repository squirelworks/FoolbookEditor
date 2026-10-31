# FoolbookEditor

The editor. [Foolbook](https://github.com/squirelworks/Foolbook) is the reader and the core. This repository is the window. It does not keep its own copy of loading, saving, office files, or OpenScript. Those calls go through `foolbookeditor.core`, which calls `foolbook.core`.

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

The desktop window is Author. Select moves an object and pulls its corners. Button, Field, Rectangle, Line, Ellipse, Polygon, Arc, and Picture place one where you drag. Page and Background choose the layer. Fill and Line colour the selected object. Front and Back put it in front of or behind everything on its layer; Forward and Backward move it one place. Array order is paint order, and there is no separate z field. `--browser` is the older window.

Pages: Add (Ctrl+M) puts a blank page right after the current page. Duplicate (Ctrl+Shift+D) copies the current page, shapes and scripts included, under a new id, and the copy is the next page. Delete (Ctrl+Shift+Delete) asks first, naming the page and how many objects go with it. The last page cannot be deleted. Up and Down (Ctrl+Shift+Up, Ctrl+Shift+Down) move the current page one place; page order is reading order.

Size under the stage sets the page's `size`. A page with none is 640 by 480. The stage draws a dashed line at the page edge. A shape that hangs past it stays in the file as it is and is drawn past the line.

Under the page list, each page has a small drawing of its shapes. A click on one shows that page.

Go to (Ctrl+G) takes a page id. Case does not matter, as in the reader. An unknown id leaves the page where it is and the status line says it is unknown. The |< < > >| buttons (Ctrl+Home, Ctrl+Page Up, Ctrl+Page Down, Ctrl+End) show the first, previous, next, and last page in book order. They move the editor, not the reader: the book's own Next button and scripts are not run.

Select picks the topmost object under the pointer. A line is picked within 3 page pixels of its stroke. With Page chosen, background objects cannot be picked; with Background chosen, only they can. Stage geometry lives in `author/geometry.py` so the web editor can be checked against the same numbers.

A drag that starts on empty page draws a box and selects every object whose bounds meet it; a line counts by its points' bounds. Ctrl-click and Shift-click in the object list also select more than one. The first selected object is the one whose script and handles are shown.

Arrow keys move the selection 1 page pixel; Shift+arrow moves it 8 (`geometry.NUDGE`, `geometry.NUDGE_BIG`). While a text box has the keyboard, arrows stay in the text. Dragging one of several selected objects moves them all.

A selected object has eight handles: four corners and the middle of each side. A side handle pulls only that side; a corner keeps the opposite corner. A line's handles are its two ends. Nothing resizes below 4 by 4 page pixels (`geometry.MIN_SIZE`).

Hold Shift while drawing: a box, ellipse, button, or field comes out square, and a line snaps to horizontal, vertical, or 45 degrees.

Grid 8 is off when the window opens. When it is on, the stage shows the grid as dots, and a drawn, moved, or resized object snaps to the 8-pixel grid when the mouse button comes up, not during the drag.

Align lines up two or more selected objects by their left, right, top, or bottom edges, or their horizontal or vertical centres. The first selected object is the reference and does not move; the menu says so. Distribute, in the same menu, spaces three or more objects with equal gaps between their bounds, across or down; the two outermost stay put.

Group puts two or more selected objects on one layer into one object of kind `group`, with the objects as its `children` at their page positions. It sits where the front-most of them was. Moving the group moves them all; resizing a group is not done yet. Foolbook paints and clicks a group's children (Foolbook#48), and `hide group "Group"` reaches them.

Export writes `.fbk`, `.fsk`, `.fsc`, a `.tbx` folder, a `.tbk` or `.sbk` shell, or `.pdf`, `.doc`, `.docx`, `.ppt`, `.pptx`, and `.odt`. A `.tbx` folder is `Book.xml` with `Book.Pages` in reading order, then one folder per page. Fields and buttons are written with bounds. The ToolBook shells are what Foolbook can open. ToolBook itself has not been shown to open one.

```bash
python3 examples/welcome.py /path/to/Foolbook/foolbook/books
```

That writes the two books a new Foolbook install opens: Using Foolbook and First Light.


Self-running export is scaffolded and not built. The Export menu and `--export-exe` name it and write nothing.

