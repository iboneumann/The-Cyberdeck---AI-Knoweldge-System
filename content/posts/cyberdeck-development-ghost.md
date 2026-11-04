+++
date = "2026-11-04"
title = "Building a Development Ghost: A Four-Pane Terminal That Fixes Its Own Scripts"
draft = false
weight = 49
+++

Summary = How a four-pane terminal, a headless AI harness, and a stubborn refusal to trust the agent's own report turned copy-paste coding into a verified loop.  


I have a folder of Python scripts that do real work: parse an Obsidian vault, generate filenames, convert notes, index a knowledge base. They were written over months, mostly by pasting code out of a chat window, reading the errors, and pasting the fix back. It works. It is also exhausting, and it does not scale past about four files.

The idea I kept circling was the one in my own project notes: an **AI Ghost** — a background process that runs system tasks rather than answering questions. Not a chatbot that suggests a fix, but a thing that reads the traceback, edits the file, runs the tests, and tells you when it is done.

This is the story of building it, including the parts that did not work.

## The three failures that came before

Every terminal-based dev tool I tried failed for the same reason, and it took me two failed attempts to name it precisely.

**The first kind** wraps a shell. Useful for running things, useless for changing them. It has no model.

**The second kind** is a chat window bolted onto a file tree. It has a model, but it has no *loop*. You ask for a change, it writes one, and then it stops — regardless of whether the change worked. You are still the one reading the error and deciding what to do next.

What was missing is the thing that makes an agent an agent: **a loop that observes the result of its own action and continues**. Write, run, read the failure, write again. That loop is the whole product.

## The architecture: four panes, one rule

The terminal has four panes, and the separation between them is the design.

| Pane | Purpose |
| :--- | :--- |
| **DEV CHAT** | Talk to the agent. Ask for refactors, explanations, new modules. |
| **CODE + NEW CODE** | Live view of the target script, plus a unified diff of the last change. |
| **TEST RUNTIME** | Structured pytest results: pass/fail counts, failing test names, messages. |
| **READY RUNTIME** | Independent execution of the script itself. |

The rule that makes it trustworthy:

> **Pane 1 fixes. Panes 3 and 4 verify.**

The agent never gets to declare success. After it stops, the terminal snapshots the file, runs pytest itself, and then runs the script itself. A green verdict comes from the terminal, not from the model's summary paragraph.

That sounds like a small thing. It is the difference between a toy and a tool. A model that says "I fixed it" is wrong often enough to be useless as an authority, and right often enough to be valuable as a worker. Put it in the worker seat.

## The stack

Three pieces, each doing one job:

- **[Textual](https://textual.textualize.io/)** for the TUI. It runs over plain SSH, in any xterm, and gives me a widget tree I can reason about.
- **[DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness)** (`dsh`) as the agent runtime. Headless profile, one task per invocation, exits when done.
- **pytest** as the oracle. Not the agent's opinion — the actual test suite.

The glue is about 900 lines of Python. The interesting part is not the UI; it is the iteration policy.

## The loop, concretely

Pressing the fix command does this:

1. **Run the tests once.** If they already pass, stop — there is nothing to fix.
2. **Snapshot the target file.** Content and mtime.
3. **Build a prompt** from the *structured* failure, not raw output. Test names, assertion messages, a stdout tail. Roughly 2 KB instead of 40 KB of pytest noise.
4. **Hand it to the agent.** One `dsh` subprocess, headless, no ports.
5. **Snapshot again and diff.** If the file did not change, stop — the agent talked but did not act.
6. **Run the tests again, yourself.** This is the step that matters. The agent's claim is ignored.
7. **If green, run the script.** A test can pass while the CLI still crashes.
8. **If red and attempts remain, repeat** with the new failure.

The attempt cap defaults to four. That is enough for most fixes and small enough that a confused agent does not burn money in a loop.

## The failures worth documenting

I am writing these down because every one of them cost time, and every one is now a known trap rather than a mystery.

### The flag that did not exist

The adapter was written against a newer headless interface than the one I installed. It passed `--json`, `--model`, and `--provider`. The installed build accepted exactly one option: `--help`.

Reading the *launcher's* help was misleading. `dsh --help` describes the boot layer — `--profile`, `--patch`, `--dump-config`. The app inside the profile has its own interface, reachable only with `dsh --profile headless --help`. Always ask the layer you are actually calling.

The fix was to stop guessing and ask the binary, then delete the three unsupported flags. Without `--json` the adapter falls back to raw-text streaming, which loses structured finish reasons but leaves the diff detection and verification untouched — those never depended on the event format.

### The plugin that would not resolve

```
plugin(s) failed to load: @deepseek-ai/dsh-sandbox-local
Cordis startup failed because these plugin(s) could not be resolved
```

The package was present in `node_modules` and still would not load. Three separate causes stacked up:

1. **pnpm refused to run build scripts.** `koffi`, a native FFI dependency of the sandbox plugin, has an install script. pnpm 10+ blocks those by default and, under `strictDepBuilds`, turns the block into a hard failure. The package gets added; its native binding never builds.
2. **Version skew inside the release.** `0.1.5-rc.2` declares its sibling dependencies as `^0.1.5-rc.2`. By the time I installed, `rc.3` existed, so npm resolved siblings *forward* while the root stayed `rc.2`. In rc.3 the sandbox plugin is no longer hoisted to the top level; it nests inside `dsh-base/node_modules`. The profile loader looks at the top level and finds nothing.
3. **A profile initialised by the broken tree** kept referencing the nested copy.

The repair was to pin the entry package to the same generation as its siblings, reinstall, and let the profile rebuild from scratch:

```bash
npm uninstall -g @deepseek-ai/dsh
npm install -g @deepseek-ai/dsh@0.1.5-rc.3
rm -rf ~/.dsh-cyberdeck && mkdir -p ~/.dsh-cyberdeck
dsh --profile headless "reply with exactly: HELLO"
```

`HELLO` coming back is the gate. Nothing else proceeds until it does.

### Ctrl+I is Tab

The fix loop was bound to `Ctrl+I`. It never fired.

In ASCII, `Ctrl+I` **is** `0x09` — the tab character. A terminal cannot distinguish them. Textual received `tab`, matched its built-in "focus next widget" binding, and silently moved focus to the chat input. Then `Ctrl+L` cleared the panes, leaving only the newly-focused input visible — which looked like "Ctrl+L opens the dev chat."

`Ctrl+Q` has the same class of problem: it is XON flow-control and gets eaten before the app sees it.

The lesson is not "pick better keys." It is **do not bind the loop to a control character if typing works just as well.** The commands are now typed:

```
/fix    /do    /target    /tests    /test    /run    /clear    /help
```

Typed commands survive tmux, SSH, and every xterm variant. They are also discoverable in a way that a hidden chord is not.

### pytest was not installed

`pyproject.toml` declared `textual` and `rich`. The example tests use `tmp_path` and `capsys`. So the runner probed for pytest, found nothing, and returned:

```
pytest is not installed for /home/.../bin/python; run pip install -r requirements.txt
```

with `rounds=0`. Zero rounds is a useful signal: the loop never started. It is a different failure from "the agent tried and failed," and worth distinguishing in your own tooling.

## Two verbs with different guarantees

The honest part of the design is that there are two ways to ask for work, and they do not claim the same thing.

**`/fix` requires a failing test.** It short-circuits on green, loops on red, and re-verifies after every attempt. Its verdict is <span class="verdict verdict-ready">READY</span>, and that word means a test passed.

**`/do` requires nothing.** It runs the agent once, shows the diff, runs tests if a test file happens to exist, then executes the script. Its verdict is <span class="verdict verdict-executed">EXECUTED</span> — which means *the file changed and the script still runs*, and nothing more.

Why keep both? Because "embed this class into that script" is mechanical work where a test contract is overhead, and "make this parser handle malformed input" is behavioural work where a test is the entire point. Refusing to offer the weaker tool would just push people to the chat pane, which verifies *nothing* and does not even show a diff.

The discipline that makes `/do` safe is git:

```bash
git add -A && git commit -m "before autonomous edit"
```

A test contract is one kind of undo. `git checkout -- file.py` is another. When you drop the first, you need the second.

## What it costs

The agent runs on the DeepSeek API. A `/fix` on a small script is a single model turn of perhaps 30k input and 3k output tokens. At current `deepseek-flash` rates that is fractions of a cent.

A full evening of iterating on four scripts — dozens of runs, a long architecture conversation, some wasted attempts — lands in the **low tens of cents**. The five-dollar balance I topped up is not going to run out on this project.

The long design conversations are especially cheap, because they are almost entirely *input*, and repeated prefixes bill as cache hits at roughly a fiftieth of the miss rate.

## What it actually changed

The scripts got better, but that is not the interesting part. The interesting part is that I stopped being the loop.

Before: read the traceback, decide what it means, paste it into a chat, read the suggested diff, judge whether it is right, apply it, re-run, discover it broke something else, repeat. The model was a suggestion engine and I was the control flow.

After: name the file, state the test, press go, read the diff. The model is the control flow and I am the reviewer. That is a different job, and a much better one.

The design that made it work was not the TUI and not the model. It was the refusal to let the model grade its own homework. Four panes, one rule: **the agent fixes, the terminal verifies.** Everything else is implementation detail.

---

*The full source and setup guide are in the [documentation](/docs/cyberdeck-terminal/). The harness is [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness), currently in developer preview — expect breaking changes, pin your versions, and keep `DSH_HOME` isolated per environment.*