# FoolbookEditor

The editor. [Foolbook](https://github.com/squirelworks/Foolbook) is the reader. This repository writes the books that Foolbook opens.

```bash
python3 -m foolbookeditor                         # new book, browser, port 6767
python3 -m foolbookeditor path/to/book.fbk        # edit that book
python3 -m foolbookeditor --desktop path/to/book.fbk
```

Save writes an `.fbk` and a `.json` working copy. It can also open `.pdf`, `.ppt`, `.pptx`, `.doc`, `.docx`, and `.odt` and turn them into pages. Pictures and styles are dropped.

Foolbook reads those office files. Writing one back uses `engine.office.write` from the reader, which is the inverse of that reader. The window that edits lives here.

Self-running export is scaffolded and not built. ToolBook could save a book as an executable that carried its own runtime. `python3 -m foolbookeditor --export-exe book.fbk` names that export and writes nothing. The desktop window has the same button.

