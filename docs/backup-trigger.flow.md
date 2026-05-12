---
name: Backup Trigger Flow
description: How and when automatic backups are created on pantry mutations
---

# Backup Trigger Flow

## Entry point

Every pantry write goes through `pantri/db.py:save_wb(wb)`. This is the single choke-point for all mutations (add, edit, delete, adjust, bulk-add, set-minimum).

---

## Pipeline

| Step | File / Function | What happens |
|------|----------------|--------------|
| 1 | `db.save_wb(wb)` | Called by all inventory mutation routes after building the in-memory workbook |
| 2 | `db.dedup_workbook(wb)` | Merges duplicate (item, unit) rows in-memory |
| 3 | `db.wb.save(XLSX)` | Writes the workbook to disk — data is now persisted |
| 4 | `backup.backup_wb()` (wrapped in try/except) | Checks whether a backup is due; creates one if so |
| 5 | `backup._do_backup(env)` | Writes a timestamped zip of the xlsx + state files to `backups/`; trims oldest files to BACKUP_MAX |

---

## Backup modes

| Mode | Trigger condition |
|------|------------------|
| `actions` | `action_count >= BACKUP_EVERY_N` (default: 10); count resets after each backup |
| `interval` | `now - last_backup_ts >= BACKUP_INTERVAL_HRS * 3600`; `last_backup_ts = 0` on first run so first mutation always fires |
| `manual` | Never triggers automatically; only via "Backup Now" button |

---

## State file

`state/backup_state.json` — persists `action_count` and `last_backup_ts` across restarts.

---

## Failure modes

| Condition | Behavior |
|-----------|----------|
| Backup dir missing | `BACKUP_DIR.mkdir(exist_ok=True)` inside `_do_backup` creates it |
| `_do_backup` throws (disk full, permissions) | Exception is caught in `save_wb`; save already completed (step 3 runs before step 4) — backup fails silently, data is safe |
| `backup_state.json` unwriteable | `save_backup_state` raises; caught in same try/except; action_count/timestamp may not update, but save is unaffected |
| Mode switched from `actions` to `interval` | `last_backup_ts` carries over from last actions-mode backup; first interval backup fires when `BACKUP_INTERVAL_HRS` have elapsed since that last backup, not since the mode switch |
