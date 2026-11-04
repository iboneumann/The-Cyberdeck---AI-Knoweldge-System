---
title = 'Installation'
date = '2026-11-04'
draft = false
weight = 120
+++

Every step below ends with a check. Do not proceed past a failed check — later steps
assume it passed, and the resulting errors point at the wrong layer.

## 1. Node.js 22

Ubuntu's default Node is too old. Use nvm:

```bash
node --version 2>/dev/null || echo "no node"
```

If missing or below `v22.19`:

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
source ~/.bashrc
nvm install 22 && nvm use 22
```

**Check:**

```bash
node --version    # v22.x
npm --version
```

## 2. pnpm

The harness delegates plugin management to pnpm:

```bash
npm install -g pnpm
```

**Check:**

```bash
pnpm --version    # prints a version, e.g. 10.x
```

## 3. DeepSeek Harness, pinned

Install an explicit version. Never a tag — tag installs can produce a mixed-generation
dependency tree that fails to boot with a misleading plugin error.

```bash
npm install -g @deepseek-ai/dsh@0.1.5-rc.3
```

**Check:**

```bash
dsh --version     # must print, and must return in under two seconds
```

If it hangs, stop. The adapter will hang too.

## 4. Isolated profile home

Keep development state away from any future production profile:

```bash
export DSH_HOME="$HOME/.dsh-cyberdeck"
mkdir -p "$DSH_HOME"
```

Put this in a guarded file, not directly in `.bashrc`:

```bash
cat > ~/.cyberdeck-env <<'EOF'
export DEEPSEEK_API_KEY="sk-PASTE_YOUR_KEY_HERE"
export DSH_HOME="$HOME/.dsh-cyberdeck"
export TERM=xterm-256color
EOF

chmod 600 ~/.cyberdeck-env
nano ~/.cyberdeck-env        # paste the real key
source ~/.cyberdeck-env

echo 'source ~/.cyberdeck-env' >> ~/.bashrc
```

## 5. Credentials and balance

```bash
curl -s https://api.deepseek.com/user/balance \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY"
```

**Check:** JSON containing `"is_available":true` and a `total_balance`.

A `401` means the key is wrong or not yet active. Fix it now — otherwise every agent
call fails mid-loop with a confusing error.

## 6. The boot gate

```bash
dsh --profile headless "reply with exactly: HELLO"
```

**Check:** it prints `HELLO` and exits.

If it fails with `plugin(s) failed to load`, see [Troubleshooting](/docs/cyberdeck-terminal/troubleshooting/).
Do not continue until this passes — every later step depends on it.

If the profile does not exist yet, the first run creates it. If it was created by a
broken install, rebuild it:

```bash
rm -rf ~/.dsh-cyberdeck && mkdir -p ~/.dsh-cyberdeck
dsh --profile headless "reply with exactly: HELLO"
```

## 7. Python environment

```bash
python3 -m venv ~/cyberdeck-env313
source ~/cyberdeck-env313/bin/activate

cd "/path/to/cyberdeck-terminal"
pip install -e .
pip install pytest
```

**Check:**

```bash
python -c "import pytest, sys; print(pytest.__version__); print(sys.executable)"
which pytest
```

Both paths must contain `cyberdeck-env313`. The runner invokes `sys.executable`
directly, so a venv mismatch produces `pytest is not installed` even when pytest
is on your PATH.

## 8. Launch

```bash
cd "/path/to/cyberdeck-terminal"
source ~/.cyberdeck-env
source ~/cyberdeck-env313/bin/activate

python -m cyberdeck \
  --target scripts/example_target.py \
  --tests tests/test_example_target.py
```

**Check:** four bordered panes open, and pane 1's banner says `harness: online`.

If it says `OFFLINE`, `dsh` is not on the PATH this shell sees:

```bash
which dsh && dsh --version
```

## 9. First loop

The bundled example ships with one deliberate defect: `parse_frontmatter` lowercases
all keys, but `index_notes` reads `meta["Title"]`, so any note with `Title:` in its
frontmatter raises `KeyError`.

Type in the chat input:

```
/fix
```

Press Enter.

**Check, in order:**

1. Pane 3: `fix loop engaged` → `baseline test run` → `FAIL exit=1` → `failed=1 passed=5`
2. Pane 3: `attempt 1/4`
3. Pane 1: agent reasoning streams as text
4. Pane 2: `── new code +1 / -1` with a hunk changing `meta["Title"]`
5. Pane 3: `PASS exit=0` → `passed=6` → `◉ READY — green after 1 attempt(s)`
6. Pane 4: `RUN exit=0` with JSON output

If pane 3 shows `PASS` immediately at the baseline, the bug was already fixed — restore it:

```bash
git checkout scripts/example_target.py
```

## 10. Verify outside the TUI

Do this once per session. It is what keeps "the tool says ready" honest.

```bash
python -m pytest tests/test_example_target.py -q
grep -n 'title =' scripts/example_target.py
```

Expect `6 passed` and `title = meta.get("title") or path.stem`.
