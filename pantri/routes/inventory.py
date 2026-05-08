"""Inventory blueprint — /, /add, /edit/<row_key>, /delete/<row_key>, /add/bulk"""

from flask import Blueprint, request, redirect, url_for, render_template, jsonify
from pantry_utils import COLS, to_title
from pantri.db import load_wb, save_wb, get_all_rows, get_location_sheets
from pantri.state import load_units

bp = Blueprint('inventory', __name__)


@bp.route('/')
def index():
    tab = request.args.get('tab', 'items')
    q   = request.args.get('q', '').lower()
    loc = request.args.get('loc', '')
    wb        = load_wb()
    all_raw   = get_all_rows(wb)
    locations = get_location_sheets()
    rows = [(f'{s}:{r}', d) for s, r, d in all_raw]
    if q:
        rows = [(i, r) for i, r in rows if q in str(r.get('Item', '')).lower()]
    if loc:
        rows = [(i, r) for i, r in rows if str(r.get('Location', '')) == loc or i.startswith(loc + ':')]
    return render_template('inventory.html', items=rows, total=len(rows),
                           locations=locations, q=q, loc=loc,
                           tab=tab, bulk_results=[], units=load_units())


@bp.route('/add', methods=['GET', 'POST'])
def add():
    location_sheets = get_location_sheets()
    if request.method == 'POST':
        item     = to_title((request.form.get('Item', '') or '').strip())
        quantity = request.form.get('Quantity', '') or None
        unit     = request.form.get('Unit', '') or None
        location = request.form.get('Location', '')
        sheet_name = location if location in location_sheets else location_sheets[0]
        wb  = load_wb()
        ws  = wb[sheet_name]
        # Check if same item + unit already exists in this sheet — merge if so
        existing = next((r for r in range(2, ws.max_row + 1)
                         if str(ws.cell(row=r, column=1).value or '').lower() == (item or '').lower()
                         and str(ws.cell(row=r, column=3).value or '').lower() == (unit or '').lower()), None)
        if existing:
            try:
                cur = float(str(ws.cell(row=existing, column=2).value or 0))
                add_qty = float(quantity) if quantity else 1
                merged = cur + add_qty
                ws.cell(row=existing, column=2).value = int(merged) if merged == int(merged) else merged
            except (ValueError, TypeError):
                pass
        else:
            row = next((r for r in range(2, ws.max_row + 2) if not ws.cell(row=r, column=1).value), ws.max_row + 1)
            ws.cell(row=row, column=1).value = item or None
            ws.cell(row=row, column=2).value = quantity
            ws.cell(row=row, column=3).value = unit
            ws.cell(row=row, column=4).value = sheet_name
        save_wb(wb)
        return redirect(url_for('inventory.index', tab='add'))
    return redirect(url_for('inventory.index', tab='add'))


@bp.route('/edit/<path:row_key>', methods=['GET', 'POST'])
def edit(row_key):
    sheet_name, row_idx = row_key.rsplit(':', 1)
    row_idx = int(row_idx)
    location_sheets = get_location_sheets()
    wb = load_wb()
    ws = wb[sheet_name]
    if request.method == 'POST':
        item     = to_title((request.form.get('Item', '') or '').strip())
        quantity = request.form.get('Quantity', '') or None
        unit     = request.form.get('Unit', '') or None
        location = request.form.get('Location', '') or sheet_name
        new_sheet = location if location in location_sheets else sheet_name
        if new_sheet != sheet_name:
            # Clear old row
            for col in range(1, 9):
                ws.cell(row=row_idx, column=col).value = None
            ws2 = wb[new_sheet]
            # Check if same item + unit already exists in destination — merge quantities if so
            existing = next((r for r in range(2, ws2.max_row + 1)
                             if str(ws2.cell(row=r, column=1).value or '').lower() == (item or '').lower()
                             and str(ws2.cell(row=r, column=3).value or '').lower() == (unit or '').lower()), None)
            if existing:
                try:
                    cur = float(str(ws2.cell(row=existing, column=2).value or 0))
                    add_qty = float(quantity) if quantity else 0
                    merged = cur + add_qty
                    ws2.cell(row=existing, column=2).value = int(merged) if merged == int(merged) else merged
                except (ValueError, TypeError):
                    pass
            else:
                new_row = next((r for r in range(2, ws2.max_row + 2) if not ws2.cell(row=r, column=1).value), ws2.max_row + 1)
                ws2.cell(row=new_row, column=1).value = item or None
                ws2.cell(row=new_row, column=2).value = quantity
                ws2.cell(row=new_row, column=3).value = unit
                ws2.cell(row=new_row, column=4).value = new_sheet
        else:
            # Same sheet — check for collision with another row (different row_idx, same name + unit)
            collision = next((r for r in range(2, ws.max_row + 1)
                              if r != row_idx
                              and str(ws.cell(row=r, column=1).value or '').lower() == (item or '').lower()
                              and str(ws.cell(row=r, column=3).value or '').lower() == (unit or '').lower()), None)
            if collision:
                try:
                    cur = float(str(ws.cell(row=collision, column=2).value or 0))
                    add_qty = float(quantity) if quantity else 0
                    merged = cur + add_qty
                    ws.cell(row=collision, column=2).value = int(merged) if merged == int(merged) else merged
                except (ValueError, TypeError):
                    pass
                # Clear the row being edited since we merged into the existing one
                for col in range(1, 9):
                    ws.cell(row=row_idx, column=col).value = None
            else:
                ws.cell(row=row_idx, column=1).value = item or None
                ws.cell(row=row_idx, column=2).value = quantity
                ws.cell(row=row_idx, column=3).value = unit
                ws.cell(row=row_idx, column=4).value = sheet_name
        save_wb(wb)
        return redirect(url_for('inventory.index'))
    values = {field: ws.cell(row=row_idx, column=col).value or ''
              for col, field in enumerate(COLS, 1)}
    return render_template('edit.html', title=f'Edit: {values.get("Item", "")}',
                           values=values, locations=location_sheets, units=load_units())


@bp.route('/delete/<path:row_key>')
def delete(row_key):
    sheet_name, row_idx = row_key.rsplit(':', 1)
    row_idx = int(row_idx)
    wb = load_wb()
    ws = wb[sheet_name]
    for col in range(1, 9):
        ws.cell(row=row_idx, column=col).value = None
    save_wb(wb)
    return redirect(url_for('inventory.index'))


@bp.route('/items.json')
def items_json():
    from pantri import _pluralize_unit
    q   = request.args.get('q', '').lower()
    loc = request.args.get('loc', '')
    wb      = load_wb()
    all_raw = get_all_rows(wb)
    rows = []
    for s, r, d in all_raw:
        key = f'{s}:{r}'
        if q and q not in str(d.get('Item', '')).lower():
            continue
        if loc and str(d.get('Location', '')) != loc and not key.startswith(loc + ':'):
            continue
        rows.append({
            'key':      key,
            'item':     d.get('Item') or '',
            'qty':      d.get('Quantity', 0),
            'unit':     _pluralize_unit(d.get('Unit'), d.get('Quantity')) or '',
            'location': d.get('Location') or '',
            'edit_url': url_for('inventory.edit', row_key=key),
            'del_url':  url_for('inventory.delete', row_key=key),
        })
    return jsonify({'items': rows, 'total': len(rows)})


@bp.route('/item/adjust', methods=['POST'])
def adjust():
    row_key = request.form.get('row_key', '')
    try:
        delta = float(request.form.get('delta', '0'))
    except ValueError:
        return jsonify({'ok': False}), 400
    try:
        sheet_name, row_idx = row_key.rsplit(':', 1)
        row_idx = int(row_idx)
    except (ValueError, AttributeError):
        return jsonify({'ok': False}), 400
    wb = load_wb()
    if sheet_name not in wb.sheetnames:
        return jsonify({'ok': False}), 404
    ws = wb[sheet_name]
    try:
        current = float(str(ws.cell(row=row_idx, column=2).value or 0))
    except (ValueError, TypeError):
        current = 0
    new_qty = max(0, current + delta)
    new_qty = int(new_qty) if new_qty == int(new_qty) else new_qty
    ws.cell(row=row_idx, column=2).value = new_qty
    save_wb(wb)
    return jsonify({'ok': True, 'qty': new_qty})


@bp.route('/add/bulk', methods=['GET', 'POST'])
def bulk_add():
    location_sheets = get_location_sheets()
    results = []
    if request.method == 'POST':
        bulk_text        = request.form.get('bulk', '')
        default_location = request.form.get('default_location', location_sheets[0] if location_sheets else '')
        wb = load_wb()

        for line in bulk_text.splitlines():
            line = line.strip()
            if not line:
                continue
            parts = [p.strip() for p in line.split(',')]
            item     = to_title(parts[0]) if parts else ''
            quantity = parts[1] if len(parts) > 1 else None
            unit     = parts[2] if len(parts) > 2 else None
            location = parts[3] if len(parts) > 3 else default_location
            if location not in location_sheets:
                location = default_location

            if not item:
                continue

            ws = wb[location]
            unit_lower = (unit or '').lower()
            existing = next((r for r in range(2, ws.max_row + 1)
                             if str(ws.cell(row=r, column=1).value or '').lower() == item.lower()
                             and str(ws.cell(row=r, column=3).value or '').lower() == unit_lower), None)
            if existing:
                try:
                    cur = float(str(ws.cell(row=existing, column=2).value or 0))
                    add_qty = float(quantity) if quantity else 1
                    merged = cur + add_qty
                    ws.cell(row=existing, column=2).value = int(merged) if merged == int(merged) else merged
                    results.append(f'✅ Updated <strong>{item}</strong> (merged)')
                except (ValueError, TypeError):
                    results.append(f'⚠️ Could not merge quantities for <strong>{item}</strong>')
            else:
                row = next((r for r in range(2, ws.max_row + 2) if not ws.cell(row=r, column=1).value),
                           ws.max_row + 1)
                ws.cell(row=row, column=1).value = item
                ws.cell(row=row, column=2).value = quantity
                ws.cell(row=row, column=3).value = unit
                ws.cell(row=row, column=4).value = location
                results.append(f'✅ Added <strong>{item}</strong> → {location}')

        save_wb(wb)
        wb2     = load_wb()
        all_raw = get_all_rows(wb2)
        rows    = [(f'{s}:{r}', d) for s, r, d in all_raw]
        return render_template('inventory.html', items=rows, total=len(rows),
                               locations=location_sheets, q='', loc='',
                               tab='add', bulk_results=results, units=load_units())

    return redirect(url_for('inventory.index', tab='add'))
