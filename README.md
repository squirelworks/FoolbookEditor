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

The desktop window is Author. Select moves an object and pulls its corners. Button, Field, Rectangle, Line, Ellipse, Polygon, Arc, and Picture place one where you drag. Page and Background choose the layer. Fill and Line colour the selected object. Front and Back reorder it on that layer. `--browser` is the older window.

Pages: Add (Ctrl+M) puts a blank page right after the current page. Duplicate (Ctrl+Shift+D) copies the current page, shapes and scripts included, under a new id, and the copy is the next page. Delete (Ctrl+Shift+Delete) asks first, naming the page and how many objects go with it. The last page cannot be deleted. Up and Down (Ctrl+Shift+Up, Ctrl+Shift+Down) move the current page one place; page order is reading order.

Size under the stage sets the page's `size`. A page with none is 640 by 480. The stage draws a dashed line at the page edge. A shape that hangs past it stays in the file as it is and is drawn past the line.

Under the page list, each page has a small drawing of its shapes. A click on one shows that page.

Go to (Ctrl+G) takes a page id. Case does not matter, as in the reader. An unknown id leaves the page where it is and the status line says it is unknown. The |< < > >| buttons (Ctrl+Home, Ctrl+Page Up, Ctrl+Page Down, Ctrl+End) show the first, previous, next, and last page in book order. They move the editor, not the reader: the book's own Next button and scripts are not run.

Export writes `.fbk`, `.fsk`, `.fsc`, a `.tbx` folder, a `.tbk` or `.sbk` shell, or `.pdf`, `.doc`, `.docx`, `.ppt`, `.pptx`, and `.odt`. A `.tbx` folder is `Book.xml` with `Book.Pages` in reading order, then one folder per page. Fields and buttons are written with bounds. The ToolBook shells are what Foolbook can open. ToolBook itself has not been shown to open one.

```bash
python3 examples/welcome.py /path/to/Foolbook/foolbook/books
```

That writes the two books a new Foolbook install opens: Using Foolbook and First Light.


Self-running export is scaffolded and not built. The Export menu and `--export-exe` name it and write nothing.

