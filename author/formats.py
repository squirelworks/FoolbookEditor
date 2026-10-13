"""Book envelope.

The format lives with the reader. This module re-exports it so the
editor can load and save .fbk and .json without owning a second copy.
"""

from engine.formats import (  # noqa: F401
    FBK,
    FLAG_COMPRESSED,
    FORMAT_VERSION,
    FSK,
    MAGIC,
    is_book,
    is_system,
    kind_of,
    load,
    pack,
    save_book,
    save_system,
    unpack,
)
