"""A folder of PNG pages for proofing. No window.

Foolbook's `draw` paints the page, the same call the stage makes. Here it
paints onto `PngCanvas`, which keeps the handful of canvas calls `draw`
uses and turns them into Pillow drawing. Pillow is already a Foolbook
dependency. Fonts are Pillow's built-in face at the shape's size, so the
words are where the stage puts them but not in the book's face.
"""

from __future__ import annotations

import base64
import io
import re
from contextlib import contextmanager
from pathlib import Path

PAGE = (640, 480)


class _Photo:
    def __init__(self, image):
        self.image = image


class PngCanvas:
    """The canvas calls `engine.graphics.draw` makes, painted with Pillow."""

    def __init__(self, width: int, height: int, paper: str = "#ffffff"):
        from PIL import Image, ImageDraw
        self.image = Image.new("RGB", (width, height), self._rgb(paper) or (255, 255, 255))
        self.pen = ImageDraw.Draw(self.image)
        self.items = 0

    def _rgb(self, color):
        if not color:
            return None
        from PIL import ImageColor
        try:
            return ImageColor.getrgb(str(color))
        except ValueError:
            return None

    def _drew(self) -> int:
        self.items += 1
        return self.items

    def find_all(self):
        return list(range(1, self.items + 1))

    def create_rectangle(self, x0, y0, x1, y1, fill="", outline="black", **_):
        box = [min(x0, x1), min(y0, y1), max(x0, x1) - 1, max(y0, y1) - 1]
        if box[2] >= box[0] and box[3] >= box[1]:
            self.pen.rectangle(box, fill=self._rgb(fill), outline=self._rgb(outline))
        return self._drew()

    def create_oval(self, x0, y0, x1, y1, fill="", outline="black", **_):
        box = [min(x0, x1), min(y0, y1), max(x0, x1) - 1, max(y0, y1) - 1]
        if box[2] >= box[0] and box[3] >= box[1]:
            self.pen.ellipse(box, fill=self._rgb(fill), outline=self._rgb(outline))
        return self._drew()

    def create_polygon(self, *flat, fill="", outline="", **_):
        points = list(zip(flat[0::2], flat[1::2]))
        if len(points) >= 3:
            self.pen.polygon(points, fill=self._rgb(fill), outline=self._rgb(outline))
        return self._drew()

    def create_line(self, *flat, fill="black", width=1, **_):
        points = list(zip(flat[0::2], flat[1::2]))
        if len(points) >= 2 and self._rgb(fill):
            self.pen.line(points, fill=self._rgb(fill), width=int(width or 1))
        return self._drew()

    def create_text(self, x, y, text="", anchor="nw", font=None, fill="black", width=0, **_):
        face = _font(font)
        lines = _wrap(str(text), face, int(width or 0))
        step = int(face.size * 1.2) if hasattr(face, "size") else 14
        tall = step * len(lines)
        wide = max((self.pen.textlength(line, font=face) for line in lines), default=0)
        left, top = x, y
        if anchor in ("w", "center", "e"):
            top = y - tall / 2
        if anchor == "center":
            left = x - wide / 2
        elif anchor == "e":
            left = x - wide
        ink = self._rgb(fill) or (0, 0, 0)
        for i, line in enumerate(lines):
            self.pen.text((left, top + i * step), line, fill=ink, font=face)
        return self._drew()

    def create_image(self, x, y, image=None, anchor="nw", **_):
        picture = getattr(image, "image", None)
        if picture is not None:
            self.image.paste(picture, (int(x), int(y)), picture if picture.mode == "RGBA" else None)
        return self._drew()


def _font(font):
    from PIL import ImageFont
    size = 12
    if isinstance(font, tuple) and len(font) >= 2:
        size = abs(int(font[1])) or 12
    return ImageFont.load_default(size=size)


def _wrap(text: str, face, width: int) -> list[str]:
    from PIL import Image, ImageDraw
    if width <= 0:
        return text.split("\n")
    pen = ImageDraw.Draw(Image.new("1", (1, 1)))
    out = []
    for para in text.split("\n"):
        line = ""
        for word in re.split(r"(\s+)", para):
            trial = line + word
            if line and pen.textlength(trial.rstrip(), font=face) > width:
                out.append(line.rstrip())
                line = word.lstrip()
            else:
                line = trial
        out.append(line.rstrip())
    return out


@contextmanager
def _pictures():
    """`draw` asks Tk for a photo. Here the photo is the Pillow image itself."""
    from engine import graphics
    kept = graphics._photo

    def photo(_canvas, shape, base):
        from PIL import Image
        try:
            if shape.get("src") and base:
                image = Image.open(Path(base) / shape["src"])
            elif shape.get("data"):
                image = Image.open(io.BytesIO(base64.b64decode(shape["data"])))
            else:
                return None
            image = image.convert("RGBA")
            width, height = int(shape.get("w") or 0), int(shape.get("h") or 0)
            if width > 1 and height > 1 and image.size != (width, height):
                image = image.resize((width, height), Image.Resampling.NEAREST)
            return _Photo(image)
        except Exception:
            return None

    graphics._photo = photo
    try:
        yield
    finally:
        graphics._photo = kept


def page_shapes(book: dict, page: dict, base: str | Path | None = None) -> list[dict]:
    """What the reader paints: the shared background, then the page. Hidden stays hidden."""
    from author.document import background_of
    under = background_of(book, page)
    rows = [dict(shape, layer=shape.get("layer") or "background") for shape in (under or {}).get("shapes") or []]
    rows += [shape for shape in page.get("shapes") or [] if isinstance(shape, dict)]
    return [_embedded(shape, base) for shape in rows]


def _embedded(shape: dict, base) -> dict:
    """A button's picture file is read here, so `draw` takes the photo path, not Tk's file loader."""
    if shape.get("kind") != "button" or not shape.get("src"):
        return shape
    path = Path(shape["src"])
    if not path.is_file() and base:
        path = Path(base) / shape["src"]
    copy = dict(shape)
    copy.pop("src")
    if path.is_file():
        copy["data"] = base64.b64encode(path.read_bytes()).decode("ascii")
    return copy


def export_pngs(book: dict, folder: str | Path, base: str | Path | None = None) -> list[Path]:
    """Write NNN_<id>.png for every page that is not a background. Returns the files."""
    from engine.graphics import draw
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    written = []
    number = 0
    with _pictures():
        for page in book.get("pages") or []:
            if page.get("background"):
                continue
            number += 1
            size = page.get("size") or book.get("size") or PAGE
            canvas = PngCanvas(int(size[0]), int(size[1]), page.get("fill") or "#ffffff")
            draw(canvas, page_shapes(book, page, base), base=base)
            safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", str(page.get("id") or "page"))
            out = folder / f"{number:03d}_{safe}.png"
            canvas.image.save(out)
            written.append(out)
    return written
