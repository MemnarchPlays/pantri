#!/usr/bin/env python3
"""Pantri — start the web app: py pantry_app.py"""

import socket
import threading
import webbrowser
from pantri import create_app
from pantri.backup import restore_default_if_needed
from pantri.bot import _kill_stale_bot, start_bot
from pantry_utils import read_env

app = create_app()
restore_default_if_needed()

if __name__ == '__main__':
    _kill_stale_bot()
    port = int(read_env().get('PORT', '5000'))
    print(f'Starting Pantri at http://localhost:{port}')

    def _port_open(p):
        try:
            with socket.create_connection(('localhost', p), timeout=0.5):
                return True
        except OSError:
            return False

    if not _port_open(port):
        threading.Timer(1.2, webbrowser.open, args=[f'http://localhost:{port}']).start()

    start_bot()
    app.run(host='0.0.0.0', port=port)
