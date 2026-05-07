"""Discord bot subprocess management."""

import subprocess
import sys
from datetime import datetime
from pathlib import Path
from pantry_utils import read_env

BOT_SCRIPT   = Path(__file__).parent.parent / 'discord_bot.py'
BOT_PID_FILE = Path(__file__).parent.parent / 'bot.pid'
BOT_LOG_FILE = Path(__file__).parent.parent / 'bot.log'

_bot_process = None


def bot_running():
    return _bot_process is not None and _bot_process.poll() is None


def _kill_stale_bot():
    """Kill any bot process left over from a previous Flask session."""
    if not BOT_PID_FILE.exists():
        return
    try:
        pid = int(BOT_PID_FILE.read_text().strip())
        import os, signal
        os.kill(pid, signal.SIGTERM)
    except (ValueError, OSError, AttributeError):
        pass
    try:
        BOT_PID_FILE.unlink()
    except OSError:
        pass


def start_bot():
    global _bot_process
    if bot_running():
        _bot_process.terminate()
        _bot_process.wait()
    _kill_stale_bot()
    token = read_env().get('DISCORD_TOKEN', '')
    if not token:
        return False
    log = open(BOT_LOG_FILE, 'a', encoding='utf-8')
    log.write(f'\n--- Bot started {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ---\n')
    log.flush()
    import os as _os
    bot_env = _os.environ.copy()
    bot_env['DISCORD_TOKEN'] = token
    _bot_process = subprocess.Popen(
        [sys.executable, str(BOT_SCRIPT)],
        cwd=str(BOT_SCRIPT.parent),
        stdout=log, stderr=log,
        env=bot_env,
    )
    BOT_PID_FILE.write_text(str(_bot_process.pid))
    return True


def stop_bot():
    global _bot_process
    if bot_running():
        _bot_process.terminate()
        _bot_process.wait()
    _bot_process = None
    _kill_stale_bot()
