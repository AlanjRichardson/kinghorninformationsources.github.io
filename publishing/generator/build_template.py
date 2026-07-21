#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Abden framework-freeze template with Scribus 1.6.x."""

import sys
import traceback

try:
    import scribus
except ImportError:
    raise SystemExit("Run this script inside Scribus: Script > Execute Script…")

from abden_config import OUTPUT_TEMPLATE, PAGE, PROJECT
from abden_layout import (
    create_analysis_page,
    create_appendix_page,
    create_chapter_opening,
    create_contents_page,
    create_copyright_page,
        create_feature_record,
        create_reconstruction_page,
    create_front_matter_pages,
    create_title_page,
)
from abden_masterpages import apply_master_pages, create_master_pages
from abden_styles import create_character_styles, create_paragraph_styles, discover_fonts

PAGE_COUNT = 14


def _ensure_pages():
    while scribus.pageCount() < PAGE_COUNT:
        scribus.newPage(-1)


def build():
    OUTPUT_TEMPLATE.parent.mkdir(parents=True, exist_ok=True)
    fonts = discover_fonts()

    if scribus.haveDoc():
        response = scribus.messageBox(
            "Abden Generator v%s" % PROJECT["generator_version"],
            "A document is already open.\n\nThe generator will create a new document.",
            scribus.ICON_INFORMATION,
            scribus.BUTTON_OK | scribus.BUTTON_CANCEL,
        )
        if response == scribus.BUTTON_CANCEL:
            return

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
        raise RuntimeError("Scribus could not create the document.")

    scribus.setDocType(scribus.FACINGPAGES, scribus.FIRSTPAGERIGHT)
    scribus.setInfo(
        PROJECT["author"],
        PROJECT["series"],
        "Abden Publishing Generator v%s research environment; manuscript %s."
        % (PROJECT["generator_version"], PROJECT["manuscript_version"]),
    )
    scribus.setBleeds(0.0, 0.0, 0.0, 0.0)

    scribus.setRedraw(False)
    try:
        _ensure_pages()
        create_character_styles(fonts)
        create_paragraph_styles()
        create_master_pages()
        apply_master_pages()

        create_title_page(fonts)
        create_copyright_page()
        create_contents_page(3)
        create_chapter_opening(4)
        create_front_matter_pages()
        create_feature_record(8)
        create_analysis_page(9, "Historical Map Analysis", "Map or plan")
        create_analysis_page(10, "Photograph Analysis", "Photograph")
        create_analysis_page(11, "LiDAR and Terrain Analysis", "LiDAR dataset")
        create_reconstruction_page(12)
        create_appendix_page(13)

        scribus.gotoPage(1)
        scribus.docChanged(True)
        scribus.saveDocAs(str(OUTPUT_TEMPLATE))
    finally:
        scribus.setRedraw(True)
        scribus.redrawAll()

    scribus.messageBox(
        "Abden Generator v%s" % PROJECT["generator_version"],
        "Created:\n\n%s\n\nThe permanent eight-master architecture is retained. "
        "The document now includes fourteen working pages for the frozen research, "
        "evidence and Blender-specification framework." % OUTPUT_TEMPLATE,
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
                "Abden Generator v%s — error" % PROJECT["generator_version"],
                details,
                scribus.ICON_CRITICAL,
                scribus.BUTTON_OK,
            )
        except Exception:
            print(details)
