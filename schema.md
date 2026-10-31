# The book dict

Foolbook reads one dict. The desktop editor and the web editor write it. `author/schema.py` is the same list in code. A field that is here round-trips through Save and Open. A field one editor writes and the other drops is a bug.

An `.fbk` is `FBK1`, a flags byte (bit 0 means zlib), then this dict as JSON. An `.fsk` is the same with `FSK1`.

## Book

- `id`: the book's id, a string.
- `title`: the title the reader shows.
- `pages`: the pages, in reading order.
- `_magic`: the web editor's note of the envelope magic, `FBK1`. It is envelope state, not a field. Neither editor writes it into the payload; the reader never read it.

The reader stamps `format`, `format_version`, `fbk` (the book version, now 1), and `foolbook` (the reader's own version) on every save. The editor drops those before it saves so the reader writes them in its own order.

## Page

- `id`: the page's id. Jumps and `go to page` find a page by it.
- `text`: the page's words, a list of strings, one per paragraph.
- `items`: the jumps on the page, each `{"label", "page"}`.
- `shapes`: what is drawn on the page, in paint order. A new page has an empty list. The old `widgets` key is not read by the reader and a new page does not get it.
- `script`: the page script, one string. The reader splits it into handlers.
- `name`: the page's name. The reader uses it as the id when `id` is missing.
- `size`: `[w, h]` in pixels. A page without it uses the book's size.
- `background`: `true` on a shared background page. Other pages leave it out.
- `uses`: the id of the shared background this page sits on. Missing means none.
- `transition`: the transition's name. Foolbook ignores it for now; it is kept so a later reader can honour it. Missing means none.
- `quiz`: the quiz on the page, as the Quiz tool writes it. Missing means no quiz.
- `records`: a record page's `{"fields", "rows", "at"}`. Missing means not a record page.
