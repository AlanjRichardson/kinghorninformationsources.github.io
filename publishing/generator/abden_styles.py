# -*- coding: utf-8 -*-
"""Font discovery and reusable Scribus styles for Generator v0.5.0."""

import scribus
from abden_config import TYPOGRAPHY


def find_font(candidates, required_terms):
    fonts = list(scribus.getFontNames())
    folded = {name.casefold(): name for name in fonts}
    for candidate in candidates:
        match = folded.get(candidate.casefold())
        if match:
            return match
    terms = [term.casefold() for term in required_terms]
    for font in fonts:
        test = font.casefold()
        if all(term in test for term in terms):
            return font
    related = [
        font for font in fonts
        if "libert" in font.casefold() or "biolin" in font.casefold()
    ]
    raise RuntimeError(
        "Suitable Linux Libertine/Biolinum fonts were not found.\n\n"
        + "Related installed fonts:\n" + "\n".join(related)
    )


def discover_fonts():
    return {
        "serif_regular": find_font(
            ["Linux Libertine O Regular", "Linux Libertine O"],
            ["linux", "libertine", "regular"],
        ),
        "serif_italic": find_font(
            ["Linux Libertine O Italic"], ["linux", "libertine", "italic"]
        ),
        "serif_bold": find_font(
            ["Linux Libertine O Bold"], ["linux", "libertine", "bold"]
        ),
        "sans_regular": find_font(
            ["Linux Biolinum O Regular", "Linux Biolinum O"],
            ["linux", "biolinum", "regular"],
        ),
        "sans_bold": find_font(
            ["Linux Biolinum O Bold"], ["linux", "biolinum", "bold"]
        ),
    }


def create_character_styles(fonts):
    t = TYPOGRAPHY
    definitions = [
        ("Abden Body Character", fonts["serif_regular"], t["body_size"]),
        ("Abden Body Italic", fonts["serif_italic"], t["body_size"]),
        ("Abden Body Bold", fonts["serif_bold"], t["body_size"]),
        ("Abden Chapter Number Character", fonts["sans_bold"], t["chapter_number_size"]),
        ("Abden Chapter Title Character", fonts["sans_bold"], t["chapter_title_size"]),
        ("Abden Heading 1 Character", fonts["sans_bold"], t["heading_1_size"]),
        ("Abden Heading 2 Character", fonts["sans_bold"], t["heading_2_size"]),
        ("Abden Heading 3 Character", fonts["sans_bold"], t["heading_3_size"]),
        ("Abden Caption Character", fonts["serif_italic"], t["caption_size"]),
        ("Abden Figure Source Character", fonts["serif_regular"], t["footnote_size"]),
        ("Abden Footnote Character", fonts["serif_regular"], t["footnote_size"]),
        ("Abden Running Header Character", fonts["sans_regular"], t["running_size"]),
        ("Abden Page Number Character", fonts["sans_regular"], t["running_size"]),
        ("Abden Quote Character", fonts["serif_regular"], t["quote_size"]),
        ("Abden Archive Character", fonts["serif_regular"], t["archive_size"]),
        ("Abden Note Character", fonts["serif_regular"], t["body_size"]),
        ("Abden Bibliography Character", fonts["serif_regular"], t["bibliography_size"]),
        ("Abden Contents Character", fonts["serif_regular"], t["body_size"]),
        ("Abden Contents Chapter Character", fonts["sans_regular"], t["body_size"]),
        ("Abden Technical Character", fonts["serif_regular"], t["technical_size"]),
        ("Abden Technical Bold Character", fonts["sans_bold"], t["technical_size"]),
        ("Abden Status Character", fonts["sans_regular"], t["status_size"]),
        ("Abden Status Bold Character", fonts["sans_bold"], t["status_size"]),
    ]
    existing = set(scribus.getCharStyles())
    for name, font, size in definitions:
        if name not in existing:
            scribus.createCharStyle(
                name=name, font=font, fontsize=size,
                fillcolor="Black", language="en_GB",
            )


def create_paragraph_styles():
    t = TYPOGRAPHY
    mm5 = 14.173228
    mm7 = 19.842520
    mm10 = 28.346457
    definitions = [
        dict(name="Abden Body", linespacingmode=0, linespacing=t["body_leading"], alignment=3, firstindent=mm5, gapbefore=0.0, gapafter=0.0, charstyle="Abden Body Character"),
        dict(name="Abden Body First", linespacingmode=0, linespacing=t["body_leading"], alignment=3, firstindent=0.0, gapbefore=0.0, gapafter=0.0, charstyle="Abden Body Character"),
        dict(name="Abden Chapter Number", linespacingmode=0, linespacing=t["chapter_number_leading"], alignment=0, firstindent=0.0, gapbefore=0.0, gapafter=8.0, charstyle="Abden Chapter Number Character"),
        dict(name="Abden Chapter Title", linespacingmode=0, linespacing=t["chapter_title_leading"], alignment=0, firstindent=0.0, gapbefore=0.0, gapafter=20.0, charstyle="Abden Chapter Title Character"),
        dict(name="Abden Heading 1", linespacingmode=0, linespacing=t["heading_1_leading"], alignment=0, firstindent=0.0, gapbefore=14.0, gapafter=6.0, charstyle="Abden Heading 1 Character"),
        dict(name="Abden Heading 2", linespacingmode=0, linespacing=t["heading_2_leading"], alignment=0, firstindent=0.0, gapbefore=11.0, gapafter=4.0, charstyle="Abden Heading 2 Character"),
        dict(name="Abden Heading 3", linespacingmode=0, linespacing=t["heading_3_leading"], alignment=0, firstindent=0.0, gapbefore=9.0, gapafter=3.0, charstyle="Abden Heading 3 Character"),
        dict(name="Abden Figure Caption", linespacingmode=0, linespacing=t["caption_leading"], alignment=0, firstindent=0.0, gapbefore=4.0, gapafter=8.0, charstyle="Abden Caption Character"),
        dict(name="Abden Table Caption", linespacingmode=0, linespacing=t["caption_leading"], alignment=0, firstindent=0.0, gapbefore=4.0, gapafter=8.0, charstyle="Abden Caption Character"),
        dict(name="Abden Figure Source", linespacingmode=0, linespacing=t["footnote_leading"], alignment=0, firstindent=0.0, gapbefore=0.0, gapafter=0.0, charstyle="Abden Figure Source Character"),
        dict(name="Abden Footnote", linespacingmode=0, linespacing=t["footnote_leading"], alignment=0, firstindent=0.0, gapbefore=0.0, gapafter=2.0, charstyle="Abden Footnote Character"),
        dict(name="Abden Running Header", linespacingmode=0, linespacing=t["running_leading"], alignment=0, firstindent=0.0, gapbefore=0.0, gapafter=0.0, charstyle="Abden Running Header Character"),
        dict(name="Abden Page Number Left", linespacingmode=0, linespacing=t["running_leading"], alignment=0, firstindent=0.0, gapbefore=0.0, gapafter=0.0, charstyle="Abden Page Number Character"),
        dict(name="Abden Page Number Right", linespacingmode=0, linespacing=t["running_leading"], alignment=2, firstindent=0.0, gapbefore=0.0, gapafter=0.0, charstyle="Abden Page Number Character"),
        dict(name="Abden Quote", linespacingmode=0, linespacing=t["quote_leading"], alignment=0, leftmargin=mm10, rightmargin=mm10, firstindent=0.0, gapbefore=8.0, gapafter=8.0, charstyle="Abden Quote Character"),
        dict(name="Abden Archive Reference", linespacingmode=0, linespacing=t["archive_leading"], alignment=0, leftmargin=mm7, rightmargin=mm7, firstindent=0.0, gapbefore=6.0, gapafter=6.0, charstyle="Abden Archive Character"),
        dict(name="Abden Reconstruction Note", linespacingmode=0, linespacing=t["body_leading"], alignment=0, leftmargin=mm7, rightmargin=mm7, firstindent=0.0, gapbefore=8.0, gapafter=8.0, charstyle="Abden Note Character"),
        dict(name="Abden Evidence Assessment", linespacingmode=0, linespacing=t["body_leading"], alignment=0, leftmargin=mm7, rightmargin=mm7, firstindent=0.0, gapbefore=8.0, gapafter=8.0, charstyle="Abden Note Character"),
        dict(name="Abden Appendix Heading", linespacingmode=0, linespacing=t["chapter_title_leading"], alignment=0, firstindent=0.0, gapbefore=0.0, gapafter=20.0, charstyle="Abden Chapter Title Character"),
        dict(name="Abden Bibliography Entry", linespacingmode=0, linespacing=t["bibliography_leading"], alignment=0, leftmargin=mm5, firstindent=-mm5, gapbefore=0.0, gapafter=4.0, charstyle="Abden Bibliography Character"),
        dict(name="Abden Contents Entry", linespacingmode=0, linespacing=t["body_leading"], alignment=0, firstindent=0.0, gapbefore=0.0, gapafter=4.0, tabs=[(453.5433, 1)], charstyle="Abden Contents Character"),
        dict(name="Abden Contents Chapter", linespacingmode=0, linespacing=t["body_leading"], alignment=0, firstindent=0.0, gapbefore=6.0, gapafter=4.0, tabs=[(453.5433, 1)], charstyle="Abden Contents Chapter Character"),
        dict(name="Abden Contents Part", linespacingmode=0, linespacing=t["heading_3_leading"], alignment=0, firstindent=0.0, gapbefore=10.0, gapafter=4.0, charstyle="Abden Technical Bold Character"),
        dict(name="Abden Evidence Heading", linespacingmode=0, linespacing=t["heading_3_leading"], alignment=0, firstindent=0.0, gapbefore=8.0, gapafter=3.0, charstyle="Abden Technical Bold Character"),
        dict(name="Abden Confidence Rating", linespacingmode=0, linespacing=t["technical_leading"], alignment=0, leftmargin=mm7, rightmargin=mm7, firstindent=0.0, gapbefore=5.0, gapafter=5.0, charstyle="Abden Technical Bold Character"),
        dict(name="Abden Blender Note", linespacingmode=0, linespacing=t["technical_leading"], alignment=0, leftmargin=mm7, rightmargin=mm7, firstindent=0.0, gapbefore=6.0, gapafter=6.0, charstyle="Abden Technical Character"),
        dict(name="Abden Research Status", linespacingmode=0, linespacing=t["status_leading"], alignment=0, firstindent=0.0, gapbefore=0.0, gapafter=2.0, charstyle="Abden Status Character"),
        dict(name="Abden Research Status Label", linespacingmode=0, linespacing=t["status_leading"], alignment=0, firstindent=0.0, gapbefore=0.0, gapafter=2.0, charstyle="Abden Status Bold Character"),
        dict(name="Abden Outstanding Question", linespacingmode=0, linespacing=t["technical_leading"], alignment=0, leftmargin=mm7, firstindent=-mm5, gapbefore=3.0, gapafter=3.0, charstyle="Abden Technical Character"),
        dict(name="Abden Technical Specification", linespacingmode=0, linespacing=t["technical_leading"], alignment=0, firstindent=0.0, gapbefore=2.0, gapafter=2.0, charstyle="Abden Technical Character"),
        dict(name="Abden Figure Reference", linespacingmode=0, linespacing=t["technical_leading"], alignment=0, firstindent=0.0, gapbefore=2.0, gapafter=2.0, charstyle="Abden Technical Character"),
        dict(name="Abden Table Reference", linespacingmode=0, linespacing=t["technical_leading"], alignment=0, firstindent=0.0, gapbefore=2.0, gapafter=2.0, charstyle="Abden Technical Character"),
        dict(name="Abden Metadata Label", linespacingmode=0, linespacing=t["technical_leading"], alignment=0, firstindent=0.0, gapbefore=0.0, gapafter=2.0, charstyle="Abden Technical Bold Character"),
        dict(name="Abden Metadata Value", linespacingmode=0, linespacing=t["technical_leading"], alignment=0, firstindent=0.0, gapbefore=0.0, gapafter=2.0, charstyle="Abden Technical Character"),
    ]
    existing = set(scribus.getParagraphStyles())
    for definition in definitions:
        if definition["name"] not in existing:
            scribus.createParagraphStyle(**definition)


def apply_whole_frame(frame, style):
    length = scribus.getTextLength(frame)
    if length:
        scribus.selectText(0, length, frame)
        scribus.setParagraphStyle(style, frame)
