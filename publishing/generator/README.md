# Abden Scribus Generator — Version 0.5.1

Version 0.5.1 is the **Framework Freeze** release for Volume I of the Abden Shipyard Reconstruction Project.

## Corrections from the v0.5.0 visual test

- Production guide lines have been removed.
- The Chapter 1 status panel has been shortened and moved upward so that it clears the bottom margin and page-number frame.
- Pages 1, 2 and 14 remain intentionally without visible page numbers: title, copyright and blank masters respectively.
- Page 14 remains intentionally blank for pagination control.

## Working pages generated

1. Title
2. Copyright and document metadata
3. Full Volume I contents
4. Chapter 1 — The Geography of Abden, with internal status panel
5. Preface
6. Executive Summary
7. Research Methodology
8. Feature Record
9. Historical Map Analysis
10. Photograph Analysis
11. LiDAR and Terrain Analysis
12. Blender Reconstruction Specification
13. Appendix A — Feature Register
14. Intentionally blank page

The permanent eight-master-page architecture and the v0.5.0 style set are frozen. Future changes should normally be restricted to genuine defects.

## Running

Place the files in `publishing/generator/`, then in Scribus 1.6.x choose **Script → Execute Script…** and run `build_template.py`.

Output:

```text
publishing/templates/Abden_Master_Template_v0.5.1_working.sla
```

Inspect all fourteen pages before committing the generated `.sla`.

## Suggested Git release sequence

```bash
git status
git diff
git add publishing/generator publishing/templates/Abden_Master_Template_v0.5.1_working.sla
git commit -m "Freeze Abden Scribus framework at v0.5.1"
git tag -a v0.5.1-framework-freeze -m "Abden Scribus framework freeze"
git push
git push origin v0.5.1-framework-freeze
```

The Python source can be syntax-checked outside Scribus, but the Scribus API and page rendering must be tested inside Scribus.
