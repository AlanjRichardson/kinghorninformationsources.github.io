# -*- coding: utf-8 -*-
"""Master-page creation for the Abden Publishing Generator.

Version 0.3.4, Phase 3 margin correction

Phase 2 retains the tested left/right masters and adds the chapter-opening
master. Chapter-specific number and title frames are deliberately created on
the document page, not on the master page, so that they remain editable for
each chapter.
"""

import scribus

from abden_config import MASTER_PAGES, PAGE, PROJECT
from abden_styles import apply_whole_frame

# Scribus special character used for an automatic page number.
PAGE_NUMBER_TOKEN = chr(30)


def _master_exists(name):
    """Return True when a master page named *name* already exists."""
    return name in scribus.masterPageNames()


def _create_or_edit(name):
    """Create a master page if required, then enter master-page edit mode."""
    if not _master_exists(name):
        scribus.createMasterPage(name)
    scribus.editMasterPage(name)


def _close_master():
    """Leave master-page edit mode."""
    scribus.closeMasterPage()


def _page_number_frame(right_hand, name):
    """Create an automatic page-number frame at the outside foot."""
    frame_width = 25.0

    if right_hand:
        x = PAGE["width_mm"] - PAGE["outside_mm"] - frame_width
        style = "Abden Page Number Right"
    else:
        x = PAGE["outside_mm"]
        style = "Abden Page Number Left"

    frame = scribus.createText(
        x,
        PAGE["footer_y_mm"],
        frame_width,
        PAGE["footer_height_mm"],
        name,
    )
    scribus.insertText(PAGE_NUMBER_TOKEN, 0, frame)
    apply_whole_frame(frame, style)
    return frame


def _running_header(right_hand, text, name):
    """Create a running-header frame inside the page's text measure."""
    if right_hand:
        x = PAGE["inside_mm"]
        far_margin = PAGE["outside_mm"]
        alignment = 2  # right
    else:
        x = PAGE["outside_mm"]
        far_margin = PAGE["inside_mm"]
        alignment = 0  # left

    width = PAGE["width_mm"] - x - far_margin
    frame = scribus.createText(
        x,
        PAGE["header_y_mm"],
        width,
        PAGE["header_height_mm"],
        name,
    )
    scribus.setText(text, frame)
    apply_whole_frame(frame, "Abden Running Header")
    scribus.setTextAlignment(alignment, frame)
    return frame



def create_title_master_page():
    """Create the title master page.

    The master intentionally contains no fixed text and no page number. Title
    content is created as editable document-page objects so metadata can be
    changed without altering or detaching master-page items.
    """
    name = MASTER_PAGES["title"]
    _create_or_edit(name)
    _close_master()


def _title_text_frame(y, height, text, style, name):
    """Create one centred title-page text frame."""
    # The title page is a right-hand page: its inside margin is on the left.
    x = PAGE["inside_mm"]
    width = PAGE["width_mm"] - PAGE["inside_mm"] - PAGE["outside_mm"]
    frame = scribus.createText(x, y, width, height, name)
    scribus.setText(text, frame)
    apply_whole_frame(frame, style)
    scribus.setTextAlignment(1, frame)
    return frame


def create_title_page_content(project=None):
    """Add editable, metadata-driven title-page content to the current page."""
    data = PROJECT if project is None else project
    frames = []
    frames.append(_title_text_frame(38.0, 12.0, data["series"], "Abden Title Series", "Title_Series"))
    frames.append(_title_text_frame(61.0, 34.0, "ABDEN SHIPYARD", "Abden Title Main", "Title_Main"))
    frames.append(_title_text_frame(98.0, 18.0, "RECONSTRUCTION PROJECT", "Abden Title Series", "Title_Project"))
    frames.append(_title_text_frame(132.0, 12.0, data["volume"], "Abden Title Volume", "Title_Volume"))
    frames.append(_title_text_frame(149.0, 28.0, data["title"], "Abden Title Subtitle", "Title_Subtitle"))
    frames.append(_title_text_frame(203.0, 12.0, data["author"], "Abden Title Author", "Title_Author"))
    imprint_text = data["imprint"] + "\n" + data["publication_year"]
    frames.append(_title_text_frame(247.0, 20.0, imprint_text, "Abden Title Imprint", "Title_Imprint"))
    return tuple(frames)

def create_left_master_page():
    """Create the normal left-hand master page."""
    name = MASTER_PAGES["left"]
    _create_or_edit(name)
    try:
        _running_header(False, PROJECT["series"], "MP_Left_Running_Header")
        _page_number_frame(False, "MP_Left_Page_Number")
    finally:
        _close_master()


def create_right_master_page():
    """Create the normal right-hand master page."""
    name = MASTER_PAGES["right"]
    _create_or_edit(name)
    try:
        # Placeholder until chapter-title variables are introduced.
        _running_header(True, "Chapter Title", "MP_Right_Running_Header")
        _page_number_frame(True, "MP_Right_Page_Number")
    finally:
        _close_master()


def create_chapter_master_page():
    """Create the chapter-opening master page.

    Chapter openings have no running header. They retain a page number at the
    outside bottom corner. The Abden convention starts chapters on a right-hand
    page, so the number is right-aligned.
    """
    name = MASTER_PAGES["chapter"]
    _create_or_edit(name)
    try:
        _page_number_frame(True, "MP_Chapter_Page_Number")
    finally:
        _close_master()


def create_chapter_opening_content(
    chapter_number="CHAPTER 1",
    chapter_title="Chapter Title",
):
    """Add editable chapter number and title frames to the current page.

    These are page objects rather than master-page objects. This is important:
    each chapter needs different text, and page objects remain directly
    editable in Scribus after the master page is applied.
    """
    right_x = PAGE["inside_mm"]
    width = PAGE["width_mm"] - PAGE["inside_mm"] - PAGE["outside_mm"]

    number_frame = scribus.createText(
        right_x,
        58.0,
        width,
        12.0,
        "Chapter_Opening_Number",
    )
    scribus.setText(chapter_number, number_frame)
    apply_whole_frame(number_frame, "Abden Chapter Number")

    title_frame = scribus.createText(
        right_x,
        76.0,
        width,
        38.0,
        "Chapter_Opening_Title",
    )
    scribus.setText(chapter_title, title_frame)
    apply_whole_frame(title_frame, "Abden Chapter Title")

    return number_frame, title_frame


def create_body_master_pages():
    """Create the chapter, left-page, and right-page masters."""
    create_chapter_master_page()
    create_left_master_page()
    create_right_master_page()


def create_left_right_master_pages():
    """Retained compatibility helper from Phase 1."""
    create_left_master_page()
    create_right_master_page()


def create_master_pages():
    """Create the complete v0.3 master-page set."""
    create_title_master_page()

    for key in ("copyright", "blank"):
        name = MASTER_PAGES[key]
        _create_or_edit(name)
        _close_master()

    _create_or_edit(MASTER_PAGES["contents"])
    try:
        _page_number_frame(True, "MP_Contents_Page_Number")
    finally:
        _close_master()

    create_body_master_pages()

    _create_or_edit(MASTER_PAGES["figure"])
    try:
        _page_number_frame(True, "MP_Figure_Page_Number")
    finally:
        _close_master()


def apply_master_pages():
    """Apply representative masters to the eight generated proof pages."""
    assignments = {
        1: MASTER_PAGES["title"],
        2: MASTER_PAGES["copyright"],
        3: MASTER_PAGES["contents"],
        4: MASTER_PAGES["chapter"],
        5: MASTER_PAGES["right"],
        6: MASTER_PAGES["left"],
        7: MASTER_PAGES["figure"],
        8: MASTER_PAGES["blank"],
    }
    for page_number, master_name in assignments.items():
        scribus.applyMasterPage(master_name, page_number)
