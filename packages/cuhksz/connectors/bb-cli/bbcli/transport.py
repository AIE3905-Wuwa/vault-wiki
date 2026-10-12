"""Transport layer: curl_cffi session + browser TLS fingerprint + session persistence + automatic re-login on 401.

Following bbwatch's empirical findings: impersonate="chrome124" passes the
site's fingerprint checks — no real browser needed; the cookie jar can be
serialized to the user directory for reuse across processes.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from urllib.parse import urljoin

from curl_cffi import requests as creq

from . import config


class TransportError(Exception):
    pass


class TooLarge(TransportError):
    """Download exceeded the size cap (--max-size breaker); partial writes already cleaned up."""


class ApiError(Exception):
    def __init__(self, status: int, url: str, body: str):
        self.status = status
        self.url = url
        self.body = body[:500]
        super().__init__(f"HTTP {status} {url}: {self.body}")


class Transport:
    def __init__(self, relogin=None):
        self._sess = creq.Session(impersonate=config.IMPERSONATE)
        self._relogin = relogin  # no-arg callback; on success the session is renewed; if None, a 401 propagates as-is
        self._in_relogin = False

    # ---- Session persistence ----
    def export_cookies(self) -> list[dict]:
        return [
            {"name": c.name, "value": c.value, "domain": c.domain, "path": c.path}
            for c in self._sess.cookies.jar
        ]

    def import_cookies(self, jar: list[dict]) -> None:
        for c in jar:
            self._sess.cookies.set(
                c["name"], c["value"], domain=c.get("domain", ""), path=c.get("path", "/")
            )

    def clear_cookies(self) -> None:
        self._sess.cookies.jar.clear()

    def save_session(self) -> None:
        p = config.session_path()
        p.write_text(json.dumps(self.export_cookies(), ensure_ascii=False, indent=1), encoding="utf-8")

    def load_session(self) -> bool:
        p = config.session_path()
        if not p.exists():
            return False
        try:
            jar = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return False
        if not isinstance(jar, list) or not jar:
            return False
        self.import_cookies(jar)
        return True

    # ---- Requests ----
    def request(self, method: str, url: str, *, absolute: bool = False, **kw):
        if not absolute:
            url = urljoin(config.BB_HOST + "/", url.lstrip("/"))
        kw.setdefault("timeout", config.REQUEST_TIMEOUT)
        if config.proxy():
            kw["proxy"] = config.proxy()
        kw.setdefault("allow_redirects", True)
        r = self._sess.request(method, url, **kw)
        if r.status_code == 401 and self._relogin and not self._in_relogin:
            self._in_relogin = True
            try:
                self.clear_cookies()
                self._relogin()  # re-login once, then replay; a failure or another 401 during re-login propagates as-is
            finally:
                self._in_relogin = False
            r = self._sess.request(method, url, **kw)
        return r

    def get_json(self, path: str, params: dict | None = None) -> dict:
        r = self.request("GET", path, params=params)
        if r.status_code != 200:
            raise ApiError(r.status_code, path, r.text or "")
        try:
            return r.json()
        except ValueError as e:
            raise ApiError(r.status_code, path, r.text[:200] or str(e)) from e

    def download(self, url: str, dest: Path, max_bytes: int | None = None) -> int:
        if not url.startswith("http"):
            url = urljoin(config.BB_HOST + "/", url.lstrip("/"))
        r = self.request("GET", url, stream=True)  # curl_cffi needs streaming enabled at request time for iter_content
        if r.status_code != 200:
            raise ApiError(r.status_code, url, r.text or "")
        dest.parent.mkdir(parents=True, exist_ok=True)
        tmp = dest.with_suffix(dest.suffix + ".part")
        written = 0
        try:
            with open(tmp, "wb") as f:
                for chunk in r.iter_content(65536):
                    if chunk:
                        written += len(chunk)
                        if max_bytes and written > max_bytes:
                            raise TooLarge(
                                f"Exceeded cap of {max_bytes // 1048576}MB (wrote {written} bytes)")
                        f.write(chunk)
        except TooLarge:
            tmp.unlink(missing_ok=True)
            raise
        os.replace(tmp, dest)
        return written
