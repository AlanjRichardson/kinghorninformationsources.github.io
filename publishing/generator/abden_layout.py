# -*- coding: utf-8 -*-
"""Page geometry, guides and specimen-page construction."""

import scribus
from abden_config import FIGURE_LAYOUT, PAGE, PROJECT
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


def create_design_guides():
    """Add non-printing alignment guides where the API supports them."""
    if not hasattr(scribus, "setHGuides") or not hasattr(scribus, "setVGuides"):
        return

    horizontal = [
        PAGE["header_y_mm"],
        PAGE["top_mm"],
        PAGE["height_mm"] - PAGE["bottom_mm"],
        PAGE["footer_y_mm"],
    ]
    vertical = [
        PAGE["outside_mm"],
        PAGE["inside_mm"],
        PAGE["width_mm"] - PAGE["inside_mm"],
        PAGE["width_mm"] - PAGE["outside_mm"],
    ]
    scribus.setHGuides(horizontal)
    scribus.setVGuides(vertical)


def create_title_page(fonts):
    page = 1
    scribus.gotoPage(page)

    series = text_frame(page, 46, 18, "Title_Series")
    scribus.setText(PROJECT["series"], series)
    scribus.setFont(fonts["sans_regular"], series)
    scribus.setFontSize(14, series)
    scribus.setTextAlignment(1, series)

    volume = text_frame(page, 86, 14, "Title_Volume")
    scribus.setText(PROJECT["volume"], volume)
    scribus.setFont(fonts["sans_bold"], volume)
    scribus.setFontSize(16, volume)
    scribus.setTextAlignment(1, volume)

    title_1 = text_frame(page, 112, 20, "Title_Main_1")
    scribus.setText("Historical Synopsis", title_1)
    scribus.setFont(fonts["sans_bold"], title_1)
    scribus.setFontSize(25, title_1)
    scribus.setTextAlignment(1, title_1)

    title_2 = text_frame(page, 143, 20, "Title_Main_2")
    scribus.setText("and Reconstruction Guide", title_2)
    scribus.setFont(fonts["sans_bold"], title_2)
    scribus.setFontSize(25, title_2)
    scribus.setTextAlignment(1, title_2)

    author = text_frame(page, 205, 14, "Title_Author")
    scribus.setText(PROJECT["author"], author)
    scribus.setFont(fonts["serif_regular"], author)
    scribus.setFontSize(13, author)
    scribus.setTextAlignment(1, author)

    imprint = text_frame(page, 246, 14, "Title_Imprint")
    scribus.setText(PROJECT["imprint"], imprint)
    scribus.setFont(fonts["sans_regular"], imprint)
    scribus.setFontSize(11, imprint)
    scribus.setTextAlignment(1, imprint)


def create_copyright_page():
    page = 2
    scribus.gotoPage(page)
    x, _, width, _ = content_box(page)
    frame = scribus.createText(x, 185, width, 60, "Copyright_Text")
    text = (
        f"{PROJECT['series']}\n"
        f"{PROJECT['volume']}: {PROJECT['title']}\n\n"
        f"Copyright © {PROJECT['author']}.\n"
        "All rights reserved.\n\n"
        f"Published by {PROJECT['imprint']}."
    )
    set_frame_text(frame, text, "Abden Footnote")


def create_contents_page():
    page = 3
    scribus.gotoPage(page)
    x, _, width, _ = content_box(page)
    heading = scribus.createText(x, 48, width, 24, "Contents_Heading")
    set_frame_text(heading, "Contents", "Abden Chapter Title")

    body = scribus.createText(x, 88, width, 145, "Contents_Sample")
    text = (
        "Preface\nAcknowledgements\nList of Figures\nList of Maps\n"
        "Chapter 1   Before the First Keel\n"
        "Chapter 2   Establishment of the Shipyard\n"
        "Appendix\nBibliography"
    )
    set_frame_text(body, text, "Abden Body First")


def create_chapter_specimen(page=4):
    scribus.gotoPage(page)
    x, _, width, _ = content_box(page)

    chapter_no = scribus.createText(x, 58, width, 18, "Sample_Chapter_Number")
    set_frame_text(chapter_no, "Chapter 1", "Abden Chapter Number")

    chapter_title = scribus.createText(x, 82, width, 37, "Sample_Chapter_Title")
    set_frame_text(chapter_title, "Before the First Keel", "Abden Chapter Title")

    body = scribus.createText(x, 136, width, 105, "Sample_Body_Text")
    first = (
        "Kinghorn’s position on the northern shore of the Firth of Forth "
        "shaped both its maritime history and the later development of the "
        "Abden shipyard. This paragraph begins without an indent."
    )
    second = (
        "Subsequent paragraphs use the Abden Body style, with an eleven-and-a-half "
        "point text size, fourteen-point leading, justified setting and a "
        "five-millimetre first-line indent."
    )
    full = first + "\n" + second
    scribus.setText(full, body)
    split = len(first) + 1
    scribus.selectText(0, split, body)
    scribus.setParagraphStyle("Abden Body First", body)
    scribus.selectText(split, len(full) - split, body)
    scribus.setParagraphStyle("Abden Body", body)


def create_style_specimen(page=5):
    scribus.gotoPage(page)
    x, _, width, _ = content_box(page)
    frame = scribus.createText(x, 36, width, 220, "Style_Specimen")
    entries = [
        ("Abden Heading 1", "Evidence and Interpretation"),
        ("Abden Body First", "The house style separates documented evidence from interpretation and unresolved questions."),
        ("Abden Heading 2", "Archival evidence"),
        ("Abden Archive Reference", "Archive reference: National Records of Scotland, plans and correspondence relating to Abden."),
        ("Abden Quote", "A block quotation is inset on both sides and set slightly smaller than the body text."),
        ("Abden Reconstruction Note", "Reconstruction note: this feature is inferred from the combined map and photographic evidence."),
        ("Abden Evidence Assessment", "Established fact: the structure appears on the 1895 map. Probable interpretation: it served the adjacent workshop. Outstanding question: its exact construction date."),
        ("Abden Figure Caption", "Figure 1. Specimen caption showing the adopted caption style."),
        ("Abden Bibliography Entry", "Author, A. Title of Work. Place of publication: Publisher, year."),
    ]
    full = "\n".join(text for _, text in entries)
    scribus.setText(full, frame)
    start = 0
    for style, text in entries:
        length = len(text)
        scribus.selectText(start, length, frame)
        scribus.setParagraphStyle(style, frame)
        start += length + 1



def create_figure_specimen(page=7):
    """Create an editable full-page figure layout on a document page.

    The master page supplies the outside page number. The image, caption and
    source frames belong to the document page so that each figure can be edited
    independently without detaching master-page objects.
    """
    scribus.gotoPage(page)
    x, _, width, _ = content_box(page)
    f = FIGURE_LAYOUT

    image = scribus.createImage(
        x,
        f["image_y_mm"],
        width,
        f["image_height_mm"],
        "Figure_Image",
    )
    # Keep imported images proportional and centred in the frame.
    if hasattr(scribus, "setScaleImageToFrame"):
        scribus.setScaleImageToFrame(True, True, image)

    caption_y = f["image_y_mm"] + f["image_height_mm"] + f["caption_gap_mm"]
    caption = scribus.createText(
        x,
        caption_y,
        width,
        f["caption_height_mm"],
        "Figure_Caption",
    )
    set_frame_text(
        caption,
        "Figure 1. Full-page figure caption. Replace this text with a concise description of the map, plan, photograph or reconstruction.",
        "Abden Figure Caption",
    )

    source_y = caption_y + f["caption_height_mm"] + f["source_gap_mm"]
    source = scribus.createText(
        x,
        source_y,
        width,
        f["source_height_mm"],
        "Figure_Source",
    )
    set_frame_text(
        source,
        "Source/Credit: archive reference, map licence, photographer or collection.",
        "Abden Figure Source",
    )

    return image, caption, source
