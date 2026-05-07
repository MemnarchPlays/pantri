---
name: Recipe PDF Binder
description: Generate and download a styled PDF containing all recipes, organized by meal type with a cover page and table of contents
status: COMPLETE
---

## What It Does

`generate_pdf.py` compiles all `data/*.json` recipes into a printable PDF binder with a purple color scheme, decorative double-page border, cover page, table of contents, and one page per recipe showing macros, ingredients, instructions, substitutions, and notes. The web app exposes a "Download PDF" button that generates the PDF in memory and serves it as a download.

## Success Criteria

1. Running `py generate_pdf.py` produces `output/recipe_binder.pdf`.
2. Passing specific JSON file paths as arguments includes only those recipes.
3. The PDF has: cover page (title + month/year), table of contents grouped by meal type sorted alphabetically, then one page per recipe.
4. Each recipe page shows: name banner, prep/cook time/servings/meal-type header row, macro table, ingredients list, numbered instructions, substitutions section (if present), notes (if present).
5. Every page has a decorative double-border (outer purple, inner light purple, corner accents).
6. Recipes are sorted alphabetically within each meal type group.
7. The "⬇ Download PDF" button on the Recipes page (`/recipes/download-pdf`) triggers an in-memory PDF build and serves it as `recipe_binder_YYYYMMDD.pdf`.
8. If reportlab is not installed, the download endpoint returns a 500 with an install instruction.
9. If no recipes exist, the download endpoint returns 404.

## Status

COMPLETE

### Progress

- [x] `generate_pdf.py` CLI script
- [x] `generate_binder_bytes()` in-memory function
- [x] Cover page, TOC, recipe pages
- [x] `BorderedCanvas` subclass for decorative borders
- [x] `/recipes/download-pdf` route in web app
- [x] Substitutions section in PDF output

## Scope

- Output format: letter-size PDF via ReportLab
- Out of scope: custom cover title, recipe subset selection from web UI (CLI supports it), page numbers

## Files

- `generate_pdf.py` — PDF generation logic; `generate_binder_bytes()` used by web app
- `pantry_app.py` — route `/recipes/download-pdf`
- `data/*.json` — recipe source data
- `output/recipe_binder.pdf` — CLI output (gitignored)
