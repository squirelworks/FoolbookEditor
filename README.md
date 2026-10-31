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

Export writes `.fbk`, `.fsk`, `.fsc`, a `.tbx` folder, a `.tbk` or `.sbk` shell, or `.pdf`, `.doc`, `.docx`, `.ppt`, `.pptx`, and `.odt`. A `.tbx` folder is `Book.xml` with `Book.Pages` in reading order, then one folder per page. Fields and buttons are written with bounds. The ToolBook shells are what Foolbook can open. ToolBook itself has not been shown to open one.

```bash
python3 examples/welcome.py /path/to/Foolbook/foolbook/books
```

That writes the two books a new Foolbook install opens: Using Foolbook and First Light.


## Quizzes

A quiz is data on the page, `page["quiz"]`: `version` (1), `question`, `choices` (each `{"label", "correct"}`, exactly one right), `feedback_right`, `feedback_wrong`, and optional `next` and `again` pages. `author/quiz.py` makes and checks one. The `choices` list is the shape Foolbook already reads, so an older quiz still opens.

`insert_quiz(page, quiz)` puts the quiz on the page as shapes: the question as text, one button per choice that stores its `choice` index, and two hidden feedback texts marked `feedback: "right"` and `"wrong"`. Foolbook grades the button by that index, not by its name.

A question bank is a JSON file beside the book, `name.bank.json`: `{"bank": 1, "questions": [quiz, ...]}`, the quiz schema as an array. `author/bank.py` loads and saves it, refuses a bank version newer than it knows, and `pick(page, bank, i)` puts one question on a page. The bank is not copied into the book.

Self-running export is scaffolded and not built. The Export menu and `--export-exe` name it and write nothing.

