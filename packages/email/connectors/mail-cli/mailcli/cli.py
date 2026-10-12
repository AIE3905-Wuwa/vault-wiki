"""CLI: argument parsing and provider dispatch."""
import argparse, json, os, sys
from . import graph, gmail, imapc
from .common import (out, fail, cfg_dir, cfg_path, load_tok, save_tok,
                     refresh, P, send_policy)

def _impl(account):
    return {"graph": graph, "gmail": gmail, "imap": imapc}[P(account)]

# ---------- commands ----------

def cmd_auth(args):
    provider = getattr(args, "provider", None) or "graph"
    if args.act == "setup":
        if provider != "imap": fail("setup is only for imap (graph/gmail use start)")
        save_tok(args.account, {"provider": "imap", "account": args.user, "user": args.user,
                                "auth_code": args.auth_code,
                                "imap_host": args.imap_host, "smtp_host": args.smtp_host})
        os.chmod(cfg_path(args.account), 0o600)
        out({"ok": True, "provider": "imap", "account": args.user})
    elif args.act == "start":
        (gmail if provider == "gmail" else graph).auth_start(args)
    elif args.act == "complete":
        graph.auth_complete(args)  # gmail completes in one step via loopback, no complete
    elif args.act == "status":
        tok = load_tok(args.account)
        out({"ok": bool(tok), "provider": (tok or {}).get("provider", "graph"),
             "account": (tok or {}).get("account")})

def cmd_profiles(_):
    accs = []
    for f in sorted(os.listdir(cfg_dir())):
        if f.endswith(".json") and not f.endswith(".pending.json") and f[:-5] not in ("gcp", "policy"):
            tok = load_tok(f[:-5])
            accs.append({"account": f[:-5], "address": (tok or {}).get("account"),
                         "provider": (tok or {}).get("provider", "graph"),
                         "authorized": bool(tok)})
    out({"ok": True, "count": len(accs), "profiles": accs})

def cmd_folders(args):
    _impl(args.account).folders(args, refresh(args.account))

def cmd_fetch(args):
    _impl(args.account).fetch(args, refresh(args.account))

def cmd_read(args):
    _impl(args.account).read(args, refresh(args.account))

def cmd_search(args):
    _impl(args.account).search(args, refresh(args.account))

def cmd_attach(args):
    _impl(args.account).attach(args, refresh(args.account))

def cmd_draft(args):
    _impl(args.account).draft(args, refresh(args.account))

def cmd_send(args):
    at = refresh(args.account)
    impl = _impl(args.account)
    mode, allow = send_policy(args.account)
    if mode == "deny": fail("send_denied_by_policy")
    if P(args.account) == "graph": graph.need_write(args.account)  # reject early under read-only credentials
    if P(args.account) == "imap":
        imsg, s = impl.send_summary(at, args.id)
        do = lambda: impl.send_do(at, args.id, imsg)
    else:
        s = impl.send_summary(at, args.id)
        do = lambda: impl.send_do(at, args.id)
    if not s["to"]: fail("draft has no recipients")
    eff = mode
    if eff == "auto" and allow and not all(a in allow for a in s["to"]): eff = "confirm"
    summary = {"account": args.account, "address": (load_tok(args.account) or {}).get("account"),
               "subject": s["subject"], "to": s["to"], "cc": s["cc"], "attachments": s["attachments"]}
    if eff == "confirm" and not args.yes:
        if not sys.stdin.isatty(): fail("confirmation_required (non-interactive requires --yes, meaning the user has already explicitly consented in conversation)")
        print(json.dumps({"ok": True, "will_send": summary}, ensure_ascii=False), file=sys.stderr)
        if input("Send the above? Type yes to confirm: ").strip() != "yes": fail("aborted_by_user")
    do()
    out({"ok": True, "sent": summary, "message_id": args.id,
         "note": "copy is in the Sent folder"})

# ---------- arguments ----------

def main():
    ap = argparse.ArgumentParser(prog="mail-cli")
    sp = ap.add_subparsers(dest="cmd", required=True)

    a = sp.add_parser("auth"); asp = a.add_subparsers(dest="act", required=True)
    for act in ("start", "complete", "status", "setup"):
        p = asp.add_parser(act); p.add_argument("--account", required=True)
        if act == "start":
            p.add_argument("--provider", choices=["graph", "gmail"], default="graph")
            p.add_argument("--send", action="store_true",
                           help="request the broad scope including write/send (default is Mail.Read read-only only — the read-only surface usually needs no admin approval)")
        if act == "setup":
            p.add_argument("--provider", default="imap")
            p.add_argument("--user", required=True); p.add_argument("--auth-code", required=True)
            p.add_argument("--imap-host", default="imap.163.com"); p.add_argument("--smtp-host", default="smtp.163.com")

    sp.add_parser("profiles")

    f = sp.add_parser("folders"); f.add_argument("--account", required=True); f.add_argument("--all", action="store_true")

    f = sp.add_parser("fetch"); f.add_argument("--account", required=True)
    f.add_argument("--folder", default="inbox")
    f.add_argument("--since"); f.add_argument("--days", type=int, default=None)
    f.add_argument("--from", dest="from_addr"); f.add_argument("--unread", action="store_true")
    f.add_argument("--headers", action="store_true")
    f.add_argument("--limit", type=int, default=30); f.add_argument("--next")

    r = sp.add_parser("read"); r.add_argument("--account", required=True)
    r.add_argument("--id", required=True); r.add_argument("--text", action="store_true")

    s = sp.add_parser("search"); s.add_argument("--account", required=True)
    s.add_argument("--query", required=True); s.add_argument("--folder"); s.add_argument("--limit", type=int, default=10)

    t = sp.add_parser("attach"); tsp = t.add_subparsers(dest="act", required=True)
    for act in ("ls", "get"):
        p = tsp.add_parser(act); p.add_argument("--account", required=True); p.add_argument("--id", required=True)
        if act == "ls": continue
        p.add_argument("--att", required=True); p.add_argument("--dest", required=True); p.add_argument("--name")

    dr = sp.add_parser("draft"); dsp = dr.add_subparsers(dest="act", required=True)
    for act in ("create", "list", "show", "delete"):
        p = dsp.add_parser(act); p.add_argument("--account", required=True)
        if act == "create":
            p.add_argument("--to"); p.add_argument("--cc")
            p.add_argument("--subject", default="")
            p.add_argument("--body"); p.add_argument("--body-file")
            p.add_argument("--html", action="store_true")
            p.add_argument("--attach", action="append"); p.add_argument("--reply-to")
        elif act != "list": p.add_argument("--id", required=True)
        if act == "list": p.add_argument("--limit", type=int, default=20)

    s = sp.add_parser("send"); s.add_argument("--account", required=True)
    s.add_argument("--id", required=True); s.add_argument("--yes", action="store_true")

    args = ap.parse_args()
    {"auth": cmd_auth, "profiles": cmd_profiles, "folders": cmd_folders,
     "fetch": cmd_fetch, "read": cmd_read, "search": cmd_search, "attach": cmd_attach,
     "draft": cmd_draft, "send": cmd_send}[args.cmd](args)
