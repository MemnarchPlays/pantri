#!/usr/bin/env python3
"""Shared PDF styling — colors and BorderedCanvas — used by generate_pdf and shopping_list."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas as pdfcanvas

PURPLE       = HexColor('#6B2D8B')
DARK_PURPLE  = HexColor('#4A1E6B')
LIGHT_PURPLE = HexColor('#E8D5F0')
NEAR_BLACK   = HexColor('#1A1A1A')
WHITE        = HexColor('#FFFFFF')
GRAY         = HexColor('#F7F4FA')


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
