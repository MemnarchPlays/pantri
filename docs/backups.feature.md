---
name: Backups
description: Automatic and manual timestamped backups of the pantry xlsx, with download and restore
flow: settings.flow.md
status: COMPLETE
---

## What It Does

Every pantry mutation triggers a backup check. Three modes: every N saves (actions mode), every N hours (interval mode), or manual only. Backups are timestamped copies of the xlsx written to `backups/`. The Backups tab in Settings shows all saved backups with download and restore options. A "Backup Now" button forces an immediate backup.

## Success Criteria

1. In `actions` mode, a backup is written every N pantry saves (default: 10); the counter resets after each backup.
2. In `interval` mode, a backup is written when more than N hours have passed since the last backup.
3. In `manual` mode, no automatic backups occur.
4. The Backups tab shows the last backup time and (in actions mode) the current save count toward the next backup.
5. "Backup Now" creates an immediate timestamped backup regardless of mode.
6. Backups older than `BACKUP_MAX` (default: 10) are automatically deleted (oldest first).
7. Clicking "Download" on a backup sends the xlsx file as an attachment.
8. Clicking "Restore" on a backup first creates a safety backup of the current xlsx, then replaces it with the chosen backup.
9. Path traversal is blocked: only files inside `backups/` can be downloaded or restored.

## Status

COMPLETE

### Progress

- [x] `backup_wb()` with actions/interval/manual modes
- [x] `backup_state.json` for action count + last timestamp
- [x] Backups tab UI (settings, status, file list)
- [x] Backup Now (POST /backups/now)
- [x] Download (GET /backups/download/<filename>)
- [x] Restore with pre-restore safety backup (POST /backups/restore/<filename>)
- [x] Max backup rotation

## Scope

- xlsx only; recipe JSON files and configuration are not backed up
- Out of scope: cloud backup, scheduled restore

## Files

- `pantry_app.py` — `SETTINGS_HTML` (backups tab), routes `/settings/backups`, `/backups/now`, `/backups/download/<filename>`, `/backups/restore/<filename>`, helpers `backup_wb`, `_do_backup`, `get_backups`, `get_backup_info`, `load_backup_state`, `save_backup_state`
- `backups/` — timestamped xlsx copies (gitignored)
- `backup_state.json` — action counter + last timestamp (gitignored)
- `.env` — `BACKUP_MODE`, `BACKUP_EVERY_N`, `BACKUP_INTERVAL_HRS`, `BACKUP_MAX`
- `settings.flow.md` — flow doc
