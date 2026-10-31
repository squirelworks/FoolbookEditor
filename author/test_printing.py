"""Print writes the PNG pages and sends them only when the platform has one call for it."""

import tempfile
import unittest

from author.printing import print_book, printer


class Printer(unittest.TestCase):
    def test_windows_prints_each_file_with_startfile(self):
        calls = []
        send = printer("win32", start=lambda path, verb: calls.append((path, verb)))
        send(["a.png", "b.png"])
        self.assertEqual(calls, [("a.png", "print"), ("b.png", "print")])

    def test_lpr_prints_all_pages_in_one_call(self):
        runs = []
        send = printer("linux", which=lambda name: "/usr/bin/lpr" if name == "lpr" else None,
                       run=lambda argv, check: runs.append(argv))
        send(["a.png", "b.png"])
        self.assertEqual(runs, [["/usr/bin/lpr", "a.png", "b.png"]])

    def test_without_lpr_there_is_no_printer(self):
        self.assertIsNone(printer("darwin", which=lambda name: None))


class PrintBook(unittest.TestCase):
    def setUp(self):
        try:
            import PIL  # noqa: F401
            import engine.graphics  # noqa: F401
        except ImportError:
            self.skipTest("the PNG pages need Pillow and Foolbook")

    def test_the_pages_are_written_and_sent(self):
        book = {"pages": [{"id": "P0", "shapes": []}, {"id": "P1", "shapes": []}]}
        sent = []
        with tempfile.TemporaryDirectory() as tmp:
            written, printed = print_book(book, tmp, send=sent.append)
            self.assertEqual(len(written), 2)
            self.assertTrue(printed)
            self.assertEqual(sent, [written])

    def test_without_a_printer_the_pages_are_the_print(self):
        book = {"pages": [{"id": "P0", "shapes": []}]}
        with tempfile.TemporaryDirectory() as tmp:
            written, printed = print_book(book, tmp, send=None)
            self.assertEqual((len(written), printed), (1, False))
            self.assertTrue(written[0].exists())


if __name__ == "__main__":
    unittest.main()
