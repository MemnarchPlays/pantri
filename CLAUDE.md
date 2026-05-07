# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the app

```bash
# Install dependencies
pip install -r requirements.txt

# Start the web app (opens http://localhost:5000 automatically)
py pantry_app.py

# Or use the launcher (installs deps first, handles missing .env gracefully)
start.bat        # Windows
bash start.sh    # Linux/Mac

# Standalone Discord bot (normally launched from the web app's Settings page)
py discord_bot.py

# Generate the recipe binder PDF → output/recipe_binder.pdf
py generate_pdf.py
py generate_pdf.py data/recipe1.json data/recipe2.json   # specific recipes only

# Generate a shopping list PDF → output/shopping_list.pdf
py shopping_list.py

# CLI pantry commands
py pantry_cli.py list
py pantry_cli.py list "Brown Cabinet"
py pantry_cli.py search chicken
py pantry_cli.py can-make
```

There are no tests or linters configured.

## Architecture

### Data layer — `Food in Storage.xlsx`

All pantry state lives in a single Excel workbook. Each sheet is a physical storage location (Brown Cabinet, Pantry, End Hall Closet, Laundry Room, Kitchen). A special `Minimums` sheet tracks per-item stock thresholds for low-stock alerts. The file is **gitignored** — it's personal data that lives only on disk.

Columns: `Item, Quantity, Unit, Location, Section, Slot, Expiration, Notes`

`pantry_app.py`, `pantry_cli.py`, and `discord_bot.py` all read and write the same xlsx directly. There is no abstraction layer — each script opens the workbook, edits cells, and saves.

### Recipe data — `data/*.json`

One JSON file per recipe. Schema is defined in `.claude/skills/food-prep.md`. Valid `meal_type`: Breakfast, Lunch, Dinner, Snacks, Desserts, Other. Valid `store_section`: Produce, Meat/Seafood, Dairy/Eggs, Bakery, Pantry/Dry Goods, Frozen, Beverages, Other.

### Interfaces

| Script | Purpose |
|--------|---------|
| `pantry_app.py` | Flask web app — primary UI, also manages the Discord bot as a subprocess |
| `pantry_cli.py` | Quick CLI access to the pantry |
| `discord_bot.py` | Discord bot — reads/writes the same xlsx, sends low-stock alerts |
| `generate_pdf.py` | Compiles all `data/*.json` into a styled PDF binder via ReportLab |
| `shopping_list.py` | Builds a per-section shopping list PDF from selected recipes |

### Discord bot lifecycle

The bot runs as a **subprocess spawned by `pantry_app.py`**. `pantry_app.py` writes the child PID to `bot.pid` (gitignored) and tails output to `bot.log` (gitignored). The Settings page in the web app handles start/stop and token configuration. The bot can also be run standalone with `py discord_bot.py` if `DISCORD_TOKEN` is in `.env`.

Low-stock alerts fire when a `!add` / decrement drops an item below its `Minimums` sheet value. The alert channel is set via `DISCORD_ALERT_CHANNEL` in `.env`.

### PDF generation

Both `generate_pdf.py` and `shopping_list.py` use ReportLab with a shared purple color scheme (`#6B2D8B`) and a `BorderedCanvas` subclass that draws a decorative double border on every page during the final `save()` pass. `generate_pdf.py` also exposes `generate_binder_bytes()` for serving the PDF in-memory (used by the Discord bot's `!binder` command).

### Configuration (`.env`)

| Key | Default | Purpose |
|-----|---------|---------|
| `DISCORD_TOKEN` | — | Bot token (required for Discord features) |
| `DISCORD_ALERT_CHANNEL` | — | Channel ID for low-stock alerts |
| `BACKUP_MODE` | `actions` | `actions` or `interval` |
| `BACKUP_EVERY_N` | `10` | Write a backup every N pantry mutations (actions mode) |
| `BACKUP_INTERVAL_HRS` | `24` | Hours between backups (interval mode) |
| `BACKUP_MAX` | `10` | Max number of timestamped backups to keep in `backups/` |

Backups are timestamped copies of the xlsx written to `backups/` (gitignored). The web app Settings page exposes a UI for all of these.
