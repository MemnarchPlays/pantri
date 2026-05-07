# Pantri — Architecture & Refactor Guide

## What This App Is

Pantri is a personal pantry tracker with a Flask web app, a Discord bot, and PDF generators. All pantry data lives in `Food in Storage.xlsx` (gitignored). Recipes are individual JSON files in `data/`. Runtime state (shopping list, exclusions, units, backup counter) lives in `state/` (gitignored).

---

## Directory Layout (current state)

```
pantry_app.py          ← monolithic Flask app (3175 lines) — being split
pantry_utils.py        ← shared: COLS, to_title, read_env, load_all_recipes
pdf_utils.py           ← shared: color constants, BorderedCanvas
pantry_cli.py          ← CLI pantry commands
discord_bot.py         ← Discord bot (subprocess of pantry_app)
generate_pdf.py        ← recipe binder PDF
shopping_list.py       ← shopping list PDF (interactive)
archive/
  pantry_app_monolith.py  ← snapshot before blueprint split
data/                  ← recipe JSON files (one per recipe)
state/                 ← runtime JSON (gitignored): shopping_list, units, exclusions, backup_state, minimums
backups/               ← timestamped zip backups (gitignored)
docs/                  ← feature specs and flow diagrams (.feature.md, .flow.md)
output/                ← generated PDFs (gitignored)
```

---

## Planned Blueprint Split

The goal is to break `pantry_app.py` into focused modules. The archive is saved at `archive/pantry_app_monolith.py` for rollback.

### Target structure

```
pantri/
  __init__.py          ← create_app() factory — registers blueprints, context processors, filters
  db.py                ← workbook helpers: init_wb, load_wb, save_wb, get_all_rows,
                          get_location_sheets, get_location_info, get_minimums,
                          set_minimum, delete_minimum, dedup_workbook
  state.py             ← JSON state helpers: load/save shopping_list, exclusions, units,
                          get_unit_info, is_excluded
  backup.py            ← backup logic: load/save backup_state, _do_backup, backup_wb,
                          get_backups, get_backup_info
  bot.py               ← Discord bot subprocess: bot_running, _kill_stale_bot, start_bot, stop_bot
  routes/
    __init__.py        ← imports and registers all blueprints
    inventory.py       ← Blueprint: / /add /edit/<row_key> /delete/<row_key> /add/bulk
    recipes.py         ← Blueprint: /recipes /recipe/import /recipe/add /recipe/<slug>
                          /recipe/<slug>/use /recipe/delete/<slug> /recipe/edit/<slug>
                          /recipes/download-pdf
    shopping.py        ← Blueprint: /shopping /shopping/list/add-recipe
                          /shopping/list/toggle/<id> /shopping/list/remove/<id>
                          /shopping/list/clear-all /shopping/list/clear-checked
    settings.py        ← Blueprint: /settings /locations/* /exclusions/* /units/*
                          /settings/discord /settings/bot-* /settings/appearance
                          /settings/backups /backups/* /minimums/*
                          (also: /can-make redirect, /minimums redirect, /restock redirect)
templates/
  base.html            ← navbar, bootstrap, theme CSS var injection
  inventory.html       ← extends base — items table + add form
  edit.html            ← extends base — edit item form
  recipes.html         ← extends base — library + can-make tabs
  recipe_add.html      ← extends base — add/edit recipe form
  recipe_detail.html   ← extends base — single recipe view
  settings.html        ← extends base — all settings tabs
  shopping.html        ← extends base — restock + shopping list
pantry_app.py          ← thin launcher: calls create_app(), runs app.run()
```

### Key notes for the split

- `url_for` calls in templates will need blueprint namespacing: `url_for('inventory.index')`, `url_for('recipes.recipes_page')`, etc.
- `_bot_process` is a module-level global in `pantri/bot.py`
- Path constants (`XLSX`, `DATA_DIR`, `STATE_DIR`, `ENV_FILE`, etc.) will live in `pantry_utils.py`
- `EXCLUDE_SHEETS`, `MEAL_TYPES` will move to `pantry_utils.py`
- `write_env` (unique to app, not in pantry_utils) goes into `pantri/__init__.py` or `pantri/db.py`
- `compute_theme` and `_pluralize_unit` (Jinja filter) live in `pantri/__init__.py`
- Templates currently use `BASE_HTML.replace('{% block content %}{% endblock %}', ...)` — convert to proper `{% extends 'base.html' %}` / `{% block content %}` Jinja inheritance
- `BULK_ADD_HTML` is defined but never used — can be deleted

---

## Route → Blueprint mapping (37 routes)

| Route | Blueprint | Function |
|-------|-----------|----------|
| `GET /` | inventory | index |
| `POST /add` | inventory | add |
| `GET/POST /edit/<row_key>` | inventory | edit |
| `GET /delete/<row_key>` | inventory | delete |
| `GET/POST /add/bulk` | inventory | bulk_add |
| `GET /can-make` | settings | can_make (redirect) |
| `GET /minimums` | settings | minimums (redirect) |
| `GET/POST /minimums/set` | settings | minimums_set |
| `GET /minimums/delete/<item>` | settings | minimums_delete |
| `GET /restock` | settings | restock (redirect) |
| `GET /recipes` | recipes | recipes |
| `GET /recipe/import` | recipes | recipe_import |
| `GET/POST /recipe/add` | recipes | recipe_add |
| `GET /recipe/<slug>` | recipes | recipe_detail |
| `POST /recipe/<slug>/use` | recipes | recipe_use |
| `GET /recipe/delete/<slug>` | recipes | recipe_delete |
| `GET/POST /recipe/edit/<slug>` | recipes | recipe_edit |
| `GET /recipes/download-pdf` | recipes | download_pdf |
| `GET /shopping` | shopping | shopping |
| `POST /shopping/list/add-recipe` | shopping | shopping_list_add_recipe |
| `POST /shopping/list/toggle/<id>` | shopping | shopping_list_toggle |
| `GET /shopping/list/remove/<id>` | shopping | shopping_list_remove |
| `POST /shopping/list/clear-all` | shopping | shopping_list_clear_all |
| `POST /shopping/list/clear-checked` | shopping | shopping_list_clear_checked |
| `GET /settings` | settings | settings |
| `POST /locations/add` | settings | locations_add |
| `GET /locations/delete/<name>` | settings | locations_delete |
| `POST /exclusions/add` | settings | exclusions_add |
| `GET /exclusions/delete/<path:name>` | settings | exclusions_delete |
| `POST /exclusions/toggle/<path:name>` | settings | exclusions_toggle |
| `POST /units/add` | settings | units_add |
| `GET /units/delete/<unit>` | settings | units_delete |
| `POST /units/reorder` | settings | units_reorder |
| `POST /locations/reorder` | settings | locations_reorder |
| `POST /settings/discord` | settings | settings_discord |
| `GET /settings/bot-status` | settings | settings_bot_status |
| `POST /settings/bot-test` | settings | settings_bot_test |
| `GET /settings/bot-log` | settings | settings_bot_log |
| `POST /settings/appearance` | settings | settings_appearance |
| `POST /settings/backups` | settings | settings_backups |
| `POST /backups/now` | settings | backups_now |
| `GET /backups/download/<filename>` | settings | backups_download |
| `POST /backups/restore/<filename>` | settings | backups_restore |
| `POST /backups/upload` | settings | backups_upload |

---

## Helper functions (current location → target module)

| Function | Current | Target |
|----------|---------|--------|
| `init_wb` | pantry_app | pantri/db.py |
| `load_wb` | pantry_app | pantri/db.py |
| `save_wb` | pantry_app | pantri/db.py |
| `get_all_rows` | pantry_app | pantri/db.py |
| `get_location_sheets` | pantry_app | pantri/db.py |
| `get_location_info` | pantry_app | pantri/db.py |
| `get_minimums` | pantry_app | pantri/db.py |
| `set_minimum` | pantry_app | pantri/db.py |
| `delete_minimum` | pantry_app | pantri/db.py |
| `dedup_workbook` | pantry_app | pantri/db.py |
| `load_shopping_list` | pantry_app | pantri/state.py |
| `save_shopping_list` | pantry_app | pantri/state.py |
| `load_exclusions` | pantry_app | pantri/state.py |
| `save_exclusions` | pantry_app | pantri/state.py |
| `load_units` | pantry_app | pantri/state.py |
| `save_units` | pantry_app | pantri/state.py |
| `get_unit_info` | pantry_app | pantri/state.py |
| `is_excluded` | pantry_app | pantri/state.py |
| `load_backup_state` | pantry_app | pantri/backup.py |
| `save_backup_state` | pantry_app | pantri/backup.py |
| `_do_backup` | pantry_app | pantri/backup.py |
| `backup_wb` | pantry_app | pantri/backup.py |
| `get_backups` | pantry_app | pantri/backup.py |
| `get_backup_info` | pantry_app | pantri/backup.py |
| `bot_running` | pantry_app | pantri/bot.py |
| `_kill_stale_bot` | pantry_app | pantri/bot.py |
| `start_bot` | pantry_app | pantri/bot.py |
| `stop_bot` | pantry_app | pantri/bot.py |
| `compute_theme` | pantry_app | pantri/__init__.py |
| `write_env` | pantry_app | pantri/__init__.py |
| `_pluralize_unit` | pantry_app | pantri/__init__.py |

---

## Session history (what's been done)

1. Uploaded repo to GitHub as MemnarchPlays/pantri
2. Deleted 8 one-time recipe seed/patch scripts (add_batch*.py, create_recipes.py, etc.)
3. Extracted shared code: `pantry_utils.py` (COLS, to_title, read_env, load_all_recipes) and `pdf_utils.py` (colors, BorderedCanvas)
4. Moved runtime JSON state to `state/`, docs to `docs/`, gitignore updated
5. Archived monolith at `archive/pantry_app_monolith.py`
6. **Next: execute blueprint split per this document**
