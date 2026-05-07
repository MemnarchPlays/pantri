"""Settings blueprint — all settings, locations, exclusions, units, backups, discord, appearance."""

import json
import re
import zipfile
import shutil
from pathlib import Path
from flask import Blueprint, request, redirect, url_for, render_template, jsonify, send_file
from pantry_utils import XLSX, DATA_DIR, COLS, EXCLUDE_SHEETS, to_title, read_env
from pantri.db import load_wb, get_location_sheets, get_location_info, get_minimums, set_minimum, delete_minimum
from pantri.state import load_exclusions, save_exclusions, load_units, save_units, get_unit_info
from pantri.backup import backup_wb, get_backups, get_backup_info, _do_backup, BACKUP_DIR
from pantri.bot import bot_running, start_bot, stop_bot, BOT_LOG_FILE
from pantri import write_env

bp = Blueprint('settings', __name__)


# ── Redirect shims ──────────────────────────────────────────────────────────

@bp.route('/can-make')
def can_make():
    return redirect(url_for('recipes.recipes', tab='canmake'))


@bp.route('/minimums')
def minimums():
    return redirect(url_for('settings.settings', tab='minimums'))


@bp.route('/restock')
def restock():
    return redirect(url_for('shopping.shopping'))


# ── Main settings page ──────────────────────────────────────────────────────

@bp.route('/settings')
def settings():
    env = read_env()
    token             = env.get('DISCORD_TOKEN', '')
    alert_channel     = env.get('DISCORD_ALERT_CHANNEL', '')
    backup_mode       = env.get('BACKUP_MODE', 'actions')
    backup_every_n    = int(env.get('BACKUP_EVERY_N', '10'))
    backup_interval   = float(env.get('BACKUP_INTERVAL_HRS', '24'))
    backup_max        = int(env.get('BACKUP_MAX', '10'))
    app_port          = int(env.get('PORT', '5000'))
    backup_last_label, backup_count = get_backup_info()
    active_tab        = request.args.get('tab', 'locations')
    return render_template('settings.html', token_set=bool(token),
                           alert_channel=alert_channel,
                           minimums=get_minimums(),
                           locations=get_location_info(),
                           backups=get_backups(),
                           backup_mode=backup_mode,
                           backup_every_n=backup_every_n,
                           backup_interval=backup_interval,
                           backup_max=backup_max,
                           backup_last_label=backup_last_label,
                           backup_count=backup_count,
                           exclusions=load_exclusions(),
                           units=get_unit_info(),
                           app_port=app_port,
                           active_tab=active_tab)


# ── Locations ───────────────────────────────────────────────────────────────

@bp.route('/locations/add', methods=['POST'])
def locations_add():
    name = to_title(request.form.get('name', '').strip())
    if name and name not in EXCLUDE_SHEETS:
        existing = get_location_sheets()
        if name not in existing:
            wb = load_wb()
            ws = wb.create_sheet(name)
            for col, header in enumerate(COLS, 1):
                ws.cell(row=1, column=col).value = header
            wb.save(XLSX)
    return redirect(url_for('settings.settings', tab='locations'))


@bp.route('/locations/delete/<name>')
def locations_delete(name):
    if name in EXCLUDE_SHEETS:
        return redirect(url_for('settings.settings', tab='locations'))
    wb = load_wb()
    if name in wb.sheetnames:
        ws = wb[name]
        count = sum(1 for r in range(2, ws.max_row + 1) if ws.cell(r, 1).value)
        if count == 0:
            del wb[name]
            wb.save(XLSX)
    return redirect(url_for('settings.settings', tab='locations'))


@bp.route('/locations/reorder', methods=['POST'])
def locations_reorder():
    data = request.get_json(silent=True) or {}
    new_order = data.get('order', [])
    wb = load_wb()
    valid = [s for s in wb.sheetnames if s not in EXCLUDE_SHEETS]
    new_order = [n for n in new_order if n in valid]
    excluded = [s for s in wb.sheetnames if s in EXCLUDE_SHEETS]
    full_order = new_order + excluded
    for target_idx, name in enumerate(full_order):
        cur_idx = wb.sheetnames.index(name)
        if cur_idx != target_idx:
            wb.move_sheet(name, offset=target_idx - cur_idx)
    wb.save(XLSX)
    return ('', 204)


# ── Exclusions ──────────────────────────────────────────────────────────────

@bp.route('/exclusions/add', methods=['POST'])
def exclusions_add():
    name      = to_title(request.form.get('name', '').strip())
    container = request.form.get('container', '').strip()
    if not name:
        return redirect(url_for('settings.settings', tab='exclusions'))
    items = load_exclusions()
    if not any(ex.get('name', '').lower() == name.lower() for ex in items):
        items.append({'name': name, 'container': container, 'in_stock': True})
        save_exclusions(items)
    return redirect(url_for('settings.settings', tab='exclusions'))


@bp.route('/exclusions/delete/<path:name>')
def exclusions_delete(name):
    items = [ex for ex in load_exclusions() if ex.get('name', '').lower() != name.lower()]
    save_exclusions(items)
    return redirect(url_for('settings.settings', tab='exclusions'))


@bp.route('/exclusions/toggle/<path:name>', methods=['POST'])
def exclusions_toggle(name):
    items = load_exclusions()
    for ex in items:
        if ex.get('name', '').lower() == name.lower():
            ex['in_stock'] = not ex.get('in_stock', True)
            break
    save_exclusions(items)
    referer = request.referrer or url_for('settings.settings', tab='exclusions')
    return redirect(referer)


# ── Units ────────────────────────────────────────────────────────────────────

@bp.route('/units/add', methods=['POST'])
def units_add():
    unit = request.form.get('unit', '').strip()
    if unit:
        units = load_units()
        if unit.lower() not in [u.lower() for u in units]:
            units.append(unit)
            save_units(units)
    return redirect(url_for('settings.settings', tab='units'))


@bp.route('/units/delete/<unit>')
def units_delete(unit):
    _, count = next(((u, c) for u, c in get_unit_info() if u.lower() == unit.lower()), (None, 0))
    if count == 0:
        units = [u for u in load_units() if u.lower() != unit.lower()]
        save_units(units)
    return redirect(url_for('settings.settings', tab='units'))


@bp.route('/units/reorder', methods=['POST'])
def units_reorder():
    data = request.get_json(silent=True) or {}
    new_order = data.get('order', [])
    current = load_units()
    current_lower = [u.lower() for u in current]
    ordered = [u for u in new_order if u.lower() in current_lower]
    rest = [u for u in current if u.lower() not in [x.lower() for x in ordered]]
    save_units(ordered + rest)
    return ('', 204)


# ── Minimums ─────────────────────────────────────────────────────────────────

@bp.route('/minimums/set', methods=['POST'])
def minimums_set():
    item = to_title((request.form.get('item', '') or '').strip())
    qty_raw = request.form.get('qty', '0')
    try:
        qty = float(qty_raw)
        qty = int(qty) if qty == int(qty) else qty
    except ValueError:
        qty = 0
    if item and qty > 0:
        set_minimum(item, qty)
    return redirect(url_for('settings.settings', tab='minimums'))


@bp.route('/minimums/delete/<item>')
def minimums_delete(item):
    delete_minimum(item)
    return redirect(url_for('settings.settings', tab='minimums'))


# ── Discord bot ───────────────────────────────────────────────────────────────

@bp.route('/settings/discord', methods=['POST'])
def settings_discord():
    action = request.form.get('action', 'save')
    token  = request.form.get('token', '').strip()

    alert_channel = request.form.get('alert_channel', '').strip()
    env = read_env()

    if token:
        env['DISCORD_TOKEN'] = token

    env['DISCORD_ALERT_CHANNEL'] = alert_channel
    write_env(env)

    if action == 'stop':
        stop_bot()
    elif action in ('save_restart', 'restart'):
        start_bot()
    elif action == 'remove':
        stop_bot()
        env.pop('DISCORD_TOKEN', None)
        write_env(env)

    return redirect(url_for('settings.settings', tab='discord'))


@bp.route('/settings/bot-status')
def settings_bot_status():
    return jsonify({'running': bot_running()})


@bp.route('/settings/bot-test', methods=['POST'])
def settings_bot_test():
    import requests as req
    token = request.form.get('token', '').strip()
    if not token:
        return jsonify({'ok': False, 'msg': 'No token provided.'})
    try:
        r = req.get('https://discord.com/api/v10/users/@me',
                    headers={'Authorization': f'Bot {token}'}, timeout=8)
        if r.status_code == 200:
            name = r.json().get('username', '?')
            return jsonify({'ok': True, 'msg': f'✅ Token valid — bot is "{name}"'})
        elif r.status_code == 401:
            return jsonify({'ok': False, 'msg': '❌ Invalid token — Discord rejected it (401). Reset the token in the developer portal and try again.'})
        else:
            return jsonify({'ok': False, 'msg': f'❌ Discord returned {r.status_code}.'})
    except Exception as e:
        return jsonify({'ok': False, 'msg': f'❌ Could not reach Discord: {e}'})


@bp.route('/settings/bot-log')
def settings_bot_log():
    if not BOT_LOG_FILE.exists():
        return jsonify({'log': ''})
    text  = BOT_LOG_FILE.read_text(encoding='utf-8', errors='replace')
    # Only show the most recent session (after the last separator line)
    marker = '--- Bot started'
    idx = text.rfind(marker)
    session = text[idx:] if idx != -1 else text
    return jsonify({'log': session.strip()})


# ── Appearance ────────────────────────────────────────────────────────────────

@bp.route('/settings/appearance', methods=['POST'])
def settings_appearance():
    env = read_env()
    color = request.form.get('accent_color', '#6B2D8B').strip()
    if re.match(r'^#[0-9A-Fa-f]{6}$', color):
        env['ACCENT_COLOR'] = color
    try:
        port = int(request.form.get('port', '5000'))
        if 1024 <= port <= 65535:
            env['PORT'] = str(port)
    except ValueError:
        pass
    write_env(env)
    return redirect(url_for('settings.settings', tab='appearance'))


# ── Backups ───────────────────────────────────────────────────────────────────

@bp.route('/settings/backups', methods=['POST'])
def settings_backups():
    env  = read_env()
    mode = request.form.get('backup_mode', 'actions')
    if mode not in ('actions', 'interval', 'manual'):
        mode = 'actions'
    try:
        every_n = max(1, min(500, int(request.form.get('backup_every_n', '10'))))
    except ValueError:
        every_n = 10
    try:
        interval_hrs = max(0.25, float(request.form.get('backup_interval_hrs', '24')))
    except ValueError:
        interval_hrs = 24
    try:
        max_backups = max(1, min(50, int(request.form.get('max_backups', '10'))))
    except ValueError:
        max_backups = 10
    env['BACKUP_MODE']         = mode
    env['BACKUP_EVERY_N']      = str(every_n)
    env['BACKUP_INTERVAL_HRS'] = str(interval_hrs)
    env['BACKUP_MAX']          = str(max_backups)
    write_env(env)
    return redirect(url_for('settings.settings', tab='backups'))


@bp.route('/backups/now', methods=['POST'])
def backups_now():
    backup_wb(force=True)
    return redirect(url_for('settings.settings', tab='backups'))


@bp.route('/backups/download/<filename>')
def backups_download(filename):
    path = BACKUP_DIR / Path(filename).name
    if path.exists() and path.parent.resolve() == BACKUP_DIR.resolve():
        return send_file(path, as_attachment=True)
    return redirect(url_for('settings.settings', tab='backups'))


@bp.route('/backups/restore/<filename>', methods=['POST'])
def backups_restore(filename):
    from pantri.state import UNITS_FILE, EXCLUSIONS_FILE
    path = BACKUP_DIR / Path(filename).name
    if path.exists() and path.parent.resolve() == BACKUP_DIR.resolve():
        backup_wb(force=True)
        if path.suffix.lower() == '.zip':
            with zipfile.ZipFile(path, 'r') as zf:
                names = zf.namelist()
                if XLSX.name in names:
                    zf.extract(XLSX.name, XLSX.parent)
                if UNITS_FILE.name in names:
                    zf.extract(UNITS_FILE.name, UNITS_FILE.parent)
                if EXCLUSIONS_FILE.name in names:
                    zf.extract(EXCLUSIONS_FILE.name, EXCLUSIONS_FILE.parent)
                DATA_DIR.mkdir(exist_ok=True)
                for name in names:
                    if name.startswith('data/') and name.endswith('.json'):
                        zf.extract(name, Path(__file__).parent.parent.parent)
        else:
            shutil.copy2(path, XLSX)
    return redirect(url_for('settings.settings', tab='backups'))


@bp.route('/backups/upload', methods=['POST'])
def backups_upload():
    from datetime import datetime
    f = request.files.get('backup_file')
    if not f:
        return redirect(url_for('settings.settings', tab='backups'))
    fname = f.filename.lower()
    if not (fname.endswith('.zip') or fname.endswith('.xlsx')):
        return redirect(url_for('settings.settings', tab='backups'))
    BACKUP_DIR.mkdir(exist_ok=True)
    ts   = datetime.now().strftime('%Y%m%d_%H%M%S')
    ext  = '.zip' if fname.endswith('.zip') else '.xlsx'
    dest = BACKUP_DIR / f'pantry_backup_upload_{ts}{ext}'
    f.save(str(dest))
    env = read_env()
    max_backups = max(1, int(env.get('BACKUP_MAX', '10')))
    all_files = sorted(
        list(BACKUP_DIR.glob('*.zip')) + list(BACKUP_DIR.glob('*.xlsx')),
        key=lambda p: p.stat().st_mtime
    )
    for old in all_files[:-max_backups]:
        old.unlink(missing_ok=True)
    return redirect(url_for('settings.settings', tab='backups'))
