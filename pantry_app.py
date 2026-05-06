#!/usr/bin/env python3
"""Flask web app for the pantry tracker. Run this file then open http://localhost:5000"""

import json
import webbrowser
from pathlib import Path
from flask import Flask, request, redirect, url_for, render_template_string
import openpyxl
from openpyxl import load_workbook

app = Flask(__name__)

XLSX             = Path(__file__).parent / 'Food in Storage.xlsx'
DATA_DIR         = Path(__file__).parent / 'data'
COLS             = ['Item', 'Quantity', 'Unit', 'Location', 'Section', 'Slot', 'Expiration', 'Notes']
LOCATION_SHEETS  = ['Brown Cabinet', 'Pantry', 'End Hall Closet', 'Laundry Room', 'Kitchen']

PURPLE      = '#6B2D8B'
DARK_PURPLE = '#4A1E6B'
LIGHT_PURP  = '#E8D5F0'

BASE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Pantry Tracker</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
<style>
  :root { --purple: #6B2D8B; --dark-purple: #4A1E6B; --light-purple: #E8D5F0; }
  body { background: #f9f6fc; font-family: 'Segoe UI', sans-serif; }
  .navbar { background: var(--purple) !important; }
  .navbar-brand, .nav-link { color: white !important; font-weight: 600; }
  .nav-link:hover { color: var(--light-purple) !important; }
  .card { border: 1.5px solid var(--light-purple); border-radius: 12px; }
  .card-header { background: var(--purple); color: white; border-radius: 10px 10px 0 0 !important; font-weight: 700; }
  .btn-primary { background: var(--purple); border-color: var(--dark-purple); }
  .btn-primary:hover { background: var(--dark-purple); }
  .btn-outline-primary { color: var(--purple); border-color: var(--purple); }
  .btn-outline-primary:hover { background: var(--purple); color: white; }
  table thead { background: var(--dark-purple); color: white; }
  table tbody tr:hover { background: var(--light-purple); }
  .badge-purple { background: var(--purple); }
  .can-make-yes  { color: #2d8b2d; font-weight: 700; }
  .can-make-part { color: #8b6b2d; font-weight: 600; }
  .can-make-no   { color: #8b2d2d; }
  .search-bar { border: 2px solid var(--light-purple); border-radius: 8px; }
  .search-bar:focus { border-color: var(--purple); box-shadow: 0 0 0 0.2rem rgba(107,45,139,.15); }
  h1 small { font-size: 0.5em; color: var(--light-purple); }
</style>
</head>
<body>
<nav class="navbar navbar-expand-lg mb-4">
  <div class="container">
    <a class="navbar-brand">🥘 Pantry Tracker</a>
    <div class="navbar-nav ms-auto">
      <a class="nav-link" href="/">Inventory</a>
      <a class="nav-link" href="/can-make">Can I Make?</a>
      <a class="nav-link" href="/add">Add Item</a>
    </div>
  </div>
</nav>
<div class="container pb-5">
  {% block content %}{% endblock %}
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

INDEX_HTML = BASE_HTML.replace('{% block content %}{% endblock %}', """
<div class="d-flex justify-content-between align-items-center mb-3">
  <h1>Pantry Inventory <small>{{ total }} items</small></h1>
  <a href="/add" class="btn btn-primary">+ Add Item</a>
</div>

<div class="card mb-4">
  <div class="card-body">
    <form method="get" class="row g-2">
      <div class="col-md-5">
        <input name="q" class="form-control search-bar" placeholder="Search items..." value="{{ q }}">
      </div>
      <div class="col-md-4">
        <select name="loc" class="form-select search-bar">
          <option value="">All Locations</option>
          {% for l in locations %}
          <option value="{{ l }}" {% if loc == l %}selected{% endif %}>{{ l }}</option>
          {% endfor %}
        </select>
      </div>
      <div class="col-md-3">
        <button type="submit" class="btn btn-primary w-100">Filter</button>
      </div>
    </form>
  </div>
</div>

<div class="card">
  <div class="card-header">Items</div>
  <div class="table-responsive">
    <table class="table table-hover mb-0">
      <thead>
        <tr>
          <th>Item</th><th>Qty</th><th>Unit</th>
          <th>Location</th><th>Section</th><th>Slot</th>
          <th>Expiration</th><th>Notes</th><th></th>
        </tr>
      </thead>
      <tbody>
        {% for i, row in items %}
        <tr>
          <td><strong>{{ row.Item }}</strong></td>
          <td>{{ row.Quantity or '' }}</td>
          <td>{{ row.Unit or '' }}</td>
          <td>{{ row.Location or '' }}</td>
          <td>{{ row.Section or '' }}</td>
          <td>{{ row.Slot or '' }}</td>
          <td>{{ row.Expiration or '' }}</td>
          <td>{{ row.Notes or '' }}</td>
          <td>
            <a href="/edit/{{ i }}" class="btn btn-sm btn-outline-primary me-1">Edit</a>
            <a href="/delete/{{ i }}" class="btn btn-sm btn-outline-danger"
               onclick="return confirm('Remove this item?')">Del</a>
          </td>
        </tr>
        {% endfor %}
        {% if not items %}
        <tr><td colspan="9" class="text-center text-muted py-4">No items found.</td></tr>
        {% endif %}
      </tbody>
    </table>
  </div>
</div>
""")

EDIT_HTML = BASE_HTML.replace('{% block content %}{% endblock %}', """
<h1>{{ title }}</h1>
<div class="card mt-3" style="max-width:600px">
  <div class="card-header">{{ title }}</div>
  <div class="card-body">
    <form method="post">
      {% for field in fields %}
      <div class="mb-3">
        <label class="form-label fw-bold">{{ field }}</label>
        <input name="{{ field }}" class="form-control" value="{{ values.get(field, '') }}">
      </div>
      {% endfor %}
      <div class="d-flex gap-2">
        <button type="submit" class="btn btn-primary">Save</button>
        <a href="/" class="btn btn-outline-secondary">Cancel</a>
      </div>
    </form>
  </div>
</div>
""")

CAN_MAKE_HTML = BASE_HTML.replace('{% block content %}{% endblock %}', """
<h1>Can I Make This?</h1>
<p class="text-muted">Recipes checked against your current pantry inventory.</p>
<div class="row row-cols-1 row-cols-md-2 g-4 mt-1">
  {% for recipe in recipes %}
  <div class="col">
    <div class="card h-100">
      <div class="card-header">{{ recipe.name }}</div>
      <div class="card-body">
        <div class="mb-2">
          <span class="{{ recipe.status_class }}">{{ recipe.status_label }}</span>
          <span class="text-muted ms-2 small">{{ recipe.meal_type }} · {{ recipe.prep_time }}</span>
        </div>
        {% if recipe.missing %}
        <p class="small text-muted mb-1">Missing:</p>
        <ul class="small mb-0">
          {% for m in recipe.missing %}<li>{{ m }}</li>{% endfor %}
        </ul>
        {% endif %}
      </div>
    </div>
  </div>
  {% endfor %}
  {% if not recipes %}
  <p class="text-muted">No recipes found. Add recipe JSON files to the data/ folder.</p>
  {% endif %}
</div>
""")


def load_wb():
    return load_workbook(XLSX)


def save_wb(wb):
    wb.save(XLSX)


def get_all_rows(wb):
    """Returns list of (sheet_name, row_index, data_dict)."""
    rows = []
    for sheet_name in LOCATION_SHEETS:
        if sheet_name not in wb.sheetnames:
            continue
        ws = wb[sheet_name]
        for r in range(2, ws.max_row + 1):
            vals = [ws.cell(row=r, column=c).value for c in range(1, 9)]
            if any(v for v in vals):
                rows.append((sheet_name, r, dict(zip(COLS, vals))))
    return rows


@app.route('/')
def index():
    q   = request.args.get('q', '').lower()
    loc = request.args.get('loc', '')

    wb      = load_wb()
    all_raw = get_all_rows(wb)

    locations = sorted({s for s, _, _ in all_raw})
    rows = [(f'{s}:{r}', d) for s, r, d in all_raw]

    if q:
        rows = [(i, r) for i, r in rows if q in str(r.get('Item', '')).lower()]
    if loc:
        rows = [(i, r) for i, r in rows if str(r.get('Location', '')) == loc or i.startswith(loc + ':')]

    return render_template_string(INDEX_HTML,
                                  items=rows, total=len(rows),
                                  locations=locations, q=q, loc=loc)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        location   = request.form.get('Location', '')
        sheet_name = location if location in LOCATION_SHEETS else LOCATION_SHEETS[0]
        wb  = load_wb()
        ws  = wb[sheet_name]
        row = next((r for r in range(2, ws.max_row + 2) if not ws.cell(row=r, column=1).value), ws.max_row + 1)
        for col, field in enumerate(COLS, 1):
            ws.cell(row=row, column=col).value = request.form.get(field, '') or None
        save_wb(wb)
        return redirect(url_for('index'))

    return render_template_string(EDIT_HTML,
                                  title='Add Item', fields=COLS, values={},
                                  locations=LOCATION_SHEETS)


@app.route('/edit/<path:row_key>', methods=['GET', 'POST'])
def edit(row_key):
    sheet_name, row_idx = row_key.rsplit(':', 1)
    row_idx = int(row_idx)
    wb = load_wb()
    ws = wb[sheet_name]

    if request.method == 'POST':
        for col, field in enumerate(COLS, 1):
            ws.cell(row=row_idx, column=col).value = request.form.get(field, '') or None
        save_wb(wb)
        return redirect(url_for('index'))

    values = {field: ws.cell(row=row_idx, column=col).value or ''
              for col, field in enumerate(COLS, 1)}

    return render_template_string(EDIT_HTML,
                                  title=f'Edit: {values.get("Item", "")}',
                                  fields=COLS, values=values,
                                  locations=LOCATION_SHEETS)


@app.route('/delete/<path:row_key>')
def delete(row_key):
    sheet_name, row_idx = row_key.rsplit(':', 1)
    row_idx = int(row_idx)
    wb = load_wb()
    ws = wb[sheet_name]
    for col in range(1, 9):
        ws.cell(row=row_idx, column=col).value = None
    save_wb(wb)
    return redirect(url_for('index'))


@app.route('/can-make')
def can_make():
    wb   = load_wb()
    have = {str(d.get('Item', '')).lower() for _, _, d in get_all_rows(wb) if d.get('Item')}

    results = []
    if DATA_DIR.exists():
        for path in sorted(DATA_DIR.glob('*.json')):
            try:
                with open(path, encoding='utf-8') as f:
                    recipe = json.load(f)
            except Exception:
                continue

            ingredients = recipe.get('ingredients', [])
            needed = [(ing.get('item', '') if isinstance(ing, dict) else str(ing)).lower()
                      for ing in ingredients]

            if not needed:
                continue

            have_count = sum(1 for n in needed if any(n in h or h in n for h in have))
            total      = len(needed)
            pct        = int(have_count / total * 100) if total else 0
            missing    = [n for n in needed if not any(n in h or h in n for h in have)]

            if pct == 100:
                status_class = 'can-make-yes'
                status_label = '✓ You have everything!'
            elif pct >= 60:
                status_class = 'can-make-part'
                status_label = f'~{pct}% — almost there'
            else:
                status_class = 'can-make-no'
                status_label = f'{pct}% ({have_count}/{total} ingredients)'

            results.append({
                'name':         recipe.get('name', 'Untitled'),
                'meal_type':    recipe.get('meal_type', ''),
                'prep_time':    recipe.get('prep_time', ''),
                'status_class': status_class,
                'status_label': status_label,
                'missing':      missing[:6],
            })

    results.sort(key=lambda x: x['status_label'])
    return render_template_string(CAN_MAKE_HTML, recipes=results)


if __name__ == '__main__':
    print('Starting Pantry Tracker at http://localhost:5000')
    webbrowser.open('http://localhost:5000')
    app.run(debug=False, port=5000)
