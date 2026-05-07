---
name: Exclusions
description: Pantry staples that are never auto-decremented when a recipe is used, with in/out-of-stock tracking
flow: settings.flow.md
status: COMPLETE
---

## What It Does

The Exclusions tab in Settings manages a list of staple items (e.g. salt, oil) that should never be automatically decremented from the pantry when "Use Recipe" is clicked. Each exclusion also has an in/out-of-stock toggle; out-of-stock exclusions appear in the Shopping page as a reminder to restock.

## Success Criteria

1. The Exclusions tab shows all exclusions with name, container description, and in/out-of-stock status.
2. Adding an exclusion (name + container) appends it to `exclusions.json` with `in_stock: true`.
3. Duplicate exclusions (same name, case-insensitive) are rejected silently.
4. Clicking the in/out-of-stock toggle flips the `in_stock` flag and refreshes the display.
5. Deleting an exclusion removes it from `exclusions.json`.
6. When "Use Recipe" is run, any ingredient whose name fuzzy-matches an exclusion entry is skipped (not decremented).
7. When adding recipe missing ingredients to the shopping list, excluded items are not added.
8. Out-of-stock exclusions appear in the "Out of Stock (Staples)" card on the Shopping page.
9. Toggling an out-of-stock exclusion to in-stock from the Shopping page removes it from that card.

## Status

COMPLETE

### Progress

- [x] `exclusions.json` load/save helpers
- [x] Exclusions tab in Settings UI (add, toggle, delete)
- [x] Exclusion skip in `recipe_use` route
- [x] Exclusion skip in `shopping_list_add_recipe` route
- [x] Out-of-stock exclusions card in Shopping page

## Scope

- Name-based fuzzy matching (contains/contained-by) for exclusion checks
- Out of scope: per-recipe exclusion overrides

## Files

- `pantry_app.py` — `SETTINGS_HTML` (exclusions tab), `SHOPPING_HTML` (out-of-stock card), routes `/exclusions/add`, `/exclusions/delete/<name>`, `/exclusions/toggle/<name>`, helpers `load_exclusions`, `save_exclusions`, `is_excluded`
- `exclusions.json` — persisted exclusion list (gitignored)
- `settings.flow.md` — flow doc
