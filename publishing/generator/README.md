# Abden Publishing Framework v0.5.2

This release corrects the facing-page margin semantics in v0.5.1.

## Cause of the defect

Scribus stores facing-page margins semantically: `BORDERLEFT` is the **inside** margin and `BORDERRIGHT` is the **outside** margin. Version 0.5.1 swapped those XML values on physical left pages. Scribus then mirrored the already-swapped values, so the visible outside guide became 25 mm while the text frame remained at 20 mm.

## Correct v0.5.2 geometry

- Inside margin: 25 mm
- Outside margin: 20 mm
- Main text width: 165 mm
- Physical left page frame begins 20 mm from the left page edge
- Physical right page frame begins 25 mm from the left page edge

## Visual acceptance test in Scribus 1.6.1

1. Open `Abden_Master_Template_v0.5.2.sla`.
2. Check page 2 (copyright): its frame must align with the left blue margin guide.
3. Check a normal left page and a normal right page.
4. Save, close, and reopen the file.
5. Repeat the alignment check.

Run the automated check with:

```bash
python3 validate_scribus.py Abden_Master_Template_v0.5.2.sla
```
