---
name: Inventory Flow
description: User views, searches, adds, edits, and deletes pantry items via the web app
---

# Inventory Flow

## Entry point
`/` — navbar "Inventory" link

## Step table

| Step | What the user sees | What the system does |
|------|--------------------|----------------------|
| 1 | Lands on Inventory page, "Items" tab active | Loads all rows from all location sheets in xlsx; shows total count |
| 2 | If no locations set: prompt card directs user to Settings → Locations | No rows to show |
| 3 | Searches by name or filters by location | GET params `q` and `loc` re-filter rows; no server reload needed via form submit |
| 4 | Clicks "Edit" on a row | Navigates to `/edit/<sheet>:<row>` — pre-populated form |
| 5 | Saves edit | POST writes updated cells back to xlsx, merges if name+unit collision exists in same or target sheet, redirects to `/` |
| 6 | Clicks "Del" on a row | JS confirm prompt; GET to `/delete/<sheet>:<row>` clears cells, redirects to `/` |
| 7 | Clicks "Add Items" tab | Same page, `?tab=add`; shows single-item and bulk-add forms side by side |
| 8 | Submits single-item form | POST to `/add`; merges if item+unit already exists in target sheet, then redirects to `/?tab=add` |
| 9 | Submits bulk-add form | POST to `/add/bulk`; parses CSV lines, merges or inserts each, shows per-line results |

## Failure modes

| Condition | Behavior |
|-----------|----------|
| xlsx missing or unreadable | `init_wb()` creates a blank workbook |
| Location not in xlsx | Falls back to first available location |
| Duplicate item+unit in same sheet | Quantities are summed (merged), not duplicated |
| Bulk line missing item name | Line skipped silently |
