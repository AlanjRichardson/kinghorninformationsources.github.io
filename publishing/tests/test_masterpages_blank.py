
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Proof test for the intentionally empty H-Blank Page master."""

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
from abden_masterpages import create_master_pages
from abden_styles import (
    create_character_styles,
    create_paragraph_styles,
    discover_fonts,
)


def main():
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

    # create_master_pages() builds all eight masters. Several of them use
    # paragraph styles for running headers and page numbers, so the house
    # styles must exist before the master-page set is created.
    fonts = discover_fonts()
    create_character_styles(fonts)
    create_paragraph_styles()
    create_master_pages()

    scribus.applyMasterPage(MASTER_PAGES["blank"], 1)
    scribus.gotoPage(1)

    objects = scribus.getAllObjects()
    if objects:
        raise RuntimeError(
            "The blank page contains unexpected objects: " + ", ".join(objects)
        )

    scribus.redrawAll()
    scribus.messageBox(
        "Abden Blank Page Test v0.4.0",
        "H-Blank Page passed. The page contains no header, page number or other object.",
        scribus.ICON_INFORMATION,
        scribus.BUTTON_OK,
    )


if __name__ == "__main__":
    try:
        main()
    except Exception:
        details = traceback.format_exc()
        try:
            scribus.messageBox(
                "Abden Blank Page Test — error",
                details,
                scribus.ICON_CRITICAL,
                scribus.BUTTON_OK,
            )
        except Exception:
            print(details)
