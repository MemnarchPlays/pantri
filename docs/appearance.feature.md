---
name: Appearance Settings
description: User customizes accent color and font from the Settings page
---

# Appearance Settings

## Success criteria

- [ ] Accent color picker on Settings → Appearance lets the user pick a color
- [x] Sample text updates in real-time as the color is changed (before Apply is clicked)
- [ ] Clicking Apply saves the color to localStorage and applies it to the full UI immediately
- [ ] Font selector lets the user pick a font family; UI updates on Apply
- [ ] Color and font persist across page reloads

## [BUG] BUG-007 — Sample text does not update in real-time

**What "fixed" looks like:** Changing the color picker value immediately updates the sample text color without requiring the user to click Apply first.

**File to look at first:** `templates/settings.html` — the color picker `input[type=color]` and its `oninput`/`onchange` event handler (or lack thereof).
