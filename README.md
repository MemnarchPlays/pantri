# Pantri

A personal pantry tracker with a web UI, Discord bot, and PDF recipe binder. Track what you have, manage recipes, build shopping lists, and get low-stock alerts in Discord.

---

## Requirements

- Python 3.10+
- Windows, macOS, or Linux

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/MemnarchPlays/pantri.git
cd pantri
```

### 2. Start the app

The launchers install dependencies automatically on every run.

**Windows:**
```bat
start.bat
```

**macOS / Linux:**
```bash
bash start.sh
```

**Or directly (dependencies must already be installed):**
```bash
pip install -r requirements.txt
python pantry_app.py
```

The app opens at **http://localhost:5000** automatically.

> The first time you run it, the pantry file (`Food in Storage.xlsx`) is created automatically.

---

## Features

### Inventory
- Add, edit, and remove pantry items across multiple storage locations (Pantry, Fridge, Cabinet, etc.)
- Bulk-add items in one paste: `Item, Qty, Unit, Location`
- Duplicate items with the same name and unit are automatically merged

### Recipes
- Browse your recipe library filtered by meal type
- Add recipes manually or **import directly from any recipe website** by pasting a URL
- **Can I Make This?** — see which recipes you can make right now based on what's in your pantry, sorted by % of ingredients on hand
- Use a recipe to automatically decrement pantry quantities
- Export all recipes to a styled PDF binder

### Shopping
- **Restock Needs** — items currently below their set minimum quantity
- **Missing Ingredients** — pick a recipe and see exactly what you're missing
- Persistent shopping list — check off items as you shop, survives page reloads
- Exclusions — mark staple items (salt, pepper, oil) so they never appear in shopping lists

### Settings
- Add, rename, and reorder storage locations
- Set minimum stock thresholds per item for restock alerts
- Manage units and exclusion lists
- Automatic backups on a configurable schedule (download, restore, or upload from the Settings page)
- Accent color picker and **configurable port** (Settings → Appearance, requires restart)

---

## Discord Bot (optional)

The bot lets you query and update your pantry from any Discord server. It runs as a subprocess of the web app and can be started/stopped from **Settings → Discord**.

### Setup

1. Go to [discord.com/developers/applications](https://discord.com/developers/applications)
2. Create a new application → Bot → copy the token
3. In Pantri, go to **Settings → Discord** and paste the token
4. Click **Save & Start Bot**

To get low-stock alerts, enter your channel ID in the **Alert Channel** field on the same page.

### Bot commands

| Command | What it does |
|---------|-------------|
| `!add <item> [qty] [unit]` | Add an item (bot walks you through missing fields) |
| `!remove <item> <qty>` | Subtract quantity from an item |
| `!set <item> <qty>` | Set an item to an exact quantity |
| `!stock <item>` | Check how much of something you have |
| `!list [location]` | List all pantry items, optionally filtered by location |
| `!recipe <name>` | Show a recipe with pantry availability checkmarks |
| `!canmake [meal or name]` | See what you can make, filtered by meal type or keyword |
| `!restock` | Show items below their minimum |
| `!setmin <item> <qty>` | Set a minimum stock threshold for an item |
| `!locations` | List all storage locations |
| `!addlocation <name>` | Add a new storage location |
| `!help` | Show all commands |

---

## Configuration

All config lives in a `.env` file at the project root. All settings can be configured from the **Settings** page in the web UI — you don't need to edit `.env` directly.

| Key | Default | Description |
|-----|---------|-------------|
| `PORT` | `5000` | Port the web app listens on (requires restart) |
| `ACCENT_COLOR` | `#6B2D8B` | Web UI theme color (hex) |
| `FONT_FAMILY` | `Verdana, Geneva, sans-serif` | Web UI font |
| `INPUT_MAX_LENGTH` | `60` | Max characters allowed in text input fields |
| `INVENTORY_REFRESH_SECS` | `30` | How often the inventory page silently refreshes (seconds) |
| `LOW_STOCK_THRESHOLD` | `0` | Global fallback minimum stock level — used when an item has no individual minimum set; 0 disables it |
| `PDF_ACCENT_COLOR` | `#6B2D8B` | Accent color used in generated PDFs |
| `PDF_FONT` | `Helvetica` | Font used in generated PDFs (`Helvetica`, `Times-Roman`, or `Courier`) |
| `DEFAULT_LOCATION` | — | Pre-selected location in the Add Item form |
| `DEFAULT_UNIT` | — | Pre-selected unit in the Add Item form |
| `DISCORD_TOKEN` | — | Bot token (required for Discord features) |
| `DISCORD_ALERT_CHANNEL` | — | Channel ID for low-stock alerts |
| `BACKUP_MODE` | `actions` | `actions` (every N writes) or `interval` (every N hours) |
| `BACKUP_EVERY_N` | `10` | How many pantry writes between backups |
| `BACKUP_INTERVAL_HRS` | `24` | Hours between backups (interval mode) |
| `BACKUP_MAX` | `10` | Max number of backups to keep |

---

## PDF generation

```bash
# Full recipe binder → output/recipe_binder.pdf
python generate_pdf.py

# Specific recipes only
python generate_pdf.py data/recipe1.json data/recipe2.json

# Interactive shopping list → output/shopping_list.pdf
python shopping_list.py
```

---

## CLI (quick pantry access without the web app)

```bash
python pantry_cli.py list
python pantry_cli.py list "Brown Cabinet"
python pantry_cli.py search chicken
python pantry_cli.py add
python pantry_cli.py update "black beans"
python pantry_cli.py remove "black beans"
python pantry_cli.py can-make
```

---

## Project structure

```
pantry_app.py        — launcher (reads PORT from .env, starts Flask)
pantri/              — Flask app package
  __init__.py        — app factory
  db.py              — Excel workbook helpers
  state.py           — shopping list, units, exclusions
  backup.py          — backup logic
  bot.py             — Discord bot subprocess management
  routes/            — Flask blueprints (inventory, recipes, shopping, settings)
templates/           — Jinja2 HTML templates
data/                — recipe JSON files (~90 recipes)
state/               — runtime state, gitignored (shopping list, units, exclusions)
backups/             — timestamped zip backups, gitignored
pantry_utils.py      — shared constants and helpers
pdf_utils.py         — shared PDF colors and canvas
generate_pdf.py      — recipe binder PDF generator
shopping_list.py     — shopping list PDF generator
pantry_cli.py        — CLI pantry commands
discord_bot.py       — Discord bot
```

---

## Data & privacy

- `Food in Storage.xlsx` — all pantry data, lives only on your machine (gitignored)
- `state/` — shopping list, units, exclusions, backup counter (gitignored)
- `backups/` — timestamped zip backups (gitignored)
- `.env` — your tokens and config (gitignored)
- `data/*.json` — recipe files, tracked in git

Nothing is sent anywhere except Discord API calls if you use the bot.
