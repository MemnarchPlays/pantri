#!/usr/bin/env python3
"""Pantri — start the web app: py pantry_app.py"""

import socket
import threading
import webbrowser
from pantri import create_app
from pantri.bot import _kill_stale_bot, start_bot

app = create_app()

if __name__ == '__main__':
    _kill_stale_bot()
    print('Starting Pantri at http://localhost:5000')

    def _port_open(port):
        try:
            with socket.create_connection(('localhost', port), timeout=0.5):
                return True
        except OSError:
            return False

    if not _port_open(5000):
        threading.Timer(1.2, webbrowser.open, args=['http://localhost:5000']).start()

    start_bot()
    app.run(host='0.0.0.0', port=5000)
