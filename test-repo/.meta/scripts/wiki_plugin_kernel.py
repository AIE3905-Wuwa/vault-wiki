#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""vault-wiki plugin lifecycle mechanical kernel ((un)install / compliance / dependencies / injection / registry / copy sync).

Positioning (see .meta/protocol/actions.md execution principles): deterministic structural
operations go to this script; semantic judgment goes to the LLM. The script touches only
four places: plugin directories in and out, AGENTS.md injection-region marker blocks,
the registry.yaml plugin section, and .agents/skills/ command copies; the protocol /
reserved sections and handwritten regions are never touched.

Usage:
  python .meta/scripts/wiki_plugin_kernel.py ls          # list + dependencies
  python .meta/scripts/wiki_plugin_kernel.py validate    # compliance and dependency check (read-only, exit code 1 on errors)
  python .meta/scripts/wiki_plugin_kernel.py audit       # plugin attached audits (discovery-style execution of each plugin's scripts/check.py)
  python .meta/scripts/wiki_plugin_kernel.py inject      # rebuild AGENTS.md injection region, check inspection blocks and command usage blocks (idempotent)
  python .meta/scripts/wiki_plugin_kernel.py registry    # rebuild the registry.yaml plugin section (idempotent)
  python .meta/scripts/wiki_plugin_kernel.py deploy      # sync command and connector skill deployment copies (idempotent)
  python .meta/scripts/wiki_plugin_kernel.py all         # validate + inject + registry + deploy

The manifest is a minimal YAML subset: top-level `key: value`, `key: []`, block lists
(`  - item`), one-level field dicts (`  name: description`); double-quoted values are
unquoted; inline comments (starting with ` #`) are stripped.

Dependencies and injection order:
- depends declares behavioral or semantic dependencies (a bridging piece depending on the
  concept plugins at both ends is a semantic dependency); validate checks existence and acyclicity
- injection order = dependency topology (dependees injected first) + alphabetical within
  the same batch; no layering concept

Injection tier and budget (issue #12 layer discipline, see protocol/experiments.md):
- optional manifest field inject_tier (full|member, default full) — member exits the AGENTS.md
  injection region; exposure rides on the family root's roster line, the skill catalog, and
  L-layer reads (the manifest inject field stays the full-disclosure home either way)
- validate requires a member to reach a full-tier domain root through depends (family
  membership, else it exits into invisibility)
- the projected plugin blocks carry a byte budget (INJECT_BUDGET): over-budget is a validate
  error (compress pointer lines or re-tier domain members) the region under budget

Command-plugin binding (mutual declaration, validate checks consistency):
- command frontmatter adds owner: plugin id (multiple as an [a, b] list) or framework
  (cross-cutting, explicitly ownerless)
- plugin manifest adds the optional field commands: list of command names this plugin drives
- error cases: command missing owner, owner pointing at an uninstalled plugin, framework
  combined with other owners, plugin declaring a nonexistent command, one-sided declaration
  on either side (owner not claimed by commands, or the reverse)

Command injection (the third projection: plugin write-side contract -> command):
- command frontmatter adds optional consumes: list of plugin ids whose write-side contract
  it consumes (pull side, destination declaration); owner-driven commands must fill it in
  and include all owners
- manifest adds optional usage_routes: list of extra command names this plugin's usage
  lands on (source-side routing) — presence-as-registration on the push side: installing
  the plugin lands the projection, no need to edit hub commands; validate checks routing
  targets exist, routing plugins carry usage, and routing duplicating consumes is an error
- the manifest's usage / checks lists are the sole projection source of write-side contracts
  and inspection rules: checks project into the check command in injection order, usage
  projects into each command SKILL.md's cmd-inject marker block — disclosure order: owner
  blocks first (consumes order), routed blocks in the middle (dependency topology plus
  alphabetical), remaining consumes last; to change a contract, change PLUGIN.yaml —
  command bodies keep only the operational flow.
  PLUGIN.md returns to pure documentation (Role / Structure / Invariants / Changelog)

Global pieces and domain pieces (constitution principle 11):
- the optional manifest bridge key (必依|按需): the extension point and attach cardinality
  declared by a global piece; disclosure prose lands in PLUGIN.md's bridge section
- a domain piece = depends chain reaches domain; depending on domain directly makes a domain base
- validate checks: bridges may only be held by global pieces; a must-attach (必依) bridge
  requires every domain base to have the corresponding depends edge (missing edge is an error)

Plugin attached-audit contract (scripts/check.py, optional):
- must define check(ctx), returning an issue list: {"level": "error"|"warning"|"info", "message": str}
- ctx.root = repository root; ctx.pages = [(wiki-relative path, frontmatter dict, body)],
  shared across the single scan
- read-only with zero side effects: repair actions belong to commands/humans, attached
  audits only report; messages in Chinese, no third-party dependencies
"""
import ast
import importlib.util
import os
import re
import shutil
import sys
import types

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PLUGINS_DIR = os.path.join(ROOT, ".meta", "plugins")
COMMANDS_DIR = os.path.join(ROOT, ".meta", "command")
CONNECTORS_DIR = os.path.join(ROOT, "connectors")
SKILLS_DIR = os.path.join(ROOT, ".agents", "skills")
AGENTS_MD = os.path.join(ROOT, "AGENTS.md")
REGISTRY = os.path.join(ROOT, ".meta", "protocol", "registry.yaml")

# manifest's seven fields (id / version / depends / updated / attachment / fields / inject) + optional commands
REQUIRED_KEYS = ["id", "version", "depends", "updated", "attachment", "fields", "inject"]
INJECT_START = "<!-- wiki-inject:start -->"
INJECT_END = "<!-- wiki-inject:end -->"
CHECK_SKILL = os.path.join(COMMANDS_DIR, "check", "SKILL.md")
CHECK_INJECT_START = "<!-- check-inject:start -->"
CHECK_INJECT_END = "<!-- check-inject:end -->"
CMD_INJECT_START = "<!-- cmd-inject:start -->"
CMD_INJECT_END = "<!-- cmd-inject:end -->"
# tier law (issue #12 layer discipline): full projects into AGENTS.md, member exits the injection
# region — exposure rides on the family root's roster line, the skill catalog, and L-layer reads
INJECT_TIERS = ("full", "member")
# injection budget on the projected plugin blocks: smallest mainstream whole-file AGENTS.md cap
# (Devin 16 KiB) minus ~1 KiB instance handwritten allowance; over-budget is a validate error
INJECT_BUDGET = 15 * 1024


def ordered_plugins(plugins):
    """Injection order = dependency topology (dependees injected first) + alphabetical within a batch; shared by projection regions.

    On cycles or dangling dependencies, falls back to alphabetical output (validate
    reports the error separately; not duplicated here).
    """
    remaining = dict(plugins)
    order = []
    while remaining:
        ready = sorted(p for p, m in remaining.items()
                       if all(d not in remaining for d in (m.get("depends") or [])))
        if not ready:
            order.extend(sorted(remaining))
            break
        order.extend(ready)
        for p in ready:
            del remaining[p]
    return order


def strip_quotes(s):
    if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
        return s[1:-1]
    return s


def strip_comment(s):
    """Strip inline comments (from ` #` on) — a quoted value is protected up to its closing quote.

    The manifest contract says "quote the whole value first if it contains #"; this honors it:
    comment stripping never fires inside the quoted span (e.g. `## Section` names in disclosures).
    """
    if s.startswith('"'):
        end = s.find('"', 1)
        if end != -1:
            return s[:end + 1] + strip_comment(s[end + 1:])
    return re.split(r"\s+#", s, maxsplit=1)[0].strip()


def parse_manifest(path):
    """Parse the manifest's minimal YAML subset; raises ValueError on failure."""
    data, target = {}, None
    for raw in open(path, encoding="utf-8").read().splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith("  - "):
            if target is None:
                raise ValueError(f"list item before any key: {raw!r}")
            item = strip_quotes(strip_comment(raw.strip()[2:]))
            if not isinstance(data.get(target), list):
                data[target] = []
            data[target].append(item)
            continue
        m = re.match(r"^(\s*)([A-Za-z_][\w-]*):\s*(.*)$", raw)
        if not m:
            raise ValueError(f"unparsable line: {raw!r}")
        key, val = m.group(2), strip_comment(m.group(3))
        if m.group(1):  # indented line: fields dict item
            if target is None:
                raise ValueError(f"field item before any key: {raw!r}")
            if not isinstance(data.get(target), dict):
                data[target] = {}
            data[target][key] = strip_quotes(val)
        else:
            target = key
            if val == "":
                data[key] = None  # block style, filled by following lines
            elif val == "[]":
                data[key] = []
            elif val == "{}":
                data[key] = {}
            else:
                data[key] = strip_quotes(val)
    return data


def load_plugins():
    """Read all plugin manifests; returns (plugins, errors)."""
    plugins, errors = {}, []
    for name in sorted(os.listdir(PLUGINS_DIR)):
        pdir = os.path.join(PLUGINS_DIR, name)
        if not os.path.isdir(pdir):
            continue
        yml = os.path.join(pdir, "PLUGIN.yaml")
        md = os.path.join(pdir, "PLUGIN.md")
        if not os.path.exists(yml) or not os.path.exists(md):
            errors.append(f"[error] {name}/: PLUGIN.yaml or PLUGIN.md missing")
            continue
        try:
            m = parse_manifest(yml)
        except ValueError as e:
            errors.append(f"[error] {name}/PLUGIN.yaml: {e}")
            continue
        plugins[name] = m
    return plugins, errors


def reaches_domain(plugins, pid, seen=None):
    """Does the depends chain of pid reach the domain concept plugin (domain-piece test, principle 11)?"""
    seen = set() if seen is None else seen
    if pid in seen or pid not in plugins:
        return False
    seen.add(pid)
    deps = plugins[pid].get("depends") or []
    return "domain" in deps or any(reaches_domain(plugins, d, seen) for d in deps)


def reaches_plugin(plugins, start, target, seen=None):
    """Does the depends chain of start reach target (transitive family-membership test)?"""
    seen = set() if seen is None else seen
    if start in seen or start not in plugins:
        return False
    seen.add(start)
    deps = plugins[start].get("depends") or []
    return target in deps or any(reaches_plugin(plugins, d, target, seen) for d in deps)


def build_inject_blocks(plugins):
    """AGENTS.md injection-region plugin blocks with member-tier exits applied; returns (blocks, exited)."""
    blocks, exited = [], 0
    for pid in ordered_plugins(plugins):
        if plugins[pid].get("inject_tier") == "member":
            exited += 1
            continue
        ver = plugins[pid].get("version")
        line = plugins[pid].get("inject", "")
        blocks.append(f"<!-- plugin:{pid} v{ver} -->\n- {line}\n<!-- /plugin:{pid} -->")
    return blocks, exited


def validate(plugins, errors):
    """Compliance and dependency checks; errors are appended to errors."""
    for name, m in sorted(plugins.items()):
        for k in REQUIRED_KEYS:
            if k not in m:
                errors.append(f"[error] {name}/PLUGIN.yaml: missing field {k}")
        if m.get("id") and m["id"] != name:
            errors.append(f"[error] {name}/: id ({m['id']}) != directory name")
        if m.get("version") and not re.fullmatch(r"\d+\.\d+", str(m["version"])):
            errors.append(f"[error] {name}/: version ({m['version']}) not X.Y")
        if m.get("updated") and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(m["updated"])):
            errors.append(f"[error] {name}/: updated ({m['updated']}) not YYYY-MM-DD")
        deps = m.get("depends")
        if deps is not None and not isinstance(deps, list):
            errors.append(f"[error] {name}/: depends must be a list")
        if not m.get("inject"):
            errors.append(f"[error] {name}/: inject (projection line) empty")
        if m.get("inject_tier") is not None and m["inject_tier"] not in INJECT_TIERS:
            errors.append(f"[error] {name}/: inject_tier ({m['inject_tier']}) must be full or member")
        # stray-quote smell (post-parse): a value still carrying a quote edge means unbalanced
        # quoting — the classic artifact of a clipped value (issue #12 post-migration field report)
        if isinstance(m.get("inject"), str) and (m["inject"].startswith('"') or m["inject"].endswith('"')):
            print(f"[warning] {name}/: inject value carries a stray quote (unbalanced quoting — parse artifact or manifest typo)")
        # attached-audit contract (optional): if scripts/check.py exists it must define check(ctx) — checked statically via AST, not executed
        cpath = os.path.join(PLUGINS_DIR, name, "scripts", "check.py")
        if os.path.exists(cpath):
            try:
                tree = ast.parse(open(cpath, encoding="utf-8").read())
            except SyntaxError as e:
                errors.append(f"[error] {name}/scripts/check.py syntax error: {e}")
            else:
                if not any(isinstance(n, ast.FunctionDef) and n.name == "check" for n in tree.body):
                    errors.append(f"[error] {name}/scripts/check.py: check(ctx) not defined (audit contract)")
    # tier law (issue #12): member-tier exits are legitimate only inside a family — the depends
    # chain must reach a full-tier domain root, else the plugin exits into invisibility
    roots = [p for p in sorted(plugins)
             if reaches_domain(plugins, p) and plugins[p].get("inject_tier") != "member"]
    for name, m in sorted(plugins.items()):
        if m.get("inject_tier") == "member" and not any(reaches_plugin(plugins, name, r) for r in roots):
            errors.append(f"[error] {name}/: inject_tier member must reach a full-tier domain root through depends")
    # injection budget (hard since the issue #12 tier migration landed): over-budget blocks mechanical actions
    blocks, _ = build_inject_blocks(plugins)
    size = sum(len(b.encode("utf-8")) for b in blocks)
    if size > INJECT_BUDGET:
        errors.append(f"[error] projected injection region {size} B over the {INJECT_BUDGET} B budget — compress pointer lines or re-tier domain members (issue #12 layer discipline)")
    # dependency existence
    for name, m in sorted(plugins.items()):
        for dep in m.get("depends") or []:
            if dep not in plugins:
                errors.append(f"[error] {name}/: dependency {dep} not found")
    # cycle detection (DFS three-color marking)
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {k: WHITE for k in plugins}

    def dfs(node, path):
        color[node] = GRAY
        for dep in plugins[node].get("depends") or []:
            if dep not in plugins:
                continue
            if color[dep] == GRAY:
                errors.append(f"[error] dependency cycle: {' -> '.join(path + [node, dep])}")
            elif color[dep] == WHITE:
                dfs(dep, path + [node])
        color[node] = BLACK

    for k in sorted(plugins):
        if color[k] == WHITE:
            dfs(k, [])


def _owner_list(owner):
    """Normalize the owner value into an id list: lists as-is, strings split on commas (tolerating the [a, b] form)."""
    if isinstance(owner, list):
        vals = [str(v).strip() for v in owner]
    else:
        vals = [v.strip() for v in str(owner).replace("[", "").replace("]", "").split(",")]
    return [v for v in vals if v]


def validate_bindings(plugins, errors):
    """Command-plugin binding: owner × commands mutual consistency; consumes pull and usage_routes source-side routing."""
    import wikilib

    commands, claimed, consumes_map = [], {}, {}  # claimed: command -> owner set (framework excluded)
    for name in sorted(os.listdir(COMMANDS_DIR)):
        cdir = os.path.join(COMMANDS_DIR, name)
        path = os.path.join(cdir, "SKILL.md")
        if not os.path.isdir(cdir) or not os.path.exists(path):
            continue
        commands.append(name)
        fm = wikilib.parse_frontmatter(open(path, encoding="utf-8").read())
        if fm.get("owner") is None:
            errors.append(f"[error] command {name}/: frontmatter missing owner (plugin id or framework)")
            continue
        owners = _owner_list(fm["owner"])
        # consumes (optional; required for owner-driven commands and must include all owners): write-side contract pull declaration
        consumes = fm.get("consumes")
        consumes = _owner_list(consumes) if consumes else []
        consumes_map[name] = consumes
        if "framework" not in owners and not consumes:
            errors.append(f"[error] command {name}/: owner-driven command requires consumes (owner usage projects too)")
        for pid in consumes:
            if pid not in plugins:
                errors.append(f"[error] command {name}/: consumes {pid} is not an installed plugin")
                continue
            if not (plugins[pid].get("usage") or []):
                errors.append(f"[error] command {name}/: consumes {pid} but its manifest lacks a usage list")
        if "framework" not in owners:
            for pid in owners:
                if pid not in consumes:
                    errors.append(f"[error] command {name}/: owner {pid} not in consumes (owner usage projects too)")
        if "framework" in owners:
            if len(owners) > 1:
                errors.append(f"[error] command {name}/: framework cannot combine with other owners ({', '.join(owners)})")
            continue
        claimed[name] = set(owners)
        for pid in owners:
            if pid not in plugins:
                errors.append(f"[error] command {name}/: owner {pid} is not an installed plugin")
    for pid, m in sorted(plugins.items()):
        cmds = m.get("commands")
        if cmds is None:
            continue
        if not isinstance(cmds, list):
            errors.append(f"[error] {pid}/: commands must be a list")
            continue
        for c in cmds:
            if c not in commands:
                errors.append(f"[error] {pid}/: commands declares missing command {c} (.meta/command/{c}/)")
            elif c not in claimed:
                errors.append(f"[error] command {c}/: {pid} one-sided claim (owner is framework or missing)")
            elif pid not in claimed[c]:
                errors.append(f"[error] command {c}/: {pid} one-sided claim (owner does not include {pid})")
    for c, owners in sorted(claimed.items()):
        for pid in owners:
            if pid in plugins and c not in (plugins[pid].get("commands") or []):
                errors.append(f"[error] command {c}/: owner {pid} not claimed in manifest commands (one-sided)")
    # source-side routing (usage_routes): installing a plugin lands the projection, no destination-command edit needed
    for pid, m in sorted(plugins.items()):
        routes = m.get("usage_routes")
        if routes is None:
            continue
        if not isinstance(routes, list):
            errors.append(f"[error] {pid}/: usage_routes must be a list")
            continue
        if not (m.get("usage") or []):
            errors.append(f"[error] {pid}/: usage_routes declared but manifest lacks a usage list")
        for c in routes:
            if c not in commands:
                errors.append(f"[error] {pid}/: usage_routes target command {c} not found (.meta/command/{c}/)")
            elif pid in consumes_map.get(c, []):
                errors.append(f"[error] command {c}/: {pid} both routed and in consumes (duplicate routing)")


def validate_bridges(plugins, errors):
    """Global/domain piece bridge law (constitution principle 11): bridges are global-piece extension points; must-attach bridges check domain-base dependency completeness."""
    bases = [p for p, m in sorted(plugins.items()) if "domain" in (m.get("depends") or [])]
    for pid, m in sorted(plugins.items()):
        bridge = m.get("bridge")
        if bridge is None:
            continue
        if bridge not in ("必依", "按需"):
            errors.append(f"[error] {pid}/: bridge ({bridge}) must be 必依 (required) or 按需 (on-demand)")
            continue
        if reaches_domain(plugins, pid):
            errors.append(f"[error] {pid}/: bridge is global-only (depends chain reaches domain)")
            continue
        if bridge == "必依":
            for base in bases:
                if pid not in (plugins[base].get("depends") or []):
                    errors.append(f"[error] {base}/: missing depends {pid} (必依 bridge: every domain base must carry this edge)")


def do_audit(plugins, only=None):
    """Plugin attached audits: discovery-style execution of each plugin's scripts/check.py (contract in the module docstring).

    This is the mechanical shape of "code injection": a contract-compliant attached-audit
    script present in a plugin directory is automatically listed, and moving the directory
    out on uninstall automatically delists it — isomorphic to the AGENTS.md injection
    region (presence as registration), but the code does no text splicing (avoiding
    namespace and merge noise), using discovery + invocation instead.
    """
    import wikilib

    pages = list(wikilib.walk_pages(ROOT))  # single scan shared by all plugins (frugal invocation)
    ctx = types.SimpleNamespace(root=ROOT, pages=pages)
    counts = {"error": 0, "warning": 0, "info": 0}
    ran = 0
    for pid in sorted(plugins):
        if only and pid != only:
            continue
        cpath = os.path.join(PLUGINS_DIR, pid, "scripts", "check.py")
        if not os.path.exists(cpath):
            continue
        spec = importlib.util.spec_from_file_location(f"plugin_check_{pid}", cpath)
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
            issues = mod.check(ctx) or []
        except Exception as e:  # a check script's own failure is reported as an error, without taking down the other plugins
            print(f"[error] ({pid}) check script failed: {e}")
            counts["error"] += 1
            ran += 1
            continue
        ran += 1
        for it in issues:
            level = str(it.get("level", "warning"))
            counts[level] = counts.get(level, 0) + 1
            print(f"[{level}] ({pid}) {it.get('message', '')}")
    if ran == 0:
        print("[audit] no plugin carries scripts/check.py (optional contract; currently semantic-only)")
        return 0
    print(f"[audit] {ran} plugins, error {counts['error']} / warning {counts.get('warning', 0)} / info {counts.get('info', 0)}")
    return 1 if counts["error"] else 0


def do_inject(plugins):
    """Rebuild the AGENTS.md injection region from manifests (preamble preserved, blocks in dependency topology + alphabetical order, idempotent)."""
    text = open(AGENTS_MD, encoding="utf-8").read()
    m = re.search(re.escape(INJECT_START) + r"\n(.*?)" + re.escape(INJECT_END), text, re.S)
    if not m:
        print("[error] AGENTS.md: inject markers (wiki-inject:start/end) not found")
        return False
    region = m.group(1)
    first = region.find("<!-- plugin:")
    preamble = region[:first].rstrip() if first != -1 else region.rstrip()
    blocks, exited = build_inject_blocks(plugins)
    new_region = preamble + "\n\n" + "\n\n".join(blocks) + "\n\n"
    if new_region == region:
        print("[inject] region unchanged")
        return True
    open(AGENTS_MD, "w", encoding="utf-8", newline="\n").write(
        text[: m.start(1)] + new_region + text[m.end(1):]
    )
    tail = f", {exited} member-tier exits skipped" if exited else ""
    print(f"[inject] rebuilt ({len(blocks)} plugin blocks{tail})")
    return True


def do_check_inject(plugins):
    """Rebuild the check command's injection region from each manifest's checks list (presence as registration, idempotent).

    Isomorphic to the AGENTS.md injection region: the manifest is the body, the check
    block is the projection — to change inspection rules, change the manifest's checks
    list, and drift between projection and handwritten blocks disappears.
    """
    if not os.path.exists(CHECK_SKILL):
        print("[check-inject] check command absent, skipped")
        return True
    text = open(CHECK_SKILL, encoding="utf-8").read()
    m = re.search(re.escape(CHECK_INJECT_START) + r"\n(.*?)" + re.escape(CHECK_INJECT_END), text, re.S)
    if not m:
        print("[error] check/SKILL.md: inject markers (check-inject:start/end) not found")
        return False
    blocks = []
    for pid in ordered_plugins(plugins):
        items = plugins[pid].get("checks") or []
        if not items:
            continue
        body = "\n".join(f"- {it}" for it in items)
        blocks.append(f"<!-- check:{pid} -->\n{body}\n<!-- /check:{pid} -->")
    new_region = "\n\n".join(blocks) + "\n" if blocks else "\n"
    if new_region == m.group(1):
        print("[check-inject] unchanged")
        return True
    open(CHECK_SKILL, "w", encoding="utf-8", newline="\n").write(
        text[: m.start(1)] + new_region + text[m.end(1):]
    )
    print(f"[check-inject] rebuilt ({len(blocks)} plugin blocks)")
    return True


def do_cmd_inject(plugins):
    """Rebuild command injection regions from manifests: consumes pull + usage_routes source-side routing (presence as registration, idempotent).

    The third projection: plugin write-side contract -> command. Disclosure order: owner
    blocks first (consumes order), routed blocks in the middle (dependency topology plus
    alphabetical), remaining consumes last. Each block is the corresponding manifest usage
    list verbatim — command bodies keep only the operational flow; (un)installing plugins
    adds and removes them automatically.
    """
    import wikilib

    routed = {}  # command -> [plugins] (source-side routing, topology + alphabetical)
    for pid in ordered_plugins(plugins):
        for c in plugins[pid].get("usage_routes") or []:
            routed.setdefault(c, []).append(pid)

    ok = True
    for name in sorted(os.listdir(COMMANDS_DIR)):
        path = os.path.join(COMMANDS_DIR, name, "SKILL.md")
        if not os.path.exists(path):
            continue
        text = open(path, encoding="utf-8").read()
        fm = wikilib.parse_frontmatter(text)
        consumes = fm.get("consumes")
        if consumes is None:
            continue
        if not isinstance(consumes, list):
            consumes = _owner_list(consumes)
        m = re.search(re.escape(CMD_INJECT_START) + r"\n(.*?)" + re.escape(CMD_INJECT_END), text, re.S)
        if not m:
            print(f"[error] command {name}/: inject markers (cmd-inject:start/end) not found")
            ok = False
            continue
        owners = [o for o in _owner_list(fm.get("owner") or "") if o != "framework"]
        seq, seen = [p for p in consumes if p in owners], set()
        seen.update(seq)
        seq += [p for p in routed.get(name, []) if p not in seen]
        seen.update(seq)
        seq += [p for p in consumes if p not in seen]
        blocks = []
        for pid in seq:
            items = plugins.get(pid, {}).get("usage") or []
            if items:
                body = "\n".join(f"- {it}" for it in items)
                blocks.append(f"<!-- usage:{pid} -->\n{body}\n<!-- /usage:{pid} -->")
        new_region = "\n\n".join(blocks) + "\n" if blocks else "\n"
        if new_region == m.group(1):
            continue
        open(path, "w", encoding="utf-8", newline="\n").write(
            text[: m.start(1)] + new_region + text[m.end(1):]
        )
        print(f"[cmd-inject] {name}: rebuilt ({len(blocks)} usage blocks)")
    return ok


def do_registry(plugins):
    """Rebuild the registry.yaml plugin section from the manifests' fields (protocol / reserved sections untouched)."""
    text = open(REGISTRY, encoding="utf-8").read()
    m = re.search(r"^plugins:\n(.*?)^reserved:", text, re.S | re.M)
    if not m:
        print("[error] registry.yaml: plugins:/reserved: section structure not found")
        return False
    lines = []
    for pid in sorted(plugins):
        fields = plugins[pid].get("fields")
        if not fields:
            continue  # plugins with no fields of their own stay out of the registry plugin section
        lines.append(f"  {pid}:")
        for f in sorted(fields):
            lines.append(f"    {f}:")
            lines.append(f"      note: {fields[f]}")
    body = "\n".join(lines) + "\n\n"
    if body == m.group(1):
        print("[registry] plugin section unchanged")
        return True
    open(REGISTRY, "w", encoding="utf-8", newline="\n").write(
        text[: m.start(1)] + body + text[m.end(1):]
    )
    print("[registry] plugin section rebuilt")
    return True


def do_deploy():
    """Sync .meta/command/*/SKILL.md and connectors/*/SKILL.md -> .agents/skills/*/SKILL.md; orphan copies are reported only."""
    sources = {}
    for base in (COMMANDS_DIR, CONNECTORS_DIR):
        if not os.path.isdir(base):
            continue
        for d in sorted(os.listdir(base)):
            src = os.path.join(base, d, "SKILL.md")
            if not os.path.isfile(src):
                continue
            if d in sources:
                print(f"[warning] skill name collision: {d}/ in both commands and connectors; commands win")
                continue
            sources[d] = src
    changed = 0
    for name, src in sorted(sources.items()):
        dst_dir = os.path.join(SKILLS_DIR, name)
        dst = os.path.join(dst_dir, "SKILL.md")
        os.makedirs(dst_dir, exist_ok=True)
        if not os.path.exists(dst) or open(src, "rb").read() != open(dst, "rb").read():
            shutil.copyfile(src, dst)
            changed += 1
            print(f"[deploy] synced {name}/SKILL.md")
    if os.path.isdir(SKILLS_DIR):
        for d in sorted(os.listdir(SKILLS_DIR)):
            if d not in sources and os.path.isdir(os.path.join(SKILLS_DIR, d)):
                print(f"[warning] orphan copy .agents/skills/{d}/ (master gone; deletion belongs to human)")
    if not changed:
        print("[deploy] all in sync")
    return True


def do_ls(plugins):
    for pid in sorted(plugins):
        deps = ", ".join(plugins[pid].get("depends") or []) or "—"
        cmds = ", ".join(plugins[pid].get("commands") or []) or "—"
        tier = "member" if plugins[pid].get("inject_tier") == "member" else "full"
        size = len(str(plugins[pid].get("inject") or "").encode("utf-8"))
        print(f"  {pid:<10} {plugins[pid].get('version', '?'):<6} {tier:<6} {size:>5} B  deps {deps}; commands {cmds}")
    print(f"{len(plugins)} plugins (.meta/plugins/; injection order = dependency topo + alphabetical; inject budget {INJECT_BUDGET} B)")
    # usage routing table: plugin -> landing commands (own + source-side routes + command pulls)
    import wikilib

    consumes_map = {}
    for name in sorted(os.listdir(COMMANDS_DIR)):
        path = os.path.join(COMMANDS_DIR, name, "SKILL.md")
        if not os.path.exists(path):
            continue
        c = wikilib.parse_frontmatter(open(path, encoding="utf-8").read()).get("consumes")
        if c is None:
            continue
        consumes_map[name] = c if isinstance(c, list) else _owner_list(c)
    rows = []
    for pid in sorted(plugins):
        if not (plugins[pid].get("usage") or []):
            continue
        targets = list(dict.fromkeys(
            list(plugins[pid].get("commands") or [])
            + list(plugins[pid].get("usage_routes") or [])
            + [c for c, lst in consumes_map.items() if pid in lst]))
        rows.append(f"  {pid:<12} -> {', '.join(targets) if targets else '(no targets — contract documentation surface)'}")
    if rows:
        print("usage routing (plugin → commands):")
        print("\n".join(rows))


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    plugins, errors = load_plugins()
    if cmd == "ls":
        do_ls(plugins)
        if errors:
            print(f"[warning] {len(errors)} manifest load errors — run validate for details")
        return 0
    if cmd == "audit":
        for e in errors:
            print(e)
        return do_audit(plugins, sys.argv[2] if len(sys.argv) > 2 else None)
    if cmd not in ("validate", "inject", "registry", "deploy", "all"):
        print(__doc__)
        return 2
    validate(plugins, errors)
    validate_bindings(plugins, errors)
    validate_bridges(plugins, errors)
    for e in errors:
        print(e)
    if errors:
        print(f"[result] validation failed ({len(errors)} errors) — mechanical actions blocked")
        return 1
    print(f"[validate] all {len(plugins)} plugins passed (fields / id match / deps exist / acyclic / command bindings / usage routes / bridges)")
    if cmd in ("inject", "all"):
        if not do_inject(plugins):
            return 1
        if not do_check_inject(plugins):
            return 1
        if not do_cmd_inject(plugins):
            return 1
    if cmd in ("registry", "all"):
        if not do_registry(plugins):
            return 1
    if cmd in ("deploy", "all"):
        if not do_deploy():
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
