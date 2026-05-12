# Issues Tracker

Open bugs and tech debt. Use `/t` to investigate and fix a bug, `/w` to review this list.

---

## Open Bugs

### ~~[BUG-001] Minimums page shows "in stock" instead of correct stock status~~ FIXED
- **Root cause:** The "In Stock" column was an Exclusions toggle (not a stock status indicator). The label "In Stock" appeared on every row making it look like a stock report. Renamed to "Always On Hand" throughout `templates/settings.html`.

### ~~[BUG-002] `MINIMUMS_HTML` is dead code~~ FIXED
- **Root cause:** These dead template strings (`MINIMUMS_HTML`, `ADD_PAGE_HTML`, `CAN_MAKE_HTML`, `RESTOCK_HTML`) were eliminated by the blueprint refactor — they never existed in the `pantri/` package. The bug entries in the feature docs referenced the old monolith (`pantry_app.py`) which was replaced. No code change needed; docs updated to reflect reality.

### ~~[BUG-003] "Always On Hand" toggle on Minimums tab does not update on click~~ FIXED
- **Root cause:** Button had no `type="button"`, defaulting to `type="submit"`. The `<form class="qty-form">` inside the adjacent `<td>` is foster-parented by the browser, and in some browsers the button was treated as a submit trigger for that form — submitting to `/minimums/set` instead of firing the JS fetch. Also simplified fetch URL away from `url_for`+replace pattern; added `.catch()` for error visibility. Fix in `templates/settings.html`.

### ~~[BUG-004] All writes fail on Linux — missing directories~~ FIXED
- **Root cause:** `state/` and `backups/` are gitignored and were never auto-created. All `save_*` functions wrote directly into these paths; on a fresh clone they raised `FileNotFoundError`. Fixed by adding `STATE_DIR.mkdir(parents=True, exist_ok=True)` in `pantri/state.py` and `STATE_DIR.mkdir` + `BACKUP_DIR.mkdir` in `pantri/backup.py`. Deployment flow doc created at `docs/deployment.flow.md`.

### ~~[BUG-005] Bulk-add always writes to "End Hall Closet" regardless of selected location~~ FIXED
- **Root cause:** The bulk-add location `<select>` was missing the `selected` attribute on `<option>` tags, so the browser always defaulted to the first xlsx sheet ("End Hall Closet"). The single-item form already had this correct. Fixed by adding `{% if default_location == l %}selected{% endif %}` to the bulk-add dropdown in `templates/inventory.html`.

### ~~[BUG-006] Recipe library is empty on a fresh git clone~~ FIXED
- **Root cause:** `data/*.json` was added to `.gitignore` to protect Linux from overwrite on pull, but recipes are shared authoritative data — pull syncing them is correct. Removed `data/*.json` from `.gitignore` and re-tracked all 89 recipe files in git. Updated `docs/deployment.flow.md` to reflect that recipes are now git-managed.

---

### ~~[BUG-007] Theme color sample text does not update in real-time~~ FIXED
- **What breaks:** On Settings → Appearance, the sample text only reflects the new color after clicking Apply. Changing the color picker has no visible effect until Apply is clicked.
- **Criterion violated:** `docs/appearance.feature.md` — "Sample text updates in real-time as the color is changed"
- **Look first:** `templates/settings.html` — color picker `input[type=color]` is missing an `oninput` handler to update the sample preview.
- **Flow doc:** None — flag for `/t` to create before fixing.

---

### ~~[BUG-008] Interval backup mode does not fire on schedule~~ FIXED
- **What breaks:** With `BACKUP_MODE=interval` set to e.g. 2 hours, backups are not written after the configured time elapses.
- **Criterion violated:** `docs/backups.feature.md` criterion 2 — "a backup is written when more than N hours have passed since the last backup."
- **Look first:** `pantri/backup.py` → `backup_wb()` interval branch (timestamp comparison logic); `pantri/routes/settings.py` → POST handler writing `BACKUP_INTERVAL_HRS` to `.env`.
- **Flow doc:** `docs/settings.flow.md` covers the Backups tab save step; no dedicated backup-trigger flow doc exists — flag for `/t`.

---

## Tech Debt

_(none recorded yet)_
