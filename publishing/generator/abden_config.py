# -*- coding: utf-8 -*-
"""Central configuration for the Abden Publishing Generator v0.5.1."""

from pathlib import Path

GENERATOR_DIR = Path(__file__).resolve().parent
PUBLISHING_DIR = GENERATOR_DIR.parent
TEMPLATES_DIR = PUBLISHING_DIR / "templates"
STYLE_GUIDE_DIR = PUBLISHING_DIR / "style-guide"
DOCUMENTATION_DIR = PUBLISHING_DIR / "documentation"
ASSETS_DIR = PUBLISHING_DIR / "assets"
TESTS_DIR = PUBLISHING_DIR / "tests"
OUTPUT_TEMPLATE = TEMPLATES_DIR / "Abden_Master_Template_v0.5.1_working.sla"

PROJECT = {
    "series": "The Abden Shipyard Reconstruction Project",
    "volume": "Volume I",
    "title": "Historical Synopsis and Reconstruction Guide",
    "author": "Alan Richardson",
    "imprint": "Kinghorn Information Sources",
    "generator_version": "0.5.1",
    "document_status": "Working Draft",
    "repository": "Kinghorn Information Sources",
    "publication_date": "",
    "manuscript_version": "Draft 0.1",
    "mission": (
        "An evidence-based digital heritage reconstruction in which Volume I "
        "serves as both the historical research record and the technical "
        "specification for academic review and three-dimensional modelling."
    ),
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

CONTENTS_LAYOUT = {
    "heading_y_mm": 35.0,
    "heading_height_mm": 20.0,
    "entries_y_mm": 62.0,
    "entries_height_mm": 198.0,
    "page_number_tab_mm": 160.0,
}

FIGURE_LAYOUT = {
    "image_y_mm": 28.0,
    "image_height_mm": 190.0,
    "caption_gap_mm": 5.0,
    "caption_height_mm": 22.0,
    "source_gap_mm": 1.5,
    "source_height_mm": 12.0,
}

STATUS_LAYOUT = {
    "panel_y_mm": 164.0,
    "panel_height_mm": 82.0,
    "label_width_mm": 45.0,
    "gutter_mm": 5.0,
}

FEATURE_LAYOUT = {
    "heading_y_mm": 34.0,
    "heading_height_mm": 18.0,
    "metadata_y_mm": 58.0,
    "metadata_height_mm": 68.0,
    "body_y_mm": 134.0,
    "body_height_mm": 120.0,
}

ANALYSIS_LAYOUT = {
    "heading_y_mm": 34.0,
    "heading_height_mm": 18.0,
    "body_y_mm": 60.0,
    "body_height_mm": 194.0,
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
    "technical_size": 10.0,
    "technical_leading": 12.5,
    "status_size": 9.5,
    "status_leading": 12.0,
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

DOCUMENT_STRUCTURE = [
    ("front", "Preface"),
    ("front", "Executive Summary"),
    ("front", "Project Scope"),
    ("front", "Research Methodology"),
    ("front", "Evidence and Confidence System"),
    ("front", "How to Use this Volume"),
    ("front", "List of Figures"),
    ("front", "List of Tables"),
    ("front", "Glossary and Abbreviations"),
    ("part", "Part I — Historical Development"),
    ("chapter", "Chapter 1   The Geography of Abden"),
    ("chapter", "Chapter 2   Kinghorn Before the Shipyard"),
    ("chapter", "Chapter 3   The Development of Abden Shipyard"),
    ("chapter", "Chapter 4   Ownership"),
    ("chapter", "Chapter 5   Industrial Context"),
    ("part", "Part II — Research Evidence"),
    ("chapter", "Chapter 6   Historical Maps"),
    ("chapter", "Chapter 7   Photographic Evidence"),
    ("chapter", "Chapter 8   Engineering Evidence"),
    ("chapter", "Chapter 9   Archaeological Evidence"),
    ("chapter", "Chapter 10   LiDAR"),
    ("chapter", "Chapter 11   QGIS Reconstruction"),
    ("part", "Part III — Physical Reconstruction"),
    ("chapter", "Chapter 12   Overall Site Layout"),
    ("chapter", "Chapter 13   Buildings"),
    ("chapter", "Chapter 14   Marine Structures"),
    ("chapter", "Chapter 15   Railway Infrastructure"),
    ("chapter", "Chapter 16   Slipways"),
    ("chapter", "Chapter 17   Travelling Crane"),
    ("chapter", "Chapter 18   Infrastructure and Services"),
    ("chapter", "Chapter 19   Construction Sequence"),
    ("chapter", "Chapter 20   Operational Workflow"),
    ("part", "Part IV — Interpretation"),
    ("chapter", "Chapter 21   Confidence Assessment"),
    ("chapter", "Chapter 22   Alternative Interpretations"),
    ("chapter", "Chapter 23   Unresolved Questions"),
    ("chapter", "Chapter 24   Recommendations and Future Research"),
    ("appendix", "Appendix A   Feature Register"),
    ("appendix", "Appendix B   Evidence Register"),
    ("appendix", "Appendix C   Photograph Register"),
    ("appendix", "Appendix D   Map Register"),
    ("appendix", "Appendix E   Chronology"),
    ("appendix", "Appendix F   Bibliography"),
    ("appendix", "Appendix G   Index"),
]

CONFIDENCE_LEVELS = (
    "High — directly supported by multiple independent sources",
    "Moderate — supported, but some geometry or interpretation remains uncertain",
    "Low — plausible reconstruction based mainly on indirect evidence",
    "Unknown — insufficient evidence for a defensible reconstruction",
)
