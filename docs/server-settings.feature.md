---
name: Server Settings
description: User can configure the web server port and display timezone from Settings → Interface
---

# Server Settings

## Success criteria

- [x] Port field in Settings → Interface accepts any valid TCP port (1–65535) and saves it to `.env`
- [ ] Port changes take effect after restarting the app
- [ ] Display Timezone dropdown saves `DISPLAY_TZ` to `.env` and affects backup timestamps immediately
- [ ] Invalid port values (out of range, non-numeric) are rejected silently and the previous value is kept

## ~~[BUG] BUG-010 — Port values below 1024 are blocked by UI and server-side validation~~ FIXED

**What "fixed" looks like:** A user can enter port 80 (or any port 1–65535) in Settings → Interface, click Save, and the value persists in `.env`. The HTML input no longer shows "Value must be greater than or equal to 1024."

**Files to look at first:**
- `templates/settings.html` — port `<input>` has `min="1024"` blocking ports below 1024 at the browser level
- `pantri/routes/settings.py:settings_appearance()` — server-side guard `if 1024 <= port <= 65535` silently ignores ports 1–1023
