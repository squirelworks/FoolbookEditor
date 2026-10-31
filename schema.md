# The book dict

Foolbook reads one dict. The desktop editor and the web editor write it. `author/schema.py` is the same list in code. A field that is here round-trips through Save and Open. A field one editor writes and the other drops is a bug.

An `.fbk` is `FBK1`, a flags byte (bit 0 means zlib), then this dict as JSON. An `.fsk` is the same with `FSK1`.

## Book

- `id`: the book's id, a string.
- `title`: the title the reader shows.
- `pages`: the pages, in reading order.
- `_magic`: the web editor's note of the envelope magic, `FBK1`. It is envelope state, not a field. Neither editor writes it into the payload; the reader never read it.

## Page

- `id`: the page's id. Jumps and `go to page` find a page by it.
- `text`: the page's words, a list of strings, one per paragraph.
- `items`: the jumps on the page, each `{"label", "page"}`.
- `shapes`: what is drawn on the page, in paint order. A new page has an empty list. The old `widgets` key is not read by the reader and a new page does not get it.
- `script`: the page script, one string. The reader splits it into handlers.
- `name`: the page's name. The reader uses it as the id when `id` is missing.
- `size`: `[w, h]` in pixels. A page without it uses the book's size.

## Shape

- `kind`: what the shape is: `rect`, `ellipse`, `line`, `polygon`, `arc`, `text`, `image`, `button`.
- `name`: the shape's name. Scripts find a shape by it.
- `text`: the words in a text field or on a button.
- `x`, `y`, `w`, `h`: the bounds in page pixels, top left and size.
- `fill`, `outline`: colours as `#rrggbb`. An empty `fill` is no fill.
- `size`: the font size of the shape's text.
- `points`: a line's or polygon's points, a list of `[x, y]`.
- `item`: the jump a click follows, `{"page", "book", "label"}`. `page` is required; `book` and `label` are optional. A button with an `item` and no script still goes there in the reader. An empty page clears the item.
- `script`: the shape's script, one string.
- `src`: a picture's file, beside the book.
- `data`: a picture's PNG bytes as base64, so the book is one file.
- `visible`: `false` means the reader does not draw it. Missing means visible.
- `layer`: `page` or `background`. Missing means `page`.
- `ends`: an arc's two end points, `[[x, y], [x, y]]`. Only an arc has it.

The reader stamps `format`, `format_version`, `fbk` (the book version, now 1), and `foolbook` (the reader's own version) on every save. The editor drops those before it saves so the reader writes them in its own order.
