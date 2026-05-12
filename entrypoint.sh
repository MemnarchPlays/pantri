#!/bin/sh
set -e
mkdir -p /userdata/state /userdata/backups /userdata/data
exec python pantry_app.py
