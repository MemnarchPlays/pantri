#!/usr/bin/env python3
"""Generate a combined shopping list from selected recipes, grouped by store section."""

import json
import sys
from pathlib import Path
from collections import defaultdict
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, PageBreak
from pdf_utils import PURPLE, DARK_PURPLE, LIGHT_PURPLE, NEAR_BLACK, WHITE, BorderedCanvas

DATA_DIR   = Path(__file__).parent / 'data'
OUTPUT_DIR = Path(__file__).parent / 'output'

SECTION_ORDER = [
    'Produce', 'Meat/Seafood', 'Dairy/Eggs',
    'Bakery', 'Pantry/Dry Goods', 'Frozen', 'Beverages', 'Other'
]

SECTION_EMOJI = {
    'Produce':         '🥦',
    'Meat/Seafood':    '🥩',
    'Dairy/Eggs':      '🥛',
    'Bakery':          '🍞',
    'Pantry/Dry Goods':'🫙',
    'Frozen':          '❄️',
    'Beverages':       '🧃',
    'Other':           '🛒',
}


def list_recipes():
    paths = sorted(DATA_DIR.glob('*.json'))
    recipes = []
    for p in paths:
        try:
            with open(p, encoding='utf-8') as f:
                recipes.append((p, json.load(f)))
        except Exception:
            pass
    return recipes


def pick_recipes_interactive():
    recipes = list_recipes()
    if not recipes:
        print('No recipes found in data/. Add some recipes first.')
        return []

    print('\nAvailable recipes:')
    for i, (_, r) in enumerate(recipes, 1):
        print(f'  {i}. {r.get("name", "Untitled")}')

    print('\nEnter recipe numbers separated by commas (or "all" for everything):')
    raw = input('> ').strip()

    if raw.lower() == 'all':
        return [r for _, r in recipes]

    selected = []
    for part in raw.split(','):
        try:
            idx = int(part.strip()) - 1
            selected.append(recipes[idx][1])
        except (ValueError, IndexError):
            print(f'  Skipping invalid selection: {part.strip()}')
    return selected


def build_shopping_list(recipes):
    sections = defaultdict(list)
    for recipe in recipes:
        rname = recipe.get('name', 'Unknown')
        for ing in recipe.get('ingredients', []):
            if isinstance(ing, dict):
                section = ing.get('store_section', 'Other')
                amount  = ing.get('amount', '')
                item    = ing.get('item', '')
                entry   = f'{amount}  {item}  <i>(for {rname})</i>'
            else:
                section = 'Other'
                entry   = f'{ing}  <i>(for {rname})</i>'
            if section not in SECTION_ORDER:
                section = 'Other'
            sections[section].append(entry)
    return sections


def generate_shopping_pdf(recipes, output_name='shopping_list.pdf'):
    OUTPUT_DIR.mkdir(exist_ok=True)
    sections = build_shopping_list(recipes)
    out_path = OUTPUT_DIR / output_name

    title_style = ParagraphStyle('title', fontName='Helvetica-Bold', fontSize=26,
                                 textColor=PURPLE, alignment=TA_CENTER, spaceAfter=4)
    sub_style   = ParagraphStyle('sub', fontName='Helvetica', fontSize=11,
                                 textColor=NEAR_BLACK, alignment=TA_CENTER, spaceAfter=2)
    sect_style  = ParagraphStyle('sect', fontName='Helvetica-Bold', fontSize=13,
                                 textColor=WHITE, spaceAfter=0, spaceBefore=14)
    item_style  = ParagraphStyle('item', fontName='Helvetica', fontSize=10,
                                 textColor=NEAR_BLACK, spaceAfter=4, leftIndent=8)

    doc = SimpleDocTemplate(
        str(out_path), pagesize=letter,
        leftMargin=0.75*inch, rightMargin=0.75*inch,
        topMargin=0.75*inch,  bottomMargin=0.75*inch,
    )

    story = []
    story.append(Paragraph('Shopping List', title_style))
    names = ', '.join(r.get('name', '') for r in recipes)
    story.append(Paragraph(f'Recipes: {names}', sub_style))
    story.append(HRFlowable(width='100%', thickness=2, color=PURPLE, spaceAfter=12))

    from reportlab.platypus import Table, TableStyle
    for section in SECTION_ORDER:
        items = sections.get(section, [])
        if not items:
            continue

        label = f'  {section}'
        header_data = [[Paragraph(label, sect_style)]]
        header_table = Table(header_data, colWidths=[6*inch])
        header_table.setStyle(TableStyle([
            ('BACKGROUND',    (0, 0), (-1, -1), PURPLE),
            ('TOPPADDING',    (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING',   (0, 0), (-1, -1), 8),
        ]))
        story.append(header_table)
        story.append(Spacer(1, 4))

        for entry in items:
            story.append(Paragraph(f'☐  {entry}', item_style))

        story.append(Spacer(1, 6))

    doc.build(story, canvasmaker=BorderedCanvas)
    print(f'Shopping list saved: {out_path}')
    return str(out_path)


def print_shopping_text(recipes):
    sections = build_shopping_list(recipes)
    print('\n' + '='*50)
    print('SHOPPING LIST')
    print('='*50)
    for section in SECTION_ORDER:
        items = sections.get(section, [])
        if not items:
            continue
        print(f'\n--- {section} ---')
        for item in items:
            clean = item.replace('<i>', '').replace('</i>', '')
            print(f'  [ ]  {clean}')
    print()


if __name__ == '__main__':
    selected = pick_recipes_interactive()
    if not selected:
        sys.exit(0)

    print('\nOutput format:')
    print('  1. PDF')
    print('  2. Text (terminal)')
    print('  3. Both')
    choice = input('> ').strip()

    if choice in ('1', '3'):
        generate_shopping_pdf(selected)
    if choice in ('2', '3'):
        print_shopping_text(selected)
