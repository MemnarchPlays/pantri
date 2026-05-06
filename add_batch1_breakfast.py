#!/usr/bin/env python3
import json
from pathlib import Path
OUT = Path(__file__).parent / 'data'

recipes = [

{"name": "Avocado Toast with Fried Egg",
 "meal_type": "Breakfast", "servings": 1, "prep_time": "5 minutes", "cook_time": "5 minutes",
 "macros_per_serving": {"calories": 380, "protein_g": 14, "carbs_g": 32, "fat_g": 24},
 "ingredients": [
   {"amount": "2 slices",  "item": "sourdough bread",           "store_section": "Bakery"},
   {"amount": "1 large",   "item": "ripe avocado",              "store_section": "Produce"},
   {"amount": "2 large",   "item": "eggs",                      "store_section": "Dairy/Eggs"},
   {"amount": "1 tbsp",    "item": "olive oil",                 "store_section": "Pantry/Dry Goods"},
   {"amount": "1/2",       "item": "lemon, juiced",             "store_section": "Produce"},
   {"amount": "pinch",     "item": "red pepper flakes",         "store_section": "Pantry/Dry Goods"},
   {"amount": "to taste",  "item": "salt and pepper",           "store_section": "Pantry/Dry Goods"},
 ],
 "instructions": [
   "Toast bread until golden and crisp.",
   "Halve and pit avocado. Scoop into a bowl and mash with lemon juice, salt, and pepper.",
   "Heat olive oil in a small skillet over medium heat.",
   "Crack eggs into pan. Cook 2-3 minutes until whites are set but yolks are still runny.",
   "Spread mashed avocado generously over toast.",
   "Top each slice with a fried egg. Season with red pepper flakes and extra salt.",
 ],
 "substitutions": {
   "gluten_free": "Use gluten-free bread.",
   "vegan": "Skip eggs and top with everything bagel seasoning and hemp seeds instead.",
   "low_carb": "Serve avocado mixture over a thick slice of grilled zucchini instead of bread.",
 }},

{"name": "Breakfast Quesadilla",
 "meal_type": "Breakfast", "servings": 2, "prep_time": "5 minutes", "cook_time": "10 minutes",
 "macros_per_serving": {"calories": 480, "protein_g": 26, "carbs_g": 38, "fat_g": 24},
 "ingredients": [
   {"amount": "4 large",   "item": "flour tortillas",           "store_section": "Bakery"},
   {"amount": "4 large",   "item": "eggs, scrambled",           "store_section": "Dairy/Eggs"},
   {"amount": "4 strips",  "item": "bacon, cooked and crumbled","store_section": "Meat/Seafood"},
   {"amount": "1 cup",     "item": "shredded cheddar cheese",   "store_section": "Dairy/Eggs"},
   {"amount": "2 tbsp",    "item": "butter",                    "store_section": "Dairy/Eggs"},
   {"amount": "1/4 cup",   "item": "sour cream for serving",    "store_section": "Dairy/Eggs"},
   {"amount": "to taste",  "item": "salt and pepper",           "store_section": "Pantry/Dry Goods"},
 ],
 "instructions": [
   "Cook bacon until crispy, drain and crumble. Scramble eggs with salt and pepper.",
   "Lay one tortilla flat. Sprinkle half the cheese over one half of the tortilla.",
   "Add half the eggs and bacon over the cheese. Fold tortilla in half.",
   "Melt butter in a skillet over medium heat. Cook quesadilla 2-3 minutes per side until golden.",
   "Repeat with remaining tortilla. Slice into wedges and serve with sour cream.",
 ],
 "substitutions": {
   "dairy_free": "Use dairy-free cheese and coconut-based sour cream.",
   "gluten_free": "Use corn tortillas or gluten-free wraps.",
   "vegetarian": "Skip bacon and add diced avocado and extra cheese.",
 }},

{"name": "Chocolate Chip Muffins",
 "meal_type": "Breakfast", "servings": 12, "prep_time": "10 minutes", "cook_time": "20 minutes",
 "macros_per_serving": {"calories": 320, "protein_g": 5, "carbs_g": 48, "fat_g": 12},
 "ingredients": [
   {"amount": "2 cups",    "item": "all-purpose flour",         "store_section": "Pantry/Dry Goods"},
   {"amount": "1/2 cup",   "item": "granulated sugar",          "store_section": "Pantry/Dry Goods"},
   {"amount": "1/4 cup",   "item": "brown sugar, packed",       "store_section": "Pantry/Dry Goods"},
   {"amount": "2 tsp",     "item": "baking powder",             "store_section": "Pantry/Dry Goods"},
   {"amount": "1/2 tsp",   "item": "salt",                      "store_section": "Pantry/Dry Goods"},
   {"amount": "3/4 cup",   "item": "milk",                      "store_section": "Dairy/Eggs"},
   {"amount": "1/2 cup",   "item": "vegetable oil",             "store_section": "Pantry/Dry Goods"},
   {"amount": "2 large",   "item": "eggs",                      "store_section": "Dairy/Eggs"},
   {"amount": "2 tsp",     "item": "vanilla extract",           "store_section": "Pantry/Dry Goods"},
   {"amount": "1.5 cups",  "item": "chocolate chips",           "store_section": "Pantry/Dry Goods"},
 ],
 "instructions": [
   "Preheat oven to 375°F. Line a 12-cup muffin tin with paper liners.",
   "Whisk flour, both sugars, baking powder, and salt in a large bowl.",
   "In another bowl, whisk milk, oil, eggs, and vanilla.",
   "Pour wet ingredients into dry and stir until just combined — do not overmix.",
   "Fold in 1 cup of the chocolate chips.",
   "Divide batter evenly among muffin cups. Top with remaining chocolate chips.",
   "Bake 18-20 minutes until a toothpick comes out clean.",
   "Cool 5 minutes in pan before transferring to a wire rack.",
 ],
 "substitutions": {
   "dairy_free": "Use oat milk and dairy-free chocolate chips.",
   "gluten_free": "Use a 1:1 gluten-free flour blend.",
   "vegan": "Use plant milk, flax eggs (1 tbsp ground flax + 3 tbsp water each), and dairy-free chips.",
 },
 "notes": "Do not overmix or muffins will be dense and tough."},

{"name": "Cinnamon Roll Casserole",
 "meal_type": "Breakfast", "servings": 8, "prep_time": "10 minutes", "cook_time": "35 minutes",
 "macros_per_serving": {"calories": 420, "protein_g": 8, "carbs_g": 62, "fat_g": 16},
 "ingredients": [
   {"amount": "2 cans",    "item": "refrigerated cinnamon rolls (with icing)", "store_section": "Dairy/Eggs"},
   {"amount": "4 large",   "item": "eggs",                                     "store_section": "Dairy/Eggs"},
   {"amount": "1/2 cup",   "item": "heavy cream",                              "store_section": "Dairy/Eggs"},
   {"amount": "2 tbsp",    "item": "maple syrup",                              "store_section": "Pantry/Dry Goods"},
   {"amount": "1 tsp",     "item": "vanilla extract",                          "store_section": "Pantry/Dry Goods"},
   {"amount": "1 tsp",     "item": "cinnamon",                                 "store_section": "Pantry/Dry Goods"},
   {"amount": "2 tbsp",    "item": "butter",                                   "store_section": "Dairy/Eggs"},
 ],
 "instructions": [
   "Preheat oven to 375°F. Grease a 9x13 baking dish with butter.",
   "Cut each cinnamon roll into quarters and spread evenly in the dish.",
   "Whisk eggs, cream, maple syrup, vanilla, and cinnamon together.",
   "Pour egg mixture evenly over the cinnamon roll pieces.",
   "Bake 30-35 minutes until puffed, golden, and set in the center.",
   "Drizzle the included icing over the top while still warm. Serve immediately.",
 ],
 "substitutions": {
   "dairy_free": "Use coconut cream and dairy-free cinnamon roll dough.",
   "gluten_free": "Use gluten-free canned cinnamon rolls if available.",
 },
 "notes": "Great for holiday mornings. Assemble the night before, refrigerate, and bake in the morning."},

{"name": "Egg and Cheese Bagel Sandwich",
 "meal_type": "Breakfast", "servings": 2, "prep_time": "5 minutes", "cook_time": "10 minutes",
 "macros_per_serving": {"calories": 480, "protein_g": 28, "carbs_g": 48, "fat_g": 18},
 "ingredients": [
   {"amount": "2",         "item": "everything bagels, sliced",   "store_section": "Bakery"},
   {"amount": "4 large",   "item": "eggs",                        "store_section": "Dairy/Eggs"},
   {"amount": "4 slices",  "item": "American or cheddar cheese",  "store_section": "Dairy/Eggs"},
   {"amount": "4 strips",  "item": "bacon",                       "store_section": "Meat/Seafood"},
   {"amount": "2 tbsp",    "item": "butter",                      "store_section": "Dairy/Eggs"},
   {"amount": "to taste",  "item": "salt and pepper",             "store_section": "Pantry/Dry Goods"},
 ],
 "instructions": [
   "Cook bacon until crispy. Drain and set aside.",
   "Toast bagels until golden.",
   "Melt butter in a skillet over medium-low heat.",
   "Crack eggs in and cook 3 minutes. Flip and immediately lay cheese on top.",
   "Cover pan with a lid for 1 minute until cheese melts.",
   "Assemble: bagel bottom, 2 eggs with cheese, 2 bacon strips, bagel top.",
 ],
 "substitutions": {
   "dairy_free": "Use dairy-free cheese and butter.",
   "gluten_free": "Use a gluten-free bagel.",
   "vegetarian": "Skip bacon and add sliced avocado.",
 }},

{"name": "Shakshuka",
 "meal_type": "Breakfast", "servings": 4, "prep_time": "10 minutes", "cook_time": "25 minutes",
 "macros_per_serving": {"calories": 280, "protein_g": 18, "carbs_g": 22, "fat_g": 14},
 "ingredients": [
   {"amount": "6 large",   "item": "eggs",                          "store_section": "Dairy/Eggs"},
   {"amount": "1 can",     "item": "crushed tomatoes (28 oz)",      "store_section": "Pantry/Dry Goods"},
   {"amount": "1 large",   "item": "onion, diced",                  "store_section": "Produce"},
   {"amount": "4 cloves",  "item": "garlic, minced",                "store_section": "Produce"},
   {"amount": "1 tsp",     "item": "cumin",                         "store_section": "Pantry/Dry Goods"},
   {"amount": "1 tsp",     "item": "paprika",                       "store_section": "Pantry/Dry Goods"},
   {"amount": "1/2 tsp",   "item": "cayenne pepper",                "store_section": "Pantry/Dry Goods"},
   {"amount": "2 tbsp",    "item": "olive oil",                     "store_section": "Pantry/Dry Goods"},
   {"amount": "1/2 cup",   "item": "crumbled feta cheese",          "store_section": "Dairy/Eggs"},
   {"amount": "fresh",     "item": "parsley for garnish",           "store_section": "Produce"},
   {"amount": "to taste",  "item": "salt and pepper",               "store_section": "Pantry/Dry Goods"},
 ],
 "instructions": [
   "Heat olive oil in a large skillet over medium heat. Saute onion 5 minutes until soft.",
   "Add garlic, cumin, paprika, and cayenne. Cook 1 minute until fragrant.",
   "Pour in crushed tomatoes. Season with salt and pepper. Simmer 10 minutes.",
   "Use a spoon to make 6 wells in the sauce. Crack one egg into each well.",
   "Cover and cook 8-10 minutes until whites are set but yolks are still runny.",
   "Sprinkle feta and parsley over top. Serve directly from the pan with crusty bread.",
 ],
 "substitutions": {
   "dairy_free": "Skip feta or use dairy-free crumbles.",
   "gluten_free": "Already gluten-free — serve with gluten-free bread.",
   "vegan": "Replace eggs with silken tofu cubes added in the last 5 minutes.",
 },
 "notes": "Do not overcook the eggs — runny yolks mixed into the sauce are the best part."},

{"name": "Skillet Hash Browns and Eggs",
 "meal_type": "Breakfast", "servings": 2, "prep_time": "10 minutes", "cook_time": "20 minutes",
 "macros_per_serving": {"calories": 380, "protein_g": 16, "carbs_g": 38, "fat_g": 18},
 "ingredients": [
   {"amount": "3 large",   "item": "russet potatoes, peeled and grated", "store_section": "Produce"},
   {"amount": "4 large",   "item": "eggs",                               "store_section": "Dairy/Eggs"},
   {"amount": "3 tbsp",    "item": "butter",                             "store_section": "Dairy/Eggs"},
   {"amount": "1/2",       "item": "onion, grated",                      "store_section": "Produce"},
   {"amount": "to taste",  "item": "garlic powder, salt, and pepper",    "store_section": "Pantry/Dry Goods"},
 ],
 "instructions": [
   "Squeeze grated potatoes and onion in a clean towel to remove as much moisture as possible.",
   "Season with garlic powder, salt, and pepper. Mix well.",
   "Melt 2 tbsp butter in a large skillet over medium-high heat.",
   "Press potato mixture into an even layer. Cook undisturbed 6-7 minutes until deep golden.",
   "Flip in sections and cook another 5-6 minutes until crispy.",
   "Push hash browns to the side. Add remaining butter and fry eggs to your liking.",
   "Serve eggs over hash browns.",
 ],
 "substitutions": {
   "dairy_free": "Use dairy-free butter or olive oil.",
   "gluten_free": "Already gluten-free.",
   "vegan": "Skip eggs and serve with sliced avocado.",
 },
 "notes": "Removing moisture is the key to crispy hash browns — don't skip that step."},

{"name": "Smoothie Bowl",
 "meal_type": "Breakfast", "servings": 1, "prep_time": "10 minutes", "cook_time": "0 minutes",
 "macros_per_serving": {"calories": 340, "protein_g": 12, "carbs_g": 58, "fat_g": 8},
 "ingredients": [
   {"amount": "1 cup",     "item": "frozen mixed berries",        "store_section": "Frozen"},
   {"amount": "1",         "item": "frozen banana",               "store_section": "Frozen"},
   {"amount": "1 scoop",   "item": "vanilla protein powder",      "store_section": "Pantry/Dry Goods"},
   {"amount": "1/4 cup",   "item": "almond milk",                 "store_section": "Pantry/Dry Goods"},
   {"amount": "2 tbsp",    "item": "granola",                     "store_section": "Pantry/Dry Goods"},
   {"amount": "1 tbsp",    "item": "honey",                       "store_section": "Pantry/Dry Goods"},
   {"amount": "1 tbsp",    "item": "peanut butter",               "store_section": "Pantry/Dry Goods"},
   {"amount": "1 tbsp",    "item": "chia seeds",                  "store_section": "Pantry/Dry Goods"},
   {"amount": "fresh",     "item": "sliced banana for topping",   "store_section": "Produce"},
 ],
 "instructions": [
   "Blend frozen berries, frozen banana, protein powder, and almond milk until thick and smooth.",
   "Add more milk 1 tbsp at a time only if needed — you want it very thick.",
   "Pour into a bowl.",
   "Top with granola, sliced banana, chia seeds, a drizzle of honey, and peanut butter.",
   "Eat immediately before it melts.",
 ],
 "substitutions": {
   "dairy_free": "Already dairy-free with almond milk.",
   "gluten_free": "Use certified gluten-free granola.",
   "vegan": "Use plant-based protein powder and maple syrup instead of honey.",
   "low_carb": "Use frozen cauliflower instead of banana and skip granola.",
 },
 "notes": "Use as little liquid as possible for a thick, spoonable consistency."},

]

for r in recipes:
    fn = r['name'].lower().replace(' ', '-').replace('&', 'and').replace("'", '').replace(',', '') + '.json'
    (OUT / fn).write_text(json.dumps(r, indent=2), encoding='utf-8')
    print(f'  Saved: {fn}')
print(f'Done — {len(recipes)} breakfast recipes.')
