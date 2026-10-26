#!/usr/bin/env node
/**
 * OWFA — One Workspace For All (agents).
 *
 * The npm channel for the owfa framework. This CLI owns exactly three
 * things the framework itself cannot own: fetching a complete framework tree,
 * initializing a directory without hand-copying it, and replacing that tree
 * on upgrade. Everything semantic stays in the Python kernel
 * (.meta/scripts/wiki_plugin_kernel.py) — this file only orchestrates.
 *
 * Design rules:
 * - zero runtime dependencies; Node is needed to install, not to use
 * - no install/postinstall scripts for consumers (nothing executes on npm install)
 * - additive on init: existing content is never modified outside AGENTS.md's
 *   injection region
 * - upgrade is a tree replacement plus kernel convergence; instance-local
 *   kernel state (migration ledger, journal, registry cache) is preserved
 */
"use strict";

const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { spawnSync } = require("node:child_process");

const CLI_ROOT = path.resolve(__dirname, "..");
const PKG = JSON.parse(fs.readFileSync(path.join(CLI_ROOT, "package.json"), "utf8"));
const FRAMEWORK_VERSION = readVersion(CLI_ROOT) || "?";
const INJECT_START = "<!-- wiki-inject:start -->";
const INJECT_END = "<!-- wiki-inject:end -->";
const PAYLOAD = [".meta", ".agents"];
const INSTANCE_DIRS = ["vault", path.join("wiki", "notes"), path.join("wiki", "sessions"), path.join("wiki", "vault")];
// Kernel state that belongs to the instance, not to the framework tree.
const PRESERVED = [
  path.join(".meta", "migrations", "pending.json"),
  path.join(".meta", "kernel-journal.log"),
  path.join(".meta", "registry-cache.yaml"),
];

// ---------------------------------------------------------------------------
// small utilities
// ---------------------------------------------------------------------------

function readVersion(root) {
  try {
    return fs.readFileSync(path.join(root, ".meta", "VERSION"), "utf8").trim();
  } catch {
    return null;
  }
}

function out(line = "") {
  process.stdout.write(line + "\n");
}

function fail(message, code = 1) {
  process.stderr.write("owfa: " + message + "\n");
  process.exit(code);
}

function rel(root, p) {
  return path.relative(root, p) || ".";
}

function parseArgs(argv) {
  const args = { _: [], flags: new Set() };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--") {
      args._.push(...argv.slice(i + 1));
      break;
    }
    if (a.startsWith("--")) {
      const [key, inline] = a.slice(2).split("=", 2);
      const takesValue = ["name", "packages", "without", "from"].includes(key);
      if (takesValue && inline === undefined) {
        args[key] = argv[++i];
      } else if (takesValue) {
        args[key] = inline;
      } else {
        args.flags.add(key);
      }
    } else {
      args._.push(a);
    }
  }
  return args;
}

function copyPayload(target, { replace = false } = {}) {
  const skip = (src) => {
    const base = path.basename(src);
    if (base === "__pycache__" || base.endsWith(".pyc") || base === ".DS_Store") return false;
    if (PRESERVED.some((p) => src.endsWith(path.sep + p) || src.endsWith("/" + p.replaceAll(path.sep, "/")))) return false;
    if (base === "smoke-tmp") return false;
    return true;
  };
  for (const entry of PAYLOAD) {
    const src = path.join(CLI_ROOT, entry);
    const dst = path.join(target, entry);
    if (!fs.existsSync(src)) fail(`package is missing ${entry}/ — the npm tarball is incomplete`);
    if (replace) fs.rmSync(dst, { recursive: true, force: true });
    fs.mkdirSync(path.dirname(dst), { recursive: true });
    fs.cpSync(src, dst, { recursive: true, force: true, filter: skip });
  }
}

function ensureDirs(target) {
  for (const d of INSTANCE_DIRS) fs.mkdirSync(path.join(target, d), { recursive: true });
}

function ensureAgents(target, name) {
  const file = path.join(target, "AGENTS.md");
  const seed = fs
    .readFileSync(path.join(CLI_ROOT, "templates", "AGENTS.template.md"), "utf8")
    .replaceAll("{{name}}", name);
  if (!fs.existsSync(file)) {
    fs.writeFileSync(file, seed, "utf8");
    return "written";
  }
  const text = fs.readFileSync(file, "utf8");
  const hasStart = text.includes(INJECT_START);
  const hasEnd = text.includes(INJECT_END);
  if (hasStart && hasEnd) return "kept (injection region already present)";
  if (hasStart || hasEnd) fail("AGENTS.md has only one injection marker — restore both markers (or remove the broken one) and rerun");
  const region = seed.slice(seed.indexOf(INJECT_START));
  const glue = text.endsWith("\n") ? "\n" : "\n\n";
  fs.writeFileSync(file, text + glue + region + "\n", "utf8");
  return "appended (existing AGENTS.md preserved)";
}

function findPython() {
  if (process.env.OWFA_PYTHON) {
    return { cmd: process.env.OWFA_PYTHON, args: [] };
  }
  const candidates =
    process.platform === "win32"
      ? [{ cmd: "py", args: ["-3"] }, { cmd: "python", args: [] }, { cmd: "python3", args: [] }]
      : [{ cmd: "python3", args: [] }, { cmd: "python", args: [] }];
  for (const cand of candidates) {
    const probe = spawnSync(cand.cmd, [...cand.args, "-c", "import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)"], {
      stdio: "ignore",
    });
    if (!probe.error && probe.status === 0) {
      const v = spawnSync(cand.cmd, [...cand.args, "--version"], { encoding: "utf8" });
      return { ...cand, version: (v.stdout || v.stderr || "").trim() };
    }
  }
  return null;
}

function pythonOrFail() {
  const py = findPython();
  if (!py) {
    fail(
      "Python 3.9+ not found. The framework itself is pure-stdlib Python; install Python 3 and rerun " +
        "(or set OWFA_PYTHON=/path/to/python3)."
    );
  }
  return py;
}

function kernel(target, kernelArgs) {
  const py = pythonOrFail();
  const script = path.join(target, ".meta", "scripts", "wiki_plugin_kernel.py");
  if (!fs.existsSync(script)) fail(`no kernel at ${rel(target, script)} — is this an OWFA instance?`);
  const res = spawnSync(py.cmd, [...py.args, script, ...kernelArgs], {
    cwd: target,
    stdio: "inherit",
    // Instances should not accumulate bytecode; the framework tree stays clean.
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
  });
  return res.status === null ? 1 : res.status;
}

function versionTuple(v) {
  return String(v || "")
    .split(".")
    .map((x) => parseInt(x, 10) || 0);
}

function cmpVersion(a, b) {
  const x = versionTuple(a);
  const y = versionTuple(b);
  for (let i = 0; i < Math.max(x.length, y.length); i++) {
    const d = (x[i] || 0) - (y[i] || 0);
    if (d !== 0) return d > 0 ? 1 : -1;
  }
  return 0;
}

function timestamp() {
  const d = new Date();
  const p = (n) => String(n).padStart(2, "0");
  return `${d.getFullYear()}${p(d.getMonth() + 1)}${p(d.getDate())}-${p(d.getHours())}${p(d.getMinutes())}${p(d.getSeconds())}`;
}


function stashInstanceState(target) {
  const stash = new Map();
  for (const p of PRESERVED) {
    const src = path.join(target, p);
    if (fs.existsSync(src)) stash.set(p, fs.readFileSync(src));
  }
  return stash;
}

function restoreInstanceState(target, stash) {
  for (const [p, buf] of stash) {
    fs.mkdirSync(path.dirname(path.join(target, p)), { recursive: true });
    fs.writeFileSync(path.join(target, p), buf);
  }
}

function pendingPackages(target) {
  try {
    return Object.keys(JSON.parse(fs.readFileSync(path.join(target, ".meta", "migrations", "pending.json"), "utf8")));
  } catch {
    return [];
  }
}

function reportPending(target) {
  const pending = pendingPackages(target);
  if (!pending.length) return false;
  out("");
  out(`semantic migration pending: ${pending.join(", ")} — the package is installed, but its first-run step is an agent act, not a mechanical one.`);
  out(`  run: python .meta/scripts/wiki_plugin_kernel.py migrate ${pending[0]}`);
  out("  (read the printed page, perform the step, then rerun with --clear)");
  return true;
}

// ---------------------------------------------------------------------------
// commands
// ---------------------------------------------------------------------------

function cmdInit(args) {
  const target = path.resolve(args._[0] || ".");
  const force = args.flags.has("force");
  const hasMeta = fs.existsSync(path.join(target, ".meta"));
  if (hasMeta && !force) {
    fail(
      `${target} already contains .meta/ — refusing to overwrite. Use \`owfa upgrade\` to update the framework, ` +
        `or pass --force to re-copy the framework trees (instance data is never touched either way).`
    );
  }
  const name = args.name || path.basename(target) || "workspace";
  fs.mkdirSync(target, { recursive: true });

  out(`OWFA init — framework ${FRAMEWORK_VERSION} → ${target}`);
  if (!hasMeta && fs.existsSync(path.join(target, ".agents", "skills"))) {
    out("note: .agents/skills/ exists — framework skill copies are updated in place, other skills stay untouched");
  }
  if (hasMeta) out("warning: --force replaces the framework trees; instance vault/ and wiki/ are untouched");
  const stash = hasMeta ? stashInstanceState(target) : new Map();
  copyPayload(target, { replace: hasMeta });
  if (hasMeta) restoreInstanceState(target, stash);
  ensureDirs(target);
  out(`agents.md: ${ensureAgents(target, name)}`);

  out("");
  out("converging projections (python .meta/scripts/wiki_plugin_kernel.py all)");
  if (kernel(target, ["all"]) !== 0) {
    const pending = pendingPackages(target);
    if (pending.length) {
      fail(`convergence blocked by pending semantic migrations (${pending.join(", ")}) — clear them with \`python .meta/scripts/wiki_plugin_kernel.py migrate <pkg>\``);
    }
    fail("kernel convergence failed — the framework tree is incomplete; nothing was deleted, fix and rerun");
  }

  let installed = 0;
  if (args.packages) {
    for (const pkg of String(args.packages)
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean)) {
      out("");
      out(`installing package ${pkg} from the registry`);
      if (kernel(target, ["install", pkg, "--yes"]) !== 0) fail(`package ${pkg} failed to install (earlier packages stay installed)`);
      installed++;
      if (reportPending(target)) fail(`framework and ${pkg} are installed, but the workspace is not converged until the semantic migration above is cleared`);
    }
  }

  out("");
  out(`done — framework ${FRAMEWORK_VERSION}${installed ? ` + ${installed} package(s)` : ""} in ${target}`);
  out("");
  out("next:");
  out(`  cd ${target}`);
  out("  git init && git add -A && git commit -m \"init: OWFA workspace\"   # recommended: instance snapshots");
  out("  put any file into vault/, open your agent here, say \"map\"");
  out("  owfa doctor        # anytime: python, framework, kernel validate");
  return 0;
}

function cmdUpgrade(args) {
  const target = path.resolve(args._[0] || ".");
  const local = readVersion(target);
  if (!local) fail(`${target} is not an OWFA instance (no .meta/VERSION) — run \`owfa init\` first`);
  const incoming = FRAMEWORK_VERSION;
  const cmp = cmpVersion(local, incoming);
  const frozen = args.flags.has("check") || args.flags.has("dry-run");
  const force = args.flags.has("force");

  out(`OWFA upgrade — instance ${local} → channel ${incoming} (CLI ${PKG.version})`);
  if (cmp > 0) {
    if (!force) fail(`instance framework ${local} is newer than this CLI's ${incoming} — run \`npx owfa@latest upgrade\``);
    out(`warning: downgrading framework ${local} → ${incoming} (--force)`);
  }
  if (cmp === 0 && !force) {
    out("already at this framework version — nothing to do (pass --force to re-sync the trees)");
    return 0;
  }
  if (frozen) {
    out(`would replace ${PAYLOAD.join(" + ")} and rerun kernel all (dry run)`);
    return 0;
  }

  if (args.flags.has("backup")) {
    const dir = path.join(target, ".owfa", "backup", `${local}-${timestamp()}`);
    for (const entry of PAYLOAD) {
      const src = path.join(target, entry);
      if (fs.existsSync(src)) fs.cpSync(src, path.join(dir, entry), { recursive: true, force: true });
    }
    out(`backup: ${rel(target, dir)} (add .owfa/ to the instance .gitignore if you do not want it tracked)`);
  }

  const stash = stashInstanceState(target);
  out(`warning: local edits under ${PAYLOAD.join("/, ")}/ are replaced by the channel's tree — keep instance hotfixes in git`);
  copyPayload(target, { replace: true });
  restoreInstanceState(target, stash);

  out("");
  out("converging projections (python .meta/scripts/wiki_plugin_kernel.py all)");
  if (kernel(target, ["all"]) !== 0) {
    const pending = pendingPackages(target);
    if (pending.length) {
      fail(`trees replaced, but convergence is blocked by pending semantic migrations (${pending.join(", ")}) — run \`python .meta/scripts/wiki_plugin_kernel.py migrate <pkg>\``);
    }
    fail("kernel convergence failed after the tree replacement — the instance git snapshot is your rollback");
  }

  const pending = pendingPackages(target);
  if (pending.length) {
    out("");
    out(`pending semantic migrations: ${pending.join(", ")} — run \`python .meta/scripts/wiki_plugin_kernel.py migrate <pkg>\` and follow the page`);
  }
  out("");
  out(`done — framework ${local} → ${incoming}`);
  return 0;
}

function cmdDoctor(args) {
  const target = path.resolve(args._[0] || ".");
  const local = readVersion(target);
  const py = findPython();
  out(`owfa ${PKG.version} (channel framework ${FRAMEWORK_VERSION})`);
  out(`node ${process.version}`);
  out(`python ${py ? py.version || `${py.cmd} ${py.args.join(" ")}` : "NOT FOUND"}`);
  out(`target ${target}`);
  if (!local) fail("not an OWFA instance (no .meta/VERSION) — run `owfa init` first");
  out(`instance framework ${local}`);
  const agents = path.join(target, "AGENTS.md");
  if (!fs.existsSync(agents)) {
    out("AGENTS.md: MISSING — the agent will not see the structural contract");
  } else {
    const text = fs.readFileSync(agents, "utf8");
    const ok = text.includes(INJECT_START) && text.includes(INJECT_END);
    out(`AGENTS.md: ${ok ? "injection markers present" : "MISSING injection markers"}`);
  }
  if (!py) {
    out("kernel validate: skipped (no python)");
    return 1;
  }
  out("");
  const code = kernel(target, ["validate"]);
  out("");
  out(code === 0 ? "doctor: ok" : "doctor: kernel validate failed (see above)");
  return code;
}


function cmdList() {
  const target = process.cwd();
  if (!readVersion(target)) fail(`${target} is not an OWFA instance — run \`owfa init\` first`);
  return kernel(target, ["list-remote"]);
}

function cmdPkg() {
  const target = process.cwd();
  if (!readVersion(target)) fail(`${target} is not an OWFA instance — run \`owfa init\` first`);
  return kernel(target, ["pkg"]);
}

function cmdAdd(args) {
  const target = process.cwd();
  const pkg = args._[0];
  if (!pkg) fail("usage: owfa add <package> [--yes] [--without a,b] (run inside the instance)");
  if (!readVersion(target)) fail(`${target} is not an OWFA instance — run \`owfa init\` first`);
  const kernelArgs = ["install", pkg];
  if (args.flags.has("yes")) kernelArgs.push("--yes");
  if (args.without) kernelArgs.push("--without", args.without);
  const code = kernel(target, kernelArgs);
  if (code !== 0) return code;
  if (reportPending(target)) return 1;
  return kernel(target, ["all"]);
}

function usage() {
  out(`owfa ${PKG.version} — One Workspace For All (agents)
the owfa framework's install and upgrade channel

usage:
  owfa init [dir] [--name NAME] [--packages a,b] [--force]
      deploy a fresh workspace (framework ${FRAMEWORK_VERSION}); additive to existing content
  owfa upgrade [dir] [--check] [--backup] [--force]
      replace the framework trees with this channel's version and converge
  owfa doctor [dir]     python / framework / AGENTS.md / kernel validate
  owfa add <pkg> [--yes] [--without a,b]
      install a domain package from the registry, then converge
  owfa list             registry catalog (versions, compat, installed marks)
  owfa pkg              installed package inventory (members, core remainder)
  owfa version          CLI and framework versions
  owfa help

notes:
  - python 3.9+ is required to run the framework; node is only the installer
  - \`init\` never deletes instance data; \`upgrade\` preserves the kernel's
    migration ledger, journal and registry cache
  - no install/postinstall scripts: npm install executes nothing
`);
}

function main() {
  const argv = process.argv.slice(2);
  const cmd = argv[0];
  if (!cmd || cmd === "help" || cmd === "--help" || cmd === "-h") {
    usage();
    return 0;
  }
  if (cmd === "version" || cmd === "--version" || cmd === "-v") {
    out(`owfa ${PKG.version} (framework ${FRAMEWORK_VERSION})`);
    return 0;
  }
  const args = parseArgs(argv.slice(1));
  switch (cmd) {
    case "init":
      return cmdInit(args);
    case "upgrade":
      return cmdUpgrade(args);
    case "doctor":
      return cmdDoctor(args);
    case "add":
      return cmdAdd(args);
    case "list":
      return cmdList();
    case "pkg":
      return cmdPkg();
    default:
      usage();
      return 2;
  }
}

process.exitCode = main();
