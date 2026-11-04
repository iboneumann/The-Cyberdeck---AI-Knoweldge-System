+++
date: 2026-11-04
title: 'DeepSeek Harness on Ubuntu Server LTS: What Works and What Bites'
draft: false
weight: 50
+++
Summary: "A field report on running dsh headless on Ubuntu 22.04 and 24.04: supported versions, the pnpm build-script trap, and how to isolate a development profile from a production one."  


DeepSeek Harness (`dsh`) is an open-source agent runtime from DeepSeek AI, built on an everything-is-a-plugin architecture and powered by [Cordis](https://github.com/cordiverse/cordis). It is not a model. It orchestrates agents, tools, plugins, and model providers.

This is what I learned running it headless on Ubuntu LTS, including the parts that are not in the README.

## Ubuntu support: yes, comfortably

Ubuntu is one of the better-supported Linux targets. Community compatibility lists mark **Ubuntu 20.04+** as fully supported, with LTS versions recommended, and CI packaging verification has run on **22.04 LTS**. Deployments in the wild use 24.04 as well.

The real constraint is not the distro, it is **Node.js**:

```
^22.19.0 || >=24.0.0
```

Ubuntu's default `nodejs` package is almost always older. Install Node 22 via nvm rather than apt — it needs no sudo, lives in your home, and gives you version switching when a release breaks something:

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
source ~/.bashrc
nvm install 22 && nvm use 22
node --version   # must be v22.x
```

The glibc floor is 2.28. Ubuntu 20.04 (2.31), 22.04 (2.35), and 24.04 (2.39) all clear it. CentOS 7 (2.17) does not.

## Install pnpm before you need it

`dsh` delegates profile plugin management to `pnpm`. If it is missing you get a clear but late failure:

```
dsh: pnpm not found on PATH — install pnpm to manage profile plugins
```

Install it once:

```bash
npm install -g pnpm
pnpm --version
```

## The build-script trap

Modern pnpm blocks dependency install scripts by default, and under `strictDepBuilds` turns a block into a hard failure. The sandbox plugin depends on `koffi`, a native FFI package with an install script. Result:

```
Error: ERR_PNPM_IGNORED_BUILDS
  × adding a new package
  ╰─▶ Ignored build scripts: koffi@3.3.6
```

The package is added; its native binding never builds; the plugin never resolves. Two ways out:

**Non-interactive approval**, which writes the decision into the profile's `pnpm-workspace.yaml`:

```bash
dsh plugin --profile headless approve-builds --all
```

**Or the explicit edit**, if `--all` is unavailable in your pnpm version. Open `~/.dsh-cyberdeck/profiles/headless/pnpm-workspace.yaml` and ensure:

```yaml
allowBuilds:
  koffi@3.3.6: true
```

The version-qualified key matters. pnpm writes placeholders like `set this to true or false` when it first meets an undecided package, and an unqualified `koffi: true` may not match the pinned identity.

Approving `koffi` is defensible: it is a dependency of DeepSeek's own sandbox plugin, pinned by the profile, and its script selects a **prebuilt** binary rather than compiling from source. It is not arbitrary code from a stranger's repository.

## Version skew inside a preview release

This one cost me an evening and is worth understanding, because the error message points somewhere unhelpful.

`0.1.5-rc.2` declares its sibling dependencies as `^0.1.5-rc.2`. If `rc.3` is published when you install, npm resolves those siblings **forward** to rc.3 while the root stays rc.2. You end up with a mixed-generation tree.

In rc.3 the sandbox plugin is no longer hoisted to the top level of `node_modules` — it nests inside `dsh-base/node_modules/@deepseek-ai/`. The profile loader looks at the top level, finds nothing, and reports:

```
plugin(s) failed to load: @deepseek-ai/dsh-sandbox-local
```

No amount of reinstalling the plugin fixes this, because the plugin was never the problem. The fix is to install a self-consistent generation:

```bash
npm uninstall -g @deepseek-ai/dsh
npm install -g @deepseek-ai/dsh@0.1.5-rc.3
```

Then rebuild the profile, since the old one was initialised by the broken tree:

```bash
rm -rf ~/.dsh-cyberdeck
mkdir -p ~/.dsh-cyberdeck
dsh --profile headless "reply with exactly: HELLO"
```

**Pin to an explicit version, never a tag.** Installing by tag is what produced the mixed tree. And always gate on a bare `HELLO` before wiring the harness into anything else — it isolates "the runtime is broken" from "my integration is broken."

## Read the layer you are actually calling

`dsh --help` describes the **launcher**: `--profile`, `--from-default-profile`, `--patch`, `--dump-config`, `--version`. The app *inside* a profile has its own interface:

```bash
dsh --profile headless --help
```

Which, on current builds, is:

```
Usage: dsh --profile headless [options] [task...]
Answer one task, stream reasoning to stderr, print the final assistant message, and exit.

Options:
  -h, --help  show this help
```

One option. Everything else is the task text. Older builds took `--json` for an NDJSON event stream; that flag is gone, and passing it produces `error: unknown option '--json'` before the agent ever starts.

The practical consequence: **read stdout line by line and treat each line as text.** If you were relying on structured events for finish reasons, you lose them — but you gain a runtime that does not change shape under you.

## Isolate development from production

`DSH_HOME` is where profiles, sessions, and plugin trees live. Default is somewhere under your home directory; override it per environment:

```bash
export DSH_HOME="$HOME/.dsh-cyberdeck-dev"
```

A dev profile gets the web UI and permissive tooling. A production profile gets headless and a tighter sandbox. They never share plugin state, and a broken plugin install in dev cannot take out production.

One trap: a trailing space in `DSH_HOME` is treated as part of the path. The process then resolves a different, empty data root, and the UI appears factory-reset while your real sessions sit intact elsewhere. Print it with delimiters before debugging anything that looks like lost state:

```bash
printf 'DSH_HOME=<%s>\n' "$DSH_HOME"
```

## Headless is the right default on a server

The web profile is excellent for exploration, but on a server it is a listening service with a browser dependency. Headless opens no ports and leaves nothing running:

```bash
dsh --profile headless "run the tests and report failures"
```

Exit code `0` means the task completed. Non-zero means it aborted — which is different from "it ran and the tests failed." If you need to distinguish those, run the tests yourself afterward rather than inferring from the harness's exit code.

## A minimal working setup

```bash
# Node
nvm install 22 && nvm use 22

# pnpm and harness
npm install -g pnpm
npm install -g @deepseek-ai/dsh@0.1.5-rc.3

# Isolated profile home
export DSH_HOME="$HOME/.dsh-cyberdeck"
mkdir -p "$DSH_HOME"

# Credentials
export DEEPSEEK_API_KEY="sk-..."
curl -s https://api.deepseek.com/user/balance \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY"

# Gate
dsh --profile headless "reply with exactly: HELLO"
```

Put the exports in a `chmod 600` file sourced from your shell rc, not directly in `.bashrc`. Keys in `.bashrc` end up in backups, in dotfile repos, and in shell history.

## The honest summary

DeepSeek Harness works well on Ubuntu LTS once you get past two specific traps: pnpm's build-script policy and version skew inside a preview release. Both produce error messages that point at the wrong layer.

It is in **developer preview** and will make compatibility-breaking changes. Pin versions. Isolate `DSH_HOME`. Gate every environment change on a bare `HELLO` before building on top of it. Do that and it is a stable, fast, cheap agent runtime with no server footprint.
