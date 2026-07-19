#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Isolated proof for Abden chapter, left, and right master pages.

Run inside Scribus with Script > Execute Script.
"""

import sys
from pathlib import Path

import scribus

TESTS_DIR = Path(__file__).resolve().parent
GENERATOR_DIR = TESTS_DIR.parent / "generator"
if str(GENERATOR_DIR) not in sys.path:
    sys.path.insert(0, str(GENERATOR_DIR))

from abden_config import MASTER_PAGES, PAGE  # noqa: E402
from abden_masterpages import (  # noqa: E402
    create_body_master_pages,
    create_chapter_opening_content,
)
from abden_styles import (  # noqa: E402
    create_character_styles,
    create_paragraph_styles,
    discover_fonts,
)


def build_test():
    fonts = discover_fonts()

    created = scribus.newDocument(
        scribus.PAPER_A4_MM,
        (
            PAGE["inside_mm"],
            PAGE["outside_mm"],
            PAGE["top_mm"],
            PAGE["bottom_mm"],
        ),
        scribus.PORTRAIT,
        1,
        scribus.UNIT_MILLIMETERS,
        scribus.PAGE_2,
        1,
        3,
    )
    if not created:
        raise RuntimeError("Scribus could not create the Phase 2 test document.")

    scribus.setDocType(scribus.FACINGPAGES, scribus.FIRSTPAGERIGHT)

    # Some Scribus versions create fewer physical pages than requested when a
    # facing-page document begins on the right. Ensure that three pages exist.
    while scribus.pageCount() < 3:
        scribus.newPage(-1)

    scribus.setRedraw(False)
    try:
        create_character_styles(fonts)
        create_paragraph_styles()
        create_body_master_pages()

        # The proof sequence intentionally shows the three body-page types.
        scribus.applyMasterPage(MASTER_PAGES["right"], 1)
        scribus.applyMasterPage(MASTER_PAGES["left"], 2)
        scribus.applyMasterPage(MASTER_PAGES["chapter"], 3)

        scribus.gotoPage(3)
        create_chapter_opening_content(
            "CHAPTER 1",
            "Origins and Development of the Abden Shipyard",
        )

        scribus.gotoPage(1)
        scribus.docChanged(True)
    finally:
        scribus.setRedraw(True)
        scribus.redrawAll()

    scribus.messageBox(
        "Abden body master-page test",
        "Phase 2 created successfully.\n\n"
        "Page 1: F-Right Page\n"
        "Page 2: E-Left Page\n"
        "Page 3: D-Chapter Opening\n\n"
        "Page 3 should have no running header, an outside page number, "
        "and editable chapter number/title frames.",
        scribus.ICON_INFORMATION,
        scribus.BUTTON_OK,
    )


if __name__ == "__main__":
    build_test()
