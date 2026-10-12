"""ADFS OAuth2 login: exchange an authorization code at sts.cuhk.edu.cn for a PeopleSoft session (verified 2026-10-05).

The flow shares its source with bb-cli (same ADFS, same cuhksz\\ domain
prefix rule); the difference is the code consumer: SIS's dologin.html is a
static page whose JS builds a form POSTing to /psp/csprd/?cmd=login (fixed
service account CUSZ_SSO_LOGIN + a random password; the PeopleSoft backend
exchanges the code for a session) — the CLI replicates that form. GET
cmd=login first to warm up PSJSESSIONID before POSTing.
Success criterion: PS_TOKEN lands.
"""

from __future__ import annotations

import random
import re
import string
from urllib.parse import parse_qs, urljoin, urlparse

from bs4 import BeautifulSoup

from . import config
from .transport import Transport, TransportError


class AuthError(Exception):
    pass


class CredentialError(AuthError):
    pass


def _dump(tag: str, html: str) -> None:
    d = config.debug_dir()
    if d:
        (d / f"{tag}.html").write_text(html, encoding="utf-8", errors="replace")


def _host(u: str) -> str:
    return urlparse(str(u)).hostname or ""


def login(transport: Transport, username: str, password: str) -> dict:
    """Full login chain; on success returns a cookie-state summary (no REST identity endpoint — PS_TOKEN is the criterion)."""
    transport.clear_cookies()
    r = transport.request("GET", config.ADFS_AUTHORIZE_URL, absolute=True)
    if r.status_code != 200:
        raise TransportError(f"ADFS authorize page returned HTTP {r.status_code}")
    _dump("01-adfs-authorize", r.text)

    # code: ADFS returns it directly if a session already exists; otherwise, form login
    if _host(str(r.url)) == "sts.cuhk.edu.cn":
        if not re.search(r"[@\\]", username):
            username = f"cuhksz\\{username}"  # domain prefix rule matching the login page's custom JS
        soup = BeautifulSoup(r.text, "html.parser")
        pw_form = next((f for f in soup.find_all("form")
                        if f.find("input", {"type": "password"})), None)
        if pw_form is None:
            raise AuthError("Password form not found (login page structure changed)")
        data = {i.get("name"): i.get("value", "")
                for i in pw_form.find_all("input", {"type": "hidden"}) if i.get("name")}
        data["UserName"] = username
        data["Password"] = password
        resp = transport._sess.post(urljoin(str(r.url), pw_form.get("action") or ""),
                                    data=data, allow_redirects=True,
                                    timeout=config.REQUEST_TIMEOUT,
                                    proxy=config.proxy() or None)
        _dump("02-adfs-post-final", resp.text)
        if _host(str(resp.url)) != "sis.cuhk.edu.cn":
            raise CredentialError("Username or password rejected (still on ADFS after submission)")
        code = parse_qs(urlparse(str(resp.url)).query).get("code", [None])[0]
    else:
        code = parse_qs(urlparse(str(r.url)).query).get("code", [None])[0]
    if not code:
        raise AuthError("OAuth authorization code missing (SSO chain changed)")

    # Consume the code: warm up PSJSESSIONID → POST the login form (replicating dologin.html's JS)
    transport.request("GET", "/psp/csprd/?cmd=login")
    r3 = transport._sess.post(
        f"{config.SIS_HOST}/psp/csprd/?cmd=login&languageCd=ENG&code={code}",
        data={
            "timezoneOffset": "-480", "ptmode": "f", "ptlangcd": "ENG",
            "ptinstalledlang": "ENG,ZHT,ZHS", "userid": "CUSZ_SSO_LOGIN",
            "pwd": "".join(random.choices(string.ascii_uppercase, k=10)),
            "ptlangsel": "ENG",
        }, allow_redirects=True, timeout=config.REQUEST_TIMEOUT,
        proxy=config.proxy() or None)
    _dump("03-ps-login-final", r3.text)
    transport.follow_shell(r3, max_hops=2)  # login shell → StartPage (do not deep-follow the portal tab shell; avoids loops)
    if not any(c.name == "PS_TOKEN" and c.value for c in transport._sess.cookies.jar):
        raise AuthError("Login chain completed but PS_TOKEN never landed")
    transport.save_session()
    return {"authenticated": True, "host": "sis.cuhk.edu.cn"}


def logout(transport: Transport) -> None:
    try:
        transport.request("GET", "/psp/csprd/EMPLOYEE/HRMS/?cmd=logout")
    except TransportError:
        pass  # best effort: the local session is always cleared
    transport.clear_cookies()
    p = config.session_path()
    if p.exists():
        p.unlink()
