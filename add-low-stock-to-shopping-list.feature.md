---
name: Add Low-Stock to Shopping List
description: One-click button on the Shopping page that pushes all below-minimum pantry items onto the persistent shopping list
flow: shopping.flow.md
---

## What It Does

Adds an "Add all to shopping list" button to the Restock Needs card on `/shopping`. Clicking it queues every item currently below its minimum (excluding items already on the list and any exclusions) into `shopping_list.json`.

## Success Criteria

1. When the Restock Needs card has at least one item, an "Add all to shopping list" button is visible below the table.
2. Clicking the button adds each low-stock item to the shopping list with: name, amount needed (minimum − current, rounded to 1 decimal), and a note of "Restock".
3. Items already present on the shopping list (by name, case-insensitive) are not duplicated.
4. Items in the exclusions list are not added.
5. After the POST, the user is redirected back to `/shopping` and the Shopping List card reflects the newly added items.
6. If the Restock Needs card is empty ("Nothing below minimum"), no button is shown.
7. If all low-stock items are already on the list, the button still completes without error; the list is unchanged.

## Status

IN PROGRESS

### Progress

- [ ] Add `/shopping/list/add-low-stock` POST route to `pantry_app.py`
- [ ] Add "Add all to shopping list" button to `SHOPPING_HTML` Restock Needs card
- [ ] Verify deduplication against existing shopping list items
- [ ] Verify exclusions are respected
- [ ] Manual test: button adds correct items and amounts
- [ ] Manual test: no duplicates when clicked twice

## Scope

- Single POST route + one button in the existing HTML template string
- No new data files or models
- Out of scope: bulk-updating quantities, auto-removing items when restocked

## Files

- `pantry_app.py` — new route + HTML template change
- `shopping.flow.md` — flow doc (step 3)
