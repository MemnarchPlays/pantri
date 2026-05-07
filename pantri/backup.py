"""Backup logic — load/save backup_state, _do_backup, backup_wb, get_backups, get_backup_info."""

import json
import zipfile
import shutil
from datetime import datetime
from pathlib import Path
from pantry_utils import XLSX, DATA_DIR, read_env

STATE_DIR         = Path(__file__).parent.parent / 'state'
BACKUP_STATE_FILE = STATE_DIR / 'backup_state.json'
BACKUP_DIR        = Path(__file__).parent.parent / 'backups'

# These mirror state.py paths — used in zip backup
UNITS_FILE      = STATE_DIR / 'units.json'
EXCLUSIONS_FILE = STATE_DIR / 'exclusions.json'


def load_backup_state():
    try:
        return json.loads(BACKUP_STATE_FILE.read_text(encoding='utf-8')) if BACKUP_STATE_FILE.exists() else {}
    except Exception:
        return {}


def save_backup_state(state):
    BACKUP_STATE_FILE.write_text(json.dumps(state), encoding='utf-8')


def _do_backup(env):
    """Write a timestamped zip and trim to max. Does not touch state."""
    BACKUP_DIR.mkdir(exist_ok=True)
    ts   = datetime.now().strftime('%Y%m%d_%H%M%S')
    dest = BACKUP_DIR / f'pantry_backup_{ts}.zip'
    with zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED) as zf:
        if XLSX.exists():
            zf.write(XLSX, XLSX.name)
        if UNITS_FILE.exists():
            zf.write(UNITS_FILE, UNITS_FILE.name)
        if EXCLUSIONS_FILE.exists():
            zf.write(EXCLUSIONS_FILE, EXCLUSIONS_FILE.name)
        if DATA_DIR.exists():
            for jf in DATA_DIR.glob('*.json'):
                zf.write(jf, f'data/{jf.name}')
    max_backups = max(1, int(env.get('BACKUP_MAX', '10')))
    all_files = sorted(
        list(BACKUP_DIR.glob('*.zip')) + list(BACKUP_DIR.glob('*.xlsx')),
        key=lambda p: p.stat().st_mtime
    )
    for old in all_files[:-max_backups]:
        old.unlink(missing_ok=True)


def backup_wb(force=False):
    """Conditionally back up based on configured mode. force=True always writes."""
    if not XLSX.exists():
        return
    env   = read_env()
    mode  = env.get('BACKUP_MODE', 'actions')
    state = load_backup_state()
    state['action_count'] = state.get('action_count', 0) + 1

    do_backup = force
    if not do_backup:
        if mode == 'actions':
            n = max(1, int(env.get('BACKUP_EVERY_N', '10')))
            do_backup = state['action_count'] >= n
        elif mode == 'interval':
            hrs      = max(0.01, float(env.get('BACKUP_INTERVAL_HRS', '24')))
            last_ts  = state.get('last_backup_ts', 0)
            do_backup = (datetime.now().timestamp() - last_ts) >= (hrs * 3600)

    if do_backup:
        _do_backup(env)
        state['action_count']   = 0
        state['last_backup_ts'] = datetime.now().timestamp()

    save_backup_state(state)


def get_backups():
    if not BACKUP_DIR.exists():
        return []
    files = list(BACKUP_DIR.glob('*.zip')) + list(BACKUP_DIR.glob('*.xlsx'))
    result = []
    for p in sorted(files, key=lambda p: p.stat().st_mtime, reverse=True):
        stat = p.stat()
        kb   = stat.st_size / 1024
        result.append({
            'name':     p.name,
            'size':     f'{kb:.0f} KB' if kb >= 1 else f'{stat.st_size} B',
            'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%b %d %Y, %I:%M %p'),
        })
    return result


def get_backup_info():
    """Return (last_label, action_count) for the settings UI."""
    state = load_backup_state()
    count = state.get('action_count', 0)
    last  = state.get('last_backup_ts', 0)
    if last:
        ago_s = datetime.now().timestamp() - last
        ago_h = ago_s / 3600
        if ago_h < 1:
            last_str = f'{int(ago_s / 60)} min ago'
        elif ago_h < 24:
            last_str = f'{ago_h:.1f} hrs ago'
        else:
            last_str = f'{ago_h / 24:.1f} days ago'
        last_label = f'Last backup: {last_str}'
    else:
        last_label = 'No backup taken yet'
    return last_label, count
