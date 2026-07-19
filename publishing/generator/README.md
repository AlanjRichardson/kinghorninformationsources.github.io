# Abden Scribus Generator — Version 0.3.0

This is the complete replacement for Version 2.

## Installation location

Copy these files into:

```text
publishing/generator/
```

The generator automatically writes its output to:

```text
publishing/templates/Abden_Master_Template.sla
```

No personal or machine-specific path is hard-coded.

## Files

- `build_template.py` — execute this from Scribus
- `abden_config.py` — project metadata, portable paths, page geometry and typography
- `abden_styles.py` — font discovery and house styles
- `abden_layout.py` — page geometry, guides and specimen pages
- `abden_masterpages.py` — master pages, running headers and page numbers
- `__init__.py` — package marker and version

## Master pages

- A-Title
- B-Copyright
- C-Contents
- D-Chapter Opening
- E-Left Page
- F-Right Page
- G-Full Page Figure
- H-Blank Page

The right-page running header contains the editable placeholder `Chapter Title`.
Scribus does not automatically derive running chapter titles from paragraph styles,
so this placeholder is intentional.

## Running the generator

1. Keep all Python files together in `publishing/generator/`.
2. Ensure `publishing/templates/` exists. The script will also create it if necessary.
3. Open Scribus 1.6.x.
4. Choose **Script → Execute Script…**.
5. Select `publishing/generator/build_template.py`.
6. Open the resulting `publishing/templates/Abden_Master_Template.sla`.

## Initial checks

1. Open **Edit → Master Pages** and confirm that all eight Abden master pages exist.
2. Check pages 3–7 for page numbers in the outside footer position.
3. Check the left and right running headers.
4. Open the Style Manager and confirm the expanded Abden styles.
5. Save, close and reopen the generated `.sla`.

## Version 0.3.0 scope

This release establishes the permanent architecture and master-page system. It does
not yet generate a complete book, table of contents or dynamically updated chapter
running heads. Those belong to later generator stages.
