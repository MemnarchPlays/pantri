---
name: Can I Make?
description: Shows which recipes can be made with current pantry inventory, sorted by ingredient match percentage
flow: recipe.flow.md
status: COMPLETE
---

## What It Does

The "Can I Make?" tab at `/recipes?tab=canmake` cross-references all recipes against the current pantry. Each recipe card shows a match percentage, status label, and list of missing ingredients. Recipes are sorted best-match first. Filterable by meal type and ingredient keyword.

## Success Criteria

1. Each recipe shows a percentage of ingredients present in the pantry (fuzzy match: item name contains or is contained by pantry item name).
2. Recipes at 100% show "✓ You have everything!" in green.
3. Recipes at 60–99% show "~X% — almost there" in amber.
4. Recipes at 1–59% show "X% (have/total ingredients)" in red.
5. Recipes at 0% show "0% — missing everything" in red.
6. Up to 6 missing ingredient names are listed below the status label.
7. Recipes are sorted highest-percentage first.
8. Filtering by meal type shows only recipes of that type.
9. Filtering by ingredient keyword shows only recipes containing that ingredient.
10. Recipes with no ingredients are excluded from the list.

## Status

COMPLETE

### Progress

- [x] Pantry have-set construction
- [x] Per-recipe fuzzy ingredient matching
- [x] Percentage calculation and status label tiers
- [x] Sort by match percentage descending
- [x] Meal type filter pills
- [x] Ingredient keyword filter

## Scope

- Read-only; no actions from this page
- Out of scope: "Add missing items to shopping list" from this tab (that lives on /shopping)

## Files

- `pantry_app.py` — `RECIPES_HTML` (canmake tab), `recipes()` route canmake branch
- `recipe.flow.md` — flow doc

## Known Bugs

- [BUG] `CAN_MAKE_HTML` template (~65 lines, `pantry_app.py:698`) is dead code — it is defined but never rendered. The `/can-make` route redirects to `/recipes?tab=canmake` which uses `RECIPES_HTML`. **Fixed when:** `CAN_MAKE_HTML` is deleted from `pantry_app.py` and the `/can-make` redirect route is also removed with no change in observable behavior.
