# The book dict

Foolbook reads one dict. The desktop editor and the web editor write it. `author/schema.py` is the same list in code. A field that is here round-trips through Save and Open. A field one editor writes and the other drops is a bug.

An `.fbk` is `FBK1`, a flags byte (bit 0 means zlib), then this dict as JSON. An `.fsk` is the same with `FSK1`.

## Book

- `id`: the book's id, a string.
- `title`: the title the reader shows.
- `pages`: the pages, in reading order.
- `_magic`: the web editor's note of the envelope magic, `FBK1`. It is envelope state, not a field. Neither editor writes it into the payload; the reader never read it.

The reader stamps `format`, `format_version`, `fbk` (the book version, now 1), and `foolbook` (the reader's own version) on every save. The editor drops those before it saves so the reader writes them in its own order.
