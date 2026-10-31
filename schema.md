# The book dict

Foolbook reads one dict. The desktop editor and the web editor write it. `author/schema.py` is the same list in code. A field that is here round-trips through Save and Open. A field one editor writes and the other drops is a bug.

An `.fbk` is `FBK1`, a flags byte (bit 0 means zlib), then this dict as JSON. An `.fsk` is the same with `FSK1`.

## Book

- `id`: the book's id, a string.
- `title`: the title the reader shows.
- `pages`: the pages, in reading order.
- `_magic`: the web editor's note of the envelope magic, `FBK1`. It is envelope state, not a field. Neither editor writes it into the payload; the reader never read it.

## Shape

`kind` is one of `rect`, `roundrect`, `ellipse`, `line`, `curve`, `polygon`, `arc`, `pie`, `chord`, `text`, `button`, `image`, `hotspot`, `check`, `radio`, `list` or `combo`.

Every shape:

- `kind`: what the shape is.
- `name`: the shape's name. Scripts find a shape by it.
- `x`, `y`, `w`, `h`: the bounds in page pixels, top left and size.
- `visible`: `false` means the reader does not draw it. Missing means visible.
- `layer`: `page` or `background`. Missing means `page`.
- `script`: the shape's script, one string.
- `item`: the jump a click follows, `{"page": id, "book"?: file, "label"?: text}`. An empty page removes it.

Paint:

- `fill`: `#rrggbb`, or `""` for no fill. A hotspot always writes `""`.
- `outline`: `#rrggbb`.
- `stroke`: the line width in pixels for outlined and line kinds (`rect`, `roundrect`, `ellipse`, `line`, `curve`, `polygon`, `arc`, `pie`, `chord`). Missing means 1.
- `tile`: a fill pattern, rows of 0 and 1. A 1 is drawn in the outline colour.

Points and curves:

- `points`: `[[x, y], ...]` in page pixels. A `polygon` has at least 3, a `curve` at least 2, a `line` 2.
- `ends`: an arc's two end points, `[[x, y], [x, y]]`, as a ToolBook import gives them. An arc with `ends` is still valid.
- `radius`: a `roundrect`'s corner radius in pixels, 8 when new. The reader clamps it to half the short side.
- `start`, `sweep`: degrees for `arc`, `pie` and `chord`. Zero is east and a positive sweep turns counterclockwise. A new arc is 0/180, a pie 0/90, a chord 0/180.

Words, on `text` and `button`:

- `text`: the words.
- `font`: the face name. Missing means the reader's face.
- `size`: the point size, 1 to 288.
- `bold`, `italic`, `underline`: `true` or `false`.
- `align`: `left`, `center` or `right`. A ToolBook import's 0, 1 or 2 is still read.
- `border`: a label's border width.
- `editable`: `true` gives a text field the keyboard.
- `preset`: `label` or `icon`, the tool that made a preset shape.

Pictures, on `image`:

- `src`: a linked picture's file, relative to the book.
- `data`: an embedded picture's PNG bytes as base64, so the book is one file.
- `pixels`: the embedded picture's `[w, h]`.
- `fit`: `fill`, `contain` or `none`. Missing means `fill`.

Controls:

- `value`: a `check` or `radio`'s state, or the row a `list` or `combo` picked.
- `group`: the radios that turn each other off.
- `choices`: a `list` or `combo`'s rows.

The stage's ghost copy during a drag is never saved.

The reader stamps `format`, `format_version`, `fbk` (the book version, now 1), and `foolbook` (the reader's own version) on every save. The editor drops those before it saves so the reader writes them in its own order.
