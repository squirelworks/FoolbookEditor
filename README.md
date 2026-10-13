# FoolbookEditor

The editor. [Foolbook](https://github.com/squirelworks/Foolbook) is the reader and the core. This repository is the window. It does not keep its own copy of loading, saving, office files, or OpenScript. Those calls go through `foolbookeditor.core`, which calls `foolbook.core`.

```bash
python3 -m foolbookeditor                         # new book, browser, port 6767
python3 -m foolbookeditor path/to/book.fbk        # edit that book
python3 -m foolbookeditor --desktop path/to/book.fbk
```

Save writes an `.fbk` and a sibling `.json`. The browser editor edits the title, subject, module, page text, jumps, page script, and quiz. Other jumps, such as Begin, stay. Open can take an office file and turn it into pages. Export writes `.docx`, `.pptx`, `.odt`, `.pdf`, or a `.tbk` shell. Pictures and styles are dropped.

Self-running export is scaffolded and not built. The Export menu and `--export-exe` name it and write nothing.

