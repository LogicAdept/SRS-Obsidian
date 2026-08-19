#!/usr/bin/env python3
"""Local 127.0.0.1 helper so coverage-index.html can start a Docker cover run.

  python .cursor/sdk/cover_ui.py

Then open SRS/NamesHistory/coverage-index.html and use Agent on a row.
"""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import re
import subprocess
import sys

REPO = Path(__file__).resolve().parents[2]
_SCRIPTS = REPO / ".cursor" / "skills" / "process-topic" / "scripts"
sys.path.insert(0, str(_SCRIPTS))

from vault_cards import parse_tree_paths, vault_dir  # noqa: E402

HOST = "127.0.0.1"
PORT = 8765
TAG_RE = re.compile(r"^[A-Za-z0-9]+(?:/[A-Za-z0-9]+)*$")
LAUNCHER = REPO / ".cursor" / "sdk" / "run_cover_vault.ps1"
TAGS_MD = vault_dir(REPO) / "Format" / "Tags.md"


def _allowed_tags() -> set[str]:
    return set(parse_tree_paths(TAGS_MD))


def _cors(handler: BaseHTTPRequestHandler) -> None:
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type")


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args: object) -> None:
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    def do_OPTIONS(self) -> None:  # noqa: N802
        self.send_response(204)
        _cors(self)
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802
        if self.path.rstrip("/") != "/health":
            self.send_error(404)
            return
        self.send_response(200)
        _cors(self)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"ok":true}\n')

    def do_POST(self) -> None:  # noqa: N802
        if self.path.rstrip("/") != "/launch":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length else b"{}"
        try:
            body = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._json(400, {"ok": False, "error": "invalid JSON"})
            return
        tag = str(body.get("tag", "")).strip().lstrip("#")
        if not TAG_RE.fullmatch(tag) or tag not in _allowed_tags():
            self._json(400, {"ok": False, "error": "unknown tag"})
            return
        if not os.environ.get("CURSOR_API_KEY", "").strip():
            self._json(400, {"ok": False, "error": "set CURSOR_API_KEY in this shell"})
            return
        if not LAUNCHER.is_file():
            self._json(500, {"ok": False, "error": "launcher missing"})
            return
        creationflags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
        if sys.platform == "win32":
            creationflags |= getattr(subprocess, "DETACHED_PROCESS", 0)
        subprocess.Popen(
            [
                "powershell",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(LAUNCHER),
                tag,
            ],
            cwd=str(REPO),
            env=os.environ.copy(),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            creationflags=creationflags,
            close_fds=True,
        )
        self._json(202, {"ok": True, "tag": tag})

    def _json(self, status: int, payload: dict[str, object]) -> None:
        data = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        _cors(self)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def main() -> int:
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"cover UI helper on http://{HOST}:{PORT}")
    print("Open SRS/NamesHistory/coverage-index.html and click Agent.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
