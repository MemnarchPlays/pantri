---
name: Stock Minimums
description: Per-item minimum quantity thresholds used to detect low-stock items
flow: settings.flow.md
status: COMPLETE
---

## What It Does

The Minimums tab in Settings lets the user set a minimum quantity for any pantry item. When an item's current stock falls below its minimum, it appears in the "Restock Needs" section of the Shopping page. Minimums are stored in a dedicated `Minimums` sheet in the xlsx. Quantities can be edited inline by clicking the number.

## Success Criteria

1. The Minimums tab shows all current minimum entries sorted alphabetically.
2. Clicking a minimum quantity value reveals an inline number input pre-filled with the current value.
3. Saving the inline edit (✓ button) updates the Minimums sheet without a full page reload of the tab.
4. The "Add New Minimum" form accepts an item name and quantity; submitting creates or updates the entry.
5. Submitting a minimum for an item that already has one updates the existing row (does not duplicate).
6. Clicking "Del" removes the item's minimum entry from the xlsx.
7. Items with a minimum set appear in the Shopping page "Restock Needs" card when their stock is below the minimum.

## Status

COMPLETE

### Progress

- [x] Minimums sheet read/write helpers (`get_minimums`, `set_minimum`, `delete_minimum`)
- [x] Minimums tab in Settings UI
- [x] Inline edit (click qty to edit, JS toggling)
- [x] Add/update via single `/minimums/set` route
- [x] Delete via `/minimums/delete/<item>`
- [x] Shopping page consumes minimums for low-stock detection

## Scope

- Per-item minimum qty only (no per-location, no per-unit minimums)
- Out of scope: bulk import of minimums, minimum history

## Known Bugs

- [BUG] `MINIMUMS_HTML` template (~80 lines, `pantry_app.py:765`) is dead code — it is defined but never rendered. The `/minimums` route redirects to `/settings?tab=minimums` which uses `SETTINGS_HTML`. **Fixed when:** `MINIMUMS_HTML` is deleted and the `/minimums` redirect route is removed with no change in observable behavior.
- ~~[BUG] The Minimums page displays "in stock" for items instead of the expected status.~~ FIXED — Renamed the Exclusions toggle column from "In Stock" to "Always On Hand" in `templates/settings.html` (column header, button label, and JS update).

## Files

- `pantry_app.py` — `SETTINGS_HTML` (minimums tab), routes `/minimums/set`, `/minimums/delete/<item>`, helpers `get_minimums`, `set_minimum`, `delete_minimum`
- `Food in Storage.xlsx` — `Minimums` sheet
- `settings.flow.md` — flow doc
