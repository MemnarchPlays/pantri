"""Pantri app factory."""

import colorsys
from flask import Flask
from pantry_utils import read_env, ENV_FILE


def compute_theme(hex_color):
    try:
        h = hex_color.lstrip('#')
        r, g, b = int(h[0:2], 16)/255, int(h[2:4], 16)/255, int(h[4:6], 16)/255
    except Exception:
        r, g, b = 0.42, 0.18, 0.55
    hue, lum, sat = colorsys.rgb_to_hls(r, g, b)
    def to_hex(r, g, b):
        return '#{:02X}{:02X}{:02X}'.format(int(r*255), int(g*255), int(b*255))
    dark  = colorsys.hls_to_rgb(hue, max(0, lum * 0.70), sat)
    light = colorsys.hls_to_rgb(hue, min(1, lum + (1 - lum) * 0.75), sat * 0.4)
    return hex_color, to_hex(*dark), to_hex(*light)


def write_env(env: dict):
    lines = [f'{k}={v}' for k, v in env.items()]
    ENV_FILE.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def _pluralize_unit(unit, qty):
    try:
        n = float(qty)
    except (TypeError, ValueError):
        return unit
    if not unit or n == 1:
        return unit
    irregulars = {'loaf': 'loaves', 'bunch': 'bunches', 'box': 'boxes'}
    low = unit.lower()
    if low in irregulars:
        return irregulars[low]
    if low.startswith('can '):
        return 'cans ' + unit[4:]
    if low in ('count', 'lb', 'lbs'):
        return unit
    return unit + 's'


def create_app():
    app = Flask(__name__, template_folder='../templates')

    @app.context_processor
    def inject_theme():
        color = read_env().get('ACCENT_COLOR', '#6B2D8B')
        main, dark, light = compute_theme(color)
        css = f':root {{ --purple: {main}; --dark-purple: {dark}; --light-purple: {light}; }}'
        return {'theme_css': css, 'accent_color': color}

    app.jinja_env.filters['pluralize_unit'] = _pluralize_unit

    from pantri.routes.inventory import bp as inventory_bp
    from pantri.routes.recipes   import bp as recipes_bp
    from pantri.routes.shopping  import bp as shopping_bp
    from pantri.routes.settings  import bp as settings_bp

    app.register_blueprint(inventory_bp)
    app.register_blueprint(recipes_bp)
    app.register_blueprint(shopping_bp)
    app.register_blueprint(settings_bp)

    return app
