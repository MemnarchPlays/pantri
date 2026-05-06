# Food Prep Binder Skill

You are helping manage a personal recipe binder and pantry tracker system.
Project root: `C:\code\food-binder\`

## Folder layout
- `recipes/`  — user drops free-form `.txt` files here
- `data/`     — structured recipe `.json` files (one per recipe)
- `output/`   — generated PDFs land here
- `Food in Storage.xlsx` — pantry inventory

## Recipe JSON schema
Every recipe JSON must match this structure exactly:
```json
{
  "name": "Recipe Name",
  "meal_type": "Dinner",
  "servings": 4,
  "prep_time": "30 minutes",
  "cook_time": "45 minutes",
  "macros_per_serving": {
    "calories": 450,
    "protein_g": 35,
    "carbs_g": 42,
    "fat_g": 12
  },
  "ingredients": [
    {"amount": "2 lbs", "item": "chicken breast", "store_section": "Meat/Seafood"},
    {"amount": "1 cup", "item": "jasmine rice",   "store_section": "Pantry/Dry Goods"}
  ],
  "instructions": [
    "Preheat oven to 375°F.",
    "Season chicken with salt and pepper."
  ],
  "notes": "Optional note here."
}
```

Valid `meal_type` values: Breakfast, Lunch, Dinner, Snacks, Desserts, Other
Valid `store_section` values: Produce, Meat/Seafood, Dairy/Eggs, Bakery, Pantry/Dry Goods, Frozen, Beverages, Other

## Task: Parse a new recipe from a .txt file

When the user asks to add, parse, or import a recipe:
1. Read the `.txt` file(s) in the `recipes/` folder that haven't been processed yet.
2. Extract all available information using your best judgment — the text is free-form.
3. For each ingredient, assign the most logical `store_section`.
4. If macros (calories, protein, carbs, fat) are NOT in the text, ask the user to provide them before saving.
5. If `meal_type` is ambiguous, ask the user.
6. Write the structured JSON to `data/<recipe-name-lowercase-dashes>.json`.
7. Confirm what was saved and ask if the user wants to generate a PDF now.

## Task: Generate the recipe binder PDF

When the user wants to generate the binder:
- Run: `py generate_pdf.py` from the project root
- This compiles ALL recipes in `data/` into `output/recipe_binder.pdf`
- To include only specific recipes: `py generate_pdf.py data/recipe1.json data/recipe2.json`

## Task: Generate a shopping list

When the user wants a shopping list:
- Run: `py shopping_list.py`
- The script prompts for which recipes to include, then outputs a PDF to `output/shopping_list.pdf`
- Or call it programmatically by importing `generate_shopping_pdf(recipes)` from shopping_list.py

## Task: Pantry tracker — web app

When the user wants to open the pantry tracker:
- Run: `py pantry_app.py`
- Opens automatically at http://localhost:5000
- Features: view all inventory, search/filter, add/edit/delete items, "Can I Make?" page

## Task: Pantry tracker — CLI

Quick commands:
- `py pantry_cli.py list`                 — show all items
- `py pantry_cli.py list "Brown Cabinet"` — filter by location
- `py pantry_cli.py search chicken`       — search by name
- `py pantry_cli.py add`                  — add item interactively
- `py pantry_cli.py update "item name"`   — update an item
- `py pantry_cli.py remove "item name"`   — remove an item
- `py pantry_cli.py can-make`             — check which recipes are makeable now

## Parsing guidance for free-form text

When reading a raw recipe text file, look for:
- A title or heading at the top → `name`
- Words like "serves", "servings", "makes" → `servings`
- "prep", "preparation", "takes about" → `prep_time`
- "cook", "bake", "simmer for" → `cook_time`
- Any ingredient list (often one item per line with amounts) → `ingredients`
- Numbered steps, paragraphs of method, or "directions" → `instructions`
- Nutrition facts, macros, calories → `macros_per_serving`
- Anything else useful → `notes`

If a field is genuinely absent and cannot be inferred, omit it from the JSON (do not guess calories/macros — always ask).
