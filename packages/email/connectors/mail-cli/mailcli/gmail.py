"""Gmail API provider (loopback auth flow — device flow does not grant Gmail scopes; measured invalid_scope).

Auth needs an ssh -L <port>:localhost:<port> tunnel so the browser callback reaches this machine directly.
"""
import base64, os, re, threading, time, urllib.parse
from datetime import datetime, timezone
from .common import GMAIL, GMAIL_SCOPE, gcp_creds, out, fail, http, save_tok, strip_html, build_mime, sender_of

def b64u(s): return base64.urlsafe_b64encode(s).decode().rstrip("=")
def b64u_dec(s): return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))

# ---------- auth ----------

def auth_start(args):
    """loopback: a temporary local HTTP service receives the callback."""
    from http.server import BaseHTTPRequestHandler, HTTPServer
    import socket
    creds = gcp_creds()
    s = socket.socket(); s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]; s.close()
    box = {}
    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            box["code"] = (q.get("code") or [None])[0]; box["error"] = (q.get("error") or [None])[0]
            self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("<html><body><h3>Authorization successful; you may close this page and return to the terminal</h3></body></html>".encode())
        def log_message(*a): pass
    srv = HTTPServer(("127.0.0.1", port), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    url = ("https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
        "client_id": creds["client_id"], "redirect_uri": f"http://localhost:{port}",
        "response_type": "code", "scope": GMAIL_SCOPE, "access_type": "offline",
        "prompt": "consent"}))
    out({"ok": True, "flow": "loopback", "auth_url": url,
         "hint": f"First run ssh -L {port}:localhost:{port} april@<this machine> on the accessing side, then open auth_url in a browser"})
    deadline = time.time() + 900
    while time.time() < deadline and not box.get("code") and not box.get("error"):
        time.sleep(1)
    srv.shutdown()
    if box.get("error"): fail(box["error"])
    if not box.get("code"): fail("timeout (no callback received within 900 seconds)")
    _exchange(args.account, box["code"], f"http://localhost:{port}", creds)

def _exchange(account, code, redirect_uri, creds):
    tok = http("https://oauth2.googleapis.com/token", {
        "client_id": creds["client_id"], "client_secret": creds["client_secret"],
        "code": code, "grant_type": "authorization_code", "redirect_uri": redirect_uri})
    tok["provider"] = "gmail"
    tok["expires_at"] = time.time() + tok.get("expires_in", 3600)
    me = http(f"{GMAIL}/profile", tok=tok["access_token"])
    tok["account"] = me.get("emailAddress")
    save_tok(account, tok)
    out({"ok": True, "provider": "gmail", "account": tok["account"]})

# ---------- views ----------

def headers(m):
    return {h["name"].lower(): h["value"] for h in (m.get("payload") or {}).get("headers", [])}

def body_text(m):
    def walk(part):
        if part.get("mimeType") == "text/plain" and part.get("body", {}).get("data"):
            return b64u_dec(part["body"]["data"]).decode("utf-8", "replace"), "text"
        if part.get("mimeType") == "text/html" and part.get("body", {}).get("data"):
            return b64u_dec(part["body"]["data"]).decode("utf-8", "replace"), "html"
        for c in part.get("parts", []):
            r = walk(c)
            if r: return r
        return None
    return walk(m.get("payload") or {}) or ("", "text")

def form(m, with_headers=False):
    h = headers(m)
    d = {"id": m["id"], "conversation": m.get("threadId"),
         "received": m.get("internalDate") and datetime.fromtimestamp(
             int(m["internalDate"]) / 1000, tz=timezone.utc).isoformat(),
         "from": sender_of(h.get("from")),
         "subject": h.get("subject"),
         "unread": "UNREAD" in (m.get("labelIds") or []),
         "preview": m.get("snippet", "")[:200]}
    if with_headers:
        d["message_id"] = h.get("message-id")
        if h.get("references"): d["references"] = h["references"]
    return d

def meta(mid, tok, extra_headers=False):
    hs = ["Message-ID", "References", "Subject", "From", "Date"] if extra_headers else None
    q = "?format=metadata" + ("&metadataHeaders=" + "&metadataHeaders=".join(
        urllib.parse.quote(h) for h in hs) if hs else "")
    return http(f"{GMAIL}/messages/{mid}{q}", tok=tok)

def label_id(name, tok):
    if name in ("inbox", "INBOX"): return "INBOX"
    for lb in http(f"{GMAIL}/labels", tok=tok).get("labels", []):
        if lb["name"].lower() == name.lower() or lb["id"] == name: return lb["id"]
    fail(f"label not found: {name}")

def parts(m):
    r = []
    def walk(p):
        if p.get("filename") or p.get("attachmentId"): r.append(p)
        for c in p.get("parts", []): walk(c)
    walk(m.get("payload") or {})
    return r

# ---------- command implementations ----------

def folders(args, at):
    labels = http(f"{GMAIL}/labels", tok=at).get("labels", [])
    out({"ok": True, "count": len(labels),
         "folders": [{"id": l["id"], "name": l["name"], "system": l.get("type") == "system"}
                     for l in labels]})

def fetch(args, at):
    q = []
    if args.folder: q.append(f"in:{label_id(args.folder, at)}")
    else: q.append("in:inbox")
    if args.since:
        d = datetime.strptime(args.since, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        q.append(f"after:{int(d.timestamp())}")
    elif args.days is not None:
        q.append(f"after:{int(time.time()) - args.days * 86400}")
    if args.from_addr: q.append(f"from:{args.from_addr}")
    if args.unread: q.append("is:unread")
    url = args.next or (f"{GMAIL}/messages?maxResults={args.limit}&q=" + urllib.parse.quote(" ".join(q)))
    lst = http(url, tok=at)
    msgs = [form(meta(m["id"], at, args.headers), args.headers) for m in lst.get("messages", [])]
    out({"ok": True, "count": len(msgs), "next": lst.get("nextPageToken") and
         f"{GMAIL}/messages?maxResults={args.limit}&pageToken={lst['nextPageToken']}&q=" +
         urllib.parse.quote(" ".join(q)), "messages": msgs})

def read(args, at):
    m = http(f"{GMAIL}/messages/{urllib.parse.quote(args.id)}", tok=at)
    body, kind = body_text(m)
    if kind == "html": body = strip_html(body)
    h = headers(m)
    out({"ok": True, "subject": h.get("subject"), "from": h.get("from"),
         "received": m.get("internalDate"), "message_id": h.get("message-id"),
         "references": h.get("references"), "body": body[:8000]})

def search(args, at):
    lst = http(f"{GMAIL}/messages?maxResults={args.limit}&q=" + urllib.parse.quote(args.query), tok=at)
    msgs = [form(meta(m["id"], at), False) for m in lst.get("messages", [])]
    out({"ok": True, "count": len(msgs), "messages": msgs})

def attach(args, at):
    m = http(f"{GMAIL}/messages/{urllib.parse.quote(args.id)}", tok=at)
    if args.act == "ls":
        atts = [{"id": p.get("attachmentId") or p["body"].get("attachmentId"),
                 "name": p.get("filename"), "size": p.get("body", {}).get("size"),
                 "mime": p.get("mimeType"), "inline": p.get("mimeType", "").startswith("image/")}
                for p in parts(m) if p.get("filename")]
        out({"ok": True, "count": len(atts), "attachments": atts})
    else:
        a = http(f"{GMAIL}/messages/{urllib.parse.quote(args.id)}/attachments/"
                 f"{urllib.parse.quote(args.att, safe='')}", tok=at)
        data = b64u_dec(a["data"])
        os.makedirs(args.dest, exist_ok=True)
        path = os.path.join(args.dest, os.path.basename(args.name or a.get("filename") or "attachment.bin"))
        open(path, "wb").write(data)
        out({"ok": True, "saved": path, "bytes": len(data)})

def draft(args, at):
    if args.act == "create":
        if not args.to and not args.reply_to: fail("--to or --reply-to required")
        body = open(args.body_file).read() if args.body_file else (args.body or "")
        if not body and not args.attach: fail("body is empty (--body / --body-file) and there are no attachments")
        msg = build_mime(args.to, args.cc, args.subject, body, args.html, args.attach)
        thread_id = None
        if args.reply_to:
            orig = http(f"{GMAIL}/messages/{urllib.parse.quote(args.reply_to)}", tok=at)
            oh = headers(orig)
            if not args.subject:
                subj = oh["subject"] or ""
                msg.replace_header("Subject", subj if subj.lower().startswith("re:") else "Re: " + subj)
            msg["In-Reply-To"] = oh.get("message-id", "")
            if oh.get("references"): msg["References"] = oh["references"]
            elif oh.get("message-id"): msg["References"] = oh["message-id"]
            if not args.to: msg["To"] = sender_of(oh.get("from")) or fail("original message From cannot be parsed")
            thread_id = orig.get("threadId")
        payload = {"message": {"raw": b64u(msg.as_bytes()),
                               **({"threadId": thread_id} if thread_id else {})}}
        d = http(f"{GMAIL}/drafts", tok=at, method="POST", jdata=payload)
        out({"ok": True, "draft_id": d["id"], "subject": args.subject, "to": args.to})
    elif args.act == "list":
        d = http(f"{GMAIL}/drafts?maxResults={args.limit}", tok=at)
        ds = [{"id": x["id"], "subject": headers(x.get("message", {})).get("subject")}
              for x in d.get("drafts", [])]
        out({"ok": True, "count": len(ds), "drafts": ds})
    elif args.act == "show":
        d = http(f"{GMAIL}/drafts/{urllib.parse.quote(args.id)}", tok=at)
        m = d.get("message", {})
        bd = m.get("payload", {}).get("body", {}).get("data")
        body = b64u_dec(bd).decode("utf-8", "replace") if bd else ""
        h = headers(m)
        out({"ok": True, "id": d["id"], "subject": h.get("subject"), "to": h.get("to"),
             "cc": h.get("cc"), "body": body,
             "attachments": [p.get("filename") for p in parts(m)]})
    elif args.act == "delete":
        http(f"{GMAIL}/drafts/{urllib.parse.quote(args.id)}", tok=at, method="DELETE")
        out({"ok": True, "deleted": args.id})

def send_summary(at, draft_id):
    d = http(f"{GMAIL}/drafts/{urllib.parse.quote(draft_id)}", tok=at)
    m = d.get("message", {}); h = headers(m)
    return {"subject": h.get("subject"),
            "to": [x.strip() for x in (h.get("to") or "").split(",") if x.strip()],
            "cc": [x.strip() for x in (h.get("cc") or "").split(",") if x.strip()],
            "attachments": [{"name": p.get("filename")} for p in parts(m)]}

def send_do(at, draft_id):
    http(f"{GMAIL}/drafts/{urllib.parse.quote(draft_id)}/send", tok=at, method="POST", jdata={})
