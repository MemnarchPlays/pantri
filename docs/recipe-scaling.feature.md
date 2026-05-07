---
name: Recipe Scaling
description: Live client-side scaling of ingredient amounts when the user changes the servings on a recipe detail page
flow: recipe.flow.md
status: COMPLETE
---

## What It Does

A servings input on the recipe detail page lets the user scale ingredient amounts up or down in real time without a page reload. The original serving count is preserved in the page; all amounts are re-derived from it each time the input changes. Handles integers, decimals, common fractions (1/2), mixed numbers (1 1/2), and Unicode vulgar fractions (½ ¼ ¾ etc.).

## Success Criteria

1. Changing the servings input immediately updates all ingredient amounts on the page (no page reload).
2. Amounts that are purely textual (no leading number) are left unchanged.
3. Integer results display as integers (e.g. 4.0 → 4).
4. Results near common eighth-fractions are displayed using Unicode vulgar characters (½, ¼, ¾, ⅛, ⅜, ⅝, ⅞).
5. Mixed numbers display correctly (e.g. 1.5 → 1 ½, 2.75 → 2 ¾).
6. Scaling to the original serving count restores all amounts to their original values.
7. Setting servings to 0 or a non-number has no effect (guard condition).
8. Scaling does not affect the macro tiles (macros are per-serving and don't change with serving count).

## Status

COMPLETE

### Progress

- [x] `scaleRecipe()` JS function triggered by servings input `oninput`
- [x] `scaleAmount()` — finds leading numeric portion, scales, rejoins text
- [x] `parseFraction()` — handles integers, decimals, simple fractions, mixed numbers, vulgar chars
- [x] `formatNum()` — rounds to nearest eighth, maps to vulgar fraction chars

## Scope

- Client-side only; scaled amounts are not saved
- Out of scope: saving a scaled version as a new recipe, scaling macro totals by serving count

## Files

- `pantry_app.py` — `RECIPE_DETAIL_HTML` (servings input + `scaleRecipe` JS)
- `recipe.flow.md` — flow doc
