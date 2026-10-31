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

Save compresses by default, as Foolbook packs a book. The Compress box turns it off. A book opened from an uncompressed file, such as a web editor download, is saved uncompressed until the box is ticked.

Recent lists the last five books opened or saved. The list is kept in the user's config folder (`~/.config/foolbookeditor/recent.json`, or `%APPDATA%\foolbookeditor` on Windows), not in the repository. A book that is gone is taken off the list, and the status line says so.

A book always has at least one page. Deleting the only page is refused, and the status line says so. The editor does not make a blank page in its place. The reader cannot show a book with no pages.

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

Export writes `.fbk`, `.fsk`, `.fsc`, a `.tbx` folder, a `.tbk` or `.sbk` shell, or `.pdf`, `.doc`, `.docx`, `.ppt`, `.pptx`, and `.odt`. A `.tbx` folder is `Book.xml` with `Book.Pages` in reading order, then one folder per page. Fields and buttons are written with bounds. The ToolBook shells are what Foolbook can open. ToolBook itself has not been shown to open one.

```bash
python3 examples/welcome.py /path/to/Foolbook/foolbook/books
```

That writes the two books a new Foolbook install opens: Using Foolbook and First Light.


Self-running export is scaffolded and not built. The Export menu and `--export-exe` name it and write nothing.

