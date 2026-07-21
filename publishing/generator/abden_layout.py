# -*- coding: utf-8 -*-
"""Page construction for the Abden Publishing Generator v0.5.1."""

from datetime import date

import scribus
from abden_config import (
    ANALYSIS_LAYOUT, CONTENTS_LAYOUT, DOCUMENT_STRUCTURE, FEATURE_LAYOUT,
    FIGURE_LAYOUT, PAGE, PROJECT, STATUS_LAYOUT,
)
from abden_styles import apply_whole_frame


def is_right_page(page_number):
    return page_number % 2 == 1


def content_box(page_number):
    if is_right_page(page_number):
        x = PAGE["inside_mm"]
        right_margin = PAGE["outside_mm"]
    else:
        x = PAGE["outside_mm"]
        right_margin = PAGE["inside_mm"]
    y = PAGE["top_mm"]
    width = PAGE["width_mm"] - x - right_margin
    height = PAGE["height_mm"] - PAGE["top_mm"] - PAGE["bottom_mm"]
    return x, y, width, height


def text_frame(page_number, y, height, name):
    x, _, width, _ = content_box(page_number)
    return scribus.createText(x, y, width, height, name)


def set_frame_text(frame, text, style=None, alignment=None):
    scribus.setText(text, frame)
    if style:
        apply_whole_frame(frame, style)
    if alignment is not None:
        scribus.setTextAlignment(alignment, frame)


def styled_lines(frame, entries):
    full_text = "\n".join(text for _, text in entries)
    scribus.setText(full_text, frame)
    start = 0
    for style, text in entries:
        scribus.selectText(start, len(text), frame)
        scribus.setParagraphStyle(style, frame)
        start += len(text) + 1


def create_title_page(fonts):
    page = 1
    scribus.gotoPage(page)
    items = [
        (46, 18, "Title_Series", PROJECT["series"], fonts["sans_regular"], 14),
        (86, 14, "Title_Volume", PROJECT["volume"], fonts["sans_bold"], 16),
        (112, 20, "Title_Main_1", "Historical Synopsis", fonts["sans_bold"], 25),
        (143, 20, "Title_Main_2", "and Reconstruction Guide", fonts["sans_bold"], 25),
        (205, 14, "Title_Author", PROJECT["author"], fonts["serif_regular"], 13),
        (246, 14, "Title_Imprint", PROJECT["imprint"], fonts["sans_regular"], 11),
    ]
    for y, h, name, text, font, size in items:
        frame = text_frame(page, y, h, name)
        scribus.setText(text, frame)
        scribus.setFont(font, frame)
        scribus.setFontSize(size, frame)
        scribus.setTextAlignment(1, frame)


def create_copyright_page():
    page = 2
    scribus.gotoPage(page)
    frame = text_frame(page, 158, 94, "Copyright_Text")
    generated = date.today().strftime("%d %B %Y")
    text = (
        "%s\n%s: %s\n\nCopyright © %s. All rights reserved.\n"
        "Published by %s.\n\nGenerator\nAbden Publishing Generator %s\n\n"
        "Manuscript\n%s\n\nGenerated\n%s\n\nDocument status\n%s\n\nRepository\n%s"
    ) % (
        PROJECT["series"], PROJECT["volume"], PROJECT["title"],
        PROJECT["author"], PROJECT["imprint"], PROJECT["generator_version"],
        PROJECT["manuscript_version"], generated, PROJECT["document_status"],
        PROJECT["repository"],
    )
    set_frame_text(frame, text, "Abden Footnote")


def create_contents_page(page=3):
    scribus.gotoPage(page)
    x, _, width, _ = content_box(page)
    c = CONTENTS_LAYOUT
    heading = scribus.createText(x, c["heading_y_mm"], width, c["heading_height_mm"], "Contents_Heading")
    set_frame_text(heading, "Contents", "Abden Chapter Title")
    body = scribus.createText(x, c["entries_y_mm"], width, c["entries_height_mm"], "Contents_Entries")
    entries = []
    for kind, title in DOCUMENT_STRUCTURE:
        if kind == "part":
            entries.append(("Abden Contents Part", title))
        elif kind == "chapter":
            entries.append(("Abden Contents Chapter", title + "\t00"))
        else:
            entries.append(("Abden Contents Entry", title + "\t00"))
    styled_lines(body, entries)


def create_chapter_opening(page=4):
    scribus.gotoPage(page)
    x, _, width, _ = content_box(page)
    set_frame_text(scribus.createText(x, 44, width, 18, "Chapter_1_Number"), "Chapter 1", "Abden Chapter Number")
    set_frame_text(scribus.createText(x, 68, width, 37, "Chapter_1_Title"), "The Geography of Abden", "Abden Chapter Title")
    intro = scribus.createText(x, 116, width, 38, "Chapter_1_Introduction")
    styled_lines(intro, [
        ("Abden Body First", "This chapter establishes the physical setting of Abden and identifies the natural and altered landscape features that governed the development of the shipyard."),
        ("Abden Body", "Its purpose is to provide the geographical foundation for the historical narrative and the later QGIS and Blender reconstruction."),
    ])
    create_status_panel(page, STATUS_LAYOUT["panel_y_mm"])


def create_status_panel(page=5, y=None):
    scribus.gotoPage(page)
    x, _, width, _ = content_box(page)
    s = STATUS_LAYOUT
    y = s["panel_y_mm"] if y is None else y
    heading = scribus.createText(x, y, width, 12, "Chapter_Status_Heading_%d" % page)
    set_frame_text(heading, "Internal Chapter Status — remove or hide for publication", "Abden Heading 2")
    labels = scribus.createText(x, y + 17, s["label_width_mm"], s["panel_height_mm"] - 17, "Chapter_Status_Labels_%d" % page)
    values = scribus.createText(x + s["label_width_mm"] + s["gutter_mm"], y + 17, width - s["label_width_mm"] - s["gutter_mm"], s["panel_height_mm"] - 17, "Chapter_Status_Values_%d" % page)
    styled_lines(labels, [("Abden Research Status Label", t) for t in [
        "Status:", "Research:", "Evidence:", "Academic review:", "Blender review:", "Last updated:",
    ]])
    styled_lines(values, [("Abden Research Status", t) for t in [
        "Draft", "45%", "High", "Pending", "Not started", "____________",
    ]])


def create_working_section(page, title, purpose, headings):
    scribus.gotoPage(page)
    x, _, width, _ = content_box(page)
    set_frame_text(scribus.createText(x, 34, width, 22, "Working_Heading_%d" % page), title, "Abden Heading 1")
    body = scribus.createText(x, 64, width, 190, "Working_Body_%d" % page)
    entries = [("Abden Body First", purpose)]
    for heading, prompt in headings:
        entries.extend([("Abden Evidence Heading", heading), ("Abden Body", prompt)])
    styled_lines(body, entries)


def create_front_matter_pages():
    create_working_section(5, "Preface",
        "This preface will explain why the reconstruction project was begun, its intended public and academic value, and the author's relationship to the site.",
        [("Origins of the project", "[Draft text]"), ("Purpose of Volume I", "[Draft text]"), ("Acknowledgements", "[Draft text]")])
    create_working_section(6, "Executive Summary",
        "This section will provide academics, heritage organisations and potential collaborators with a concise account of the project's evidence, findings and intended outputs.",
        [("Historical significance", "[Draft text]"), ("Principal evidence", "[Draft text]"), ("Reconstruction outcome", "[Draft text]")])
    create_working_section(7, "Research Methodology",
        "The reconstruction separates observation, interpretation and conjecture, and records the evidence and confidence attached to every significant conclusion.",
        [("Source collection", "Maps, photographs, documentary records, LiDAR and field observations."), ("Spatial analysis", "Georeferencing, digitisation and measurement in QGIS."), ("Confidence system", "High, Moderate, Low and Unknown."), ("Traceability", "Every feature links to controlled evidence-register entries.")])


def create_feature_record(page=8):
    scribus.gotoPage(page)
    x, _, width, _ = content_box(page)
    f = FEATURE_LAYOUT
    heading = scribus.createText(x, f["heading_y_mm"], width, f["heading_height_mm"], "Feature_Record_Heading")
    set_frame_text(heading, "Feature Record", "Abden Heading 1")
    labels = scribus.createText(x, f["metadata_y_mm"], 46, f["metadata_height_mm"], "Feature_Metadata_Labels")
    values = scribus.createText(x + 51, f["metadata_y_mm"], width - 51, f["metadata_height_mm"], "Feature_Metadata_Values")
    styled_lines(labels, [("Abden Metadata Label", t) for t in ["Feature ID:", "Feature name:", "Location:", "Coordinates:", "Current condition:", "Confidence:"]])
    styled_lines(values, [("Abden Metadata Value", t) for t in ["[ID]", "[Preferred name]", "[Location]", "[British National Grid]", "[Condition]", "[High / Moderate / Low / Unknown]"]])
    body = scribus.createText(x, f["body_y_mm"], width, f["body_height_mm"], "Feature_Record_Body")
    styled_lines(body, [
        ("Abden Evidence Heading", "Historical description"), ("Abden Body First", "[Draft text]"),
        ("Abden Evidence Heading", "Evidence"), ("Abden Technical Specification", "Historical; cartographic; photographic; LiDAR; field; engineering."),
        ("Abden Evidence Heading", "Interpretation"), ("Abden Evidence Assessment", "[State the preferred interpretation and alternatives.]"),
        ("Abden Evidence Heading", "Dimensions and construction"), ("Abden Technical Specification", "[Known, measured and estimated values; materials and tolerances.]"),
        ("Abden Evidence Heading", "Blender notes"), ("Abden Blender Note", "[Object hierarchy, units, origin, editable parameters and uncertainty metadata.]"),
        ("Abden Evidence Heading", "Outstanding questions"), ("Abden Outstanding Question", "• [Question]")])


def create_analysis_page(page, title, evidence_label):
    scribus.gotoPage(page)
    x, _, width, _ = content_box(page)
    a = ANALYSIS_LAYOUT
    set_frame_text(scribus.createText(x, a["heading_y_mm"], width, a["heading_height_mm"], "Analysis_Heading_%d" % page), title, "Abden Heading 1")
    body = scribus.createText(x, a["body_y_mm"], width, a["body_height_mm"], "Analysis_Body_%d" % page)
    styled_lines(body, [
        ("Abden Evidence Heading", "Source identification"), ("Abden Technical Specification", evidence_label + ": [identifier, date, creator, repository and rights]"),
        ("Abden Evidence Heading", "Observed information"), ("Abden Body First", "Record only directly visible or measurable information."),
        ("Abden Evidence Heading", "Interpretation"), ("Abden Evidence Assessment", "Explain the source's contribution and any conflict with other evidence."),
        ("Abden Evidence Heading", "Confidence and limitations"), ("Abden Confidence Rating", "Confidence: [High / Moderate / Low / Unknown]"),
        ("Abden Evidence Heading", "Cross-references"), ("Abden Figure Reference", "Related figures, maps, feature records and evidence-register entries: [references]")])


def create_reconstruction_page(page=12):
    create_working_section(page, "Blender Reconstruction Specification",
        "This page converts the historical interpretation into a controlled modelling instruction while preserving the distinction between known and conjectural geometry.",
        [("Object identity", "Feature ID; object name; chapter and evidence links."), ("Geometry", "Location; orientation; dimensions; levels; tolerances; CRS."), ("Materials and appearance", "Construction, finish, colour, weathering and repeated components."), ("Implementation", "Hierarchy; origin; units; naming; editable parameters; level of detail."), ("Approval", "Historical, academic and modelling review status.")])


def create_appendix_page(page=13):
    scribus.gotoPage(page)
    x, _, width, _ = content_box(page)
    set_frame_text(scribus.createText(x, 42, width, 38, "Appendix_Heading"), "Appendix A\nFeature Register", "Abden Appendix Heading")
    body = scribus.createText(x, 94, width, 158, "Appendix_Body")
    styled_lines(body, [
        ("Abden Body First", "The Feature Register is the controlled index of every structure, landscape element and infrastructure component considered in the reconstruction."),
        ("Abden Evidence Heading", "Required fields"),
        ("Abden Technical Specification", "Feature ID; preferred name; aliases; category; location; date range; evidence links; confidence; chapter; Blender object name; review status.")])
