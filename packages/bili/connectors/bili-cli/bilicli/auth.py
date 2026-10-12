"""Cookie import and loading: SESSDATA/bili_jct (+buvid3), stored 0600 in ~/.bili-cli/cookies.json.

The cookie is a full-power credential — stored only in the local CONFIG_DIR,
never in any repo, never echoed in full.
"""

import json
import os
import sys

from .config import AUTH_KEYS, COOKIE_FILE


def parse_cookie_string(raw: str) -> dict:
    """Parse a "k=v; k2=v2" cookie string (the Request Header value copied straight from browser DevTools)."""
    jar = {}
    for part in raw.replace("\n", ";").split(";"):
        if "=" not in part:
            continue
        k, _, v = part.strip().partition("=")
        if k and v:
            jar[k] = v
    return jar


def save_cookies(jar: dict) -> None:
    missing = [k for k in AUTH_KEYS if k not in jar]
    if missing:
        raise SystemExit(f"cookie is missing login keys {missing} (SESSDATA and bili_jct required; copy from browser DevTools)")
    COOKIE_FILE.parent.mkdir(parents=True, exist_ok=True)
    COOKIE_FILE.write_text(json.dumps(jar, ensure_ascii=False, indent=2), encoding="utf-8")
    try:  # effective on non-Windows; best-effort on Windows
        os.chmod(COOKIE_FILE, 0o600)
    except OSError:
        pass


def load_cookies() -> dict:
    if not COOKIE_FILE.exists():
        raise SystemExit("not logged in: run bili-cli login --cookie '...' (or --file) first; credentials stay in ~/.bili-cli/ only")
    return json.loads(COOKIE_FILE.read_text(encoding="utf-8"))
