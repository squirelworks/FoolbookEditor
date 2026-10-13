# FoolbookEditor

The editor. [Foolbook](https://github.com/squirelworks/Foolbook) is the reader and the core. This repository is the window. It does not keep its own copy of loading, saving, office files, or OpenScript. Those calls go through `foolbookeditor.core`, which calls `foolbook.core`.

```bash
python3 -m foolbookeditor                         # new book, browser, port 6767
python3 -m foolbookeditor path/to/book.fbk        # edit that book
python3 -m foolbookeditor --desktop path/to/book.fbk
```

Export writes `.fbk`, `.fsk`, `.fsc`, a `.tbx` folder (`Book.xml` and one folder per page), a `.tbk` or `.sbk` shell, or `.pdf`, `.doc`, `.docx`, `.ppt`, `.pptx`, and `.odt`. The ToolBook shells are what Foolbook can open. ToolBook itself has not been shown to open one.

```bash
python3 examples/welcome.py /path/to/Foolbook/foolbook/books
```

That writes the two books a new Foolbook install opens: Using Foolbook and First Light.


Self-running export is scaffolded and not built. The Export menu and `--export-exe` name it and write nothing.

