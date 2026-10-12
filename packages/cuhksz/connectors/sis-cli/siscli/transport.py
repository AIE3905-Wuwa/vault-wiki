"""Transport layer: curl_cffi session + PS_DEVICEFEATURES + shell-page JS redirect following + cookie write-through.

Three empirically verified essentials for SIS/PeopleSoft (2026-10-05):
- On a direct psc hit the server first returns a bootstrap shell
  (self.location points at the psp-version URL); following it reaches the
  real content or a portal framework page (the TargetContent iframe);
- PORTAL-PSJSESSIONID is re-issued on a rolling basis with each response;
  a stale cross-process jar bounces back to the login shell — hence
  session.json is written through immediately after every request;
- Sessions last only minutes; callers must provide a re-login callback.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from curl_cffi import requests as creq

from . import config


class TransportError(Exception):
    pass


class DeadSession(TransportError):
    """The response is a PeopleSoft login shell (session expired or never established)."""


class Transport:
    def __init__(self, relogin=None):
        self._sess = creq.Session(impersonate=config.IMPERSONATE)
        self._sess.cookies.set("PS_DEVICEFEATURES", config.PS_DEVICEFEATURES,
                               domain="sis.cuhk.edu.cn", path="/")
        self._relogin = relogin
        self._in_relogin = False

    # ---- Session persistence (write-through) ----
    def export_cookies(self) -> list[dict]:
        return [
            {"name": c.name, "value": c.value, "domain": c.domain, "path": c.path}
            for c in self._sess.cookies.jar
        ]

    def save_session(self) -> None:
        p = config.session_path()
        p.write_text(json.dumps(self.export_cookies(), ensure_ascii=False, indent=1),
                     encoding="utf-8")

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
        for c in jar:
            self._sess.cookies.set(c["name"], c["value"],
                                   domain=c.get("domain", ""), path=c.get("path", "/"))
        # the device-features cookie does not travel with the jar; always re-seeded
        self._sess.cookies.set("PS_DEVICEFEATURES", config.PS_DEVICEFEATURES,
                               domain="sis.cuhk.edu.cn", path="/")
        return any(c["name"] == "PS_TOKEN" and c["value"] for c in jar)

    def clear_cookies(self) -> None:
        self._sess.cookies.jar.clear()
        self._sess.cookies.set("PS_DEVICEFEATURES", config.PS_DEVICEFEATURES,
                               domain="sis.cuhk.edu.cn", path="/")

    # ---- Requests ----
    def request(self, method: str, url: str, *, absolute: bool = False, **kw):
        if not absolute:
            url = urljoin(config.SIS_HOST + "/", url.lstrip("/"))
        kw.setdefault("timeout", config.REQUEST_TIMEOUT)
        if config.proxy():
            kw["proxy"] = config.proxy()
        kw.setdefault("allow_redirects", True)
        r = self._sess.request(method, url, **kw)
        self.save_session()  # PSJSESSIONID rolls per response; write through
        return r

    def follow_shell(self, r, max_hops: int = 4):
        """Follow the PeopleSoft shell page's self.location JS jump (bootstrap/login shell)."""
        for _ in range(max_hops):
            m = re.search(r"self\.location='([^']+)'", r.text)
            if not m:
                break
            target = m.group(1)
            if not target.startswith("http"):
                target = urljoin(config.SIS_HOST, target)
            r = self.request("GET", target, absolute=True)
        return r

    # ---- Page detection ----
    @staticmethod
    def page_title(html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")
        return soup.title.get_text() if soup.title else ""

    @staticmethod
    def is_signon_shell(html: str) -> bool:
        """Login-shell signature: a thin page titled with PeopleSoft sign-in / Sign-in / Sign In.

        Both shapes must be caught: the bootstrap shell (title 'Oracle PeopleSoft 登录')
        and the language-selection sign-in page (title 'Sign In', body '学生信息系统').
        (The quoted literals are actual page strings the code matches on.)
        """
        if len(html) > 6000:
            return False
        t = Transport.page_title(html)
        return "登录" in t or "Sign-in" in t or "Sign In" in t

    # ---- Component fetching ----
    def get_content(self, comp: str, nav: str) -> str:
        """Hit a component directly via psc+PTCNAV, follow the shell, drill into TargetContent, and return the real content HTML.

        Raises DeadSession when the session is dead; with a relogin callback
        set, re-logs in once automatically and replays.
        """
        for attempt in (1, 2):
            url = f"{config.SIS_HOST}/psc/csprd/EMPLOYEE/HRMS/c/{comp}?PORTALPARAM_PTCNAV={nav}"
            r = self.follow_shell(self.request("GET", url))
            html = r.text
            if self.is_signon_shell(html):
                if self._relogin and not self._in_relogin and attempt == 1:
                    self._in_relogin = True
                    try:
                        self.clear_cookies()
                        self._relogin()
                    finally:
                        self._in_relogin = False
                    continue
                raise DeadSession("Session expired and re-login ineffective (login page structure may have changed)")
            soup = BeautifulSoup(html, "html.parser")
            frame = soup.find("iframe", id="ptifrmtgtframe")
            if frame and self.page_title(html) == "Employee-facing registry content":
                html = self.request("GET", frame["src"]).text  # portal framework page → real content
            d = config.debug_dir()
            if d:
                (Path(d) / f"content-{comp.split('.')[-2] if '.' in comp else comp}.html") \
                    .write_text(html, encoding="utf-8", errors="replace")
            return html
        raise DeadSession("unreachable")

    # ---- ICAction POST navigation (query-type action primitive) ----
    def submit_icaction(self, comp: str, nav: str, action: str,
                        extra: dict[str, str] | None = None) -> str:
        """GET the component page → collect the win0 form → set ICAction (+ optional field overrides) → POST.

        PeopleSoft dropdown jumps, View Report, and term expansion all go
        through this primitive (issue #6 ①). Query-type actions only;
        data-changing buttons are constrained by caller discipline (the
        skill's Prohibitions).
        """
        html = self.get_content(comp, nav)
        soup = BeautifulSoup(html, "html.parser")
        form = soup.find("form", attrs={"name": "win0"})
        if form is None or not form.get("action"):
            raise TransportError("win0 form not found (page structure changed)")
        fields: dict[str, str] = {}
        for i in form.find_all("input"):
            n = i.get("name")
            if n and i.get("type") in (None, "hidden", "text"):
                fields[n] = i.get("value") or ""
        for sel in form.find_all("select"):
            if sel.get("name") and sel.find("option"):
                fields[sel.get("name")] = sel.find("option").get("value") or ""
        fields["ICAction"] = action
        if extra:
            fields.update(extra)
        r = self._sess.post(form["action"], data=fields, allow_redirects=True,
                            timeout=config.REQUEST_TIMEOUT)
        self.save_session()
        if self.is_signon_shell(r.text):
            raise DeadSession("Session dead after ICAction submission")
        return r.text

    # ---- term search-page submission (a query action, same as picking a term and clicking Continue on the web) ----
    def submit_search(self, search_html: str, radio_value: str,
                      action: str = "DERIVED_SSS_SCT_SSR_PB_GO") -> str:
        """Collect the win0 form from the search-page HTML, set the term radio + ICAction, POST, and return the result page.

        Query-type buttons only (Continue/Change Term); any data-changing
        button is forbidden here.
        """
        soup = BeautifulSoup(search_html, "html.parser")
        form = soup.find("form", attrs={"name": "win0"})
        if form is None or not form.get("action"):
            raise TransportError("win0 form not found (search page structure changed)")
        fields: dict[str, str] = {}
        for i in form.find_all("input"):
            n = i.get("name")
            if n and i.get("type") in (None, "hidden", "text"):
                fields[n] = i.get("value") or ""
        for sel in form.find_all("select"):
            if sel.get("name") and sel.find("option"):
                fields[sel.get("name")] = sel.find("option").get("value") or ""
        fields["SSR_DUMMY_RECV1$sels$0"] = str(radio_value)
        fields["ICAction"] = action
        r = self._sess.post(form["action"], data=fields, allow_redirects=True,
                            timeout=config.REQUEST_TIMEOUT)
        self.save_session()
        if self.is_signon_shell(r.text):
            raise DeadSession("Session dead after term submission")
        return r.text

    def download(self, url: str, dest: Path) -> int:
        raise NotImplementedError("v0.1 ships no downloads; report exports go through raw for manual verification before wrapping")
