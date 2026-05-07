---
name: Recipe Use
description: Deduct a recipe's ingredients from the pantry inventory in one click
flow: recipe.flow.md
status: COMPLETE
---

## What It Does

The "Use Recipe" button on a recipe detail page deducts each ingredient's quantity from the pantry. Exclusions (pantry staples) are never decremented. Fuzzy name matching finds pantry rows even when names don't match exactly. After use, a banner reports how many items were removed and how many weren't found.

## Success Criteria

1. Clicking "Use Recipe" shows a browser confirm before submitting.
2. For each ingredient, the leading numeric quantity is parsed from the amount string (e.g. "1.5 lbs" → 1.5); falls back to 1.0 if no number found.
3. Each ingredient is matched against pantry rows using fuzzy logic: pantry cell name contains ingredient name, or ingredient name contains pantry cell name (case-insensitive).
4. The matched pantry row's quantity is decremented by the ingredient qty, floored at 0.
5. Ingredients whose name matches any exclusion entry are skipped (not decremented).
6. After the POST, the detail page shows a green banner: "Recipe used — X ingredient(s) removed from pantry. (Y item(s) not found in pantry.)"
7. If Y > 0 (items not found), the not-found count is shown in the banner.
8. The pantry xlsx is saved after all deductions (single save, not one per ingredient).

## Status

COMPLETE

### Progress

- [x] POST /recipe/<slug>/use route
- [x] Ingredient qty parsing (leading number from amount string)
- [x] Fuzzy pantry lookup
- [x] Exclusion skip logic
- [x] Floor at 0 (no negative quantities)
- [x] Post-use banner with counts

## Scope

- One-time deduction per button press; no undo
- Out of scope: partial-quantity deduction UI, tracking recipe history

## Files

- `pantry_app.py` — route `/recipe/<slug>/use`, `RECIPE_DETAIL_HTML` (use button + banner)
- `Food in Storage.xlsx` — mutated on use
- `recipe.flow.md` — flow doc
