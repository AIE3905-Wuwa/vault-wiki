"""ADFS OAuth2 login: exchange an authorization code at sts.cuhk.edu.cn for a bb.cuhk.edu.cn session cookie.

Flow (verified live 2026-09-29; the school runs a customized paginated ADFS):
GET authorize → parse loginForm (hidden holders + password box) → prefix the
username with the `cuhksz\\` domain per the page's custom JS rule (left
unchanged if it already contains @ or \\) → a single POST → the redirect
chain lands back on bb.cuhk.edu.cn with a session. Success is detected by a
positive check (/users/me 200); the failure page's error text lives
permanently in HTML templates and cannot be used as a signal.
"""

from __future__ import annotations

import re
from urllib.parse import urljoin, urlparse

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


def _parse_forms(html: str, base_url: str):
    """Return [(action, hidden_fields, has_password, has_user_text)] in document order.

    Input tags on the page are often written across multiple lines,
    invisible to grep — an HTML parser is required.
    """
    soup = BeautifulSoup(html, "html.parser")
    out = []
    for form in soup.find_all("form"):
        action = form.get("action") or ""
        hidden = {
            i.get("name"): i.get("value", "")
            for i in form.find_all("input", {"type": "hidden"})
            if i.get("name")
        }
        has_password = bool(form.find("input", {"type": "password"}))
        has_user = any(
            (i.get("type") in (None, "text", "email")) and i.get("name")
            for i in form.find_all("input")
        )
        out.append((urljoin(base_url, action), hidden, has_password, has_user))
    return out


def login(transport: Transport, username: str, password: str) -> dict:
    """Single-step password submission (the paginated flow pages client-side; the account step sends no request).

    - The custom JS rewrites usernames without @ or \\ as `cuhksz\\<input>`
      before submitting (page constant contosoDomain = "cuhksz"; the same
      prefix rule is applied here);
    - Submitted fields = hidden holders (UserName/Kmsi/AuthMethod) + overwritten UserName/Password;
    - Reaching bb.cuhk.edu.cn means success; then verify positively via /users/me;
    - Landing back on the login page = credentials rejected.
    """

    def host_of(u: str) -> str:
        return urlparse(u).hostname or ""

    def verify_and_return() -> dict:
        me = transport.request("GET", "/learn/api/public/v1/users/me")
        if me.status_code == 200:
            return me.json()
        raise AuthError("Reached BB but REST 401 (session not established)")

    transport.clear_cookies()
    r = transport.request("GET", config.ADFS_AUTHORIZE_URL, absolute=True)
    if r.status_code != 200:
        raise TransportError(f"ADFS authorize page returned HTTP {r.status_code}")
    _dump("01-authorize", r.text)
    if host_of(str(r.url)) == "bb.cuhk.edu.cn":  # an existing session lets us straight through
        return verify_and_return()

    # Domain-prefix rewrite (matching the page's custom JS; input already carrying @ or \ is left alone)
    domain = "cuhksz"
    m = re.search(r'contosoDomain\s*=\s*"([^"]+)"', r.text)
    if m:
        domain = m.group(1)
    if not re.search(r"[@\\]", username):
        username = f"{domain}\\{username}"

    forms = _parse_forms(r.text, str(r.url))
    pw_form = next((f for f in forms if f[2]), None)
    if not pw_form:
        raise AuthError("Password form not found (login page structure changed)")
    action, hidden, _, _ = pw_form
    data = dict(hidden)
    data["UserName"] = username
    data["Password"] = password
    resp = transport._sess.post(action, data=data, allow_redirects=True,
                                timeout=config.REQUEST_TIMEOUT,
                                proxy=config.proxy() or None)
    _dump("02-password-post", resp.text)
    if host_of(str(resp.url)) == "bb.cuhk.edu.cn":
        return verify_and_return()
    raise CredentialError("Username or password rejected (still on ADFS after submission)")


def logout(transport: Transport) -> None:
    try:
        transport.request("GET", "/webapps/login/?action=logout")
    except TransportError:
        pass  # best effort: the local session is always cleared
    transport.clear_cookies()
    p = config.session_path()
    if p.exists():
        p.unlink()
