---
name: Storage Locations
description: Manage named storage locations; each location is an xlsx sheet that holds pantry items
flow: settings.flow.md
status: COMPLETE
---

## What It Does

The Locations tab in Settings manages the physical storage locations (e.g. "Brown Cabinet", "Pantry", "Fridge"). Each location corresponds to one sheet in the xlsx workbook. Adding a location creates a new sheet with column headers. Deleting is only permitted when the sheet has no items.

## Success Criteria

1. The Locations tab lists all current location sheets (excluding the Minimums sheet) with their item counts.
2. Submitting a new location name creates a new xlsx sheet with the standard column headers (`Item, Quantity, Unit, Location, Section, Slot, Expiration, Notes`).
3. A location named "Minimums" cannot be created (protected sheet name).
4. Duplicate location names are silently ignored (no duplicate sheets created).
5. Locations with 0 items show a "Delete" button.
6. Locations with items show "X items — clear first to delete" and no delete button.
7. Deleting a location removes the sheet from xlsx.
8. Newly added locations immediately appear in the inventory add/edit location dropdowns.

## Status

COMPLETE

### Progress

- [x] Location sheet creation with headers
- [x] Delete (empty-only guard)
- [x] Locations tab UI with item counts
- [x] Locations propagate to add/edit forms

## Scope

- Location = xlsx sheet; one-to-one mapping
- Out of scope: renaming locations, reordering sheets

## Files

- `pantry_app.py` — `SETTINGS_HTML` (locations tab), routes `/locations/add`, `/locations/delete/<name>`, helpers `get_location_sheets`, `get_location_info`
- `Food in Storage.xlsx` — sheets managed here
- `settings.flow.md` — flow doc
