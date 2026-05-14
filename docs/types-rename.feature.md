---
name: Types Rename
description: Inline click-to-edit for type names in Settings → Lists
flow: settings.flow.md
status: COMPLETE
---

## What It Does

Clicking a type name in the Settings → Lists tab reveals an inline text input pre-filled with the current name. Pressing ✓ saves the new name; pressing ✕ cancels without a page reload. Matches the existing quantity and type inline-edit pattern used in the Minimums table.

## Success Criteria

1. Clicking a type name in the Lists tab replaces the display span with a text input pre-filled with the current value.
2. Pressing ✓ POSTs the rename to `/types/rename`, saves the updated name, and redirects back to the Lists tab.
3. Pressing ✕ cancels — hides the input and restores the display span with no server round-trip.
4. Renaming to an empty string is rejected by the HTML `required` attribute before submission.
5. Renaming to a name that already exists (case-insensitive) is silently rejected; the existing list is unchanged.
6. Renaming to the same name (case-insensitive) is a no-op.

## Status

COMPLETE

### Progress

- [x] `/types/rename` POST route in `pantri/routes/settings.py`
- [x] Inline rename form and display span in `templates/settings.html` (Lists tab)
- [x] JS click-to-show and cancel handlers in `templates/settings.html`

## Scope

- Type name rename only — does not cascade to update existing minimums whose `type` field matches the old name
- Out of scope: cascade rename to minimums, rename history

## Files

- `pantri/routes/settings.py` — `types_rename()` route
- `templates/settings.html` — `.type-name-display` span, `.type-rename-form`, JS handlers
- `docs/settings.flow.md` — flow doc
