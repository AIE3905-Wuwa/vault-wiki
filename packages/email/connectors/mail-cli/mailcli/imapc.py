"""IMAP/SMTP provider (163 etc., authorization-code login).

Pitfalls (measured): 163 requires sending IMAP ID to self-identify, otherwise select reports Unsafe Login;
Chinese folder names are modified UTF-7; imaplib parameters are ascii-only, so Chinese searches fall back to client-side filtering.
"""
import base64, email, email.policy, os, re
from datetime import datetime, timedelta
from .common import out, fail, strip_html, build_mime, sender_of

# ---------- connection ----------

def conn(cfg):
    import imaplib
    imaplib.Commands["ID"] = ("NONAUTH", "AUTH", "SELECTED", "LOGOUT")  # RFC 2971
    c = imaplib.IMAP4_SSL(cfg["imap_host"])
    c.login(cfg["user"], cfg["auth_code"])
    try: c.enable("UTF8=ACCEPT")
    except Exception: pass
    try:  # 163 requires IMAP ID self-identification
        c._simple_command("ID", '("name" "mail-cli" "version" "1.0" "vendor" "vault-wiki")')
        c._untagged_response("OK", None, "ID")
    except Exception: pass
    return c

def utf7_decode(s):
    """IMAP modified UTF-7 -> utf-8 (163 Chinese folder names)."""
    res, i = [], 0
    while i < len(s):
        if s[i] == "&":
            j = s.find("-", i + 1)
            if j == -1: res.append(s[i:]); break
            if j == i + 1: res.append("&")
            else:
                b = s[i + 1:j].replace(",", "/")
                res.append(base64.b64decode(b + "=" * (-len(b) % 4)).decode("utf-16-be"))
            i = j + 1
        else:
            res.append(s[i]); i += 1
    return "".join(res)

def find_folder(c, want):
    """Find a folder by special attribute or common name (returns the raw wire name; Chinese ones are modified UTF-7)."""
    typ, data = c.list()
    marks = {"drafts": "\\Drafts", "sent": "\\Sent"}
    names = {"drafts": ["草稿箱", "Drafts"], "sent": ["已发送", "Sent"],
             "inbox": ["INBOX"]}.get(want, [want])
    for line in data or []:
        if not line: continue
        seg = line.decode("utf-8", "replace")
        wire = seg.rsplit('"', 2)[-2]
        if want in marks and marks[want] in seg:
            return wire
        try: disp = utf7_decode(wire)
        except Exception: disp = wire
        for n in names:
            if disp == n: return wire
    return None

def draft_folder(c):
    f = find_folder(c, "drafts")
    if not f: fail("drafts folder not found (look up its name via folders)")
    return f

# ---------- views ----------

def parse(raw):
    return email.message_from_bytes(raw, policy=email.policy.default)

def body(m, plain=True):
    if m.is_multipart():
        html_part = None
        for p in m.walk():
            ct = p.get_content_type()
            if plain and ct == "text/plain" and not p.is_multipart():
                return p.get_content()
            if ct == "text/html": html_part = p.get_content()
        return strip_html(html_part) if html_part else ""
    return m.get_content()

def view(m, preview=False):
    frm = m.get("From") or ""
    d = {"id": m.get("Message-ID", ""), "received": m.get("Date") or "",
         "from": sender_of(frm), "subject": m.get("Subject") or "", "unread": None}
    if preview:
        d["preview"] = body(m)[:200]
    else:
        d["message_id"] = m.get("Message-ID"); d["references"] = m.get("References")
        d["body"] = body(m)[:8000]
    return d

def crit(args):
    c = []
    if args.since:
        d = datetime.strptime(args.since, "%Y-%m-%d")
        c.append(f'SINCE {d.strftime("%d-%b-%Y")}')
    elif getattr(args, "days", None) is not None:
        since = datetime.now() - timedelta(days=args.days)
        c.append(f'SINCE {since.strftime("%d-%b-%Y")}')
    if getattr(args, "unread", False): c.append("UNSEEN")
    fa = getattr(args, "from_addr", None)
    if fa: c.append(f'FROM "{fa}"')
    return " ".join(c) or "ALL"

# ---------- command implementations ----------

def folders(args, cfg):
    c = conn(cfg)
    try:
        typ, data = c.list()
        out({"ok": True, "count": len(data or []),
             "folders": [{"name": utf7_decode(l.decode("utf-8", "replace").rsplit('"', 2)[-2])
                          if (l or b"").count(b'"') >= 2 else l.decode("utf-8", "replace")}
                         for l in data if l]})
    finally: c.logout()

def fetch(args, cfg):
    c = conn(cfg)
    try:
        c.select(args.folder if args.folder != "inbox" else "INBOX", readonly=True)
        typ, data = c.uid("search", None, crit(args))
        uids = (data[0].split() if data and data[0] else [])[-args.limit:][::-1]
        msgs = []
        for uid in uids:
            typ, d = c.uid("fetch", uid, "(BODY.PEEK[HEADER.FIELDS (SUBJECT FROM DATE MESSAGE-ID REFERENCES)] BODY.PEEK[TEXT]<0.300>)")
            if not d or not d[0]: continue
            m = parse(d[0][1])
            v = view(m, preview=True); v["id"] = uid.decode()
            if args.headers:
                v["message_id"] = m.get("Message-ID"); v["references"] = m.get("References")
            msgs.append(v)
        out({"ok": True, "count": len(msgs), "next": None, "messages": msgs})
    finally: c.logout()

def read(args, cfg):
    c = conn(cfg)
    try:
        c.select(find_folder(c, "inbox") or "INBOX", readonly=True)
        typ, d = c.uid("fetch", args.id.encode(), "(BODY.PEEK[])")
        v = view(parse(d[0][1])); v["id"] = args.id
        out({"ok": True, **v})
    finally: c.logout()

def search(args, cfg):
    c = conn(cfg)
    try:
        c.select("INBOX", readonly=True)
        crit_ = f'TEXT "{args.query}"' if args.query.isascii() else "ALL"
        typ, data = c.uid("search", None, crit_)
        uids = (data[0].split() if data and data[0] else [])[-200:]
        msgs = []
        for uid in uids[::-1]:
            typ, d = c.uid("fetch", uid, "(BODY.PEEK[HEADER.FIELDS (SUBJECT FROM DATE)])")
            if not d or not d[0]: continue
            m = parse(d[0][1])
            if not args.query.isascii() and args.query not in (m.get("Subject") or "") + (m.get("From") or ""):
                continue
            v = view(m, preview=True); v["id"] = uid.decode()
            msgs.append(v)
            if len(msgs) >= args.limit: break
        out({"ok": True, "count": len(msgs), "messages": msgs})
    finally: c.logout()

def attach(args, cfg):
    c = conn(cfg)
    try:
        c.select(find_folder(c, "inbox") or "INBOX", readonly=True)
        typ, d = c.uid("fetch", args.id.encode(), "(BODY.PEEK[])")
        m = parse(d[0][1])
        parts = [p for p in m.walk() if p.get_filename()]
        if args.act == "ls":
            out({"ok": True, "count": len(parts),
                 "attachments": [{"id": p.get_filename(), "name": p.get_filename(),
                                  "size": len(p.get_payload(decode=True) or b""),
                                  "mime": p.get_content_type(), "inline": False} for p in parts]})
        else:
            os.makedirs(args.dest, exist_ok=True)
            name = os.path.basename(args.name or args.att)
            for p in parts:
                if p.get_filename() == args.att:
                    data = p.get_payload(decode=True)
                    open(os.path.join(args.dest, name), "wb").write(data)
                    out({"ok": True, "saved": os.path.join(args.dest, name), "bytes": len(data)})
                    return
            fail(f"attachment not found: {args.att}")
    finally: c.logout()

def draft(args, cfg):
    c = conn(cfg)
    try:
        if args.act == "create":
            if not args.to and not args.reply_to: fail("--to or --reply-to required")
            text = open(args.body_file).read() if args.body_file else (args.body or "")
            msg = build_mime(args.to, args.cc, args.subject, text, args.html, args.attach)
            if args.reply_to:
                c.select(find_folder(c, "inbox") or "INBOX", readonly=True)
                typ, d = c.uid("search", None, f'HEADER MESSAGE-ID "{args.reply_to}"')
                if d and d[0]:
                    typ, dd = c.uid("fetch", d[0].split()[-1], "(BODY.PEEK[HEADER.FIELDS (SUBJECT FROM MESSAGE-ID REFERENCES)])")
                    orig = parse(dd[0][1])
                    if not args.subject:
                        msg.replace_header("Subject", "Re: " + (orig.get("Subject") or ""))
                    msg["In-Reply-To"] = orig.get("Message-ID", "")
                    refs = (orig.get("References") or "").strip()
                    new_refs = (refs + " " + (orig.get("Message-ID") or "")).strip()
                    if new_refs: msg["References"] = new_refs
                    if not args.to:
                        msg["To"] = sender_of(orig.get("From")) or fail("original message From cannot be parsed")
            df = draft_folder(c)
            c.append(df, "\\Seen", None, msg.as_bytes())
            typ, _ = c.select(df)
            typ, dd = c.uid("search", None, "ALL")
            uids = dd[0].split() if dd and dd[0] else []
            out({"ok": True, "draft_id": uids[-1].decode() if uids else None,
                 "subject": args.subject, "to": args.to})
        else:
            df = draft_folder(c)
            c.select(df, readonly=(args.act != "delete"))  # delete needs read-write access to expunge
            if args.act == "list":
                typ, data = c.uid("search", None, "ALL")
                uids = (data[0].split() if data and data[0] else [])[-args.limit:][::-1]
                ds = []
                for uid in uids:
                    typ, dd = c.uid("fetch", uid, "(BODY.PEEK[HEADER.FIELDS (SUBJECT TO)])")
                    m = parse(dd[0][1])
                    ds.append({"id": uid.decode(), "subject": m.get("Subject"), "to": m.get("To")})
                out({"ok": True, "count": len(ds), "drafts": ds})
            elif args.act == "show":
                typ, dd = c.uid("fetch", args.id.encode(), "(BODY.PEEK[])")
                m = parse(dd[0][1])
                out({"ok": True, "id": args.id, "subject": m.get("Subject"), "to": m.get("To"),
                     "cc": m.get("Cc"), "body": body(m),
                     "attachments": [p.get_filename() for p in m.walk() if p.get_filename()]})
            elif args.act == "delete":
                c.uid("store", args.id.encode(), "+FLAGS", "(\\Deleted)"); c.expunge()
                out({"ok": True, "deleted": args.id})
    finally: c.logout()

def send_summary(cfg, draft_id):
    c = conn(cfg)
    try:
        df = draft_folder(c)
        c.select(df, readonly=True)
        typ, dd = c.uid("fetch", draft_id.encode(), "(BODY.PEEK[])")
        m = parse(dd[0][1])
        return m, {"subject": m.get("Subject"),
                   "to": [x.strip() for x in (m.get("To") or "").split(",") if x.strip()],
                   "cc": [x.strip() for x in (m.get("Cc") or "").split(",") if x.strip()],
                   "attachments": [{"name": p.get_filename()} for p in m.walk() if p.get_filename()]}
    finally: c.logout()

def send_do(cfg, draft_id, m):
    import smtplib
    raw = m.as_bytes()
    sm = smtplib.SMTP_SSL(cfg["smtp_host"], 465)
    try:
        sm.login(cfg["user"], cfg["auth_code"])
        sm.sendmail(cfg["user"],
                    [x for x in (m.get("To") or "").split(",") if x.strip()], raw)
    finally: sm.quit()
    c = conn(cfg)
    try:
        sent = find_folder(c, "sent")
        if sent: c.append(sent, None, None, raw)
        c.select(draft_folder(c))
        c.uid("store", draft_id.encode(), "+FLAGS", "(\\Deleted)"); c.expunge()
    finally: c.logout()
