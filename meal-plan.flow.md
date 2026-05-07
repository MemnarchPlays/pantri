---
name: Meal Plan Flow
description: User builds a weekly meal plan and generates a combined shopping list from it
---

# Meal Plan Flow

## Entry point
`/meal-plan` — new navbar link "Meal Plan"

## Step table

| Step | What the user sees | What the system does |
|------|--------------------|----------------------|
| 1 | Lands on Meal Plan page (Mon–Sun grid) | Loads saved plan from `meal_plan.json`; loads all recipes |
| 2 | Each day row has a dropdown to pick a recipe (or "— none —") | Plan is pre-populated from saved state |
| 3 | Selects recipes for desired days | No save yet — form state only |
| 4 | Clicks "Save Plan" | POSTs to `/meal-plan/save`; writes `meal_plan.json` |
| 5 | Saved plan persists across sessions | Plan reloads on next visit |
| 6 | Clicks "Add plan to shopping list" | POSTs to `/meal-plan/shopping`; for each recipe in plan, adds missing ingredients (not in pantry, not already on list, not excluded) to `shopping_list.json` |
| 7 | Redirected to `/shopping` | Shopping list now contains combined missing items for the week |

## Failure modes

| Condition | Behavior |
|-----------|----------|
| No recipes exist | All day dropdowns show only "— none —" |
| All ingredients already in pantry | Shopping list unchanged; success message shown |
| `meal_plan.json` missing | Page renders with all days empty |
