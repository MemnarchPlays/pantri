---
name: Settings Flow
description: User configures locations, minimums, exclusions, Discord bot, and backups via the Settings page
---

# Settings Flow

## Entry point
`/settings` — navbar "⚙ Settings" link; tabs: Discord Bot, Minimums, Locations, Backups, Exclusions

---

## Locations tab

| Step | What the user sees | What the system does |
|------|--------------------|----------------------|
| 1 | Table of existing storage locations with item counts | Each location is a sheet in the xlsx |
| 2 | Types a name and clicks "Add" | POST to `/locations/add`; creates new xlsx sheet with column headers |
| 3 | Clicks "Delete" on an empty location | GET to `/locations/delete/<name>`; removes sheet from xlsx |
| 4 | Location has items — delete blocked | "X items — clear first to delete" message; no delete button shown |

---

## Minimums tab

| Step | What the user sees | What the system does |
|------|--------------------|----------------------|
| 1 | Table of items with minimum quantities | Reads `Minimums` sheet from xlsx |
| 2 | Clicks a quantity value | Inline edit: number input replaces the display |
| 3 | Saves inline edit | POST to `/minimums/set`; updates or inserts row in Minimums sheet |
| 4 | Fills "Add New Minimum" form and saves | POST to `/minimums/set`; same route handles both create and update |
| 5 | Clicks "Del" on a row | GET to `/minimums/delete/<item>`; removes row from Minimums sheet |

---

## Exclusions tab

| Step | What the user sees | What the system does |
|------|--------------------|----------------------|
| 1 | Table of excluded items with container description and in/out-of-stock toggle | Reads `exclusions.json` |
| 2 | Adds an item (name + container) | POST to `/exclusions/add`; appends to `exclusions.json`, defaults to in-stock |
| 3 | Toggles in/out of stock | POST to `/exclusions/toggle/<name>`; flips `in_stock` flag; out-of-stock items appear in Shopping page |
| 4 | Deletes an exclusion | GET to `/exclusions/delete/<name>`; removes from `exclusions.json` |

---

## Discord Bot tab

| Step | What the user sees | What the system does |
|------|--------------------|----------------------|
| 1 | Bot status badge (Online/Offline), token field, alert channel field, bot log | Status polled via `/settings/bot-status` on load; log fetched via `/settings/bot-log` |
| 2 | Pastes token, saves | POST to `/settings/discord` with `action=save`; writes to `.env` |
| 3 | Clicks "Save & Restart Bot" | POST with `action=save_restart`; writes `.env`, calls `start_bot()` |
| 4 | Clicks "Stop Bot" | POST with `action=stop`; terminates subprocess, clears `bot.pid` |
| 5 | Clicks "Remove Connection" | POST with `action=remove`; stops bot, removes token from `.env` |

---

## Backups tab

| Step | What the user sees | What the system does |
|------|--------------------|----------------------|
| 1 | Backup mode selector (every X saves / every X hours / manual), counts-to-backup status, list of saved backups | Reads `.env` for config; reads `backup_state.json` for counts |
| 2 | Changes settings and saves | POST to `/settings/backups`; writes `BACKUP_MODE`, `BACKUP_EVERY_N`, `BACKUP_INTERVAL_HRS`, `BACKUP_MAX` to `.env` |
| 3 | Clicks "Backup Now" | POST to `/backups/now`; forces a timestamped copy to `backups/` |
| 4 | Clicks "Download" on a backup | GET to `/backups/download/<filename>`; sends file as attachment |
| 5 | Clicks "Restore" on a backup | POST to `/backups/restore/<filename>`; first backs up current xlsx, then copies backup over it |

## Interface tab (Appearance + Server)

| Step | What the user sees | What the system does |
|------|--------------------|----------------------|
| 1 | Color picker, font selector, preset buttons, Preview card | JS reads `window._pantri` (color/font from localStorage) and populates controls on load |
| 2 | Drags color picker or clicks preset | `applyColor()` updates CSS vars live; sample Preview boxes reflect change immediately |
| 3 | Clicks **Apply** | `applyAndSave()` writes color + font to `localStorage`; applies to full page |
| 4 | Selects port and/or timezone; clicks **Save** | POST to `/settings/appearance`; writes `PORT`, `DISPLAY_TZ`, `ACCENT_COLOR`, `FONT_FAMILY` to `.env`; redirects to `?tab=interface` |

---

## Failure modes

| Condition | Behavior |
|-----------|----------|
| Location delete: sheet has items | Delete button not shown; instructional message shown instead |
| Bot start: no token set | `start_bot()` returns False silently; bot stays offline |
| Backup restore: file not in backups/ dir | Redirect without action (path traversal guard) |
| Always On Hand toggle: fetch fails (server error) | Button shows "Error — try again"; exclusion state unchanged |
| Always On Hand button near `<form>` in same table row | Button must have `type="button"` to prevent form hijack; foster-parented `<form>` inside `<td>` can capture adjacent buttons in some browsers |
| Port < 1024 entered in Interface tab | Valid and saved; binding to privileged ports on Linux requires root or `CAP_NET_BIND_SERVICE` — that is the user's responsibility, not enforced by the app |
