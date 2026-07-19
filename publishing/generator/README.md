# Abden Scribus Generator — Version 0.4.0

Version 0.4.0 completes and freezes the eight-page master-page architecture for the Abden publishing system.

## Installation location

Copy the generator files into:

```text
publishing/generator/
```

Copy the tests into:

```text
publishing/tests/
```

The generator writes its output to:

```text
publishing/templates/Abden_Master_Template.sla
```

No personal or machine-specific path is hard-coded.

## Master pages

- A-Title
- B-Copyright
- C-Contents
- D-Chapter Opening
- E-Left Page
- F-Right Page
- G-Full Page Figure
- H-Blank Page

The H-Blank Page master is intentionally empty: it has no header, page number or other object. It is used when pagination requires a blank verso before a chapter begins on a recto page.

## Running the generator

1. Open Scribus 1.6.x.
2. Choose **Script → Execute Script…**.
3. Select `publishing/generator/build_template.py`.
4. Open `publishing/templates/Abden_Master_Template.sla`.

## Tests

Run the individual scripts in `publishing/tests/` from Scribus. The blank-page test checks that the H-Blank Page master creates no objects.

## Version 0.4.0 scope

This release completes the permanent page architecture. Later versions can concentrate on document assembly, automated contents, figure numbering, bibliography support, cross-references, PDF export and pre-flight checks without changing the eight core master pages.
