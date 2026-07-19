#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Abden Master Template with Scribus 1.6.x."""

import sys
import traceback

try:
    import scribus
except ImportError:
    raise SystemExit("Run this script inside Scribus: Script > Execute Script…")

from abden_config import OUTPUT_TEMPLATE, PAGE, PROJECT
from abden_layout import (
    create_chapter_specimen,
    create_contents_page,
    create_copyright_page,
    create_design_guides,
    create_figure_specimen,
    create_style_specimen,
    create_title_page,
)
from abden_masterpages import apply_master_pages, create_master_pages
from abden_styles import (
    create_character_styles,
    create_paragraph_styles,
    discover_fonts,
)


def _ensure_eight_pages():
    while scribus.pageCount() < 8:
        scribus.newPage(-1)


def build():
    OUTPUT_TEMPLATE.parent.mkdir(parents=True, exist_ok=True)
    fonts = discover_fonts()

    if scribus.haveDoc():
        response = scribus.messageBox(
            "Abden Generator v0.4.0",
            "A document is already open.\n\nThe generator will create a new document.",
            scribus.ICON_INFORMATION,
            scribus.BUTTON_OK | scribus.BUTTON_CANCEL,
        )
        if response == scribus.BUTTON_CANCEL:
            return

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
        2,
    )
    if not created:
        raise RuntimeError("Scribus could not create the document.")

    scribus.setDocType(scribus.FACINGPAGES, scribus.FIRSTPAGERIGHT)
    scribus.setInfo(
        PROJECT["author"],
        PROJECT["series"],
        "Abden Publishing Generator v0.4.0 master-page and house-style proof.",
    )
    scribus.setBleeds(0.0, 0.0, 0.0, 0.0)

    scribus.setRedraw(False)
    try:
        _ensure_eight_pages()
        create_character_styles(fonts)
        create_paragraph_styles()
        create_master_pages()
        apply_master_pages()

        create_title_page(fonts)
        create_copyright_page()
        create_contents_page()
        create_chapter_specimen(4)
        create_style_specimen(5)
        create_figure_specimen(7)

        scribus.gotoPage(1)
        create_design_guides()
        scribus.docChanged(True)
        scribus.saveDocAs(str(OUTPUT_TEMPLATE))
    finally:
        scribus.setRedraw(True)
        scribus.redrawAll()

    scribus.messageBox(
        "Abden Generator v0.4.0",
        "Created:\n\n" + str(OUTPUT_TEMPLATE)
        + "\n\nThe document contains eight master pages, running furniture, "
          "automatic page-number tokens and the expanded Abden house style.",
        scribus.ICON_INFORMATION,
        scribus.BUTTON_OK,
    )


if __name__ == "__main__":
    try:
        build()
    except Exception:
        details = traceback.format_exc()
        try:
            scribus.messageBox(
                "Abden Generator v0.4.0 — error",
                details,
                scribus.ICON_CRITICAL,
                scribus.BUTTON_OK,
            )
        except Exception:
            print(details)
