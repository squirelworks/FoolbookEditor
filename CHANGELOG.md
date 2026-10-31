# Changelog

## 2026-10-31

- The pages, stage, and properties panes reopen at the widths you left them. The sashes are kept in `settings.json` under the user config directory (`$XDG_CONFIG_HOME` or `~/.config/foolbookeditor`, `%APPDATA%` on Windows), not in the book. A smaller window still leaves the stage at least 300 pixels. Test: `author/test_settings.py`.
- Proof PNGs writes one picture per page (`001_P0.png`, ...) into a folder, the shared background first, using Foolbook's `draw` as the stage does. It needs no window, and backgrounds are not pages. Text uses Pillow's built-in face. PDF was already in Export, through Foolbook. Test: `author/test_proof.py`.
- Import .tbk reads a ToolBook book through Foolbook into a book the editor saves as an `.fbk` beside it. The `.tbk` is not written. A report window lists what the reader left behind: groups kept as loose objects, arcs drawn as their ellipse, curves and other kinds it does not draw, handlers with no source, and the limits no `.tbk` import has yet. Test: `author/test_import.py`.
- System book: a page book names one `.fsk` in the toolbar, stored as `system`. Foolbook runs that book's handlers first once squirelworks/Foolbook#40 lands. Open takes an `.fsk`, which opens as its handlers (the status line counts them) plus any pages it has. Test: `author/test_system_book.py`.
- Viewer: Previous, Next, and Page number checkboxes store the book's first viewer (`viewers[0]`: name, size, buttons). Foolbook shows those buttons under the page once squirelworks/Foolbook#34 lands. Test: `author/test_viewers.py`.
- New background adds an empty shared background at the end of the book (`Background`, `Background 2`, ...). The page list marks each one `(background)`, and the Background list on every page offers all of them. Test: `author/test_backgrounds.py` `SeveralBackgrounds`.
- The page form has a Background list. It names the shared backgrounds in the book (pages with `"background": true`) and `(none)`. Picking one sets the page's `uses`, and the stage draws that background under the page. `(none)` clears it. The model refuses a name that is not a background. Test: `author/test_backgrounds.py`.

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
