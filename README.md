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

The desktop window is Author. Select is the tool it starts with, and Escape goes back to it. Select moves an object and pulls its corners. Button, Field, Rectangle, Rounded, Line, Ellipse, Arc, and Picture place one where you drag. Polygon is clicked out one point at a time. Double-click or Enter closes it, and Escape drops it without leaving a piece on the page. A new rectangle is filled `#f7f4ee` with a `#071428` outline. Rounded is the same with corners of radius 8 (`kind: roundrect`). Page and Background choose the layer. Fill and Line colour the selected object. Front and Back reorder it on that layer. `--browser` is the older window.

Export writes `.fbk`, `.fsk`, `.fsc`, a `.tbx` folder, a `.tbk` or `.sbk` shell, or `.pdf`, `.doc`, `.docx`, `.ppt`, `.pptx`, and `.odt`. A `.tbx` folder is `Book.xml` with `Book.Pages` in reading order, then one folder per page. Fields and buttons are written with bounds. The ToolBook shells are what Foolbook can open. ToolBook itself has not been shown to open one.

```bash
python3 examples/welcome.py /path/to/Foolbook/foolbook/books
```

That writes the two books a new Foolbook install opens: Using Foolbook and First Light.


Self-running export is scaffolded and not built. The Export menu and `--export-exe` name it and write nothing.

