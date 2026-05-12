"""Shopping blueprint."""

import json
from datetime import datetime
from flask import Blueprint, request, redirect, url_for, render_template
from pantry_utils import DATA_DIR
from pantri.db import load_wb, get_all_rows, get_minimums
from pantri.state import load_shopping_list, save_shopping_list, load_exclusions

bp = Blueprint('shopping', __name__)


@bp.route('/shopping')
def shopping():
    wb   = load_wb()
    rows = get_all_rows(wb)
    mins = get_minimums()

    stock = {}
    units = {}
    for _, _, d in rows:
        name = str(d.get('Item') or '').strip().lower()
        if not name:
            continue
        try:
            qty = float(str(d.get('Quantity') or 0))
        except ValueError:
            qty = 0
        stock[name] = stock.get(name, 0) + qty
        if name not in units:
            units[name] = str(d.get('Unit') or '').strip()

    restock = []
    for m in mins:
        key     = m['item'].lower()
        current = stock.get(key, 0)
        if current < m['qty']:
            restock.append({
                'name': m['item'],
                'have': current,
                'unit': units.get(key, ''),
                'need': round(m['qty'] - current, 1),
                'type': m['type'],
            })
    restock.sort(key=lambda x: (x['type'].lower() or 'zzz', x['name'].lower()))

    have = {str(d.get('Item', '')).lower() for _, _, d in rows if d.get('Item')}

    all_recipes = []
    if DATA_DIR.exists():
        for p in sorted(DATA_DIR.glob('*.json')):
            try:
                r = json.load(open(p, encoding='utf-8'))
                r['slug'] = p.stem
                all_recipes.append(r)
            except Exception:
                continue
    all_recipes.sort(key=lambda x: x.get('name', ''))

    selected_recipe = request.args.get('recipe', '')
    missing_ingredients = []
    if selected_recipe:
        chosen = next((r for r in all_recipes if r['slug'] == selected_recipe), None)
        if chosen:
            for ing in chosen.get('ingredients', []):
                item_name = ing.get('item', '').lower()
                if not any(item_name in h or h in item_name for h in have):
                    missing_ingredients.append(ing)

    return render_template('shopping.html', restock=restock, all_recipes=all_recipes,
                           selected_recipe=selected_recipe,
                           missing_ingredients=missing_ingredients,
                           shopping_list=load_shopping_list())


@bp.route('/shopping/list/add-restock', methods=['POST'])
def shopping_list_add_restock():
    wb   = load_wb()
    rows = get_all_rows(wb)
    mins = get_minimums()

    stock = {}
    units = {}
    for _, _, d in rows:
        name = str(d.get('Item') or '').strip().lower()
        if not name:
            continue
        try:
            qty = float(str(d.get('Quantity') or 0))
        except ValueError:
            qty = 0
        stock[name] = stock.get(name, 0) + qty
        if name not in units:
            units[name] = str(d.get('Unit') or '').strip()

    items    = load_shopping_list()
    existing = {i['name'].lower() for i in items}

    for m in mins:
        key     = m['item'].lower()
        current = stock.get(key, 0)
        if current >= m['qty']:
            continue
        if key in existing:
            continue
        need      = round(m['qty'] - current, 1)
        unit_str  = f" {units[key]}" if key in units and units[key] else ''
        items.append({
            'id':            str(int(datetime.now().timestamp() * 1000)) + str(len(items)),
            'name':          m['item'],
            'amount':        f"need {need}{unit_str}",
            'note':          f"{m['type'] or 'Restock'}",
            'checked':       False,
            'store_section': '',
        })
        existing.add(key)

    save_shopping_list(items)
    return redirect(url_for('shopping.shopping'))


@bp.route('/shopping/list/add-recipe', methods=['POST'])
def shopping_list_add_recipe():
    slug = request.form.get('recipe', '')
    if not slug or not DATA_DIR.exists():
        return redirect(url_for('shopping.shopping', recipe=slug))
    path = DATA_DIR / f'{slug}.json'
    if not path.exists():
        return redirect(url_for('shopping.shopping', recipe=slug))

    recipe = json.loads(path.read_text(encoding='utf-8'))
    recipe_name = recipe.get('name', slug)

    wb   = load_wb()
    have = {str(d.get('Item', '')).lower() for _, _, d in get_all_rows(wb) if d.get('Item')}

    items = load_shopping_list()
    existing_names = {i['name'].lower() for i in items}

    exclusions = load_exclusions()
    excluded_names = {ex.get('name', '').lower() for ex in exclusions}

    for ing in recipe.get('ingredients', []):
        item_name = ing.get('item', '').strip()
        if not item_name:
            continue
        item_lower = item_name.lower()
        if any(item_lower == ex or item_lower in ex or ex in item_lower for ex in excluded_names):
            continue
        if any(item_lower in h or h in item_lower for h in have):
            continue
        if item_lower in existing_names:
            continue
        items.append({
            'id':            str(int(datetime.now().timestamp() * 1000)) + str(len(items)),
            'name':          item_name,
            'amount':        ing.get('amount', ''),
            'note':          f'For: {recipe_name}',
            'checked':       False,
            'store_section': ing.get('store_section', ''),
        })
        existing_names.add(item_lower)

    save_shopping_list(items)
    return redirect(url_for('shopping.shopping', recipe=slug))


@bp.route('/shopping/list/toggle/<item_id>', methods=['POST'])
def shopping_list_toggle(item_id):
    items = load_shopping_list()
    for item in items:
        if item['id'] == item_id:
            item['checked'] = not item['checked']
            break
    save_shopping_list(items)
    recipe = request.args.get('recipe', '')
    return redirect(url_for('shopping.shopping', recipe=recipe) if recipe else url_for('shopping.shopping'))


@bp.route('/shopping/list/remove/<item_id>')
def shopping_list_remove(item_id):
    items = [i for i in load_shopping_list() if i['id'] != item_id]
    save_shopping_list(items)
    return redirect(url_for('shopping.shopping'))


@bp.route('/shopping/list/clear-all', methods=['POST'])
def shopping_list_clear_all():
    save_shopping_list([])
    return redirect(url_for('shopping.shopping'))


@bp.route('/shopping/list/clear-checked', methods=['POST'])
def shopping_list_clear_checked():
    items = [i for i in load_shopping_list() if not i['checked']]
    save_shopping_list(items)
    return redirect(url_for('shopping.shopping'))
