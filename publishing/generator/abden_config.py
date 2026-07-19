# -*- coding: utf-8 -*-
"""Central configuration for the Abden Publishing Generator v0.3.0."""

from pathlib import Path

GENERATOR_DIR = Path(__file__).resolve().parent
PUBLISHING_DIR = GENERATOR_DIR.parent
TEMPLATES_DIR = PUBLISHING_DIR / "templates"
STYLE_GUIDE_DIR = PUBLISHING_DIR / "style-guide"
DOCUMENTATION_DIR = PUBLISHING_DIR / "documentation"
ASSETS_DIR = PUBLISHING_DIR / "assets"
TESTS_DIR = PUBLISHING_DIR / "tests"
OUTPUT_TEMPLATE = TEMPLATES_DIR / "Abden_Master_Template.sla"

PROJECT = {
    "series": "The Abden Shipyard Reconstruction Project",
    "volume": "Volume I",
    "title": "Historical Synopsis and Reconstruction Guide",
    "author": "Alan Richardson",
    "imprint": "Kinghorn Information Sources",
    "generator_version": "0.3.6",
}

PAGE = {
    "size": "A4",
    "width_mm": 210.0,
    "height_mm": 297.0,
    "inside_mm": 25.0,
    "outside_mm": 20.0,
    "top_mm": 20.0,
    "bottom_mm": 25.0,
    "header_y_mm": 11.0,
    "header_height_mm": 6.0,
    "footer_y_mm": 278.0,
    "footer_height_mm": 7.0,
}

FIGURE_LAYOUT = {
    # Vertical arrangement for a full-page figure on a normal text page.
    # Values are millimetres and are shared by the generator and tests.
    "image_y_mm": 28.0,
    "image_height_mm": 190.0,
    "caption_gap_mm": 5.0,
    "caption_height_mm": 22.0,
    "source_gap_mm": 1.5,
    "source_height_mm": 12.0,
}

TYPOGRAPHY = {
    "body_size": 11.5,
    "body_leading": 14.0,
    "chapter_number_size": 18.0,
    "chapter_number_leading": 26.0,
    "chapter_title_size": 24.0,
    "chapter_title_leading": 35.0,
    "heading_1_size": 16.0,
    "heading_1_leading": 20.0,
    "heading_2_size": 13.0,
    "heading_2_leading": 17.0,
    "heading_3_size": 11.5,
    "heading_3_leading": 15.0,
    "caption_size": 10.0,
    "caption_leading": 12.0,
    "footnote_size": 9.0,
    "footnote_leading": 11.0,
    "running_size": 9.0,
    "running_leading": 11.0,
    "quote_size": 10.5,
    "quote_leading": 13.0,
    "archive_size": 10.0,
    "archive_leading": 12.5,
    "bibliography_size": 10.5,
    "bibliography_leading": 13.0,
}

MASTER_PAGES = {
    "title": "A-Title",
    "copyright": "B-Copyright",
    "contents": "C-Contents",
    "chapter": "D-Chapter Opening",
    "left": "E-Left Page",
    "right": "F-Right Page",
    "figure": "G-Full Page Figure",
    "blank": "H-Blank Page",
}
