+++
title = "Cyberdeck Terminal"
date = 2026-11-04
draft = false
weight = 10
tags = ["cyberdeck", "textual", "deepseek-harness"]
summary = "A four-pane terminal development environment: the agent fixes, the terminal verifies."
+++

A terminal development environment for Python scripts, built around one rule:

> **Pane 1 fixes. Panes 3 and 4 verify.**

The agent never declares success. After it stops, the terminal runs the tests itself, then runs the script itself. A green verdict comes from the terminal, not the model.

## The four panes

| Pane | Purpose |
| :--- | :--- |
| 1 · **DEV CHAT** | Talk to the agent. Ask for refactors, explanations, new modules. |
| 2 · **CODE + NEW CODE** | Live source with line numbers, plus a unified diff of the last change. |
| 3 · **TEST RUNTIME** | Structured pytest results: counts, failing test names, messages. |
| 4 · **READY RUNTIME** | Independent execution of the script itself. |

## Requirements

- Python 3.10+
- Node.js `^22.19.0 || >=24.0.0`
- `dsh` on PATH (or `npx` available)
- A DeepSeek API key
- pytest

## Pages in this section

Use the sidebar or the list below to navigate the documentation:

- **[Installation](/docs/cyberdeck-terminal/installation/)** — from a clean Ubuntu install to a working loop.
- **[Commands](/docs/cyberdeck-terminal/commands/)** — every slash command and what it guarantees.
- **[Architecture](/docs/cyberdeck-terminal/architecture/)** — how the loop, the adapter, and the verifier fit together.
- **[Source code](/docs/cyberdeck-terminal/source-code/)** — the complete implementation.
- **[Troubleshooting](/docs/cyberdeck-terminal/troubleshooting/)** — the failures that cost the most time, and their fixes.

## Two verbs, two guarantees

| Command | Requires | Verdict means |
| :--- | :--- | :--- |
| `/fix` | a failing test | a test passed, re-run independently by the terminal |
| `/do` | nothing | the file changed and the script still runs — nothing more |

`/do` is safe **only** when paired with git. Commit before every run; `git checkout -- file.py` is the undo that a test contract would otherwise provide.  

