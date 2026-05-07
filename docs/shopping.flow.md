---
name: Shopping Flow
description: User navigates to /shopping to review what needs restocking and build a shopping list
---

# Shopping Flow

## Entry point
`/shopping` — navbar "Shopping" link

## Step table

| Step | What the user sees | What the system does |
|------|--------------------|----------------------|
| 1 | Lands on Shopping page | Loads pantry stock, minimums, all recipes, saved shopping list |
| 2 | "Restock Needs" card shows items below minimum with current qty, amount needed, unit | Compares stock totals against Minimums sheet |
| 3 | Clicks "Add all to shopping list" | POSTs to `/shopping/list/add-low-stock`; appends each low item (not already on list, not excluded) |
| 4 | "Missing Recipe Ingredients" card — picks a recipe from dropdown | Page reloads with missing ingredients listed |
| 5 | Clicks "Add N missing items to shopping list" | POSTs to `/shopping/list/add-recipe`; appends missing ingredients |
| 6 | "Shopping List" card shows all queued items | Loaded from `shopping_list.json` |
| 7 | Checks off items as they're purchased | Toggles `checked` flag via `/shopping/list/toggle/<id>` |
| 8 | Clicks "Remove checked" | Clears checked items from list |

## Failure modes

| Condition | Behavior |
|-----------|----------|
| No minimums set | Restock Needs card says "Nothing below minimum" |
| All low items already on list | Add all button adds 0 new items; list unchanged |
| No recipes loaded | Recipe dropdown is empty |
| Pantry xlsx unreadable | Page fails with 500 |
