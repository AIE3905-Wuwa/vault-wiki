"""Common layer: config/credentials/HTTP/policy/token renewal/view utilities."""
import email, email.policy, json, mimetypes, os, re, sys, time
import urllib.request, urllib.parse, urllib.error

GRAPH = "https://graph.microsoft.com/v1.0"
GMAIL = "https://gmail.googleapis.com/gmail/v1/users/me"
GMAIL_SCOPE = "https://mail.google.com/"  # full access — gmail accounts require explicit user delegation

# ---------- config & credentials (local machine only, never in any repo) ----------

def cfg_dir():
    d = os.path.expanduser("~/.config/mail-cli")
    os.makedirs(d, exist_ok=True)
    return d
def cfg_path(p): return os.path.join(cfg_dir(), f"{p}.json")
def load_tok(p):
    f = cfg_path(p)
    return json.load(open(f)) if os.path.exists(f) else None
def save_tok(p, t): json.dump(t, open(cfg_path(p), "w"))

def gcp_creds():
    f = os.path.join(cfg_dir(), "gcp.json")
    try: return json.load(open(f))
    except Exception: fail("missing ~/.config/mail-cli/gcp.json (GCP OAuth client, human-provided, never in any repo)")

# ---------- output ----------

def out(d): print(json.dumps(d, ensure_ascii=False))
def fail(e): sys.exit(json.dumps({"ok": False, "error": e}, ensure_ascii=False))

# ---------- HTTP ----------

def http(url, data=None, tok=None, binary=False, method=None, jdata=None, raise_err=False):
    body = urllib.parse.urlencode(data).encode() if data else (json.dumps(jdata).encode() if jdata is not None else None)
    req = urllib.request.Request(url, data=body, method=method)
    if data: req.add_header("Content-Type", "application/x-www-form-urlencoded")
    if jdata is not None: req.add_header("Content-Type", "application/json")
    if tok: req.add_header("Authorization", f"Bearer {tok}")
    try:
        with urllib.request.urlopen(req) as r:
            b = r.read()
            if binary: return b
            return json.loads(b) if b else {}
    except urllib.error.HTTPError as e:
        if raise_err: raise
        try: err = json.loads(e.read()).get("error", {})
        except Exception: err = {"message": str(e)}
        if isinstance(err, dict): err = err.get("code") or err.get("message") or str(err)
        fail(err)

# ---------- send policy (manually configured policy.json; the connector only reads it; absent = deny) ----------

def load_policy():
    f = os.path.join(cfg_dir(), "policy.json")
    try: return json.load(open(f))
    except FileNotFoundError: return {}
    except Exception as e: fail(f"policy.json parse failed: {e}")

def send_policy(account):
    p = load_policy().get(account) or {}
    return p.get("send", "deny"), p.get("auto_allow") or []

# ---------- provider & token renewal ----------

def P(account): return (load_tok(account) or {}).get("provider", "graph")

def refresh(account):
    """Return the graph/gmail access_token; for imap return the config dict itself."""
    tok = load_tok(account)
    if not tok: fail("not_authorized")
    if tok.get("provider") == "imap": return tok
    if tok.get("expires_at", 0) > time.time() + 60: return tok["access_token"]
    if tok.get("provider") == "gmail":
        creds = gcp_creds()
        data = {"client_id": creds["client_id"], "grant_type": "refresh_token",
                "refresh_token": tok["refresh_token"]}
        if creds.get("client_secret"): data["client_secret"] = creds["client_secret"]
        nt = http("https://oauth2.googleapis.com/token", data)
    else:
        from . import graph
        nt = http("https://login.microsoftonline.com/common/oauth2/v2.0/token", {
            "client_id": graph.CLIENT_ID, "grant_type": "refresh_token",
            "refresh_token": tok["refresh_token"],
            "scope": tok.get("scope") or graph.READ_SCOPE})
    nt.setdefault("provider", tok.get("provider", "graph"))
    nt["expires_at"] = time.time() + nt.get("expires_in", 3600)
    nt["account"] = tok.get("account")
    if tok.get("scope"): nt.setdefault("scope", tok["scope"])  # preserve the originally granted surface (response may lack scope)
    save_tok(account, nt)
    return nt["access_token"]

# ---------- view utilities ----------

def strip_html(h):
    h = re.sub(r"(?is)<(script|style).*?>.*?</\1>", "", h)
    h = re.sub(r"(?i)<br\s*/?>", "\n", h)
    h = re.sub(r"(?i)</(p|div|tr|li|h[1-6])>", "\n", h)
    h = re.sub(r"<[^>]+>", "", h)
    import html as H
    h = H.unescape(h)
    return re.sub(r"\n{3,}", "\n\n", h).strip()

def build_mime(to, cc, subject, body, html=False, attach_paths=None):
    msg = email.message.EmailMessage(email.policy.SMTP)
    if to: msg["To"] = to
    if cc: msg["Cc"] = cc
    msg["Subject"] = subject
    msg.set_content(body, subtype="html" if html else "plain")
    for path in attach_paths or []:
        data = open(path, "rb").read()
        maintype, subtype = (mimetypes.guess_type(path)[0] or "application/octet-stream").split("/")
        msg.add_attachment(data, maintype=maintype, subtype=subtype, filename=os.path.basename(path))
    return msg

def sender_of(from_header):
    m = re.search(r"<([^>]+)>", from_header or "") or re.search(r"(\S+@\S+)", from_header or "")
    return m.group(1) if m else (from_header or "")
