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

---

## Tech Debt

_(none recorded yet)_
