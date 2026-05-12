---
name: Appearance / Theme Flow
description: How the color picker, font selector, and preview update the UI theme
---

# Appearance / Theme Flow

## Entry point

`/settings?tab=interface` → Interface tab → Theme Color card

---

## Pipeline

| Step | What the user does | What the system does |
|------|--------------------|----------------------|
| 1 | Opens Interface tab | Inline `<script>` reads `window._pantri.color` / `.font` (set by base.html on page load from localStorage) and populates the color picker, hex label, and font select |
| 2 | Drags color picker or types a hex value | `input` event fires on `#color-pick`; updates `#color-hex` text and calls `window._pantri.applyColor()` to update CSS vars live |
| 3 | Clicks a preset button | `setPreset(color)` sets picker value, hex label, and calls `applyColor()` |
| 4 | Clicks **Apply** | `applyAndSave()` writes color + font to `localStorage`, calls `applyColor()`, updates `document.body.fontFamily`, briefly shows "Saved!" on the button |
| 5 | Clicks **Reset** | Removes `pantri_accent` and `pantri_font` from localStorage, reloads page |
| 6 | Revisits any page | `base.html` inline script reads localStorage on load and sets CSS vars before first paint |

---

## Key identifiers

| ID / function | Role |
|---------------|------|
| `window._pantri.applyColor(hex)` | Computes dark/light variants and sets `--purple`, `--dark-purple`, `--light-purple` on `document.documentElement` |
| `window._pantri.color` | Current accent color (from localStorage or default `#6B2D8B`) |
| `#color-pick` | `<input type="color">` — the picker |
| `#color-hex` | Hex label shown next to the picker |
| `#font-select` | Font family dropdown |
| `#font-preview` | Sample text that updates on font change |
| Preview boxes | `div` elements using `var(--purple)` / `var(--light-purple)` inline styles — update whenever CSS vars change |

---

## Failure modes

| Condition | Behavior |
|-----------|----------|
| `applyColor()` not called on picker `input` | Preview boxes don't update until Apply is clicked (BUG-007 — fixed) |
| Preset button doesn't call `applyColor()` | Same as above for presets — fixed alongside BUG-007 |
| User changes color but doesn't click Apply | Color reverts on next page load (correct — Apply is the save action) |
