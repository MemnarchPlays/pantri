---
name: Deployment Flow
description: Steps to deploy Pantri on a new machine (Windows or Linux) from a git clone
---

# Deployment Flow

## Entry point

`git clone` / `git pull` → `pip install -r requirements.txt` → `py pantry_app.py` (or `bash start.sh`)

---

## Required directories (gitignored — must exist before first write)

| Directory | Purpose | Auto-created? |
|-----------|---------|---------------|
| `state/`  | Runtime JSON: shopping list, exclusions, units, types, backup counter | **Yes** — created at import of `pantri/state.py` |
| `backups/` | Timestamped zip backups | **Yes** — created at import of `pantri/backup.py` |
| `output/` | Generated PDFs | **Yes** — created inside `generate_binder()` / `generate_shopping_pdf()` before write |
| `data/`   | Recipe JSON files | Yes (empty dir committed) |

On a fresh clone, `state/` and `backups/` do not exist. Any write operation that touches these paths will raise `FileNotFoundError`.

---

## Required files (gitignored — must be provided manually)

| File | Source | Notes |
|------|--------|-------|
| `Food in Storage.xlsx` | Copy from existing machine | All pantry data; must be present before app starts or xlsx ops will fail |
| `.env` | Create from template or copy | Discord token, port, backup config; app starts without it (defaults used) |
| `data/*.json` | Copy from existing machine or add via UI | Recipes; app runs without them but recipe features are empty |

---

## Startup sequence

| Step | What happens | Failure mode |
|------|-------------|--------------|
| 1 | `create_app()` — registers blueprints, context processors | Import errors if deps missing |
| 2 | `_kill_stale_bot()` — reads `bot.pid`, kills stale process | Safe if `bot.pid` absent |
| 3 | `app.run(host='0.0.0.0', port=PORT)` | `AddressInUse` if port taken |
| 4 | First request hits a write route (add item, save setting, etc.) | `FileNotFoundError` if `state/` or `backups/` absent |
| 5 | Any xlsx read/write | `FileNotFoundError` if `Food in Storage.xlsx` absent |

---

## Linux-specific notes

- File ownership: run the app as the same user who owns the xlsx and state files. Running `sudo py pantry_app.py` then `py pantry_app.py` creates files owned by different users — subsequent writes fail with `PermissionError`.
- Firewall: Flask binds to `0.0.0.0`; open the configured port (default 5000) if accessing from another machine.
- Auto-start: use `systemd` or `screen`/`tmux`; the app does not daemonize itself.

---

## Failure modes

| Condition | Symptom | Fix |
|-----------|---------|-----|
| `state/` missing | ~~`FileNotFoundError` on first write~~ — now auto-created at startup | Fixed: `STATE_DIR.mkdir` in `pantri/state.py` |
| `backups/` missing | ~~`FileNotFoundError` on first backup~~ — now auto-created at startup | Fixed: `BACKUP_DIR.mkdir` in `pantri/backup.py` |
| `Food in Storage.xlsx` missing | 500 error on any inventory page | Copy xlsx from source machine |
| File owned by wrong user | `PermissionError` on write | `chown -R <user> .` in the project dir |
| Port in use | `OSError: [Errno 98] Address already in use` | Change `PORT` in `.env` or kill the existing process |
