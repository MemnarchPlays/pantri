---
name: Recipe Management
description: Add, edit, delete, and import recipes via the web UI
flow: recipe.flow.md
status: COMPLETE
---

## What It Does

Provides create, edit, and delete operations for recipes. New recipes can be added manually via a form or auto-filled by importing from any recipe URL with schema.org JSON-LD markup. Editing uses the same form pre-populated. Renaming a recipe renames the backing JSON file.

## Success Criteria

1. `/recipe/add` renders a blank recipe form with: name, meal type, servings, prep time, cook time, macros, dynamic ingredient rows, dynamic instruction steps, substitutions, and notes.
2. Pasting a URL into the import field and clicking "Import" fetches and parses the page's schema.org Recipe data and fills all form fields without a page reload.
3. If the URL has no schema.org Recipe data, an error message is shown below the import field.
4. Saving a new recipe writes `data/<slug>.json` (slug derived from lowercase name with hyphens) and redirects to the library.
5. `/recipe/edit/<slug>` pre-populates all fields from the existing JSON.
6. Saving an edit overwrites the JSON; if the name changed, the old file is deleted and the new slug is used.
7. `/recipe/delete/<slug>` (after JS confirm) deletes the JSON file and redirects to the library.
8. Import correctly parses: name, servings, prep time, cook time, calories, protein, carbs, fat, ingredients (with amounts), instruction steps.
9. The substitutions section (dairy-free, gluten-free, vegan, vegetarian, low-carb) is optional and omitted from JSON if all blank.

## Status

COMPLETE

### Progress

- [x] Add recipe form (GET/POST /recipe/add)
- [x] URL import endpoint (/recipe/import — schema.org JSON-LD scraper)
- [x] Edit recipe (GET/POST /recipe/edit/<slug>)
- [x] Delete recipe (/recipe/delete/<slug>)
- [x] Dynamic ingredient/instruction rows (JS add/remove)
- [x] Slug rename on name change

## Scope

- Full recipe CRUD + URL import
- Out of scope: importing from .txt files (manual via food-prep skill), duplicate slug handling (silently overwrites)

## Files

- `pantry_app.py` — `ADD_RECIPE_HTML`, routes `/recipe/add`, `/recipe/import`, `/recipe/edit/<slug>`, `/recipe/delete/<slug>`
- `data/*.json` — recipe data output
- `recipe.flow.md` — flow doc
