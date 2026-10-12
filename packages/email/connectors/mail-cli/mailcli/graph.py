"""Microsoft Graph provider (school/office accounts, device flow)."""
import base64, json, os, sys, time, urllib.parse, urllib.error
from datetime import datetime, timedelta, timezone
from .common import GRAPH, out, fail, http, load_tok, save_tok, cfg_path, strip_html

TENANT = "common"
CLIENT_ID = "14d82eec-204b-4c2f-b7e8-296a70dab67e"  # public Microsoft Graph PowerShell client
# Least privilege: by default only read-only scopes are requested (admin approval usually only blocks
# consent surfaces that include write/send); write/send scopes must be explicitly requested via
# auth start --send — that is when tenant admin approval may be triggered.
READ_SCOPE = "Mail.Read offline_access"
FULL_SCOPE = "Mail.Read Mail.ReadWrite Mail.Send offline_access"

def scope_of(tok):
    """The set of scopes the token actually holds (Graph token responses carry a scope field; old credentials without it fall back to the full set, for compatible judgment)."""
    return set((tok.get("scope") or FULL_SCOPE).split())

def need_write(account):
    if not {"Mail.ReadWrite", "Mail.Send"} <= scope_of(load_tok(account) or {}):
        fail(f"token_read_only (current credentials are read-only; for drafts/sending re-authorize with auth start --account {account} "
             "--send — the broad scope may trigger tenant admin approval)")

# ---------- auth ----------

def auth_start(args):
    scope = FULL_SCOPE if getattr(args, "send", False) else READ_SCOPE
    d = http(f"https://login.microsoftonline.com/{TENANT}/oauth2/v2.0/devicecode",
             {"client_id": CLIENT_ID, "scope": scope})
    save_tok(args.account + ".pending",
            {"device_code": d["device_code"], "interval": d.get("interval", 5),
             "provider": "graph", "scope": scope})
    out({"ok": True, "verification_url": d.get("verification_url") or d.get("verification_uri"),
         "user_code": d["user_code"], "expires_in": d.get("expires_in", 900)})

def auth_complete(args):
    pend = load_tok(args.account + ".pending")
    if not pend: fail("no_pending_start")
    deadline = time.time() + 900
    while time.time() < deadline:
        try:
            tok = http(f"https://login.microsoftonline.com/{TENANT}/oauth2/v2.0/token", {
                "client_id": CLIENT_ID,
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                "device_code": pend["device_code"], "scope": pend.get("scope", READ_SCOPE)}, raise_err=True)
        except urllib.error.HTTPError as e:
            err = json.loads(e.read()).get("error")
            if err == "authorization_pending": time.sleep(pend.get("interval", 5))
            else: fail(err)
            continue
        tok["provider"] = "graph"
        tok["expires_at"] = time.time() + tok.get("expires_in", 3600)
        try:
            me = http(f"{GRAPH}/me", tok=tok["access_token"])
            tok["account"] = me.get("userPrincipalName")
        except SystemExit: pass
        save_tok(args.account, tok)
        os.remove(cfg_path(args.account + ".pending"))
        out({"ok": True, "provider": "graph", "account": tok.get("account")})
        return
    fail("timeout")

# ---------- views ----------

def hdrs(m):
    hs = m.get("internetMessageHeaders") or []
    return {h["name"].lower(): h["value"] for h in hs if h.get("name")}

def form(m, with_headers=False):
    d = {"id": m["id"], "conversation": m.get("conversationId"),
         "received": m.get("receivedDateTime"),
         "from": (m.get("from") or {}).get("emailAddress", {}).get("address"),
         "subject": m.get("subject"), "unread": not m.get("isRead", True),
         "preview": m.get("bodyPreview", "")[:200]}
    if with_headers:
        h = hdrs(m)
        d["message_id"] = h.get("message-id")
        if h.get("references"): d["references"] = h["references"]
    return d

def rcpt_list(s):
    return [{"emailAddress": {"address": a.strip()}} for a in (s or "").split(",") if a.strip()]

def draft_view(d):
    return {"id": d["id"], "subject": d.get("subject"),
            "to": [r.get("emailAddress", {}).get("address") for r in d.get("toRecipients", [])],
            "cc": [r.get("emailAddress", {}).get("address") for r in d.get("ccRecipients", [])],
            "body": d.get("body", {}).get("content", ""),
            "attachments": [{"name": a.get("name"), "size": a.get("size")} for a in d.get("attachments", [])]}

# ---------- command implementations ----------

def folders(args, at):
    def walk(parent=None, depth=0, max_depth=1):
        q = "$top=50"
        base = (f"{GRAPH}/me/mailFolders?{q}" if parent is None
                else f"{GRAPH}/me/mailFolders/{urllib.parse.quote(parent)}/childFolders?{q}")
        res = []
        for f in http(base, tok=at).get("value", []):
            res.append({"id": f["id"], "name": f["displayName"], "path": f["displayName"],
                        "unread": f.get("unreadItemCount", 0), "total": f.get("totalItemCount", 0),
                        "children": f.get("childFolderCount", 0)})
            if depth < max_depth and f.get("childFolderCount"):
                for c in walk(f["id"], depth + 1, max_depth):
                    c["path"] = f"{f['displayName']}/{c['path']}"
                    res.append(c)
        return res
    fs = walk(max_depth=99 if args.all else 1)
    out({"ok": True, "count": len(fs), "folders": fs})

def fetch(args, at):
    filt = []
    if args.since:
        s = args.since if "T" in args.since else f"{args.since}T00:00:00Z"
        filt.append(f"receivedDateTime ge {s}")
    elif args.days is not None:
        since = (datetime.now(timezone.utc) - timedelta(days=args.days)).strftime("%Y-%m-%dT%H:%M:%SZ")
        filt.append(f"receivedDateTime ge {since}")
    if args.unread: filt.append("isRead eq false")
    if args.from_addr and "@" in args.from_addr:
        filt.append(f"from/emailAddress/address eq '{args.from_addr}'")
    q = {"$top": args.limit, "$orderby": "receivedDateTime desc",
         "$select": ("id,conversationId,receivedDateTime,from,subject,bodyPreview,isRead"
                     + (",internetMessageHeaders" if args.headers else ""))}
    if filt: q["$filter"] = " and ".join(filt)
    url = args.next or f"{GRAPH}/me/mailFolders/{args.folder}/messages?{urllib.parse.urlencode(q)}"
    d = http(url, tok=at)
    msgs = [form(m, args.headers) for m in d.get("value", [])]
    if args.from_addr and "@" not in args.from_addr:  # substring matching falls back to the client side
        msgs = [m for m in msgs if (m["from"] or "").lower().find(args.from_addr.lower()) >= 0]
    out({"ok": True, "count": len(msgs), "next": d.get("@odata.nextLink"), "messages": msgs})

def read(args, at):
    d = http(f"{GRAPH}/me/messages/{urllib.parse.quote(args.id)}"
             f"?$select=id,subject,conversationId,body,internetMessageHeaders", tok=at)
    body = d.get("body", {}).get("content", "")
    if args.text and d.get("body", {}).get("contentType") == "html":
        body = strip_html(body)
    out({"ok": True, "subject": d.get("subject"),
         "from": (d.get("from") or {}).get("emailAddress", {}).get("address"),
         "received": d.get("receivedDateTime"),
         "message_id": hdrs(d).get("message-id"),
         "references": hdrs(d).get("references"),
         "body": body[:8000]})

def search(args, at):
    q = urllib.parse.quote(f'"{args.query}"')
    url = (f"{GRAPH}/me/mailFolders/{args.folder}/messages?$search={q}&$top={args.limit}"
           if args.folder else f"{GRAPH}/me/messages?$search={q}&$top={args.limit}")
    d = http(url, tok=at)
    out({"ok": True, "count": len(d.get("value", [])),
         "messages": [form(m) for m in d.get("value", [])]})

def attach(args, at):
    if args.act == "ls":
        d = http(f"{GRAPH}/me/messages/{urllib.parse.quote(args.id)}/attachments", tok=at)
        out({"ok": True, "count": len(d.get("value", [])),
             "attachments": [{"id": a["id"], "name": a.get("name"), "size": a.get("size"),
                              "mime": a.get("contentType"), "inline": a.get("isInline", False)}
                             for a in d.get("value", [])]})
    else:
        os.makedirs(args.dest, exist_ok=True)
        url = f"{GRAPH}/me/messages/{urllib.parse.quote(args.id)}/attachments/{urllib.parse.quote(args.att, safe='')}/$value"
        b = http(url, tok=at, binary=True)
        path = os.path.join(args.dest, os.path.basename(args.name or "attachment.bin"))
        open(path, "wb").write(b)
        out({"ok": True, "saved": path, "bytes": len(b)})

def draft(args, at):
    if args.act in ("create", "delete"): need_write(args.account)
    if args.act == "create":
        if not args.to and not args.reply_to: fail("--to or --reply-to required")
        body = open(args.body_file).read() if args.body_file else (args.body or "")
        if not body and not args.attach: fail("body is empty (--body / --body-file) and there are no attachments")
        payload = {"subject": args.subject,
                   "body": {"contentType": "html" if args.html else "text", "content": body}}
        if args.to: payload["toRecipients"] = rcpt_list(args.to)
        if args.cc: payload["ccRecipients"] = rcpt_list(args.cc)
        atts = []
        for path in args.attach or []:
            if not os.path.exists(path): fail(f"attachment not found: {path}")
            atts.append({"@odata.type": "#microsoft.graph.fileAttachment",
                         "name": os.path.basename(path),
                         "contentBytes": base64.b64encode(open(path, "rb").read()).decode()})
        if atts: payload["attachments"] = atts
        if args.reply_to:  # server-side createReply preserves the thread (References/Re: subject), then PATCH fills in the content
            d = http(f"{GRAPH}/me/messages/{urllib.parse.quote(args.reply_to)}/createReply",
                     tok=at, method="POST", jdata={})
            d = http(f"{GRAPH}/me/messages/{urllib.parse.quote(d['id'])}",
                     tok=at, method="PATCH", jdata=payload)
        else:
            d = http(f"{GRAPH}/me/messages", tok=at, method="POST", jdata=payload)
        out({"ok": True, "draft_id": d["id"], **{k: v for k, v in draft_view(d).items() if k != "id"}})
    elif args.act == "list":
        d = http(f"{GRAPH}/me/mailFolders/Drafts/messages?$top={args.limit}"
                 f"&$select=id,subject,toRecipients,lastModifiedDateTime", tok=at)
        out({"ok": True, "count": len(d.get("value", [])),
             "drafts": [{"id": m["id"], "subject": m.get("subject"),
                         "to": [r.get("emailAddress", {}).get("address") for r in m.get("toRecipients", [])],
                         "modified": m.get("lastModifiedDateTime")} for m in d.get("value", [])]})
    elif args.act == "show":
        d = http(f"{GRAPH}/me/messages/{urllib.parse.quote(args.id)}", tok=at)
        out({"ok": True, **draft_view(d)})
    elif args.act == "delete":
        http(f"{GRAPH}/me/messages/{urllib.parse.quote(args.id)}", tok=at, method="DELETE")
        out({"ok": True, "deleted": args.id})

def send_summary(at, draft_id):
    v = draft_view(http(f"{GRAPH}/me/messages/{urllib.parse.quote(draft_id)}", tok=at))
    return {"subject": v["subject"], "to": v["to"], "cc": v["cc"], "attachments": v["attachments"]}

def send_do(at, draft_id):
    http(f"{GRAPH}/me/messages/{urllib.parse.quote(draft_id)}/send", tok=at, method="POST", jdata={})
