---
name: Weekly Meal Planner
description: A Mon–Sun meal plan page that saves recipe selections and pushes all missing ingredients to the shopping list in one click
flow: meal-plan.flow.md
---

## What It Does

Adds a `/meal-plan` page where the user picks one recipe per day of the week. The plan persists across sessions in `meal_plan.json`. A single "Add plan to shopping list" button queues all missing ingredients for the week's recipes (filtered against pantry inventory and exclusions) into the shopping list.

## Success Criteria

1. `/meal-plan` renders a grid with one row per day (Monday–Sunday), each with a dropdown of all available recipes plus a "— none —" option.
2. Previously saved selections are pre-populated on page load from `meal_plan.json`.
3. Clicking "Save Plan" POSTs and persists the selection; the page reloads showing the saved state.
4. Clicking "Add plan to shopping list" adds missing ingredients for all planned recipes — an ingredient is missing if no pantry item name contains it or is contained by it (same logic as `/shopping/list/add-recipe`).
5. Excluded items (from exclusions list) are not added to the shopping list.
6. Items already on the shopping list are not duplicated; the note field reads "Meal plan: {Recipe Name}".
7. After "Add plan to shopping list", the user is redirected to `/shopping`.
8. If no recipes are selected for any day, "Add plan to shopping list" redirects to `/shopping` without modifying the list.
9. If no recipes exist in `data/`, all dropdowns show only "— none —" and the add button is disabled.
10. "Meal Plan" appears in the navbar between "Recipes" and "Shopping".

## Status

IN PROGRESS

### Progress

- [ ] Add `meal_plan.json` load/save helpers
- [ ] Add `GET /meal-plan` route + `MEAL_PLAN_HTML` template string
- [ ] Add `POST /meal-plan/save` route
- [ ] Add `POST /meal-plan/shopping` route (missing-ingredient aggregation across all planned recipes)
- [ ] Add "Meal Plan" nav link to `BASE_HTML` navbar
- [ ] Manual test: plan saves and reloads correctly
- [ ] Manual test: add-to-shopping deduplicates and respects exclusions
- [ ] Manual test: empty plan does not modify shopping list

## Scope

- New page, two new routes, new navbar link, new `meal_plan.json` data file
- One recipe per day slot; no multi-recipe-per-day in this iteration
- Out of scope: drag-and-drop reordering, recurring plans, plan history

## Files

- `pantry_app.py` — new routes + HTML template + navbar update
- `meal_plan.json` — persisted plan (gitignored, personal data)
- `meal-plan.flow.md` — flow doc
