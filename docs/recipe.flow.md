---
name: Recipe Flow
description: User browses, views, adds, edits, deletes, imports, and uses recipes via the web app
---

# Recipe Flow

## Entry point
`/recipes` — navbar "Recipes" link

## Step table — Library & Detail

| Step | What the user sees | What the system does |
|------|--------------------|----------------------|
| 1 | Lands on Recipes page, "Recipe Library" tab active | Loads all `data/*.json` files; shows name, meal type, prep time, servings |
| 2 | Searches by name or filters by meal type | GET params `q` and `meal` filter the list |
| 3 | Clicks a recipe name | Navigates to `/recipe/<slug>`; loads JSON, checks pantry for each ingredient |
| 4 | On detail page: ingredients show ✅ if found in pantry, • if not | Fuzzy match: item name contains or is contained by pantry item |
| 5 | Changes servings input | JS scales all ingredient amounts in real time (client-side only) |
| 6 | Clicks "Use Recipe" | JS confirm; POST to `/recipe/<slug>/use`; deducts each ingredient qty from pantry xlsx, respects exclusions |
| 7 | Post-use: banner shows how many items were removed / not found | Redirects back to detail page with `used_count` and `not_found_count` query params |

## Step table — Add / Edit

| Step | What the user sees | What the system does |
|------|--------------------|----------------------|
| 1 | Clicks "+ Add Recipe" | Navigates to `/recipe/add`; blank form with URL import panel |
| 2 | Pastes a recipe URL and clicks "Import" | JS `fetch('/recipe/import?url=…')` — server scrapes schema.org JSON-LD, returns parsed fields |
| 3 | Form pre-fills with imported data | User reviews and adjusts before saving |
| 4 | Submits form | POST to `/recipe/add`; writes `data/<slug>.json`, redirects to library |
| 5 | Clicks "Edit Recipe" on detail page | Navigates to `/recipe/edit/<slug>`; same form pre-populated |
| 6 | Saves edit | POST to `/recipe/edit/<slug>`; overwrites JSON; if name changed, old file is deleted and new slug used; redirects to detail |

## Step table — Delete

| Step | What the user sees | What the system does |
|------|--------------------|----------------------|
| 1 | Clicks "Del" in library or "Delete" on detail page | JS confirm prompt |
| 2 | Confirms | GET to `/recipe/delete/<slug>`; unlinks JSON file; redirects to library |

## Step table — Can I Make?

| Step | What the user sees | What the system does |
|------|--------------------|----------------------|
| 1 | Clicks "Can I Make?" tab | `/recipes?tab=canmake`; loads pantry `have` set and all recipes |
| 2 | Each recipe card shows % ingredient match and missing items | Fuzzy match against pantry; sorted best-match first |
| 3 | Filters by meal type or ingredient keyword | Query params `cm_meal` and `ingredient` re-filter |

## Failure modes

| Condition | Behavior |
|-----------|----------|
| Recipe JSON malformed | File silently skipped in listing |
| URL import: no schema.org Recipe found | Error message shown below import field |
| URL import: page unreachable | "Could not fetch page" error shown |
| Recipe slug collision on add | Overwrites existing file with same slug |
| Use Recipe: ingredient not in pantry | Counted in `not_found_count`; not an error |
| Use Recipe: ingredient is excluded | Skipped (not decremented) |
