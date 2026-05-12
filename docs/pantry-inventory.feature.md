---
name: Pantry Inventory
description: View, search, filter, add, edit, and delete items in the pantry via the web UI
flow: inventory.flow.md
status: COMPLETE
---

## What It Does

Primary inventory management UI at `/`. Shows all items across all storage locations with search/filter. Supports adding single items, editing existing items, and deleting items. Duplicate item+unit combinations are automatically merged rather than duplicated.

## Success Criteria

1. All pantry items across all location sheets are visible in a single table on `/`.
2. Searching by name (`?q=`) filters results to items whose name contains the query (case-insensitive).
3. Filtering by location (`?loc=`) shows only items in that location.
4. Clicking "Edit" on a row opens `/edit/<sheet>:<row>` with all fields pre-populated.
5. Saving an edit writes back to the correct xlsx row; if location changed, the item moves to the new sheet.
6. If an edited item's name+unit matches another row in the target sheet, quantities are merged and the original row is cleared.
7. Clicking "Del" shows a browser confirm; on confirm, the row is cleared from xlsx and the item disappears from the list.
8. The "Add Items" tab (`?tab=add`) shows a single-item form and a bulk-add form.
9. Adding a single item that already exists (same name + unit in target sheet) increments its quantity rather than creating a duplicate row.
10. If no storage locations are configured, a prompt card is shown instead of the item table or add forms.

## Status

COMPLETE

### Progress

- [x] Index route with search/filter
- [x] Add single item (POST /add with merge logic)
- [x] Edit item (/edit/<row_key>)
- [x] Delete item (/delete/<row_key>)
- [x] Bulk add (/add/bulk)
- [x] Empty-state prompt when no locations exist

## Scope

- All inventory CRUD operations in the web UI
- Auto-merge on duplicate name+unit
- Out of scope: sorting columns, pagination, quantity adjustments without full edit

## Known Bugs

- [BUG] `ADD_PAGE_HTML` template (~80 lines, `pantry_app.py:618`) is dead code — it is defined but never rendered. The `/add` GET route redirects to `/?tab=add`; add forms live inside `INDEX_HTML`. **Fixed when:** `ADD_PAGE_HTML` is deleted from `pantry_app.py` with no change in observable behavior.
- ~~[BUG] **SYSTEMIC — Linux only.** All write operations fail on a fresh Linux install.~~ FIXED — `STATE_DIR.mkdir` added to `pantri/state.py`; `STATE_DIR.mkdir` + `BACKUP_DIR.mkdir` added to `pantri/backup.py`. Deployment guide at `docs/deployment.flow.md`.

## Files

- `pantry_app.py` — `INDEX_HTML`, `EDIT_HTML`, routes `/`, `/add`, `/edit/<row_key>`, `/delete/<row_key>`, `/add/bulk`
- `Food in Storage.xlsx` — data source (gitignored)
- `inventory.flow.md` — flow doc
