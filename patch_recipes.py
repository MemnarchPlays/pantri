#!/usr/bin/env python3
"""Remove bell peppers, mushrooms, and tomatoes from all recipes."""
import json
from pathlib import Path

DATA = Path(__file__).parent / 'data'

def load(name):
    p = DATA / name
    return json.loads(p.read_text(encoding='utf-8')), p

def save(p, r):
    p.write_text(json.dumps(r, indent=2), encoding='utf-8')
    print(f'  Updated: {p.name}')

def remove_ingredients(recipe, remove_terms):
    """Drop any ingredient whose item contains one of the remove_terms."""
    orig = recipe['ingredients']
    recipe['ingredients'] = [
        ing for ing in orig
        if not any(t in (ing.get('item','') if isinstance(ing, dict) else str(ing)).lower()
                   for t in remove_terms)
    ]

# ── 1. BLT Club — drop tomatoes ────────────────────────────────────────────
r, p = load('blt-club-sandwich.json')
remove_ingredients(r, ['tomato'])
r['name'] = 'Club Sandwich'
r['instructions'] = [
    'Cook bacon until crispy. Drain on paper towels.',
    'Toast bread until golden.',
    'Spread mayo on one side of each slice.',
    'Layer: first slice — lettuce, bacon. Add second slice. Layer turkey, cheese, avocado. Top with third slice.',
    'Secure with toothpicks and cut diagonally into quarters.',
]
save(p, r)

# ── 2. Chicken Stir Fry — replace bell pepper with zucchini ────────────────
r, p = load('chicken-stir-fry.json')
remove_ingredients(r, ['bell pepper'])
# Insert zucchini in its place
r['ingredients'].insert(3, {"amount": "1 medium", "item": "zucchini, sliced", "store_section": "Produce"})
save(p, r)

# ── 3. Chicken Tikka Masala — replace crushed tomatoes with coconut milk ────
r, p = load('chicken-tikka-masala.json')
remove_ingredients(r, ['tomato'])
r['ingredients'].insert(2, {"amount": "1 can (13.5 oz)", "item": "coconut milk", "store_section": "Pantry/Dry Goods"})
r['ingredients'].insert(3, {"amount": "1/2 cup", "item": "chicken broth", "store_section": "Pantry/Dry Goods"})
r['instructions'] = [
    'Marinate chicken in yogurt, half the garam masala, and salt for at least 30 minutes.',
    'Broil marinated chicken 8-10 minutes until slightly charred. Set aside.',
    'Melt butter in a large pan. Sauté onion until golden, 8 minutes.',
    'Add garlic and ginger. Cook 2 minutes.',
    'Add remaining spices and cook 1 minute.',
    'Pour in coconut milk and chicken broth. Simmer 15 minutes until slightly thickened.',
    'Stir in broiled chicken. Simmer 10 more minutes.',
    'Serve over basmati rice with naan bread.',
]
r['notes'] = 'Using coconut milk instead of tomatoes gives this a rich, slightly sweet curry base.'
save(p, r)

# ── 4. Classic Chili — replace tomatoes with beef broth base ───────────────
r, p = load('classic-chili.json')
remove_ingredients(r, ['tomato'])
r['ingredients'].insert(3, {"amount": "2 cups", "item": "beef broth", "store_section": "Pantry/Dry Goods"})
r['ingredients'].insert(4, {"amount": "2 tbsp", "item": "Worcestershire sauce", "store_section": "Pantry/Dry Goods"})
r['ingredients'].insert(5, {"amount": "1 tbsp", "item": "tomato-free chili paste or chipotle in adobo", "store_section": "Pantry/Dry Goods"})
r['instructions'] = [
    'Brown ground beef in a large pot over medium-high heat. Drain fat.',
    'Add onion and garlic. Cook 5 minutes until softened.',
    'Stir in chili powder, cumin, paprika, and Worcestershire sauce. Cook 1 minute.',
    'Add beef broth and chili paste. Stir well.',
    'Add drained kidney beans.',
    'Bring to a boil then reduce heat. Simmer 30 minutes, stirring occasionally.',
    'Taste and season with salt and pepper. Serve with sour cream and shredded cheese.',
]
r['notes'] = 'Tomato-free chili — beef broth and Worcestershire give it great depth.'
save(p, r)

# ── 5. Greek Chicken Salad — drop cherry tomatoes ──────────────────────────
r, p = load('greek-chicken-salad.json')
remove_ingredients(r, ['tomato'])
save(p, r)

# ── 6. Guacamole — drop roma tomatoes ──────────────────────────────────────
r, p = load('guacamole-and-chips.json')
remove_ingredients(r, ['tomato'])
save(p, r)

# ── 7. Hummus with Veggies — remove bell pepper from the dippers ───────────
r, p = load('hummus-with-veggies.json')
for ing in r['ingredients']:
    if isinstance(ing, dict) and 'bell pepper' in ing.get('item', '').lower():
        ing['item'] = 'carrots, cucumber, celery, broccoli'
save(p, r)

# ── 8. Spaghetti Bolognese — replace tomatoes with broth + cream ───────────
r, p = load('spaghetti-bolognese.json')
remove_ingredients(r, ['tomato'])
r['ingredients'].insert(7, {"amount": "1.5 cups", "item": "beef broth", "store_section": "Pantry/Dry Goods"})
r['ingredients'].insert(8, {"amount": "1/2 cup", "item": "heavy cream", "store_section": "Dairy/Eggs"})
r['name'] = 'White Bolognese'
r['instructions'] = [
    'Heat olive oil in a large heavy pot. Sauté onion, carrots, and celery 8 minutes.',
    'Add garlic and cook 1 minute.',
    'Add ground beef and pork. Cook until browned, breaking up the meat.',
    'Pour in wine and cook until evaporated, 3 minutes.',
    'Add beef broth. Stir well and bring to a simmer.',
    'Stir in milk and heavy cream.',
    'Reduce heat to low and simmer uncovered 45 minutes, stirring occasionally.',
    'Season with salt and pepper. Serve over spaghetti topped with parmesan.',
]
r['notes'] = 'White bolognese — rich and creamy without tomatoes. Equally delicious.'
save(p, r)

# ── 9. Tomato Basil Soup — replace with Broccoli Cheddar Soup ──────────────
r, p = load('tomato-basil-soup.json')
r['name'] = 'Broccoli Cheddar Soup'
r['meal_type'] = 'Lunch'
r['servings'] = 4
r['prep_time'] = '10 minutes'
r['cook_time'] = '30 minutes'
r['macros_per_serving'] = {"calories": 380, "protein_g": 18, "carbs_g": 20, "fat_g": 26}
r['ingredients'] = [
    {"amount": "4 cups",   "item": "broccoli florets, chopped small",  "store_section": "Produce"},
    {"amount": "1 large",  "item": "onion, diced",                     "store_section": "Produce"},
    {"amount": "3 cloves", "item": "garlic, minced",                   "store_section": "Produce"},
    {"amount": "2 cups",   "item": "chicken broth",                    "store_section": "Pantry/Dry Goods"},
    {"amount": "2 cups",   "item": "milk",                             "store_section": "Dairy/Eggs"},
    {"amount": "1 cup",    "item": "heavy cream",                      "store_section": "Dairy/Eggs"},
    {"amount": "2 cups",   "item": "sharp cheddar cheese, shredded",   "store_section": "Dairy/Eggs"},
    {"amount": "4 tbsp",   "item": "butter",                           "store_section": "Dairy/Eggs"},
    {"amount": "3 tbsp",   "item": "all-purpose flour",                "store_section": "Pantry/Dry Goods"},
    {"amount": "1/2 tsp",  "item": "smoked paprika",                   "store_section": "Pantry/Dry Goods"},
    {"amount": "to taste", "item": "salt and pepper",                  "store_section": "Pantry/Dry Goods"},
]
r['instructions'] = [
    'Melt butter in a large pot over medium heat. Sauté onion until soft, 5 minutes.',
    'Add garlic and cook 1 minute.',
    'Whisk in flour and cook 2 minutes to remove raw flour taste.',
    'Slowly whisk in chicken broth, then milk and cream. Bring to a simmer.',
    'Add broccoli and smoked paprika. Cook 15 minutes until broccoli is very tender.',
    'Use an immersion blender to partially blend — leave some chunks for texture.',
    'Reduce heat to low. Stir in cheddar a handful at a time until melted and smooth.',
    'Season with salt and pepper. Serve with crusty bread.',
]
r['substitutions'] = {
    "dairy_free": "Use oat milk, coconut cream, dairy-free butter, and vegan cheddar.",
    "gluten_free": "Replace flour with cornstarch (1.5 tbsp) and use gluten-free bread.",
    "low_carb": "Skip the flour and thicken with 1 tsp xanthan gum instead.",
    "vegan": "Use vegetable broth, oat milk, and vegan cheddar.",
}
r['notes'] = 'Don\'t add cheese while the soup is boiling — it will go grainy. Keep heat low.'
save(p, r)

# ── 10. Veggie Omelette — replace bell pepper and mushrooms ────────────────
r, p = load('veggie-omelette.json')
remove_ingredients(r, ['bell pepper', 'mushroom'])
r['ingredients'].insert(2, {"amount": "1/4 cup", "item": "zucchini, diced small", "store_section": "Produce"})
r['ingredients'].insert(3, {"amount": "1/4 cup", "item": "asparagus, chopped", "store_section": "Produce"})
r['instructions'] = [
    'Whisk eggs with milk, salt, and pepper until combined.',
    'Melt butter in a non-stick skillet over medium heat.',
    'Sauté onion, zucchini, and asparagus 3-4 minutes until tender.',
    'Add spinach and cook 1 minute until wilted. Push veggies to one side.',
    'Pour egg mixture over entire pan. Let set around the edges, 2 minutes.',
    'Sprinkle cheese over one half. Fold omelette in half over the filling. Serve.',
]
save(p, r)

print('\nAll recipes updated.')
