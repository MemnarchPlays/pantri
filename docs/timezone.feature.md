---
name: Timezone Setting
description: User can select a display timezone in Settings so timestamps match their local time regardless of server timezone
---

# Timezone Setting

## Success criteria

- [x] Settings → Interface exposes a timezone dropdown (IANA tz names, e.g. "America/Chicago")
- [x] Selected timezone is saved to `.env` as `DISPLAY_TZ` and persists across restarts
- [x] All displayed timestamps (backup list dates) are rendered in the selected timezone
- [x] Default is UTC so behavior is predictable on any server if no timezone is configured

## ~~[BUG] BUG-009 — Timestamps shown in server local time, not user's timezone~~ FIXED

**What "fixed" looks like:** A user on a US Central server whose home server runs UTC sees backup timestamps in their chosen timezone (e.g. "America/Chicago") after selecting it in Settings → Interface and saving. Timestamps update on the next page load without restarting the app.

**Files to look at first:**
- `pantri/backup.py` → `get_backups()` and `get_backup_info()` — both use `datetime.fromtimestamp()` and `datetime.now()` with no tz argument
- `pantri/routes/settings.py` → settings GET route to add `DISPLAY_TZ` to template context
- `templates/settings.html` → Interface tab to add timezone dropdown

## Scope

- Display only — the xlsx and backup zip files are not renamed; only rendered labels change
- Out of scope: per-user timezone (single global setting for the server instance)
