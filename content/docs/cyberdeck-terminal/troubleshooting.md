---
title: "Troubleshooting"
date: 2026-11-04
draft: false
weight: 60
tags: ["cyberdeck", "troubleshooting"]
summary: "The failures that cost the most time, what they actually mean, and the fix for each."
---

Ordered by how much time they cost, not by how common they are.

## `error: unknown option '--json'`

**Cause:** the adapter was written against a newer headless interface. Current
builds accept only `--profile` and the task text.

**Diagnose:**

```bash
dsh --profile headless --help
```

If the options list is just `-h, --help`, there is no structured-output flag.

**Fix:** remove `--json`, `--model`, and `--provider` from the adapter's argv so it
builds `[*prefix, "--profile", profile, prompt]`.

**Consequence:** output streams as raw text. Pane 2's diff and panes 3–4's
verification are unaffected — they never depended on the event format.

## `plugin(s) failed to load: @deepseek-ai/dsh-sandbox-local`

**Cause:** three stacked possibilities. Work through them in order.

**1. pnpm blocked a build script.**

```
Error: ERR_PNPM_IGNORED_BUILDS
  ╰─▶ Ignored build scripts: koffi@3.3.6
```

Fix:

```bash
dsh plugin --profile headless approve-builds --all
```

Or edit `~/.dsh-cyberdeck/profiles/headless/pnpm-workspace.yaml`:

```yaml
allowBuilds:
  koffi@3.3.6: true
```

The version-qualified key matters — an unqualified `koffi: true` may not match.

**2. Mixed-generation install.** If the approval succeeds and the plugin still will
not resolve, the package is present but nested where the loader cannot see it:

```bash
node -e "console.log(require.resolve('@deepseek-ai/dsh-sandbox-local', \
  { paths: ['$HOME/.dsh-cyberdeck/profiles/headless'] }))"
```

A path inside `dsh-base/node_modules` means version skew. Fix:

```bash
npm uninstall -g @deepseek-ai/dsh
npm install -g @deepseek-ai/dsh@0.1.5-rc.3
```

**3. Profile initialised by the broken tree.** Always rebuild after changing versions:

```bash
rm -rf ~/.dsh-cyberdeck && mkdir -p ~/.dsh-cyberdeck
dsh --profile headless "reply with exactly: HELLO"
```

## The fix key does nothing

**Cause:** `Ctrl+I` is `0x09` — the same byte as Tab. The terminal cannot distinguish
them, Textual matches its focus binding, and focus moves to the input. `Ctrl+Q` has
the same class of problem (XON flow control).

**Fix:** use the typed commands — `/fix`, `/do`, `/target`, `/tests`, `/test`,
`/run`, `/clear`, `/help`. They work over SSH, in tmux, and in any xterm.

## `pytest is not installed for <path>; run pip install -r requirements.txt`

**Cause:** pytest is missing from the interpreter the runner invokes. `rounds=0`
in the same message confirms the loop never started.

**Fix:**

```bash
source ~/cyberdeck-env313/bin/activate
pip install pytest
```

**Verify both paths agree:**

```bash
python -c "import pytest, sys; print(pytest.__version__); print(sys.executable)"
which pytest
```

Both must contain `cyberdeck-env313`. The runner uses `sys.executable`, so a
system-wide pytest on your PATH does not satisfy it.

## `/fix` returns `READY` without changing anything

**Cause:** the baseline test run was already green. The orchestrator short-circuits
before invoking the agent — by design.

**Check:**

```bash
python -m pytest tests/ -q
```

If it passes, there is nothing to fix. For work with no test, use `/do` instead.

## `/do` reports `agent made no changes to the target`

**Cause:** the agent edited a *different* file. Only `--target` is watched, diffed,
and executed.

**Fix:** retarget first:

```
/target path/to/the/actual/file.py
/do your demand
```

Then check what else moved:

```bash
git status --short
```

`/do` cannot see edits outside the target. `git status` can.

## Banner says `harness: online` but the agent never replies

**Cause:** credentials, usually.

**Check:**

```bash
curl -s https://api.deepseek.com/user/balance \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY"
```

A `401` means the key is wrong or inactive. An `is_available: false` means no
balance.

**Also check the PATH the venv sees:**

```bash
which dsh && dsh --version
```

A hang here is the known post-install startup bug on some Node builds. Try Node 24:

```bash
nvm install 24 && nvm use 24
```

## Changes are not detected on an external drive

**Cause:** exFAT and NTFS have coarse timestamp resolution (2 seconds on exFAT), so
`mtime`-based comparison can miss an edit.

The adapter falls back to content comparison, so diffs still work — but do not rely
on `stat` timestamps as proof of a write. Read the file, or use `git diff`.

**Better fix:** move the project to an ext4 filesystem and use the external drive
for backup.

## `dsh` hangs after install

**Cause:** a known startup boundary on some Node builds — the process burns CPU
without binding a port or printing.

**Diagnose:**

```bash
npx --yes @deepseek-ai/dsh@latest --version
npx --yes @deepseek-ai/dsh@latest web > dsh-web.log 2>&1
```

If `--version` works but the app never starts, preserve the log and try a different
Node version (22 vs 24) before reinstalling anything.

## A patch script fails with `AssertionError: anchor missing`

**Cause:** the anchor line it searched for is not in your file — usually because a
different patch already changed that region, or was never applied.

**Do not** bypass the assertion. It exists so the script refuses to write a
half-patched file that will not import.

**Diagnose the actual state:**

```bash
grep -n 'command in {' cyberdeck/app.py
grep -n 'def run_demand' cyberdeck/orchestrator.py
python -c "import ast; ast.parse(open('cyberdeck/app.py').read()); print('syntax OK')"
```

Then apply only the missing piece. Prefer patches that check for their own marker
before editing, so a partially-applied state repairs itself.
