#!/usr/bin/env python3
"""Shared PDF styling — colors, fonts, and BorderedCanvas — used by generate_pdf and shopping_list."""

import colorsys
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas as pdfcanvas
from pantry_utils import read_env

_FONT_VARIANTS = {
    'Helvetica':   ('Helvetica',   'Helvetica-Bold',   'Helvetica-Oblique'),
    'Times-Roman': ('Times-Roman', 'Times-Bold',        'Times-Italic'),
    'Courier':     ('Courier',     'Courier-Bold',       'Courier-Oblique'),
}

def _compute_theme(hex_color):
    try:
        h = hex_color.lstrip('#')
        r, g, b = int(h[0:2],16)/255, int(h[2:4],16)/255, int(h[4:6],16)/255
    except Exception:
        r, g, b = 0.42, 0.18, 0.55
    hue, lum, sat = colorsys.rgb_to_hls(r, g, b)
    def to_hex(r, g, b):
        return '#{:02X}{:02X}{:02X}'.format(int(r*255), int(g*255), int(b*255))
    dark  = colorsys.hls_to_rgb(hue, max(0, lum * 0.70), sat)
    light = colorsys.hls_to_rgb(hue, min(1, lum + (1-lum)*0.75), sat*0.4)
    return hex_color, to_hex(*dark), to_hex(*light)

_env   = read_env()
_main, _dark, _light = _compute_theme(_env.get('PDF_ACCENT_COLOR', '#6B2D8B'))

PURPLE       = HexColor(_main)
DARK_PURPLE  = HexColor(_dark)
LIGHT_PURPLE = HexColor(_light)
NEAR_BLACK   = HexColor('#1A1A1A')
WHITE        = HexColor('#FFFFFF')
GRAY         = HexColor('#F7F4FA')

_base           = _FONT_VARIANTS.get(_env.get('PDF_FONT', 'Helvetica'), _FONT_VARIANTS['Helvetica'])
PDF_FONT        = _base[0]
PDF_FONT_BOLD   = _base[1]
PDF_FONT_ITALIC = _base[2]


class BorderedCanvas(pdfcanvas.Canvas):
    def __init__(self, *args, **kwargs):
        pdfcanvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self._draw_border()
            pdfcanvas.Canvas.showPage(self)
        pdfcanvas.Canvas.save(self)

    def _draw_border(self):
        w, h = letter
        outer = 0.35 * inch
        inner = 0.48 * inch

        self.setStrokeColor(PURPLE)
        self.setLineWidth(3)
        self.rect(outer, outer, w - 2*outer, h - 2*outer, stroke=1, fill=0)

        self.setStrokeColor(LIGHT_PURPLE)
        self.setLineWidth(0.75)
        self.rect(inner, inner, w - 2*inner, h - 2*inner, stroke=1, fill=0)

        corner = 0.18 * inch
        self.setStrokeColor(DARK_PURPLE)
        self.setLineWidth(1.5)
        for x, y in [(outer, outer), (w-outer, outer), (outer, h-outer), (w-outer, h-outer)]:
            dx = corner if x == outer else -corner
            dy = corner if y == outer else -corner
            self.line(x, y, x + dx, y)
            self.line(x, y, x, y + dy)
