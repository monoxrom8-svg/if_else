#!/usr/bin/env sh
set -eu

python - <<'PY'
import os
import socket
import sys
import time

host = os.getenv("DB_HOST", "db")
port = int(os.getenv("DB_PORT", "3306"))
timeout_s = int(os.getenv("DB_WAIT_TIMEOUT", "60"))

deadline = time.time() + timeout_s
last_err = None
while time.time() < deadline:
    try:
        with socket.create_connection((host, port), timeout=2):
            sys.exit(0)
    except OSError as e:
        last_err = e
        time.sleep(1)

print(f"Database is not reachable at {host}:{port} after {timeout_s}s: {last_err}", file=sys.stderr)
sys.exit(1)
PY

exec "$@"
