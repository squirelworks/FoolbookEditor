"""instructor-map.md lists every Instructor job once, and says where it stands."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

MAP = Path(__file__).resolve().parents[1] / "instructor-map.md"

JOBS = (
    "make a book",
    "make a page",
    "make a background",
    "place an object",
    "set properties",
    "write a script",
    "make a quiz",
    "make a menu",
    "import a picture",
    "choose a palette",
    "spellcheck",
    "package a catalog",
    "run as a student",
    "run as an author",
)

STATUS = ("not started", "started", "done")

# Names that belong to the vendor install, not to a job.
VENDOR = re.compile(r"\b\w+\.(exe|dll|sbk|spb|lex|pal)\b|TB80|Inst80|MENUED|PALED|BITED|ICONED", re.I)


def rows() -> dict[str, list[str]]:
    found = {}
    for line in MAP.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 4 and cells[0].lower() in JOBS:
            found.setdefault(cells[0].lower(), []).append(cells)
    return found


class InstructorMapTests(unittest.TestCase):
    def test_every_job_is_listed_once(self):
        found = rows()
        for job in JOBS:
            self.assertEqual(len(found.get(job, [])), 1, job)

    def test_every_job_has_a_status(self):
        for job, [cells] in rows().items():
            self.assertIn(cells[1].lower(), STATUS, job)

    def test_a_job_that_is_not_started_still_names_its_items(self):
        for job, [cells] in rows().items():
            self.assertRegex(cells[2], r"\d", job)

    def test_a_started_job_says_where_it_is(self):
        for job, [cells] in rows().items():
            if cells[1].lower() != "not started":
                self.assertTrue(cells[3] and cells[3] != "-", job)

    def test_the_map_names_jobs_not_vendor_files(self):
        for job, [cells] in rows().items():
            self.assertIsNone(VENDOR.search(" ".join(cells)), job)


if __name__ == "__main__":
    unittest.main()
