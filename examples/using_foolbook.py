"""Write Using Foolbook, the manual a new Foolbook install opens.

  python3 examples/using_foolbook.py /path/to/Foolbook/_books/using_foolbook

The book is made with the editor's model calls, page by page, so the copy
in Foolbook's sample folder is something a person can regenerate. A test
writes it again and compares it with that copy.
"""

from __future__ import annotations

import sys
from pathlib import Path

_root = Path(__file__).resolve().parents[1]
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from author.catalog import place_shape  # noqa: E402
from author.document import add_page, set_id, set_text  # noqa: E402
from foolbookeditor.core import save_book  # noqa: E402

INK = "#0b1c3d"
GOLD = "#e6b325"
PAPER = "#f4f0e6"
WHITE = "#ffffff"
BLACK = "#1a1a1a"
GREY = "#3d4a5c"
CORAL = "#e36b4a"


def _page(book: dict, page_id: str, text: list[str], items: list[dict]) -> dict:
    at = add_page(book)
    page = book["pages"][at]
    set_id(page, page_id)
    set_text(page, text)
    page["items"] = [dict(item) for item in items]
    page.pop("widgets", None)
    page["shapes"] = []
    return page


def _frame(page: dict, title: str) -> None:
    """Paper, the band, the gold edge, and the title in the band."""
    _box(page, 0, 0, 720, 500, PAPER, PAPER)
    _box(page, 0, 0, 720, 58, INK, INK)
    _box(page, 0, 0, 10, 500, GOLD, GOLD)
    _text(page, 28, 14, 560, 34, title, WHITE, 22, True)


def _box(page: dict, x: int, y: int, w: int, h: int, fill: str | None, outline: str) -> None:
    shape = {"kind": "rect", "x": x, "y": y, "w": w, "h": h}
    if fill is not None:
        shape["fill"] = fill
    shape["outline"] = outline
    place_shape(page, shape)


def _oval(page: dict, x: int, y: int, w: int, h: int, fill: str, outline: str) -> None:
    place_shape(page, {"kind": "ellipse", "x": x, "y": y, "w": w, "h": h, "fill": fill, "outline": outline})


def _polygon(page: dict, points: list[list[int]], fill: str, outline: str) -> None:
    place_shape(page, {"kind": "polygon", "points": [list(pt) for pt in points], "fill": fill, "outline": outline})


def _text(page: dict, x: int, y: int, w: int, h: int, text: str, ink: str, size: int, bold: bool) -> None:
    place_shape(page, {"kind": "text", "x": x, "y": y, "w": w, "h": h, "text": text, "outline": ink, "size": size, "bold": bold})


def _button(page: dict, label: str, target: str, x: int, y: int, w: int, h: int, book: str | None = None) -> None:
    item = {"label": label, "page": target}
    if book:
        item["book"] = book
    place_shape(page, {
        "kind": "button", "name": label, "text": label, "x": x, "y": y, "w": w, "h": h,
        "fill": INK, "outline": INK, "size": 15, "item": item,
    })


def using_foolbook() -> dict:
    book = {"id": "using_foolbook", "title": "Using Foolbook", "subject": "Foolbook", "module": "Start here", "pages": []}
    p = _page(book, 'P0', ['Using Foolbook', 'How to open a book, move through it, and use what is on the page.'], [{'label': 'Start', 'page': 'P10'}, {'label': 'Open First Light', 'page': 'P0', 'book': 'first_light'}])
    _frame(p, 'Using Foolbook')
    _text(p, 28, 90, 460, 70, 'Using Foolbook', INK, 40, True)
    _text(p, 28, 168, 460, 40, 'How to open a book, move through it,\nand use what is on the page.', GREY, 18, False)
    _oval(p, 500, 100, 170, 170, GOLD, GOLD)
    _oval(p, 528, 78, 150, 150, INK, INK)
    _box(p, 548, 200, 28, 28, CORAL, CORAL)
    _oval(p, 590, 200, 28, 28, WHITE, WHITE)
    _polygon(p, [[640, 228], [654, 200], [668, 228]], GOLD, GOLD)
    _button(p, 'Start', 'P10', 28, 250, 160, 36)
    _button(p, 'Open First Light', 'P0', 204, 250, 200, 36, book='first_light')

    p = _page(book, 'P10', ['Contents', 'Pick a part.'], [{'label': 'What a book is', 'page': 'P20'}, {'label': 'The window', 'page': 'P30'}, {'label': 'The shelf', 'page': 'P40'}, {'label': 'Open a file', 'page': 'P50'}, {'label': 'Pages', 'page': 'P60'}, {'label': 'Next and Back', 'page': 'P70'}, {'label': 'A click', 'page': 'P80'}, {'label': 'Words', 'page': 'P90'}, {'label': 'Pictures', 'page': 'P100'}, {'label': 'Shapes', 'page': 'P110'}, {'label': 'Another book', 'page': 'P120'}, {'label': 'ToolBook files', 'page': 'P130'}, {'label': 'Foolcourse', 'page': 'P140'}, {'label': 'When a picture is missing', 'page': 'P150'}, {'label': 'Check yourself', 'page': 'P160'}, {'label': 'Cover', 'page': 'P0'}])
    _frame(p, 'Contents')
    _text(p, 28, 74, 640, 28, 'Pick a part. Next walks the book in order.', GREY, 16, False)
    _button(p, 'What a book is', 'P20', 28, 118, 310, 36)
    _button(p, 'The window', 'P30', 368, 118, 310, 36)
    _button(p, 'The shelf', 'P40', 28, 164, 310, 36)
    _button(p, 'Open a file', 'P50', 368, 164, 310, 36)
    _button(p, 'Pages', 'P60', 28, 210, 310, 36)
    _button(p, 'Next and Back', 'P70', 368, 210, 310, 36)
    _button(p, 'A click', 'P80', 28, 256, 310, 36)
    _button(p, 'Words', 'P90', 368, 256, 310, 36)
    _button(p, 'Pictures', 'P100', 28, 302, 310, 36)
    _button(p, 'Shapes', 'P110', 368, 302, 310, 36)
    _button(p, 'Another book', 'P120', 28, 348, 310, 36)
    _button(p, 'ToolBook files', 'P130', 368, 348, 310, 36)
    _button(p, 'Foolcourse', 'P140', 28, 394, 310, 36)
    _button(p, 'When a picture is missing', 'P150', 368, 394, 310, 36)
    _button(p, 'Check yourself', 'P160', 28, 440, 310, 36)

    p = _page(book, 'P20', ['What a book is', 'A Foolbook book is a file. The usual name ends in .fbk. Open it and you get pages. A page is a picture made of words, boxes, and buttons.'], [{'label': 'Contents', 'page': 'P10'}, {'label': 'Back', 'page': 'P0'}, {'label': 'Next', 'page': 'P30'}])
    _frame(p, 'What a book is')
    _text(p, 28, 78, 660, 280, 'A Foolbook book is a file. The usual name ends in .fbk. Open it and\nyou get pages. A page is a picture made of words, boxes, and\nbuttons.\n\nThis book is one of those files. It is here so the program has\nsomething to show on a new install. First Light is the smaller one\nbeside it.', BLACK, 16, False)

    p = _page(book, 'P30', ['The window', 'The window has three jobs. The shelf is the row of books you can open without hunting for a file. The list on the left is the pages of the book that is open. The large area is the page itself.'], [{'label': 'Contents', 'page': 'P10'}, {'label': 'Back', 'page': 'P20'}, {'label': 'Next', 'page': 'P40'}])
    _frame(p, 'The window')
    _text(p, 28, 78, 660, 150, 'The window has three jobs. The shelf is the row of books you can\nopen without hunting for a file. The list on the left is the pages\nof the book that is open. The large area is the page itself.\n\nPrev and Next sit above the page. They move one page at a time. A\nbutton drawn on the page can jump farther than that.', BLACK, 16, False)
    _box(p, 40, 250, 150, 70, '#d9d3c5', INK)
    _text(p, 48, 258, 134, 20, 'Shelf', INK, 14, True)
    _text(p, 48, 280, 134, 30, 'books you can open', GREY, 12, False)
    _box(p, 210, 250, 120, 160, '#f7f4ee', INK)
    _text(p, 218, 258, 104, 20, 'Pages', INK, 14, True)
    _box(p, 218, 286, 104, 16, INK, INK)
    _box(p, 218, 308, 104, 16, '#e7e1d6', '#e7e1d6')
    _box(p, 218, 330, 104, 16, '#e7e1d6', '#e7e1d6')
    _box(p, 348, 250, 330, 160, WHITE, INK)
    _text(p, 360, 262, 300, 22, 'The page', INK, 16, True)
    _text(p, 360, 292, 300, 80, 'Words and pictures\nland here.', BLACK, 15, False)

    p = _page(book, 'P40', ['The shelf', 'The shelf is a convenience, not the library. First Light, Using Foolbook, and Using Grok ship with Foolbook. The tax lessons and the phone lesson come from Foolcourse.'], [{'label': 'Contents', 'page': 'P10'}, {'label': 'Back', 'page': 'P30'}, {'label': 'Next', 'page': 'P50'}])
    _frame(p, 'The shelf')
    _text(p, 28, 78, 660, 280, 'The shelf is a convenience, not the library. First Light, Using\nFoolbook, and Using Grok ship with Foolbook. The tax lessons and the\nphone lesson come from Foolcourse.\n\nClicking a name opens that book from its published file. Your own\nfile is not on the shelf until you use Open a book.', BLACK, 16, False)

    p = _page(book, 'P50', ['Open a file', 'Open a book reads a file from your computer. It does not upload it anywhere. Foolbook accepts .fbk and .fsk. A ToolBook .tbk or .sbk is opened with the ToolBook reader. An .fbk that is really a ToolBook file is still read as ToolBook.'], [{'label': 'Contents', 'page': 'P10'}, {'label': 'Back', 'page': 'P40'}, {'label': 'Next', 'page': 'P60'}])
    _frame(p, 'Open a file')
    _text(p, 28, 78, 660, 280, 'Open a book reads a file from your computer. It does not upload it\nanywhere. Foolbook accepts .fbk and .fsk. A ToolBook .tbk or .sbk is\nopened with the ToolBook reader. An .fbk that is really a ToolBook\nfile is still read as ToolBook.\n\nIf the program cannot read the file, the status line under the\nbuttons says so. The page you had open stays put.', BLACK, 16, False)

    p = _page(book, 'P60', ['Pages', 'Every page has an id, such as P0 or P10. The list on the left shows that id and the first line of words on the page, so you can tell them apart.'], [{'label': 'Contents', 'page': 'P10'}, {'label': 'Back', 'page': 'P50'}, {'label': 'Next', 'page': 'P70'}])
    _frame(p, 'Pages')
    _text(p, 28, 78, 660, 280, 'Every page has an id, such as P0 or P10. The list on the left shows\nthat id and the first line of words on the page, so you can tell\nthem apart.\n\nThe order in the list is the order of the book. Next follows that\norder. A button may skip ahead. The id is the name a button uses. It\nis not a page number printed for a student.', BLACK, 16, False)

    p = _page(book, 'P70', ['Next and Back', 'Next goes to the following page in the list. Back goes to the one before it. On the last page, Next stays there. On the first page, Back stays there.'], [{'label': 'Contents', 'page': 'P10'}, {'label': 'Back', 'page': 'P60'}, {'label': 'Next', 'page': 'P80'}])
    _frame(p, 'Next and Back')
    _text(p, 28, 78, 660, 280, 'Next goes to the following page in the list. Back goes to the one\nbefore it. On the last page, Next stays there. On the first page,\nBack stays there.\n\nThe buttons above the page do the same job. Use those when the page\nitself has no Next of its own. This book puts Next on the pages so\nyou can stay inside the page.', BLACK, 16, False)

    p = _page(book, 'P80', ['A click', 'A button is a click that names a page. If the page is in this book, you go there. If the name is another book, Foolbook looks on the shelf. First Light, on the cover of this book, is that kind of click.'], [{'label': 'Contents', 'page': 'P10'}, {'label': 'Back', 'page': 'P70'}, {'label': 'Next', 'page': 'P90'}, {'label': 'Open First Light', 'page': 'P0', 'book': 'first_light'}])
    _frame(p, 'A click')
    _text(p, 28, 78, 660, 280, 'A button is a click that names a page. If the page is in this book,\nyou go there. If the name is another book, Foolbook looks on the\nshelf. First Light, on the cover of this book, is that kind of\nclick.\n\nIf the book is not on the shelf, the status line tells you the name.\nOpen that file yourself. The website viewer can also ask the page\naround it, which is how Foolcourse hands over a lesson.', BLACK, 16, False)

    p = _page(book, 'P90', ['Words', 'Words are a text shape. They have a place, a width, a size, and a color. A line break in the text is a new line. The box clips anything that does not fit, so a short box hides the end of a sentence.'], [{'label': 'Contents', 'page': 'P10'}, {'label': 'Back', 'page': 'P80'}, {'label': 'Next', 'page': 'P100'}])
    _frame(p, 'Words')
    _text(p, 28, 78, 660, 280, 'Words are a text shape. They have a place, a width, a size, and a\ncolor. A line break in the text is a new line. The box clips\nanything that does not fit, so a short box hides the end of a\nsentence.\n\nColor is the ink. On a dark header the ink is white. On the paper it\nis near black. If both the ink and the fill are pale, the viewer\ndarkens the ink so the line can be read.', BLACK, 16, False)

    p = _page(book, 'P100', ['Pictures', 'A picture in a Foolbook file is stored with the page and drawn in its box. A ToolBook picture is read from the file when the page opens and turned into a PNG, because a browser will not reliably draw the original bitmap.'], [{'label': 'Contents', 'page': 'P10'}, {'label': 'Back', 'page': 'P90'}, {'label': 'Next', 'page': 'P110'}])
    _frame(p, 'Pictures')
    _text(p, 28, 78, 660, 280, 'A picture in a Foolbook file is stored with the page and drawn in\nits box. A ToolBook picture is read from the file when the page\nopens and turned into a PNG, because a browser will not reliably\ndraw the original bitmap.\n\nA button face is a picture with a click. If the face is missing, the\nbutton is still a button: the words on it are the click.', BLACK, 16, False)

    p = _page(book, 'P110', ['Shapes', 'A page is built from a few kinds of shape. A rect is a box. An ellipse is a round. A polygon is a run of points, used here as a roof. Text is words. A button is a rect that goes somewhere.'], [{'label': 'Contents', 'page': 'P10'}, {'label': 'Back', 'page': 'P100'}, {'label': 'Next', 'page': 'P120'}])
    _frame(p, 'Shapes')
    _text(p, 28, 78, 660, 150, 'A page is built from a few kinds of shape. A rect is a box. An\nellipse is a round. A polygon is a run of points, used here as a\nroof. Text is words. A button is a rect that goes somewhere.\n\nNothing on this page is a photograph. It is the same drawing the\nfirst short book used, kept so you can see the pieces.', BLACK, 16, False)
    _box(p, 40, 268, 200, 150, '#8ecae6', '#8ecae6')
    _oval(p, 560, 250, 64, 64, '#ffb703', '#ffb703')
    _polygon(p, [[40, 340], [140, 268], [240, 340]], '#2a9d8f', '#2a9d8f')
    _box(p, 100, 340, 70, 78, '#f6f1e7', '#c4b8a4')
    _polygon(p, [[86, 342], [135, 292], [184, 342]], CORAL, CORAL)
    _box(p, 124, 372, 22, 46, '#6b3a2a', '#6b3a2a')
    _text(p, 270, 300, 270, 80, 'Rect, ellipse, polygon.\nThe house is three of each.', INK, 16, True)

    p = _page(book, 'P120', ['Another book', 'Some clicks leave the book. The cover of this one opens First Light at its first page. Foolcourse does the same thing when you pick a lesson: it tells the viewer the address of that .fbk.'], [{'label': 'Contents', 'page': 'P10'}, {'label': 'Back', 'page': 'P110'}, {'label': 'Next', 'page': 'P130'}])
    _frame(p, 'Another book')
    _text(p, 28, 78, 660, 280, 'Some clicks leave the book. The cover of this one opens First Light\nat its first page. Foolcourse does the same thing when you pick a\nlesson: it tells the viewer the address of that .fbk.\n\nThe viewer does not keep a private copy of every course. It opens\nthe file it was given. That is why a lesson can live in another\nrepository and still show up here.', BLACK, 16, False)

    p = _page(book, 'P130', ['ToolBook files', 'ToolBook books end in .tbk. The matching system books end in .sbk. Foolbook reads those formats. Pages, fields, buttons, and the pictures it knows how to pull out are drawn. A click that says go to a page follows that page.'], [{'label': 'Contents', 'page': 'P10'}, {'label': 'Back', 'page': 'P120'}, {'label': 'Next', 'page': 'P140'}])
    _frame(p, 'ToolBook files')
    _text(p, 28, 78, 660, 280, 'ToolBook books end in .tbk. The matching system books end in .sbk.\nFoolbook reads those formats. Pages, fields, buttons, and the\npictures it knows how to pull out are drawn. A click that says go to\na page follows that page.\n\nA click that names a page in a different ToolBook file is reported,\nnot invented. You open the other file. The website does not store\nthose files.', BLACK, 16, False)

    p = _page(book, 'P140', ['Foolcourse', 'Foolcourse is the shelf of a curriculum. It lists subjects, modules, and lessons. Foolbook is the window a lesson opens in. On the website, Foolcourse puts Foolbook in a frame and sends it the lesson.'], [{'label': 'Contents', 'page': 'P10'}, {'label': 'Back', 'page': 'P130'}, {'label': 'Next', 'page': 'P150'}])
    _frame(p, 'Foolcourse')
    _text(p, 28, 78, 660, 280, 'Foolcourse is the shelf of a curriculum. It lists subjects, modules,\nand lessons. Foolbook is the window a lesson opens in. On the\nwebsite, Foolcourse puts Foolbook in a frame and sends it the\nlesson.\n\nA lesson listed with no file stays in the list and says the book is\nnot in the folder. That is a missing file, not a broken viewer.', BLACK, 16, False)

    p = _page(book, 'P150', ['When a picture is missing', 'If a picture does not load, the words and the buttons are still there. Use the words. A blank rectangle with a name is a picture the file named and the viewer could not draw.'], [{'label': 'Contents', 'page': 'P10'}, {'label': 'Back', 'page': 'P140'}, {'label': 'Next', 'page': 'P160'}])
    _frame(p, 'When a picture is missing')
    _text(p, 28, 78, 660, 280, 'If a picture does not load, the words and the buttons are still\nthere. Use the words. A blank rectangle with a name is a picture the\nfile named and the viewer could not draw.\n\nButtons at the bottom of a page were added because the page named a\ndestination and did not draw the button itself. They are real\nclicks. They are not a second copy of a button you can already see.', BLACK, 16, False)

    p = _page(book, 'P160', ['Check yourself', 'Next, on a page of this book, goes where?'], [{'label': 'It stays on this page.', 'page': 'P161'}, {'label': 'It opens the next page in the list.', 'page': 'P162'}, {'label': 'Contents', 'page': 'P10'}, {'label': 'Back', 'page': 'P150'}])
    _frame(p, 'Check yourself')
    _text(p, 28, 80, 660, 80, 'Next, on a page of this book, goes where?', BLACK, 18, True)
    _button(p, 'It stays on this page.', 'P161', 28, 180, 520, 36)
    _button(p, 'It opens the next page in the list.', 'P162', 28, 228, 520, 36)

    p = _page(book, 'P161', ['Not that one', 'Next follows the list. It does not stay put unless you are already on the last page. Go back and pick the other answer.'], [{'label': 'Contents', 'page': 'P10'}, {'label': 'Back', 'page': 'P160'}])
    _frame(p, 'Not that one')
    _text(p, 28, 78, 660, 280, 'Next follows the list. It does not stay put unless you are already\non the last page. Go back and pick the other answer.', BLACK, 16, False)

    p = _page(book, 'P162', ['That is the one', 'Next is the next page in the book. A button on the page may jump somewhere else, but Next itself does not.'], [{'label': 'Contents', 'page': 'P10'}, {'label': 'Back', 'page': 'P160'}, {'label': 'Next', 'page': 'P170'}])
    _frame(p, 'That is the one')
    _text(p, 28, 78, 660, 280, 'Next is the next page in the book. A button on the page may jump\nsomewhere else, but Next itself does not.', BLACK, 16, False)

    p = _page(book, 'P170', ['One more', 'You open a .tbk file. What should Foolbook do?'], [{'label': 'Refuse it, because it is not an .fbk.', 'page': 'P171'}, {'label': 'Read it as a ToolBook book.', 'page': 'P172'}, {'label': 'Contents', 'page': 'P10'}, {'label': 'Back', 'page': 'P162'}])
    _frame(p, 'One more')
    _text(p, 28, 80, 660, 80, 'You open a .tbk file. What should Foolbook do?', BLACK, 18, True)
    _button(p, 'Refuse it, because it is not an .fbk.', 'P171', 28, 180, 520, 36)
    _button(p, 'Read it as a ToolBook book.', 'P172', 28, 228, 520, 36)

    p = _page(book, 'P171', ['Not that one', 'The ending tells the reader which rules to use. .tbk and .sbk are ToolBook. An .fbk that still has a ToolBook header is read as ToolBook too.'], [{'label': 'Contents', 'page': 'P10'}, {'label': 'Back', 'page': 'P170'}])
    _frame(p, 'Not that one')
    _text(p, 28, 78, 660, 280, 'The ending tells the reader which rules to use. .tbk and .sbk are\nToolBook. An .fbk that still has a ToolBook header is read as\nToolBook too.', BLACK, 16, False)

    p = _page(book, 'P172', ['That is the one', 'ToolBook files open in the same window. Pictures the reader can pull out are drawn. A page that lives in a different file is named, and you open that file.'], [{'label': 'Contents', 'page': 'P10'}, {'label': 'Back', 'page': 'P170'}, {'label': 'Next', 'page': 'P180'}])
    _frame(p, 'That is the one')
    _text(p, 28, 78, 660, 280, 'ToolBook files open in the same window. Pictures the reader can pull\nout are drawn. A page that lives in a different file is named, and\nyou open that file.', BLACK, 16, False)

    p = _page(book, 'P180', ['You can read a book', 'Open a file, or pick one from the shelf. Use the list when you know the page. Use Next when you do not. Click the thing that says where it goes.'], [{'label': 'Contents', 'page': 'P10'}, {'label': 'Back', 'page': 'P172'}, {'label': 'Cover', 'page': 'P0'}, {'label': 'Open First Light', 'page': 'P0', 'book': 'first_light'}])
    _frame(p, 'You can read a book')
    _text(p, 28, 78, 660, 280, 'Open a file, or pick one from the shelf. Use the list when you know\nthe page. Use Next when you do not. Click the thing that says where\nit goes.\n\nIf you are writing a book, the pages you just saw are the pieces: a\npaper, a header, words, a few shapes, and a button with a page id.\nFirst Light is the short version of the same idea.', BLACK, 16, False)

    return book


def main(argv: list[str] | None = None) -> int:
    argv = list(argv if argv is not None else sys.argv[1:])
    dest = Path(argv[0]) if argv else Path.cwd()
    dest.mkdir(parents=True, exist_ok=True)
    book = using_foolbook()
    print(save_book(dest / "using_foolbook.fbk", book))
    # The sample folder keeps a .json working copy beside the .fbk.
    print(save_book(dest / "using_foolbook.json", book))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
