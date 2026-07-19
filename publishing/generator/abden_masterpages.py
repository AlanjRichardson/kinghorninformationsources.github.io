# -*- coding: utf-8 -*-
"""Creation and application of Scribus master pages."""

import scribus
from abden_config import MASTER_PAGES, PAGE, PROJECT
from abden_styles import apply_whole_frame

PAGE_NUMBER_TOKEN = chr(30)


def _master_exists(name):
    return name in scribus.masterPageNames()


def _create_or_edit(name):
    if not _master_exists(name):
        scribus.createMasterPage(name)
    scribus.editMasterPage(name)


def _close_master():
    scribus.closeMasterPage()


def _page_number_frame(right_hand, name):
    width = 25.0
    x = PAGE["width_mm"] - PAGE["outside_mm"] - width if right_hand else PAGE["outside_mm"]
    frame = scribus.createText(
        x,
        PAGE["footer_y_mm"],
        width,
        PAGE["footer_height_mm"],
        name,
    )
    scribus.insertText(PAGE_NUMBER_TOKEN, 0, frame)
    style = "Abden Page Number Right" if right_hand else "Abden Page Number Left"
    apply_whole_frame(frame, style)
    return frame


def _running_header(right_hand, text, name):
    if right_hand:
        x = PAGE["inside_mm"]
        right_margin = PAGE["outside_mm"]
        alignment = 2
    else:
        x = PAGE["outside_mm"]
        right_margin = PAGE["inside_mm"]
        alignment = 0

    width = PAGE["width_mm"] - x - right_margin
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


def create_master_pages():
    """Create the complete Version 0.3.6 master-page set."""
    for key in ("title", "copyright", "blank"):
        name = MASTER_PAGES[key]
        _create_or_edit(name)
        _close_master()

    _create_or_edit(MASTER_PAGES["contents"])
    _page_number_frame(True, "MP_Contents_Page_Number")
    _close_master()

    _create_or_edit(MASTER_PAGES["chapter"])
    _page_number_frame(False, "MP_Chapter_Page_Number")
    _close_master()

    _create_or_edit(MASTER_PAGES["left"])
    _running_header(False, PROJECT["series"], "MP_Left_Running_Header")
    _page_number_frame(False, "MP_Left_Page_Number")
    _close_master()

    _create_or_edit(MASTER_PAGES["right"])
    _running_header(True, "Chapter Title", "MP_Right_Running_Header")
    _page_number_frame(True, "MP_Right_Page_Number")
    _close_master()

    _create_or_edit(MASTER_PAGES["figure"])
    _page_number_frame(True, "MP_Figure_Page_Number")
    _close_master()


def apply_master_pages():
    """Apply representative masters to the generated specimen pages."""
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
