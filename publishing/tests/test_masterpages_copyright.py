#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Isolated proof for the Abden B-Copyright master page.

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
    create_copyright_master_page,
    create_copyright_page_content,
)
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
        2,
    )
    if not created:
        raise RuntimeError("Scribus could not create the Phase 4 copyright-page test document.")

    scribus.setDocType(scribus.FACINGPAGES, scribus.FIRSTPAGERIGHT)
    scribus.setRedraw(False)
    try:
        create_character_styles(fonts)
        create_paragraph_styles()
        create_copyright_master_page()
        scribus.applyMasterPage(MASTER_PAGES["copyright"], 2)
        scribus.gotoPage(2)
        create_copyright_page_content()
        scribus.docChanged(True)
    finally:
        scribus.setRedraw(True)
        scribus.redrawAll()

    scribus.messageBox(
        "Abden copyright master-page test",
        "Phase 4 created successfully.\n\n"
        "Page 1 is intentionally blank.\n"
        "Page 2: B-Copyright\n\n"
        "The copyright page should be left-aligned within the correct left-page "
        "margins and should have no running header or page number.",
        scribus.ICON_INFORMATION,
        scribus.BUTTON_OK,
    )


if __name__ == "__main__":
    build_test()
