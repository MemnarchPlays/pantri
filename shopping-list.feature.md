---
name: Shopping List
description: Track items to buy — from low-stock alerts, missing recipe ingredients, or manually — with check-off and clear functionality
flow: shopping.flow.md
status: COMPLETE
---

## What It Does

The Shopping page at `/shopping` has three panels: a "Restock Needs" table (items below minimum), a "Missing Recipe Ingredients" picker (select a recipe, see what's missing, add to list), and the persistent Shopping List (check off items as purchased, remove individual items or clear all checked). Out-of-stock exclusions get their own card. The shopping list persists across sessions in `shopping_list.json`.

## Success Criteria

1. The "Restock Needs" card lists every item whose current stock is below its minimum, showing current qty, amount needed (minimum − current), and unit.
2. The "Missing Recipe Ingredients" card has a recipe dropdown; selecting a recipe shows ingredients not found in the pantry (fuzzy match).
3. Clicking "Add N missing items to shopping list" appends each missing, non-excluded, not-already-on-list ingredient to `shopping_list.json` with a `note` of "For: {Recipe Name}".
4. Shopping list items show name, amount, note, and a check checkbox.
5. Checking an item marks it visually (struck-through or dimmed) without removing it.
6. "Remove checked" clears all checked items from the list.
7. Unchecked items persist across page reloads.
8. Individual items can be removed via a remove button.
9. Out-of-stock exclusions appear in a separate card; toggling them to in-stock removes them from that card.
10. Items already on the shopping list are not duplicated when adding from a recipe.
11. Excluded items are never added to the shopping list via the add-recipe route.

## Status

COMPLETE

### Progress

- [x] Restock Needs card (low-stock from minimums)
- [x] Missing recipe ingredients picker
- [x] Add missing items to shopping list (POST /shopping/list/add-recipe)
- [x] Shopping list display with check/uncheck
- [x] Toggle checked (POST /shopping/list/toggle/<id>)
- [x] Remove individual item (/shopping/list/remove/<id>)
- [x] Clear checked (POST /shopping/list/clear-checked)
- [x] Out-of-stock exclusions card
- [x] Deduplication and exclusion filtering on add

## Scope

- Manual list management only; no auto-sync from pantry changes
- Out of scope: adding low-stock items to list with one button (tracked in `add-low-stock-to-shopping-list.feature.md`)

## Known Bugs

- [BUG] `RESTOCK_HTML` template (~30 lines, `pantry_app.py:1832`) is dead code — it is defined but never rendered. The `/restock` route redirects to `/shopping` which uses `SHOPPING_HTML`. **Fixed when:** `RESTOCK_HTML` is deleted and the `/restock` redirect route is removed with no change in observable behavior.

## Files

- `pantry_app.py` — `SHOPPING_HTML`, routes `/shopping`, `/shopping/list/add-recipe`, `/shopping/list/toggle/<id>`, `/shopping/list/remove/<id>`, `/shopping/list/clear-checked`, helpers `load_shopping_list`, `save_shopping_list`
- `shopping_list.json` — persisted list (gitignored)
- `shopping.flow.md` — flow doc
