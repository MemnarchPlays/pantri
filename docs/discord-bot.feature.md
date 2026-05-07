---
name: Discord Bot Integration
description: A Discord bot that reads/writes the pantry xlsx and sends low-stock alerts; managed as a subprocess from the web app
flow: settings.flow.md
status: COMPLETE
---

## What It Does

A Discord bot (`discord_bot.py`) runs as a subprocess spawned by `pantry_app.py`. It shares the same xlsx data file as the web app. The Settings page provides a UI to configure the token, start/stop the bot, and view its log. When a `!add` or decrement drops an item below its minimum, the bot posts a low-stock alert to a configured channel.

## Success Criteria

1. The Discord tab in Settings shows a live status badge (Online/Offline) polled via `/settings/bot-status`.
2. Pasting a token and clicking "Save & Restart" writes the token to `.env` and starts the bot subprocess.
3. The bot log card shows output from the most recent bot session (tail of `bot.log`).
4. Clicking "Stop Bot" terminates the subprocess.
5. Clicking "Remove Connection" stops the bot and removes the token from `.env`.
6. A stale `bot.pid` from a previous session is killed on app startup.
7. The bot reads and writes the same `Food in Storage.xlsx` used by the web app.
8. When an item drops below its minimum after a `!add` or decrement, the bot posts an alert to the channel configured in `DISCORD_ALERT_CHANNEL`.
9. The bot can also run standalone (`py discord_bot.py`) if `DISCORD_TOKEN` is in `.env`.

## Status

COMPLETE

### Progress

- [x] Bot subprocess management (start/stop/pid file)
- [x] `.env` token + alert channel config
- [x] Settings UI (start/stop/restart/remove, status badge, log viewer)
- [x] Bot reads/writes same xlsx
- [x] Low-stock alert on decrement below minimum

## Scope

- Single bot process per web app instance
- Out of scope: multi-server support, bot command reference (in `discord_bot.py`)

## Files

- `pantry_app.py` — routes `/settings/discord`, `/settings/bot-status`, `/settings/bot-log`, `/settings/bot-test`, helpers `start_bot`, `stop_bot`, `bot_running`, `_kill_stale_bot`
- `discord_bot.py` — bot implementation
- `.env` — `DISCORD_TOKEN`, `DISCORD_ALERT_CHANNEL` (gitignored)
- `bot.pid`, `bot.log` — runtime files (gitignored)
- `settings.flow.md` — flow doc
