# Changelog

## Unreleased — 2026-10-31

- The README says how to install the editor: a venv, `pip install -e .`, and `python3 -m foolbookeditor`.
- Foolbook is pinned to commit 031e8d8, not to a floating main. A pull request that needs a newer reader bumps the pin and names the function.
- `python3 -m foolbookeditor --selftest` builds a book in memory, saves it, loads it, and checks the page id, one shape, and one script. No window.
- The self test also opens the saved book and Using Foolbook through the reader, so an editor change that breaks the reader fails it.
- A book the editor opens and saves again, uncompressed, is the same bytes. The editor drops the envelope keys the reader stamps (`format`, `format_version`, `fbk`, `foolbook`) before a save, so they come back in the reader's order. `tests/fixtures/tiny.fbk` is the golden file.
- The compressed form has a golden file too, `tests/fixtures/tiny_z.fbk`: flags byte 1, then a zlib stream the reader decompresses. Opened and saved compressed, it is the same bytes.
- A new book carries `"fbk": 1`, the book version Foolbook already stamps. The editor refuses to save a book whose version is newer than the installed reader writes, and says the number. A book with no version key still opens and saves.
- Save is not Export. Save writes `.fbk`, `.fsk`, or `.json`. A book opened from a `.tbk`, an `.sbk`, or an office file is saved beside it as `.fbk` (or `.fsk`), and the original is not written. Saving an `.fsk` keeps it a system book; it was written as an `.fbk`. The status line names the file written. Export stays its own button.
- `schema.md` and `author/schema.py` write the book dict down, starting with the book fields `id`, `title`, and `pages`. `_magic` is the web editor's envelope state and is not written into the payload; the reader opens a book with or without it.
- The page fields are written down: `id`, `text` (a list of strings), `items`, `shapes`, `script`, `name`, `size` (`[w, h]`). Each round-trips, and the reader sees them. A new page gets `shapes`, not the `widgets` key the reader never read.
- The shape fields are written down: `kind`, `name`, `text`, `x`, `y`, `w`, `h`, `fill`, `outline`, `size`, `points`, `item`, `script`, `src`, `data`, `visible`, `layer`, and an arc's `ends`. Each round-trips, an embedded picture included, and the reader keeps them. The Tk tools write no other field.
- `set_item(shape, page, book, label)` sets the jump a click follows, and an empty page clears it. A button with an item and no script goes there in the reader; `foolbookeditor.core.click` is the headless click the test uses.
- Page ids are unique in a book, without regard to case, as the reader finds them. `rename_page` refuses a rename onto another page's id and the status line says so. The casing typed is kept. A new page's id no longer collides with an id in another case.
- `move_page` is tested at the ends: the first page, the last page, and a one-page book. Moving past an end does nothing. No behavior changed.
- Deleting the only page is refused with a sentence, in the model (`LastPage`), not silently ignored. No blank page is made. The README says so.
- Save writes a page's background shapes ahead of its page shapes. The reader paints in array order, so a background shape added after a page shape (a web editor book) was drawn on top of it. Backgrounds stay on the page, tagged `layer: background`; `schema.md` says why.
- Open sniffs the bytes. A ToolBook file renamed `.fbk` opens as ToolBook, and an `.fbk` named `.tbk` opens as a Foolbook book. Save after opening a renamed ToolBook file asks for a name instead of writing over it. A file that will not open says why instead of stopping the window.
- A book the web editor downloaded (`FBK1`, flags 0, plain JSON, no `_magic`) opens under the name the browser gave it, and keeps its shapes through a desktop save. A download with the header and no book after it, which the web editor's Download wrote until the site fixes it, says so instead of a JSON error.
- Save writes compressed or uncompressed. Compressed stays the default, matching Foolbook's `pack`. A Compress box turns it off, and a book opened from an uncompressed file saves uncompressed.
- Save as by extension is tested: `.fbk` writes a book, `.fsk` a system book, no extension a book, and an empty system book is a valid `FSK1` the reader opens. No behavior changed; #22 made it so.

## 0.4.0 — 2026-10-24

- Page and Background are separate. The list and a new object follow the one that is selected. The picture still shows both, background first.
- Line, Ellipse, Polygon, Arc, and Picture place a shape Foolbook draws. Fill and Line set the colour of the selected object. Front and Back move it within its own layer.

## 0.3.5 — 2026-10-24

- Select drags the object under the pointer. The four squares on a selected object pull its corners, and the opposite corner stays put.

## 0.3.4 — 2026-10-24

- The Author window opens large enough for three panes. The picture is the middle one. The page list and the object list cannot push it off the screen.

## 0.3.3 — 2026-10-24

- The desktop window is what opens. `--browser` is the other one.
- Button, Field, and Rectangle place an object where you drag on the picture. Select still picks the object under the pointer.

## 0.3.2 — 2026-10-24

- The browser editor, which is what starts with no `--desktop` flag, now has the page in the middle. Pages stay on the left. Objects and the object script stay on the right. A `.tbk` is read through Foolbook, so the picture is the book's objects.

## 0.3.1 — 2026-10-24

- The middle of Author is the page Foolbook draws. Pages stay on the left and the object script stays on the right. A click on the picture selects the object. Opening a `.tbk` reads it through Foolbook.

## 0.3.0 — 2026-10-24

- Author lists the objects on the selected page, in book order. A field Reader hides is still in the list. The selected object's script can be edited. Save still writes an `.fbk`.

## 0.2.3 — 2026-10-22

- The conversion note that said bitmaps are missing is gone. A button picture is in the `.fbk` once Foolbook 1.0.5r15 has read it.

## 0.2.2 — 2026-10-22

- No loader of its own. A `.tbk` converted after Foolbook 1.0.5r13 keeps the object store: page order, field text, polygon outlines, the background colour, and button bitmaps.
