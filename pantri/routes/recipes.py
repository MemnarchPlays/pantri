"""Recipes blueprint."""

import io
import json
import re
import shutil
from pathlib import Path
from flask import Blueprint, request, redirect, url_for, render_template, jsonify, send_file, send_from_directory, abort
from werkzeug.utils import secure_filename
from pantry_utils import DATA_DIR, MEAL_TYPES, EXCLUDE_SHEETS
from pantri.db import load_wb, save_wb, get_all_rows
from pantri.state import load_exclusions

bp = Blueprint('recipes', __name__)

STARTER_DIR = Path(__file__).parent.parent.parent / 'starter-recipes'
IMAGES_DIR = DATA_DIR / 'images'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}


def _allowed_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/recipe-images/<slug>/<filename>')
def recipe_image(slug, filename):
    img_dir = IMAGES_DIR / slug
    if not img_dir.is_dir():
        abort(404)
    return send_from_directory(str(img_dir), filename)


@bp.route('/recipes')
def recipes():
    tab        = request.args.get('tab', 'library')
    q          = request.args.get('q', '').lower()
    meal       = request.args.get('meal', '')
    cm_meal    = request.args.get('cm_meal', '')
    ingredient = request.args.get('ingredient', '').strip().lower()

    all_recipes = []
    if DATA_DIR.exists():
        for path in sorted(DATA_DIR.glob('*.json')):
            try:
                r = json.load(open(path, encoding='utf-8'))
            except Exception:
                continue
            r['slug'] = path.stem
            all_recipes.append(r)

    lib_recipes = [r for r in all_recipes
                   if (not q or q in r.get('name', '').lower())
                   and (not meal or meal.lower() in r.get('meal_type', '').lower())]
    lib_recipes.sort(key=lambda x: (not x.get('favorite', False), x.get('name', '').lower()))

    cm_recipes = []
    if tab == 'canmake':
        wb   = load_wb()
        have = {str(d.get('Item', '')).lower() for _, _, d in get_all_rows(wb) if d.get('Item')}
        for r in all_recipes:
            if cm_meal and cm_meal.lower() not in r.get('meal_type', '').lower():
                continue
            ingredients = r.get('ingredients', [])
            needed = [(i.get('item', '') if isinstance(i, dict) else str(i)).lower() for i in ingredients]
            if not needed:
                continue
            if ingredient and not any(ingredient in n or n in ingredient for n in needed):
                continue
            have_count = sum(1 for n in needed if any(n in h or h in n for h in have))
            total = len(needed)
            pct   = int(have_count / total * 100) if total else 0
            missing = [n for n in needed if not any(n in h or h in n for h in have)]
            if pct == 100:
                status_class, status_label = 'text-success fw-bold', '✓ You have everything!'
            elif pct >= 60:
                status_class, status_label = 'text-warning fw-bold', f'~{pct}% — almost there'
            elif pct > 0:
                status_class, status_label = 'text-danger', f'{pct}% ({have_count}/{total} ingredients)'
            else:
                status_class, status_label = 'text-danger', '0% — missing everything'
            cm_recipes.append({'name': r.get('name', 'Untitled'), 'meal_type': r.get('meal_type', ''),
                               'prep_time': r.get('prep_time', ''), 'status_class': status_class,
                               'status_label': status_label, 'missing': missing[:6], 'pct': pct})
        cm_recipes.sort(key=lambda x: x['pct'], reverse=True)

    starter_count = len(list(STARTER_DIR.glob('*.json'))) if STARTER_DIR.exists() else 0
    return render_template('recipes.html', recipes=lib_recipes, q=q, meal=meal,
                           tab=tab, cm_recipes=cm_recipes, cm_meal=cm_meal,
                           ingredient=ingredient, meal_types=MEAL_TYPES,
                           total_recipes=len(all_recipes),
                           starter_count=starter_count)


@bp.route('/recipe/import')
def recipe_import():
    import requests as req
    from bs4 import BeautifulSoup

    url = request.args.get('url', '').strip()
    if not url:
        return json.dumps({'error': 'No URL provided'}), 400, {'Content-Type': 'application/json'}

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        resp = req.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        return json.dumps({'error': f'Could not fetch page: {e}'}), 400, {'Content-Type': 'application/json'}

    soup = BeautifulSoup(resp.text, 'html.parser')

    # Find schema.org Recipe in any JSON-LD block
    recipe_data = None
    for script in soup.find_all('script', type='application/ld+json'):
        try:
            data = json.loads(script.string or '{}')
        except Exception:
            continue
        candidates = data if isinstance(data, list) else data.get('@graph', [data])
        for item in candidates:
            if isinstance(item, dict) and 'Recipe' in str(item.get('@type', '')):
                recipe_data = item
                break
        if recipe_data:
            break

    if not recipe_data:
        return json.dumps({'error': 'No recipe data found on this page. Try the original source URL instead of a saved CopyMeThat link.'}), 404, {'Content-Type': 'application/json'}

    def parse_duration(iso):
        if not iso:
            return ''
        h = re.search(r'(\d+)H', str(iso))
        m = re.search(r'(\d+)M', str(iso))
        parts = []
        if h:
            n = int(h.group(1))
            parts.append(f"{n} hour{'s' if n != 1 else ''}")
        if m:
            n = int(m.group(1))
            parts.append(f"{n} minute{'s' if n != 1 else ''}")
        return ' '.join(parts) or str(iso)

    def parse_servings(val):
        if not val:
            return 4
        if isinstance(val, list):
            val = val[0]
        m = re.search(r'\d+', str(val))
        return int(m.group()) if m else 4

    def extract_num(val):
        if not val:
            return 0
        m = re.search(r'[\d.]+', str(val))
        return float(m.group()) if m else 0

    UNITS = {
        'cup','cups','tablespoon','tablespoons','tbsp','teaspoon','teaspoons','tsp',
        'pound','pounds','lb','lbs','ounce','ounces','oz','gram','grams','g',
        'kilogram','kilograms','kg','liter','liters','ml','milliliter','milliliters',
        'can','cans','jar','jars','package','packages','pkg','clove','cloves',
        'slice','slices','piece','pieces','bunch','bunches','pinch','dash',
        'quart','quarts','pint','pints','gallon','gallons','sprig','sprigs',
    }

    def parse_ingredient(text):
        text = text.strip()
        parts = text.split()
        if not parts:
            return '', text
        # Must start with a digit or vulgar fraction to have an amount
        if not (parts[0][0].isdigit() or parts[0][0] in '½¼¾⅓⅔⅛⅜⅝⅞'):
            return '', text
        # Take leading number tokens (handles "1 1/2")
        i = 0
        while i < len(parts) and (parts[i].replace('/', '').replace('.', '').isdigit()
                                   or parts[i] in '½¼¾⅓⅔⅛⅜⅝⅞'):
            i += 1
        # Optionally include a unit word
        if i < len(parts) and parts[i].lower().rstrip('s.') in UNITS or (i < len(parts) and parts[i].lower() in UNITS):
            i += 1
        amount = ' '.join(parts[:i])
        item   = ' '.join(parts[i:])
        return amount, item

    def parse_instructions(raw):
        steps = []
        for item in (raw if isinstance(raw, list) else []):
            if isinstance(item, str):
                steps.append(item.strip())
            elif isinstance(item, dict):
                t = item.get('@type', '')
                if 'HowToStep' in t:
                    steps.append(item.get('text', '').strip())
                elif 'HowToSection' in t:
                    for sub in item.get('itemListElement', []):
                        if isinstance(sub, dict):
                            steps.append(sub.get('text', '').strip())
        return [s for s in steps if s]

    category = recipe_data.get('recipeCategory', '') or ''
    if isinstance(category, list):
        category = category[0] if category else ''
    meal_type = 'Dinner'
    for mt in MEAL_TYPES:
        if mt.lower() in str(category).lower():
            meal_type = mt
            break

    nutrition = recipe_data.get('nutrition') or {}
    ingredients = []
    for ing in recipe_data.get('recipeIngredient', []):
        amount, item = parse_ingredient(str(ing))
        ingredients.append({'amount': amount, 'item': item})

    def extract_image_url(image):
        if not image:
            return ''
        if isinstance(image, list):
            image = image[0] if image else ''
        if isinstance(image, dict):
            return image.get('url', '')
        return str(image)

    result = {
        'name':         recipe_data.get('name', '').strip(),
        'meal_type':    meal_type,
        'servings':     parse_servings(recipe_data.get('recipeYield')),
        'prep_time':    parse_duration(recipe_data.get('prepTime')),
        'cook_time':    parse_duration(recipe_data.get('cookTime')),
        'calories':     int(extract_num(nutrition.get('calories'))),
        'protein':      extract_num(nutrition.get('proteinContent')),
        'carbs':        extract_num(nutrition.get('carbohydrateContent')),
        'fat':          extract_num(nutrition.get('fatContent')),
        'ingredients':  ingredients,
        'instructions': parse_instructions(recipe_data.get('recipeInstructions', [])),
        'notes':        (recipe_data.get('description') or '').strip(),
        'image_url':    extract_image_url(recipe_data.get('image')),
    }
    return json.dumps(result), 200, {'Content-Type': 'application/json'}


@bp.route('/recipe/add', methods=['GET', 'POST'])
def recipe_add():
    if request.method == 'POST':
        name      = request.form.get('name', '').strip()
        meal_type = request.form.get('meal_type', '')
        servings  = int(request.form.get('servings') or 1)
        prep_time = request.form.get('prep_time', '').strip()
        cook_time = request.form.get('cook_time', '').strip()

        try:
            calories = float(request.form.get('calories') or 0)
            protein  = float(request.form.get('protein') or 0)
            carbs    = float(request.form.get('carbs') or 0)
            fat      = float(request.form.get('fat') or 0)
        except ValueError:
            calories = protein = carbs = fat = 0

        amounts     = request.form.getlist('amount[]')
        ingredients_raw = request.form.getlist('ingredient[]')
        ingredients = [{'amount': a.strip(), 'item': i.strip()}
                       for a, i in zip(amounts, ingredients_raw) if i.strip()]

        instructions = [s.strip() for s in request.form.getlist('instruction[]') if s.strip()]

        subs = {}
        for key in ['dairy_free', 'gluten_free', 'vegan', 'vegetarian', 'low_carb']:
            val = request.form.get(f'sub_{key}', '').strip()
            if val:
                subs[key] = val

        recipe = {
            'name':      name,
            'meal_type': meal_type,
            'servings':  servings,
            'prep_time': prep_time,
            'cook_time': cook_time,
            'macros_per_serving': {
                'calories': calories, 'protein_g': protein,
                'carbs_g': carbs, 'fat_g': fat,
            },
            'ingredients':  ingredients,
            'instructions': instructions,
        }
        if subs:
            recipe['substitutions'] = subs
        notes = request.form.get('notes', '').strip()
        if notes:
            recipe['notes'] = notes

        DATA_DIR.mkdir(exist_ok=True)
        slug = re.sub(r"[^a-z0-9]+", '-', name.lower()).strip('-')

        photos = []

        import_image_url = request.form.get('import_image_url', '').strip()
        if import_image_url:
            try:
                import requests as _req
                _headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                _ir = _req.get(import_image_url, headers=_headers, timeout=10)
                _ir.raise_for_status()
                _ct = _ir.headers.get('Content-Type', '').split(';')[0].strip()
                _ext_map = {'image/jpeg': 'jpg', 'image/jpg': 'jpg', 'image/png': 'png',
                            'image/gif': 'gif', 'image/webp': 'webp'}
                _ext = _ext_map.get(_ct, '')
                if not _ext:
                    _stem = import_image_url.split('?')[0]
                    _ue = _stem.rsplit('.', 1)[-1].lower() if '.' in _stem else ''
                    if _ue in ALLOWED_EXTENSIONS:
                        _ext = _ue
                if _ext:
                    _idir = IMAGES_DIR / slug
                    _idir.mkdir(parents=True, exist_ok=True)
                    _fname = f'imported.{_ext}'
                    (_idir / _fname).write_bytes(_ir.content)
                    photos.append(_fname)
            except Exception:
                pass

        for f in request.files.getlist('photos'):
            if f and f.filename:
                if not _allowed_image(f.filename):
                    abort(400, f"'{f.filename}' is not an allowed image type. Accepted: jpg, jpeg, png, gif, webp.")
                fname = secure_filename(f.filename)
                img_dir = IMAGES_DIR / slug
                img_dir.mkdir(parents=True, exist_ok=True)
                f.save(str(img_dir / fname))
                photos.append(fname)
        if photos:
            recipe['photos'] = photos

        (DATA_DIR / f'{slug}.json').write_text(json.dumps(recipe, indent=2), encoding='utf-8')
        return redirect(url_for('recipes.recipes'))

    rv = {'name':'','meal_type':'','servings':4,'prep_time':'','cook_time':'',
          'calories':'','protein':'','carbs':'','fat':'','notes':'',
          'ingredients':[],'instructions':[],'photos':[],
          'sub_dairy_free':'','sub_gluten_free':'','sub_vegan':'','sub_vegetarian':'','sub_low_carb':''}
    return render_template('recipe_add.html', meal_types=MEAL_TYPES, rv=rv,
                           page_title='Add Recipe', edit_mode=False)


@bp.route('/recipe/<slug>')
def recipe_detail(slug):
    path = DATA_DIR / f'{slug}.json'
    if not path.exists():
        return redirect(url_for('recipes.recipes'))
    recipe = json.load(open(path, encoding='utf-8'))
    wb   = load_wb()
    have = {str(d.get('Item', '')).lower() for _, _, d in get_all_rows(wb) if d.get('Item')}
    used_count      = request.args.get('used_count')
    not_found_count = request.args.get('not_found_count')
    kwargs = {'recipe': recipe, 'slug': slug, 'have': have}
    if used_count is not None:
        kwargs['used_count']      = int(used_count)
        kwargs['not_found_count'] = int(not_found_count or 0)
    return render_template('recipe_detail.html', **kwargs)


@bp.route('/recipe/<slug>/use', methods=['POST'])
def recipe_use(slug):
    path = DATA_DIR / f'{slug}.json'
    if not path.exists():
        return redirect(url_for('recipes.recipes'))

    recipe = json.load(open(path, encoding='utf-8'))
    wb = load_wb()
    used_count = 0
    not_found_count = 0

    exclusions = load_exclusions()
    excluded_names = {ex.get('name', '').lower() for ex in exclusions}

    for ing in recipe.get('ingredients', []):
        item_name  = (ing.get('item', '') if isinstance(ing, dict) else str(ing)).strip()
        amount_str = (ing.get('amount', '') if isinstance(ing, dict) else '').strip()
        if not item_name:
            continue

        # Skip items on the exclusion list — never auto-decrement these
        ilow = item_name.lower()
        if any(ilow == ex or ilow in ex or ex in ilow for ex in excluded_names):
            continue

        # Parse the leading number from the amount string
        m = re.search(r'[\d.]+', amount_str)
        qty = float(m.group()) if m else 1.0

        # Search all pantry sheets for a fuzzy name match
        found = False
        for sheet_name in [s for s in wb.sheetnames if s not in EXCLUDE_SHEETS]:
            ws = wb[sheet_name]
            for r in range(2, ws.max_row + 1):
                cell = str(ws.cell(row=r, column=1).value or '').strip().lower()
                if not cell:
                    continue
                if cell == item_name.lower() or item_name.lower() in cell or cell in item_name.lower():
                    try:
                        current = float(str(ws.cell(row=r, column=2).value or 0))
                    except (ValueError, TypeError):
                        current = 0
                    new_qty = max(0, current - qty)
                    ws.cell(row=r, column=2).value = int(new_qty) if new_qty == int(new_qty) else new_qty
                    found = True
                    used_count += 1
                    break
            if found:
                break

        if not found:
            not_found_count += 1

    save_wb(wb)
    return redirect(url_for('recipes.recipe_detail', slug=slug,
                            used_count=used_count, not_found_count=not_found_count))


@bp.route('/recipe/<slug>/favorite', methods=['POST'])
def recipe_favorite(slug):
    path = DATA_DIR / f'{slug}.json'
    if not path.exists():
        return jsonify({'ok': False}), 404
    recipe = json.loads(path.read_text(encoding='utf-8'))
    recipe['favorite'] = not recipe.get('favorite', False)
    path.write_text(json.dumps(recipe, indent=2), encoding='utf-8')
    return jsonify({'favorite': recipe['favorite']})


@bp.route('/recipe/delete/<slug>')
def recipe_delete(slug):
    path = DATA_DIR / f'{slug}.json'
    if path.exists():
        path.unlink()
    img_dir = IMAGES_DIR / slug
    if img_dir.exists():
        shutil.rmtree(img_dir)
    return redirect(url_for('recipes.recipes'))


@bp.route('/recipe/edit/<slug>', methods=['GET', 'POST'])
def recipe_edit(slug):
    path = DATA_DIR / f'{slug}.json'
    if not path.exists():
        return redirect(url_for('recipes.recipes'))

    if request.method == 'POST':
        existing_for_photos = json.load(open(path, encoding='utf-8'))
        old_photos = existing_for_photos.get('photos', [])

        name      = request.form.get('name', '').strip()
        meal_type = request.form.get('meal_type', '')
        servings  = int(request.form.get('servings') or 1)
        prep_time = request.form.get('prep_time', '').strip()
        cook_time = request.form.get('cook_time', '').strip()

        try:
            calories = float(request.form.get('calories') or 0)
            protein  = float(request.form.get('protein') or 0)
            carbs    = float(request.form.get('carbs') or 0)
            fat      = float(request.form.get('fat') or 0)
        except ValueError:
            calories = protein = carbs = fat = 0

        amounts         = request.form.getlist('amount[]')
        ingredients_raw = request.form.getlist('ingredient[]')
        ingredients     = [{'amount': a.strip(), 'item': i.strip()}
                           for a, i in zip(amounts, ingredients_raw) if i.strip()]
        instructions    = [s.strip() for s in request.form.getlist('instruction[]') if s.strip()]

        subs = {}
        for key in ['dairy_free', 'gluten_free', 'vegan', 'vegetarian', 'low_carb']:
            val = request.form.get(f'sub_{key}', '').strip()
            if val:
                subs[key] = val

        recipe = {
            'name': name, 'meal_type': meal_type, 'servings': servings,
            'prep_time': prep_time, 'cook_time': cook_time,
            'macros_per_serving': {'calories': calories, 'protein_g': protein,
                                   'carbs_g': carbs, 'fat_g': fat},
            'ingredients': ingredients, 'instructions': instructions,
        }
        if subs:
            recipe['substitutions'] = subs
        notes = request.form.get('notes', '').strip()
        if notes:
            recipe['notes'] = notes

        new_slug = re.sub(r"[^a-z0-9]+", '-', name.lower()).strip('-')

        # Delete photos the user removed
        kept_photos = request.form.getlist('existing_photo[]')
        for fname in [p for p in old_photos if p not in kept_photos]:
            old_file = IMAGES_DIR / slug / fname
            if old_file.exists():
                old_file.unlink()

        # Handle new uploads into current slug directory (before any rename)
        new_photos = []
        for f in request.files.getlist('photos'):
            if f and f.filename:
                if not _allowed_image(f.filename):
                    abort(400, f"'{f.filename}' is not an allowed image type. Accepted: jpg, jpeg, png, gif, webp.")
                fname = secure_filename(f.filename)
                img_dir = IMAGES_DIR / slug
                img_dir.mkdir(parents=True, exist_ok=True)
                f.save(str(img_dir / fname))
                new_photos.append(fname)

        all_photos = kept_photos + new_photos
        if all_photos:
            recipe['photos'] = all_photos

        # If name changed, rename the JSON file and image folder
        if new_slug != slug:
            old_img_dir = IMAGES_DIR / slug
            new_img_dir = IMAGES_DIR / new_slug
            if old_img_dir.exists():
                old_img_dir.rename(new_img_dir)
            path.unlink()

        (DATA_DIR / f'{new_slug}.json').write_text(json.dumps(recipe, indent=2), encoding='utf-8')
        return redirect(url_for('recipes.recipe_detail', slug=new_slug))

    existing = json.load(open(path, encoding='utf-8'))
    m = existing.get('macros_per_serving', {})
    subs = existing.get('substitutions', {})
    rv = {
        'name':       existing.get('name', ''),
        'meal_type':  existing.get('meal_type', ''),
        'servings':   existing.get('servings', 4),
        'prep_time':  existing.get('prep_time', ''),
        'cook_time':  existing.get('cook_time', ''),
        'calories':   m.get('calories', ''),
        'protein':    m.get('protein_g', ''),
        'carbs':      m.get('carbs_g', ''),
        'fat':        m.get('fat_g', ''),
        'notes':      existing.get('notes', ''),
        'ingredients':   existing.get('ingredients', []),
        'instructions':  existing.get('instructions', []),
        'photos':        existing.get('photos', []),
        'sub_dairy_free':  subs.get('dairy_free', ''),
        'sub_gluten_free': subs.get('gluten_free', ''),
        'sub_vegan':       subs.get('vegan', ''),
        'sub_vegetarian':  subs.get('vegetarian', ''),
        'sub_low_carb':    subs.get('low_carb', ''),
    }
    return render_template('recipe_add.html', meal_types=MEAL_TYPES, rv=rv,
                           page_title=f'Edit: {rv["name"]}', edit_mode=True, slug=slug)


@bp.route('/recipes/download-pdf')
def download_pdf():
    import io as _io
    try:
        import sys as _sys
        from pathlib import Path as _Path
        _sys.path.insert(0, str(_Path(__file__).parent.parent.parent))
        from generate_pdf import generate_binder_bytes
    except ImportError:
        return 'reportlab is not installed. Run: pip install reportlab', 500

    data = generate_binder_bytes()
    if not data:
        return 'No recipes found.', 404

    from datetime import datetime
    filename = f'recipe_binder_{datetime.now().strftime("%Y%m%d")}.pdf'
    return send_file(
        _io.BytesIO(data),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=filename
    )


@bp.route('/recipes/delete-all', methods=['POST'])
def recipes_delete_all():
    if DATA_DIR.exists():
        for f in DATA_DIR.glob('*.json'):
            f.unlink()
    if IMAGES_DIR.exists():
        shutil.rmtree(IMAGES_DIR)
    return redirect(url_for('recipes.recipes'))


@bp.route('/recipes/load-basics', methods=['POST'])
def load_basics():
    if not STARTER_DIR.exists():
        return redirect(url_for('recipes.recipes'))
    DATA_DIR.mkdir(exist_ok=True)
    for src in STARTER_DIR.glob('*.json'):
        dest = DATA_DIR / src.name
        if not dest.exists():
            shutil.copy2(src, dest)
    return redirect(url_for('recipes.recipes'))
