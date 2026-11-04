---
title: "Commands"
date = '2026-11-04'
draft = false
weight = 130
+++

Commands are **typed into the chat input**, not bound to keys. This is deliberate:
`Ctrl+I` is indistinguishable from Tab in ASCII, and `Ctrl+Q` is XON flow-control.
Typed commands survive tmux, SSH, and every xterm variant.

## Reference

| Command | Alias | Requires | Verdict |
| :--- | :--- | :--- | :--- |
| `/fix [directive]` | `/iterate`, `/loop` | a failing test | `READY` or `NOT READY` |
| `/do <demand>` | `/demand` | nothing | `EXECUTED` or `INCOMPLETE` |
| `/target <path>` | `/t` | — | retargets pane 2 and 4 |
| `/tests <path>` | — | — | sets the test path |
| `/test` | `/tests` | — | runs pytest once |
| `/run` | `/ready` | — | executes the target script once |
| `/clear` | — | — | wipes all four panes |
| `/help` | `/?` | — | lists commands |

## `/fix` — verified repair

Loops until tests pass or the attempt cap is reached. The terminal re-runs pytest
after every agent edit; the agent's own claim is ignored.

```
/fix refactor DeckStore so persistence goes through one atomic-write method
```

The optional directive is injected into the prompt alongside the structured failure.
Use it when the fix requires a specific approach, not just "make it pass."

**Verdicts:**

- `◉ READY — green after N attempt(s)` — tests passed, re-run independently.
- `◌ NOT READY — agent made no changes` — the agent replied without editing.
- `◌ NOT READY — attempt cap reached (4)` — edits happened, tests still fail.

**Short-circuit:** if the baseline test run already passes, the agent is never
invoked. This is why a test must exist and fail before `/fix` does anything.

## `/do` — unverified execution

One agent call, one diff, no loop. Tests run only if a test file exists at the
configured path.

```
/do embed class NoteStore from classes/NoteStore.py into production/deck.py,
keep its public API identical, add required imports at module level
```

**Verdicts:**

- `◉ EXECUTED — script runs — not test-verified` — the file changed and the script
  still executes. That is the entire claim.
- `◌ INCOMPLETE — agent made no changes to the target` — nothing was written.
- `◌ INCOMPLETE — script exits N` — the edit broke execution.

**`/do` never returns `READY`.** If it does, something is wrong.

### When `/do` is appropriate

Mechanical, unambiguous work you can judge by reading the diff:

- copying or embedding a class
- adding imports at module level
- renaming a method and its call sites
- writing a launcher script
- converting `sys.argv` parsing to `argparse`

### When it is not

Anything where "it runs" differs from "it is right":

- data transformations — wrong output still exits 0
- parsing logic — silently drops records and runs fine
- anything with a behavioural contract

Write the test and use `/fix`.

### The git discipline

`/do` is safe only with an undo:

```bash
git add -A && git commit -m "before autonomous edit"
```

After:

```bash
git diff                              # what actually changed
git checkout -- production/deck.py    # undo it
```

## `/target` — retarget the watched file

```
/target production/launch.py
```

Relative paths resolve against the **launch directory** (where you ran
`python -m cyberdeck`), not your last `cd`. The snapshot is discarded so the new
file renders fresh.

The file need not exist. Pointing at a missing path is the intended way to create
a new file: the diff will show the whole thing as added.

**`/target` does not change `/tests`.** After retargeting, set the matching test
path or `/fix` will try to satisfy the old file's tests.

## `/tests` — retarget the test path

```
/tests production/tests/test_launch.py
```

Accepts a file or a directory. Directories recurse.

## `/test` and `/run` — single checks

```
/test
/run
```

`/test` runs pytest once and renders the structured result. `/run` executes the
target script and shows stdout, stderr, and exit code. Neither invokes the agent.
Use them to check state before committing to a loop.

## `/clear`

Wipes all four panes and re-renders the code pane. Useful after a noisy session.

## Directives

`/fix` and `/do` both accept text after the command. It is passed to the agent
verbatim, alongside the structured failure for `/fix` and the target path for both.

Be specific. "Add the class" produces a guess; "add class NoteStore with methods
`put(key, text)`, `get(key)` returning text or None, and `count()`, preserving the
existing CLI" produces the class you wanted.

## Session behaviour

- `/target` and `/tests` are **session-only**. Restarting returns to the command-line
  values.
- Workers are exclusive per group. Do not fire `/do` while `/fix` is running — they
  can write to the same file concurrently.
- Every chat turn is persisted to `.cyberdeck/state.json`. Read it when you need to
  copy text out of the TUI:

```bash
python3 -c "
import json
s = json.load(open('.cyberdeck/state.json'))
for m in s['chat'][-4:]:
    print(f\"--- {m['role']} ---\")
    print(m['text'][:1500])
"
```
