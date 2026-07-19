#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Isolated proof for the Abden A-Title master page.

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
from abden_masterpages import create_title_master_page, create_title_page_content  # noqa: E402
from abden_styles import create_character_styles, create_paragraph_styles, discover_fonts  # noqa: E402


def build_test():
    fonts = discover_fonts()
    created = scribus.newDocument(
        scribus.PAPER_A4_MM,
        (PAGE["inside_mm"], PAGE["outside_mm"], PAGE["top_mm"], PAGE["bottom_mm"]),
        scribus.PORTRAIT,
        1,
        scribus.UNIT_MILLIMETERS,
        scribus.PAGE_2,
        1,
        1,
    )
    if not created:
        raise RuntimeError("Scribus could not create the Phase 3 title-page test document.")

    scribus.setDocType(scribus.FACINGPAGES, scribus.FIRSTPAGERIGHT)
    scribus.setRedraw(False)
    try:
        create_character_styles(fonts)
        create_paragraph_styles()
        create_title_master_page()
        scribus.applyMasterPage(MASTER_PAGES["title"], 1)
        scribus.gotoPage(1)
        create_title_page_content()
        scribus.docChanged(True)
    finally:
        scribus.setRedraw(True)
        scribus.redrawAll()

    scribus.messageBox(
        "Abden title master-page test",
        "Phase 3 created successfully.\n\n"
        "Page 1: A-Title\n\n"
        "The page should have centred, editable title content, generous white space, "
        "and no running header or page number.",
        scribus.ICON_INFORMATION,
        scribus.BUTTON_OK,
    )


if __name__ == "__main__":
    build_test()
