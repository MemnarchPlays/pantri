---
name: Recipe Library
description: Browse, search, filter, and view recipes in the web UI
flow: recipe.flow.md
status: COMPLETE
---

## What It Does

The Recipe Library tab at `/recipes` lists all recipes from `data/*.json`. Supports filtering by name and meal type. Each recipe links to a detail page showing ingredients (with pantry availability markers), instructions, macros, substitutions, and a live serving-scaler.

## Success Criteria

1. All recipes in `data/*.json` appear in the library table sorted alphabetically.
2. Searching by name (`?q=`) filters to recipes whose name contains the query.
3. Filtering by meal type (`?meal=`) filters to matching meal types.
4. Each recipe row in the table links to `/recipe/<slug>`.
5. The detail page shows: name, meal type, prep/cook time, servings, macro tiles, ingredient list, instructions, substitutions (if any), and notes (if any).
6. Each ingredient on the detail page shows ✅ if a pantry item name fuzzy-matches it, and • if not.
7. Changing the servings input scales all ingredient amounts in real time without a page reload.
8. Malformed JSON files are silently skipped; they don't break the page.

## Status

COMPLETE

### Progress

- [x] Recipe listing with search/filter
- [x] Recipe detail page
- [x] Pantry availability markers per ingredient
- [x] Serving scaler (client-side JS, handles fractions and vulgar fraction characters)
- [x] PDF download button in header

## Scope

- Read-only browsing and viewing
- Out of scope: recipe CRUD (see `recipe-management.feature.md`), can-make tab (see `can-i-make.feature.md`)

## Known Bugs

- ~~[BUG] Recipe library is empty on a fresh git clone.~~ FIXED — removed `data/*.json` from `.gitignore`; all 89 recipes are now tracked in git and present after a fresh clone.

## Files

- `pantry_app.py` — `RECIPES_HTML`, `RECIPE_DETAIL_HTML`, routes `/recipes`, `/recipe/<slug>`
- `data/*.json` — recipe data
- `recipe.flow.md` — flow doc
