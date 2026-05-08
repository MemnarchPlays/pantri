#!/usr/bin/env python3
"""Generate a printable recipe binder PDF from recipe JSON files in the data/ folder."""

import io
import json
import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.colors import HexColor
from datetime import datetime
from pdf_utils import PURPLE, DARK_PURPLE, LIGHT_PURPLE, NEAR_BLACK, WHITE, GRAY, BorderedCanvas, PDF_FONT, PDF_FONT_BOLD, PDF_FONT_ITALIC

DATA_DIR   = Path(__file__).parent / 'data'
OUTPUT_DIR = Path(__file__).parent / 'output'

STORE_ORDER = [
    'Produce', 'Meat/Seafood', 'Dairy/Eggs',
    'Bakery', 'Pantry/Dry Goods', 'Frozen', 'Beverages', 'Other'
]

MEAL_ORDER = ['Breakfast', 'Lunch', 'Dinner', 'Snacks', 'Desserts', 'Other']


def build_styles():
    base = getSampleStyleSheet()
    return {
        'cover_title': ParagraphStyle('cover_title', fontName=PDF_FONT_BOLD,
                                      fontSize=36, textColor=PURPLE, alignment=TA_CENTER,
                                      spaceAfter=8),
        'cover_sub':   ParagraphStyle('cover_sub', fontName=PDF_FONT,
                                      fontSize=14, textColor=NEAR_BLACK, alignment=TA_CENTER,
                                      spaceAfter=4),
        'toc_header':  ParagraphStyle('toc_header', fontName=PDF_FONT_BOLD,
                                      fontSize=18, textColor=PURPLE, spaceAfter=12),
        'toc_meal':    ParagraphStyle('toc_meal', fontName=PDF_FONT_BOLD,
                                      fontSize=12, textColor=DARK_PURPLE, spaceBefore=10, spaceAfter=4),
        'toc_item':    ParagraphStyle('toc_item', fontName=PDF_FONT,
                                      fontSize=10, textColor=NEAR_BLACK, leftIndent=16, spaceAfter=2),
        'recipe_name': ParagraphStyle('recipe_name', fontName=PDF_FONT_BOLD,
                                      fontSize=22, textColor=WHITE, alignment=TA_LEFT,
                                      spaceAfter=0),
        'section_hdr': ParagraphStyle('section_hdr', fontName=PDF_FONT_BOLD,
                                      fontSize=11, textColor=DARK_PURPLE, spaceBefore=10, spaceAfter=4),
        'body':        ParagraphStyle('body', fontName=PDF_FONT,
                                      fontSize=10, textColor=NEAR_BLACK, spaceAfter=3),
        'step':        ParagraphStyle('step', fontName=PDF_FONT,
                                      fontSize=10, textColor=NEAR_BLACK, spaceAfter=5,
                                      leftIndent=8, firstLineIndent=-8),
        'note':        ParagraphStyle('note', fontName=PDF_FONT_ITALIC,
                                      fontSize=9, textColor=HexColor('#555555'), spaceAfter=3),
    }


def cover_page(styles):
    now = datetime.now().strftime('%B %Y')
    return [
        Spacer(1, 2.2 * inch),
        Paragraph('Pantri', styles['cover_title']),
        Spacer(1, 0.2 * inch),
        HRFlowable(width='60%', thickness=2, color=PURPLE, spaceAfter=10),
        Paragraph('Personal Collection', styles['cover_sub']),
        Spacer(1, 0.3 * inch),
        Paragraph(now, styles['cover_sub']),
        PageBreak(),
    ]


def toc_page(recipes_by_meal, styles):
    items = [Paragraph('Table of Contents', styles['toc_header']),
             HRFlowable(width='100%', thickness=1, color=LIGHT_PURPLE, spaceAfter=8)]
    for meal in MEAL_ORDER:
        group = sorted(recipes_by_meal.get(meal, []), key=lambda r: r.get('name', '').lower())
        if not group:
            continue
        items.append(Paragraph(meal, styles['toc_meal']))
        for r in group:
            items.append(Paragraph(f'• {r["name"]}', styles['toc_item']))
    items.append(PageBreak())
    return items


def macro_table(recipe, styles):
    m = recipe.get('macros_per_serving', {})
    data = [
        ['Calories', 'Protein', 'Carbs', 'Fat'],
        [
            str(m.get('calories', '—')),
            f'{m.get("protein_g", "—")}g',
            f'{m.get("carbs_g", "—")}g',
            f'{m.get("fat_g", "—")}g',
        ]
    ]
    t = Table(data, colWidths=[1.5*inch]*4)
    t.setStyle(TableStyle([
        ('BACKGROUND',   (0, 0), (-1, 0), PURPLE),
        ('TEXTCOLOR',    (0, 0), (-1, 0), WHITE),
        ('FONTNAME',     (0, 0), (-1, 0), PDF_FONT_BOLD),
        ('FONTSIZE',     (0, 0), (-1, 0), 10),
        ('BACKGROUND',   (0, 1), (-1, 1), LIGHT_PURPLE),
        ('TEXTCOLOR',    (0, 1), (-1, 1), NEAR_BLACK),
        ('FONTNAME',     (0, 1), (-1, 1), PDF_FONT_BOLD),
        ('FONTSIZE',     (0, 1), (-1, 1), 11),
        ('ALIGN',        (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN',       (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [PURPLE, LIGHT_PURPLE]),
        ('GRID',         (0, 0), (-1, -1), 0.5, DARK_PURPLE),
        ('TOPPADDING',   (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 6),
        ('ROUNDEDCORNERS', [4]),
    ]))
    return t


def recipe_header_table(recipe):
    servings  = recipe.get('servings', '?')
    prep      = recipe.get('prep_time', '?')
    cook      = recipe.get('cook_time', '')
    cook_cell = f'Cook: {cook}' if cook else ''
    data = [[
        f'Servings: {servings}',
        f'Prep: {prep}',
        cook_cell,
        recipe.get('meal_type', ''),
    ]]
    t = Table(data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), GRAY),
        ('TEXTCOLOR',     (0, 0), (-1, -1), DARK_PURPLE),
        ('FONTNAME',      (0, 0), (-1, -1), PDF_FONT_BOLD),
        ('FONTSIZE',      (0, 0), (-1, -1), 9),
        ('ALIGN',         (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX',           (0, 0), (-1, -1), 1, PURPLE),
        ('INNERGRID',     (0, 0), (-1, -1), 0.5, LIGHT_PURPLE),
        ('TOPPADDING',    (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    return t


def recipe_name_banner(name):
    data = [[Paragraph(name, ParagraphStyle(
        'rn', fontName=PDF_FONT_BOLD, fontSize=20, textColor=WHITE))]]
    t = Table(data, colWidths=[6*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), PURPLE),
        ('LEFTPADDING',   (0, 0), (-1, -1), 12),
        ('TOPPADDING',    (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('ROUNDEDCORNERS', [4]),
    ]))
    return t


def recipe_page(recipe, styles):
    items = []
    items.append(recipe_name_banner(recipe.get('name', 'Untitled')))
    items.append(Spacer(1, 6))
    items.append(recipe_header_table(recipe))
    items.append(Spacer(1, 10))

    items.append(Paragraph('Nutrition Per Serving', styles['section_hdr']))
    items.append(macro_table(recipe, styles))
    items.append(Spacer(1, 10))

    ingredients = recipe.get('ingredients', [])
    if ingredients:
        items.append(HRFlowable(width='100%', thickness=0.5, color=LIGHT_PURPLE, spaceAfter=4))
        items.append(Paragraph('Ingredients', styles['section_hdr']))
        for ing in ingredients:
            if isinstance(ing, dict):
                line = f'<b>{ing.get("amount", "")}</b>  {ing.get("item", "")}'
            else:
                line = str(ing)
            items.append(Paragraph(f'• {line}', styles['body']))

    instructions = recipe.get('instructions', [])
    if instructions:
        items.append(Spacer(1, 8))
        items.append(HRFlowable(width='100%', thickness=0.5, color=LIGHT_PURPLE, spaceAfter=4))
        items.append(Paragraph('Instructions', styles['section_hdr']))
        for i, step in enumerate(instructions, 1):
            items.append(Paragraph(f'{i}.  {step}', styles['step']))

    subs = recipe.get('substitutions', {})
    if subs:
        items.append(Spacer(1, 8))
        items.append(HRFlowable(width='100%', thickness=0.5, color=LIGHT_PURPLE, spaceAfter=4))
        items.append(Paragraph('Substitutions', styles['section_hdr']))
        labels = {
            'dairy_free':  'Dairy-Free',
            'gluten_free': 'Gluten-Free',
            'low_carb':    'Low-Carb',
            'vegetarian':  'Vegetarian',
            'vegan':       'Vegan',
        }
        for key, label in labels.items():
            val = subs.get(key, '').strip()
            if val:
                items.append(Paragraph(f'<b>{label}:</b>  {val}', styles['body']))

    notes = recipe.get('notes', '').strip()
    if notes:
        items.append(Spacer(1, 6))
        items.append(Paragraph(f'<i>Note: {notes}</i>', styles['note']))

    items.append(PageBreak())
    return items


def load_recipes(specific_files=None):
    if specific_files:
        paths = [Path(f) for f in specific_files]
    else:
        paths = sorted(DATA_DIR.glob('*.json'))
    recipes = []
    for p in paths:
        try:
            with open(p, encoding='utf-8') as f:
                recipes.append(json.load(f))
        except Exception as e:
            print(f'  Warning: could not load {p.name}: {e}')
    return recipes


def group_by_meal(recipes):
    groups = {m: [] for m in MEAL_ORDER}
    for r in recipes:
        meal = r.get('meal_type', 'Other')
        if meal not in groups:
            meal = 'Other'
        groups[meal].append(r)
    return groups


def generate_binder(specific_files=None, output_name='recipe_binder.pdf'):
    OUTPUT_DIR.mkdir(exist_ok=True)
    recipes = load_recipes(specific_files)
    if not recipes:
        print('No recipes found. Add .json files to the data/ folder first.')
        return

    out_path = OUTPUT_DIR / output_name
    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=letter,
        leftMargin=0.75*inch, rightMargin=0.75*inch,
        topMargin=0.75*inch,  bottomMargin=0.75*inch,
    )

    styles = build_styles()
    groups = group_by_meal(recipes)
    story  = []

    story += cover_page(styles)
    story += toc_page(groups, styles)

    for meal in MEAL_ORDER:
        for recipe in sorted(groups.get(meal, []), key=lambda r: r.get('name', '').lower()):
            story += recipe_page(recipe, styles)

    doc.build(story, canvasmaker=BorderedCanvas)
    print(f'PDF saved: {out_path}')
    return str(out_path)


def generate_binder_bytes():
    """Generate the full recipe binder PDF in memory and return bytes."""
    recipes = load_recipes()
    if not recipes:
        return None

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=letter,
        leftMargin=0.75*inch, rightMargin=0.75*inch,
        topMargin=0.75*inch,  bottomMargin=0.75*inch,
    )

    styles = build_styles()
    groups = group_by_meal(recipes)
    story  = []
    story += cover_page(styles)
    story += toc_page(groups, styles)

    for meal in MEAL_ORDER:
        for recipe in sorted(groups.get(meal, []), key=lambda r: r.get('name', '').lower()):
            story += recipe_page(recipe, styles)

    doc.build(story, canvasmaker=BorderedCanvas)
    buf.seek(0)
    return buf.read()


if __name__ == '__main__':
    files = sys.argv[1:] if len(sys.argv) > 1 else None
    generate_binder(files)
