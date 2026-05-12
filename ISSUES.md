# Issues Tracker

Open bugs and tech debt. Use `/t` to investigate and fix a bug, `/w` to review this list.

---

## Open Bugs

### ~~[BUG-001] Minimums page shows "in stock" instead of correct stock status~~ FIXED
- **Root cause:** The "In Stock" column was an Exclusions toggle (not a stock status indicator). The label "In Stock" appeared on every row making it look like a stock report. Renamed to "Always On Hand" throughout `templates/settings.html`.

### [BUG-002] `MINIMUMS_HTML` is dead code
- **What breaks:** `MINIMUMS_HTML` template is defined but never rendered; the `/minimums` route just redirects to `/settings?tab=minimums`.
- **Criterion violated:** `stock-minimums.feature.md` Known Bugs entry.
- **Look here first:** `pantry_app.py` ~line 765 (`MINIMUMS_HTML` definition) and the `/minimums` redirect route.

### ~~[BUG-003] "Always On Hand" toggle on Minimums tab does not update on click~~ FIXED
- **Root cause:** Button had no `type="button"`, defaulting to `type="submit"`. The `<form class="qty-form">` inside the adjacent `<td>` is foster-parented by the browser, and in some browsers the button was treated as a submit trigger for that form — submitting to `/minimums/set` instead of firing the JS fetch. Also simplified fetch URL away from `url_for`+replace pattern; added `.catch()` for error visibility. Fix in `templates/settings.html`.

### ~~[BUG-004] All writes fail on Linux — missing directories~~ FIXED
- **Root cause:** `state/` and `backups/` are gitignored and were never auto-created. All `save_*` functions wrote directly into these paths; on a fresh clone they raised `FileNotFoundError`. Fixed by adding `STATE_DIR.mkdir(parents=True, exist_ok=True)` in `pantri/state.py` and `STATE_DIR.mkdir` + `BACKUP_DIR.mkdir` in `pantri/backup.py`. Deployment flow doc created at `docs/deployment.flow.md`.

---

## Tech Debt

_(none recorded yet)_
