#!/usr/bin/env python3
"""Shared constants and helpers used across pantry scripts."""

import json
import os
import re
from pathlib import Path

_BASE    = Path(__file__).parent
_DATA    = Path(os.environ['PANTRI_DATA']) if 'PANTRI_DATA' in os.environ else _BASE

COLS     = ['Item', 'Quantity', 'Unit', 'Location']
XLSX     = _DATA / 'Food in Storage.xlsx'
DATA_DIR = _DATA / 'data'
ENV_FILE = _BASE / '.env'

EXCLUDE_SHEETS = {'Minimums'}
MEAL_TYPES     = ['Breakfast', 'Lunch', 'Dinner', 'Snacks', 'Desserts']


def to_title(s):
    return re.sub(r"(?<!')\b\w", lambda m: m.group().upper(), s.lower())


def read_env():
    env = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                k, _, v = line.partition('=')
                env[k.strip()] = v.strip()
    return env


def load_all_recipes():
    """Load all recipe JSON files from DATA_DIR. Returns a list of recipe dicts."""
    recipes = []
    for path in sorted(DATA_DIR.glob('*.json')):
        try:
            recipes.append(json.loads(path.read_text(encoding='utf-8')))
        except Exception:
            continue
    return recipes
