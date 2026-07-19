#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Proof test for the Abden G-Full Page Figure layout."""

import sys
import traceback
from pathlib import Path

try:
    import scribus
except ImportError:
    raise SystemExit("Run this script inside Scribus: Script > Execute Script…")

GENERATOR_DIR = Path(__file__).resolve().parent.parent / "generator"
if str(GENERATOR_DIR) not in sys.path:
    sys.path.insert(0, str(GENERATOR_DIR))

from abden_config import MASTER_PAGES, PAGE
from abden_layout import create_figure_specimen
from abden_masterpages import create_master_pages
from abden_styles import create_character_styles, create_paragraph_styles, discover_fonts


def run():
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
        raise RuntimeError("Scribus could not create the test document.")

    scribus.setDocType(scribus.FACINGPAGES, scribus.FIRSTPAGERIGHT)
    scribus.setRedraw(False)
    try:
        fonts = discover_fonts()
        create_character_styles(fonts)
        create_paragraph_styles()
        create_master_pages()
        scribus.applyMasterPage(MASTER_PAGES["figure"], 1)
        create_figure_specimen(1)
        scribus.docChanged(True)
    finally:
        scribus.setRedraw(True)
        scribus.redrawAll()

    scribus.messageBox(
        "Abden figure-page test",
        "The right-hand page should contain:\n\n"
        "• a large empty image frame within the text margins;\n"
        "• an editable figure caption beneath it;\n"
        "• an editable source/credit line;\n"
        "• a page number at the outside bottom-right corner;\n"
        "• no running header.",
        scribus.ICON_INFORMATION,
        scribus.BUTTON_OK,
    )


if __name__ == "__main__":
    try:
        run()
    except Exception:
        details = traceback.format_exc()
        try:
            scribus.messageBox(
                "Abden figure-page test — error",
                details,
                scribus.ICON_CRITICAL,
                scribus.BUTTON_OK,
            )
        except Exception:
            print(details)
