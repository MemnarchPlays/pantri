---
name: Mobile Layout Flow
description: User accesses the app on a phone or small screen in the kitchen
---

# Mobile Layout Flow

## Entry point
Any page on a device with viewport width < 768px (phone / tablet portrait)

## Step table

| Step | What the user sees | What the system does |
|------|--------------------|----------------------|
| 1 | Lands on any page | Viewport meta scales correctly; no horizontal scroll |
| 2 | Taps hamburger menu icon | Navbar collapses/expands to show nav links vertically |
| 3 | Navigates to Inventory | Table scrolls horizontally within its container; rows are readable |
| 4 | Navigates to Recipes | Cards stack vertically; recipe names and buttons are full-width |
| 5 | Navigates to Shopping | Two-column layout collapses to single column; all cards stack |
| 6 | Navigates to a recipe detail | Ingredient list and instruction steps are readable without pinching |
| 7 | Taps any action button (add, edit, delete) | Button hit targets are at least 44px tall |

## Failure modes

| Condition | Behavior |
|-----------|----------|
| Very long recipe name | Wraps rather than overflows or truncates destructively |
| Table with many columns | Scrolls horizontally within a `table-responsive` wrapper |
| Form inputs on iOS | Font size ≥ 16px to prevent iOS auto-zoom on focus |
