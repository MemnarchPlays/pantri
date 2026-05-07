---
name: Mobile-Optimized Layout
description: Fix broken mobile navbar and improve small-screen usability across all pages
flow: mobile-layout.flow.md
---

## What It Does

Fixes the navbar so it collapses to a hamburger menu on small screens (the current `navbar-expand-lg` has no toggler button, so nav links vanish on phones). Ensures tables, cards, and forms are usable at phone-width without horizontal overflow or tiny tap targets.

## Success Criteria

1. On viewports < 768px wide, a hamburger toggle button is visible in the navbar.
2. Tapping the hamburger expands/collapses the nav links vertically (Bootstrap collapse behavior).
3. No page produces horizontal scrolling of the `<body>` on a 375px-wide viewport.
4. All tables are wrapped in `table-responsive` so they scroll horizontally within their container rather than overflowing the page.
5. All action buttons (add, edit, delete, submit) have a minimum height of 44px on mobile.
6. All `<input>` and `<select>` form elements use `font-size` ≥ 16px to prevent iOS auto-zoom on focus.
7. On the Shopping page, the two-column `col-md-6` layout stacks to single column on screens < 768px (Bootstrap default `col-12` behavior — verify no overrides break this).
8. On the Recipes page, recipe cards stack vertically and are full-width on mobile.
9. The navbar Bootstrap JS bundle is loaded so collapse toggle works (currently only CSS is loaded).

## Status

IN PROGRESS

### Progress

- [ ] Add Bootstrap JS bundle `<script>` to `BASE_HTML`
- [ ] Add hamburger toggler `<button>` to navbar in `BASE_HTML`
- [ ] Wrap `navbar-nav` in `navbar-collapse collapse` div
- [ ] Audit all `<table>` elements — add `table-responsive` wrapper where missing
- [ ] Audit form inputs for font-size < 16px — add mobile CSS override
- [ ] Audit buttons for tap target height — add `min-height` mobile CSS if needed
- [ ] Manual test at 375px width: navbar, shopping, inventory, recipes, recipe detail, settings

## Scope

- Changes confined to `BASE_HTML` and inline HTML template strings in `pantry_app.py`
- No layout redesign — Bootstrap grid already handles column stacking; this fixes the navbar JS gap and specific overflow issues
- Out of scope: dark mode, PWA/offline support, native app

## Files

- `pantry_app.py` — `BASE_HTML` (navbar fix, JS bundle, mobile CSS) + table wrappers in template strings
- `mobile-layout.flow.md` — flow doc
