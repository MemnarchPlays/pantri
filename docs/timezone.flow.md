---
name: Timezone Display Flow
description: How backup timestamps are converted to the user's configured timezone for display
---

# Timezone Display Flow

## Entry point

`/settings?tab=backups` → Backups tab → backup list and "last backup" label

---

## Pipeline

| Step | File / Function | What happens |
|------|----------------|--------------|
| 1 | `pantri/routes/settings.py:settings()` | Reads `DISPLAY_TZ` from `.env`; builds ZoneInfo object; passes to `get_backups()` and to template context |
| 2 | `pantri/backup.py:get_backups()` | Converts each file's `stat.st_mtime` (UTC epoch float) to a `datetime` in the requested timezone via `datetime.fromtimestamp(ts, tz=tz)` |
| 3 | `pantri/backup.py:get_backup_info()` | "X ago" label is timestamp arithmetic (epoch float subtraction) — timezone-independent; no conversion needed |
| 4 | `templates/settings.html` | Renders the converted datetime strings; timezone dropdown populated by `tz_options` passed from route |
| 5 | `pantri/routes/settings.py:settings_appearance()` | POST handler saves `DISPLAY_TZ` to `.env`; validates the value is a real IANA zone via `ZoneInfo(name)` |

---

## Key identifiers

| Name | Role |
|------|------|
| `DISPLAY_TZ` | `.env` key — IANA timezone name (e.g. `America/Chicago`). Default: `UTC` |
| `zoneinfo.ZoneInfo` | Python 3.9+ stdlib; needs `tzdata` pip package on Windows / Docker slim |
| `datetime.fromtimestamp(ts, tz=tz)` | Correct conversion: UTC epoch → aware datetime in target zone |
| `datetime.fromtimestamp(ts)` (old) | Wrong: uses server local time, not user timezone |

---

## Failure modes

| Condition | Behavior |
|-----------|----------|
| `DISPLAY_TZ` not set | Defaults to `UTC` — predictable across any server |
| Invalid tz name in `.env` | `ZoneInfo()` raises `ZoneInfoNotFoundError`; caught, falls back to UTC |
| `tzdata` package missing on Windows | `zoneinfo.available_timezones()` returns empty set; stdlib fallback still provides UTC |
