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


Self-running export is scaffolded and not built. The Export menu and `--export-exe` name it and write nothing.

