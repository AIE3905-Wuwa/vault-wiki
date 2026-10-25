#!/usr/bin/env node
/**
 * End-to-end smoke test for the npm channel, using the working tree as the
 * payload (no pack step): init into an empty dir, init over an existing
 * AGENTS.md, refusal on a second init, upgrade with instance-local state.
 *
 * Run: node test/smoke.js
 */
"use strict";

const assert = require("node:assert");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { spawnSync } = require("node:child_process");

const ROOT = path.resolve(__dirname, "..");
const BIN = path.join(ROOT, "bin", "owfa.js");
const PKG = JSON.parse(fs.readFileSync(path.join(ROOT, "package.json"), "utf8"));
const FW = fs.readFileSync(path.join(ROOT, ".meta", "VERSION"), "utf8").trim();

function run(args, cwd) {
  return spawnSync(process.execPath, [BIN, ...args], { cwd, encoding: "utf8" });
}

function hasPython() {
  const cands = process.platform === "win32" ? ["py", "python"] : ["python3", "python"];
  return cands.some((cmd) => {
    const r = spawnSync(cmd, ["-c", "import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)"], { stdio: "ignore" });
    return !r.error && r.status === 0;
  });
}

function countPluginBlocks(text) {
  return (text.match(/<!-- plugin:/g) || []).length;
}

const tmpRoot = fs.mkdtempSync(path.join(os.tmpdir(), "owfa-smoke-"));
let failures = 0;
function step(name, fn) {
  try {
    fn();
    console.log("  ok   " + name);
  } catch (e) {
    failures++;
    console.error("  FAIL " + name + "\n       " + (e && e.message ? e.message.split("\n").join("\n       ") : e));
  }
}

try {
  if (!hasPython()) {
    console.log("smoke: no python3 on PATH — skipping (the framework itself is Python; the channel test needs it)");
    process.exit(0);
  }

  const empty = path.join(tmpRoot, "empty");
  const existing = path.join(tmpRoot, "existing");

  step("init on an empty directory", () => {
    const r = run(["init", empty, "--name", "smoke-vault"]);
    assert.strictEqual(r.status, 0, r.stderr + r.stdout);
    assert.strictEqual(fs.readFileSync(path.join(empty, ".meta", "VERSION"), "utf8").trim(), FW);
    for (const d of ["vault", "wiki/notes", "wiki/sessions", "wiki/vault", ".agents/skills/map"]) {
      assert.ok(fs.existsSync(path.join(empty, d)), `missing ${d}`);
    }
    const agents = fs.readFileSync(path.join(empty, "AGENTS.md"), "utf8");
    assert.ok(agents.includes("# smoke-vault"), "name not substituted");
    assert.ok(agents.includes("<!-- wiki-inject:start -->") && agents.includes("<!-- wiki-inject:end -->"));
    assert.ok(countPluginBlocks(agents) >= 20, `expected core plugin blocks, got ${countPluginBlocks(agents)}`);
  });

  step("doctor passes on the fresh instance", () => {
    const r = run(["doctor", empty]);
    assert.strictEqual(r.status, 0, r.stderr + r.stdout);
    assert.ok(/doctor: ok/.test(r.stdout), r.stdout);
  });

  step("second init refuses without --force", () => {
    const r = run(["init", empty], tmpRoot);
    assert.notStrictEqual(r.status, 0);
    assert.ok(/already contains \.meta/.test(r.stderr), r.stderr);
  });

  step("init preserves an existing AGENTS.md and appends the region", () => {
    fs.mkdirSync(existing, { recursive: true });
    fs.writeFileSync(path.join(existing, "AGENTS.md"), "# my own constitution\n\nkeep this line\n", "utf8");
    const r = run(["init", existing]);
    assert.strictEqual(r.status, 0, r.stderr + r.stdout);
    const text = fs.readFileSync(path.join(existing, "AGENTS.md"), "utf8");
    assert.ok(text.startsWith("# my own constitution"), "handwritten prefix lost");
    assert.ok(text.includes("keep this line"));
    assert.ok(text.includes("<!-- wiki-inject:start -->"));
    assert.ok(countPluginBlocks(text) >= 20);
  });

  step("upgrade replaces the framework and preserves instance kernel state", () => {
    fs.writeFileSync(path.join(empty, ".meta", "VERSION"), "0.2", "utf8");
    fs.writeFileSync(path.join(empty, ".meta", "kernel-journal.log"), "keep-me\n", "utf8");
    fs.mkdirSync(path.join(empty, ".meta", "migrations"), { recursive: true });
    fs.writeFileSync(path.join(empty, ".meta", "migrations", "pending.json"), "{}\n", "utf8");
    const r = run(["upgrade", empty], tmpRoot);
    assert.strictEqual(r.status, 0, r.stderr + r.stdout);
    assert.strictEqual(fs.readFileSync(path.join(empty, ".meta", "VERSION"), "utf8").trim(), FW);
    assert.strictEqual(fs.readFileSync(path.join(empty, ".meta", "kernel-journal.log"), "utf8"), "keep-me\n");
    assert.strictEqual(fs.readFileSync(path.join(empty, ".meta", "migrations", "pending.json"), "utf8"), "{}\n");
  });

  step("init --force preserves kernel state and instance data", () => {
    fs.writeFileSync(path.join(empty, "vault", "keep.txt"), "asset\n", "utf8");
    const r = run(["init", empty, "--force"]);
    assert.strictEqual(r.status, 0, r.stderr + r.stdout);
    assert.strictEqual(fs.readFileSync(path.join(empty, "vault", "keep.txt"), "utf8"), "asset\n");
    assert.strictEqual(fs.readFileSync(path.join(empty, ".meta", "kernel-journal.log"), "utf8"), "keep-me\n");
  });

  step("upgrade --check is read-only", () => {
    fs.writeFileSync(path.join(empty, ".meta", "VERSION"), "0.2", "utf8");
    const r = run(["upgrade", empty, "--check"]);
    assert.strictEqual(r.status, 0, r.stderr + r.stdout);
    assert.strictEqual(fs.readFileSync(path.join(empty, ".meta", "VERSION"), "utf8").trim(), "0.2");
  });

  console.log(`\nsmoke: ${failures ? failures + " failure(s)" : "all green"} (owfa ${PKG.version}, framework ${FW})`);
} finally {
  fs.rmSync(tmpRoot, { recursive: true, force: true });
}
process.exit(failures ? 1 : 0);
