---
title = 'Source Code'
date = '2026-11-04'
draft = false
weight = 150
+++

MIT licensed, matching DeepSeek Harness. This is the current working state —
the version that runs against `dsh` headless builds that accept only
`--profile` and the task text.

## Layout

```
cyberdeck-terminal/
  pyproject.toml
  requirements.txt
  cyberdeck/
    __init__.py
    __main__.py
    config.py
    state.py
    watcher.py
    runner.py
    dsh_adapter.py
    orchestrator.py
    app.py
    theme.tcss
  scripts/example_target.py
  tests/test_example_target.py
```

## `pyproject.toml`

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "cyberdeck-terminal"
version = "0.1.0"
description = "Four-pane terminal development environment driving DeepSeek Harness"
requires-python = ">=3.10"
dependencies = ["textual>=0.86", "rich>=13.7"]

[project.scripts]
cyberdeck = "cyberdeck.__main__:main"

[tool.setuptools]
packages = ["cyberdeck"]
```

## `requirements.txt`

```text
textual>=0.86
rich>=13.7
pytest>=8.0
```

## `cyberdeck/config.py`

```python
"""Configuration for the Cyberdeck terminal."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class Config:
    """Runtime configuration, resolved from CLI flags and environment."""

    target: Path = Path("scripts/example_target.py")
    tests: Path = Path("tests/test_example_target.py")
    workdir: Path = field(default_factory=Path.cwd)

    # Harness
    dsh_command: str = "dsh"
    profile: str = "headless"
    model: str = "deepseek-v4-flash"
    provider: str = "deepseek-official"
    dsh_home: Path | None = None
    agent_timeout: float = 600.0

    # Loop policy
    max_attempts: int = 4

    # Execution
    python_exec: str = "python3"
    run_timeout: float = 120.0
    test_timeout: float = 300.0

    # State
    state_dir: Path = Path(".cyberdeck")

    @classmethod
    def from_env(cls, **overrides) -> "Config":
        cfg = cls()
        home = os.environ.get("DSH_HOME")
        if home:
            cfg.dsh_home = Path(home)
        for key, value in overrides.items():
            if value is not None and hasattr(cfg, key):
                setattr(cfg, key, value)
        cfg.target = Path(cfg.target)
        cfg.tests = Path(cfg.tests)
        return cfg

    def ensure_state_dir(self) -> Path:
        path = self.workdir / self.state_dir
        path.mkdir(parents=True, exist_ok=True)
        return path
```

## `cyberdeck/watcher.py`

```python
"""File snapshots and unified diffs for the CODE + NEW CODE pane."""

from __future__ import annotations

import difflib
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Snapshot:
    path: Path
    content: str
    mtime: float

    @classmethod
    def take(cls, path: Path) -> "Snapshot":
        try:
            stat = path.stat()
            return cls(
                path=path,
                content=path.read_text(encoding="utf-8", errors="replace"),
                mtime=stat.st_mtime,
            )
        except OSError:
            return cls(path=path, content="", mtime=0.0)

    def changed_since(self, other: "Snapshot | None") -> bool:
        if other is None:
            return True
        # Content comparison, not mtime alone: exFAT has 2s resolution.
        return self.mtime != other.mtime or self.content != other.content

    def unified_diff(self, other: "Snapshot") -> list[str]:
        """Diff from `other` (older) to `self` (newer)."""
        return list(difflib.unified_diff(
            other.content.splitlines(),
            self.content.splitlines(),
            fromfile=f"a/{other.path.name}",
            tofile=f"b/{self.path.name}",
            lineterm="",
            n=3,
        ))

def summarize_diff(lines: list[str]) -> tuple[int, int]:
    added = sum(1 for ln in lines if ln.startswith("+") and not ln.startswith("+++"))
    removed = sum(1 for ln in lines if ln.startswith("-") and not ln.startswith("---"))
    return added, removed
```

## `cyberdeck/runner.py`

```python
"""Structured execution of tests and target scripts.

The agent is never handed raw, noisy process output. Every function here
returns a small typed result with the failure signal already extracted.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

_FAIL_LINE = re.compile(r"^(FAILED|ERROR)\s+(\S+)(?:\s+-\s+(.*))?$", re.MULTILINE)
_PASSED = re.compile(r"(\d+)\s+passed")
_FAILED_COUNT = re.compile(r"(\d+)\s+failed")
_ERROR_COUNT = re.compile(r"(\d+)\s+errors?")
_SKIPPED = re.compile(r"(\d+)\s+skipped")

@dataclass
class Failure:
    name: str
    message: str

@dataclass
class RunResult:
    ok: bool
    command: list[str]
    exit_code: int
    duration: float
    stdout: str = ""
    stderr: str = ""
    failures: list[Failure] = field(default_factory=list)
    summary: dict[str, int] = field(default_factory=dict)

    def brief(self, tail: int = 2500) -> str:
        """Compact representation for the agent's prompt."""
        payload = {
            "ok": self.ok,
            "exit_code": self.exit_code,
            "summary": self.summary,
            "failures": [asdict(f) for f in self.failures[:20]],
            "stdout_tail": self.stdout[-tail:],
            "stderr_tail": self.stderr[-1200:],
        }
        return json.dumps(payload, indent=2)

    def to_dict(self) -> dict:
        data = asdict(self)
        data["command"] = list(self.command)
        return data

class Runner:
    def __init__(self, python_exec: str = sys.executable, workdir: Path | None = None):
        self.python_exec = python_exec
        self.workdir = workdir or Path.cwd()

    def run_tests(self, test_path: Path, timeout: float = 300.0) -> RunResult:
        if self._has_pytest():
            command = [
                self.python_exec, "-m", "pytest", str(test_path),
                "-q", "--tb=short", "--no-header", "-p", "no:cacheprovider",
            ]
            return self._execute(command, timeout, parse="pytest")
        command = [self.python_exec, "-m", "unittest", "discover", "-s", str(test_path.parent)]
        return self._execute(command, timeout, parse="unittest")

    def _has_pytest(self) -> bool:
        try:
            proc = subprocess.run(
                [self.python_exec, "-m", "pytest", "--version"],
                capture_output=True, text=True, timeout=20,
            )
            return proc.returncode == 0
        except (OSError, subprocess.SubprocessError):
            return False

    def run_script(self, script: Path, args: list[str] | None = None,
                   timeout: float = 120.0) -> RunResult:
        command = [self.python_exec, str(script), *(args or [])]
        return self._execute(command, timeout, parse="script")

    def _execute(self, command: list[str], timeout: float, parse: str) -> RunResult:
        started = time.monotonic()
        try:
            proc = subprocess.run(
                command, cwd=str(self.workdir), capture_output=True,
                text=True, timeout=timeout,
            )
            result = RunResult(
                ok=proc.returncode == 0,
                command=command,
                exit_code=proc.returncode,
                duration=time.monotonic() - started,
                stdout=proc.stdout or "",
                stderr=proc.stderr or "",
            )
        except subprocess.TimeoutExpired as exc:
            result = RunResult(
                ok=False, command=command, exit_code=124,
                duration=time.monotonic() - started,
                stdout=(exc.stdout or "") if isinstance(exc.stdout, str) else "",
                stderr=f"TIMEOUT after {timeout:.0f}s",
                failures=[Failure(name="<timeout>", message=f"exceeded {timeout:.0f}s")],
            )
        except OSError as exc:
            result = RunResult(
                ok=False, command=command, exit_code=127,
                duration=time.monotonic() - started,
                stderr=str(exc),
                failures=[Failure(name="<exec>", message=str(exc))],
            )

        if parse == "pytest":
            self._parse_pytest(result)
        elif parse == "script":
            self._parse_script(result)
        return result

    @staticmethod
    def _parse_pytest(result: RunResult) -> None:
        output = result.stdout + "\n" + result.stderr
        counts = {
            "passed": _first_int(_PASSED, output),
            "failed": _first_int(_FAILED_COUNT, output),
            "errors": _first_int(_ERROR_COUNT, output),
            "skipped": _first_int(_SKIPPED, output),
        }
        result.summary = {k: v for k, v in counts.items() if v}

        seen: set[str] = set()
        for match in _FAIL_LINE.finditer(output):
            name = match.group(2)
            if name in seen:
                continue
            seen.add(name)
            result.failures.append(
                Failure(name=name, message=(match.group(3) or "").strip()))

        if result.failures:
            result.ok = False

    @staticmethod
    def _parse_script(result: RunResult) -> None:
        if result.ok:
            return
        if not result.failures:
            last = ""
            for line in reversed(result.stderr.strip().splitlines()):
                if line.strip():
                    last = line.strip()
                    break
            result.failures.append(
                Failure(
                    name=result.command[1] if len(result.command) > 1 else "<script>",
                    message=last or f"exit code {result.exit_code}",
                )
            )

def _first_int(pattern: re.Pattern[str], text: str) -> int:
    match = pattern.search(text)
    return int(match.group(1)) if match else 0
```

## `cyberdeck/dsh_adapter.py`

```python
"""Bridge to DeepSeek Harness.

Runs `dsh --profile <profile> "<prompt>"` as a subprocess, streams output line
by line, and degrades gracefully if the harness is missing or its output shape
differs from expectations.

Current headless builds accept only the profile and the task text. There is no
--json flag; every line is treated as text. Structured event parsing is kept as
an opportunistic bonus, never a dependency.
"""

from __future__ import annotations

import asyncio
import json
import os
import shutil
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

EventCallback = Callable[[str, dict], None]

@dataclass
class TaskResult:
    ok: bool
    exit_code: int
    output: str
    duration: float
    events: list[dict] = field(default_factory=list)
    finish_reason: str = "unknown"

class DshAdapter:
    def __init__(
        self,
        command: str = "dsh",
        profile: str = "headless",
        model: str = "deepseek-v4-flash",
        provider: str = "deepseek-official",
        dsh_home: Path | None = None,
        on_event: EventCallback | None = None,
    ):
        self.command = command
        self.profile = profile
        self.model = model
        self.provider = provider
        self.dsh_home = dsh_home
        self.on_event = on_event

    def resolve_binary(self) -> list[str] | None:
        explicit = shutil.which(self.command)
        if explicit:
            return [explicit]
        npx = shutil.which("npx")
        if npx:
            return [npx, "--yes", "@deepseek-ai/dsh"]
        return None

    def available(self) -> bool:
        return self.resolve_binary() is not None

    def run(self, prompt: str, cwd: Path | None = None,
            timeout: float = 600.0) -> TaskResult:
        """Synchronous entry point. Call from a worker thread only."""
        try:
            return asyncio.run(self._run_async(prompt, cwd, timeout))
        except RuntimeError:
            loop = asyncio.new_event_loop()
            try:
                return loop.run_until_complete(self._run_async(prompt, cwd, timeout))
            finally:
                loop.close()

    async def _run_async(self, prompt: str, cwd: Path | None,
                         timeout: float) -> TaskResult:
        prefix = self.resolve_binary()
        if prefix is None:
            message = (
                "DeepSeek Harness not found.\n"
                "Install it with:  npm install -g @deepseek-ai/dsh\n"
                "or ensure npx is on PATH."
            )
            self._emit("error", {"message": message})
            return TaskResult(ok=False, exit_code=127, output=message,
                              duration=0.0, finish_reason="missing-runtime")

        # Current headless builds: profile + task text only.
        argv = [*prefix, "--profile", self.profile, prompt]

        env = os.environ.copy()
        if self.dsh_home:
            env["DSH_HOME"] = str(self.dsh_home)

        started = time.monotonic()
        try:
            proc = await asyncio.create_subprocess_exec(
                *argv,
                cwd=str(cwd) if cwd else None,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env,
            )
        except OSError as exc:
            self._emit("error", {"message": f"failed to launch dsh: {exc}"})
            return TaskResult(ok=False, exit_code=127, output=str(exc),
                              duration=0.0, finish_reason="launch-failed")

        events: list[dict] = []
        chunks: list[str] = []
        finish_reason = "completed"

        async def drain(stream, is_stderr: bool) -> None:
            nonlocal finish_reason
            while True:
                line = await stream.readline()
                if not line:
                    return
                text = line.decode("utf-8", errors="replace").rstrip("\n")
                if not text:
                    continue
                event = self._parse_line(text, is_stderr)
                events.append(event)
                rendered = self._render_event(event)
                if rendered:
                    chunks.append(rendered)
                if event.get("kind") == "finish":
                    finish_reason = str(event.get("reason", "completed"))
                self._emit("dsh", event)

        try:
            await asyncio.wait_for(
                asyncio.gather(drain(proc.stdout, False), drain(proc.stderr, True)),
                timeout=timeout,
            )
            exit_code = await asyncio.wait_for(proc.wait(), timeout=30)
        except asyncio.TimeoutError:
            proc.kill()
            await proc.wait()
            self._emit("error", {"message": f"agent timed out after {timeout:.0f}s"})
            return TaskResult(ok=False, exit_code=124, output="".join(chunks),
                              duration=time.monotonic() - started,
                              events=events, finish_reason="timeout")

        return TaskResult(
            ok=exit_code == 0,
            exit_code=exit_code,
            output="".join(chunks),
            duration=time.monotonic() - started,
            events=events,
            finish_reason=finish_reason,
        )

    def _parse_line(self, text: str, is_stderr: bool) -> dict:
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            return {"kind": "stderr" if is_stderr else "raw", "text": text}
        if not isinstance(data, dict):
            return {"kind": "raw", "text": text}

        kind = str(data.get("type") or data.get("event") or "event")
        if kind in {"finish", "done", "completed"}:
            return {
                "kind": "finish",
                "reason": data.get("reason") or data.get("finish_reason") or "completed",
                "payload": data,
            }
        return {"kind": kind, "payload": data, "text": self._extract_text(data)}

    @staticmethod
    def _extract_text(data: dict) -> str:
        for key in ("delta", "text", "content", "message", "output"):
            value = data.get(key)
            if isinstance(value, str) and value:
                return value
            if isinstance(value, dict):
                inner = value.get("text") or value.get("content")
                if isinstance(inner, str):
                    return inner
        return ""

    @staticmethod
    def _render_event(event: dict) -> str:
        text = event.get("text") or ""
        if not text:
            return ""
        if event.get("kind") in {"stderr", "error"}:
            return f"\n[stderr] {text}\n"
        return text

    def _emit(self, name: str, payload: dict) -> None:
        if self.on_event:
            try:
                self.on_event(name, payload)
            except Exception:  # noqa: BLE001 - never let a callback kill the run
                pass
```

## `cyberdeck/orchestrator.py`

```python
"""Iteration policy for the development Ghost.

The agent proposes edits. The orchestrator decides whether the result is
acceptable, and always re-verifies independently rather than trusting the
agent's own report.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Callable

from .config import Config
from .dsh_adapter import DshAdapter, TaskResult
from .runner import RunResult, Runner
from .watcher import Snapshot, summarize_diff

EventCallback = Callable[[str, dict], None]

@dataclass
class Attempt:
    index: int
    before: RunResult
    agent: TaskResult | None
    after: RunResult | None
    added: int = 0
    removed: int = 0
    duration: float = 0.0

@dataclass
class IterationReport:
    ok: bool
    attempts: list[Attempt] = field(default_factory=list)
    final: RunResult | None = None
    reason: str = ""

    @property
    def rounds(self) -> int:
        return len(self.attempts)

SYSTEM_PREAMBLE = """You are the development Ghost inside a Cyberdeck terminal.

You are repairing a Python script until its test suite passes.

Rules:
- Modify only the target script. Never edit the tests.
- Make the smallest change that fixes the real cause.
- After editing, run the tests before replying.
- If a run fails for an environmental reason (missing module, permissions),
  say so plainly instead of guessing at the code.
- Reply with one line: what you changed and whether tests now pass.
"""

class Orchestrator:
    def __init__(self, cfg: Config, adapter: DshAdapter, runner: Runner,
                 on_event: EventCallback | None = None):
        self.cfg = cfg
        self.adapter = adapter
        self.runner = runner
        self.on_event = on_event

    def _emit(self, name: str, payload: dict) -> None:
        if self.on_event:
            try:
                self.on_event(name, payload)
            except Exception:  # noqa: BLE001
                pass

    # -- verified repair -----------------------------------------------------

    def iterate(self, directive: str = "") -> IterationReport:
        report = IterationReport(ok=False)

        self._emit("status", {"text": "baseline test run"})
        baseline = self.runner.run_tests(self.cfg.tests, timeout=self.cfg.test_timeout)
        self._emit("test", baseline.to_dict())

        if baseline.ok:
            report.ok = True
            report.final = baseline
            report.reason = "tests already green"
            self._emit("status", {"text": "already ready"})
            return report

        current = baseline
        for attempt_index in range(1, self.cfg.max_attempts + 1):
            started = time.monotonic()
            before = Snapshot.take(self.cfg.target)

            self._emit("status",
                       {"text": f"attempt {attempt_index}/{self.cfg.max_attempts}"})
            prompt = self._build_prompt(current, attempt_index, directive)

            agent = self.adapter.run(prompt, cwd=self.cfg.workdir,
                                     timeout=self.cfg.agent_timeout)

            after = Snapshot.take(self.cfg.target)
            diff = after.unified_diff(before)
            added, removed = summarize_diff(diff)
            self._emit("diff", {"lines": diff, "added": added,
                                "removed": removed, "attempt": attempt_index})

            if not after.changed_since(before):
                report.attempts.append(Attempt(
                    index=attempt_index, before=current, agent=agent, after=None,
                    duration=time.monotonic() - started))
                report.final = current
                report.reason = "agent made no changes"
                self._emit("status", {"text": "no changes made — stopping"})
                break

            self._emit("status", {"text": f"verifying (attempt {attempt_index})"})
            verified = self.runner.run_tests(self.cfg.tests,
                                             timeout=self.cfg.test_timeout)
            self._emit("test", verified.to_dict())

            report.attempts.append(Attempt(
                index=attempt_index, before=current, agent=agent, after=verified,
                added=added, removed=removed,
                duration=time.monotonic() - started))
            current = verified

            if verified.ok:
                report.ok = True
                report.final = verified
                report.reason = f"green after {attempt_index} attempt(s)"
                break

        if report.final is None:
            report.final = current
        if not report.ok and not report.reason:
            report.reason = f"attempt cap reached ({self.cfg.max_attempts})"
        return report

    # -- free-form demand (no test requirement) ------------------------------

    def run_demand(self, demand: str) -> IterationReport:
        """Execute one free-form demand. No test suite required.

        Verification is deliberately degraded: diff, optional tests, smoke run.
        None of that establishes correctness. Git is the undo.
        """
        report = IterationReport(ok=False)
        before = Snapshot.take(self.cfg.target)

        self._emit("status", {"text": "executing demand"})
        prompt = self._build_demand_prompt(demand)

        agent = self.adapter.run(prompt, cwd=self.cfg.workdir,
                                 timeout=self.cfg.agent_timeout)

        after = Snapshot.take(self.cfg.target)
        diff = after.unified_diff(before)
        added, removed = summarize_diff(diff)
        self._emit("diff", {"lines": diff, "added": added,
                            "removed": removed, "attempt": 1})

        changed = after.changed_since(before)

        if self.cfg.tests.exists():
            test_result = self.runner.run_tests(self.cfg.tests,
                                                timeout=self.cfg.test_timeout)
            self._emit("test", test_result.to_dict())
        else:
            test_result = None
            self._emit("status", {"text": "no test file — skipping tests"})

        run_result = self.runner.run_script(self.cfg.target,
                                            timeout=self.cfg.run_timeout)
        self._emit("ready", run_result.to_dict())

        report.attempts.append(Attempt(
            index=1,
            before=RunResult(ok=True, command=[], exit_code=0, duration=0.0),
            agent=agent,
            after=test_result,
            added=added,
            removed=removed,
            duration=agent.duration,
        ))
        report.final = run_result

        if not changed:
            report.reason = "agent made no changes to the target"
        elif run_result.ok:
            report.ok = True
            report.reason = "script runs — not test-verified"
        else:
            report.reason = f"script exits {run_result.exit_code}"
        return report

    # -- prompt construction -------------------------------------------------

    def _build_prompt(self, result: RunResult, attempt: int,
                      directive: str = "") -> str:
        extra = (
            f"\nOperator direction — follow this, it overrides generic fixes:\n"
            f"{directive}\n" if directive.strip() else ""
        )
        return (
            f"{SYSTEM_PREAMBLE}\n"
            f"Target script: {self.cfg.target}\n"
            f"Test path: {self.cfg.tests}\n"
            f"Attempt: {attempt} of {self.cfg.max_attempts}\n"
            f"{extra}\n"
            f"Current failure:\n{result.brief()}\n\n"
            f"Fix the script so the tests pass, then re-run them."
        )

    def _build_demand_prompt(self, demand: str) -> str:
        return (
            "You are the development Ghost inside a Cyberdeck terminal.\n"
            "No test suite gates this task. Execute the demand exactly and\n"
            "make the smallest correct change.\n\n"
            f"Target file: {self.cfg.target}\n"
            f"Workspace: {self.cfg.workdir}\n\n"
            f"Demand:\n{demand}\n\n"
            "Edit files directly. Do not ask for confirmation. Reply with one\n"
            "line naming the files you changed and what you did.\n"
        )
```

## `cyberdeck/app.py`

```python
"""The Cyberdeck terminal: four panes, one loop.

Pane 1  DEV CHAT        talk to the harness
Pane 2  CODE + NEW CODE live source plus the diff from the last pass
Pane 3  TEST RUNTIME    structured pytest results
Pane 4  READY RUNTIME   independent execution of the script itself

The agent fixes. The terminal verifies.
"""

from __future__ import annotations

import time
from pathlib import Path

from rich.syntax import Syntax
from rich.text import Text
from textual import work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Grid, Vertical
from textual.widgets import Footer, Header, Input, RichLog, Static

from .config import Config
from .dsh_adapter import DshAdapter
from .orchestrator import IterationReport, Orchestrator
from .runner import Failure, RunResult, Runner
from .state import StateStore
from .watcher import Snapshot, summarize_diff

ACCENT = "#33ff66"
AMBER = "#ffb000"
DIM = "#4f8a5f"
ERROR = "#ff5555"

class CyberdeckApp(App):
    CSS_PATH = "theme.tcss"
    TITLE = "CYBERDECK // DEVELOPMENT GHOST"

    # Kept for muscle memory, but the typed commands are the real interface.
    BINDINGS = [
        Binding("f5", "iterate", "Fix loop"),
        Binding("ctrl+t", "run_tests", "Test"),
        Binding("ctrl+r", "run_ready", "Run"),
        Binding("ctrl+l", "clear_panes", "Clear"),
        Binding("f10", "quit", "Quit"),
    ]

    def __init__(self, cfg: Config | None = None, pane: str | None = None):
        super().__init__()
        self.cfg = cfg or Config.from_env()
        self.pane_mode = pane
        self.runner = Runner(python_exec=self.cfg.python_exec, workdir=self.cfg.workdir)
        self.state = StateStore(self.cfg.ensure_state_dir())
        self.snapshot: Snapshot | None = None
        self._last_state_version = -1
        self.adapter = DshAdapter(
            command=self.cfg.dsh_command,
            profile=self.cfg.profile,
            model=self.cfg.model,
            provider=self.cfg.provider,
            dsh_home=self.cfg.dsh_home,
            on_event=self._on_agent_event,
        )
        self.orchestrator = Orchestrator(
            self.cfg, self.adapter, self.runner, on_event=self._on_agent_event,
        )

    # -- layout --------------------------------------------------------------

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Grid(id="grid"):
            with Vertical(classes="pane", id="chat-pane"):
                yield Static("1 // DEV CHAT", classes="pane-title")
                yield RichLog(id="chat-log", wrap=True, markup=True)
                yield Input(placeholder="task the development ghost…", id="chat-input")
            with Vertical(classes="pane", id="code-pane"):
                yield Static("2 // CODE + NEW CODE", classes="pane-title")
                yield RichLog(id="code-log", wrap=False, markup=True)
            with Vertical(classes="pane", id="test-pane"):
                yield Static("3 // TEST RUNTIME", classes="pane-title")
                yield RichLog(id="test-log", wrap=True, markup=True)
            with Vertical(classes="pane", id="ready-pane"):
                yield Static("4 // READY RUNTIME", classes="pane-title")
                yield RichLog(id="ready-log", wrap=True, markup=True)
        yield Footer()

    def on_mount(self) -> None:
        self._banner()
        self._render_code(force=True)
        self.set_interval(2.0, self._poll)

    def _banner(self) -> None:
        log = self.query_one("#chat-log", RichLog)
        log.write(Text("CYBERDECK DEVELOPMENT GHOST", style=f"bold {ACCENT}"))
        log.write(Text(f"target : {self.cfg.target}", style=DIM))
        log.write(Text(f"tests  : {self.cfg.tests}", style=DIM))
        status = "online" if self.adapter.available() else "OFFLINE — install @deepseek-ai/dsh"
        style = ACCENT if self.adapter.available() else ERROR
        log.write(Text(f"harness: {status}", style=style))
        log.write(Text("/fix  /do  /target  /tests  /test  /run  /clear  /help", style=DIM))
        log.write(Text(""))

    # -- helpers -------------------------------------------------------------

    def _log(self, pane: str, message: str | Text, style: str | None = None) -> None:
        widget = self.query_one(pane, RichLog)
        widget.write(Text(message, style=style) if isinstance(message, str) else message)

    def _timestamped(self, message: str, style: str | None = None) -> Text:
        text = Text()
        text.append(f"[{time.strftime('%H:%M:%S')}] ", style=DIM)
        text.append(message, style=style or "")
        return text

    # -- code pane -----------------------------------------------------------

    def _render_code(self, force: bool = False) -> None:
        fresh = Snapshot.take(self.cfg.target)
        if not force and self.snapshot and not fresh.changed_since(self.snapshot):
            return
        log = self.query_one("#code-log", RichLog)
        log.clear()

        if not fresh.content:
            log.write(Text(f"cannot read {self.cfg.target}", style=ERROR))
            self.snapshot = fresh
            return

        log.write(Text(f"{self.cfg.target}", style=f"bold {AMBER}"))
        log.write(Syntax(fresh.content, "python", line_numbers=True,
                         theme="monokai", background_color="default"))

        if self.snapshot and fresh.changed_since(self.snapshot):
            diff = fresh.unified_diff(self.snapshot)
            added, removed = summarize_diff(diff)
            log.write(Text(""))
            log.write(Text(f"── new code  +{added} / -{removed}", style=f"bold {ACCENT}"))
            for line in diff:
                if line.startswith(("+++", "---")):
                    continue
                if line.startswith("+"):
                    log.write(Text(line, style=ACCENT))
                elif line.startswith("-"):
                    log.write(Text(line, style=ERROR))
                elif line.startswith("@@"):
                    log.write(Text(line, style=AMBER))
                else:
                    log.write(Text(line, style=DIM))

        self.snapshot = fresh

    # -- test / ready panes --------------------------------------------------

    def _render_test(self, result: RunResult) -> None:
        log = self.query_one("#test-log", RichLog)
        colour = ACCENT if result.ok else ERROR
        log.write(self._timestamped(
            f"{'PASS' if result.ok else 'FAIL'}  exit={result.exit_code}  "
            f"{result.duration:.1f}s", f"bold {colour}"))

        if result.summary:
            parts = " ".join(f"{k}={v}" for k, v in sorted(result.summary.items()))
            log.write(Text(f"  {parts}", style=DIM))

        for failure in result.failures[:12]:
            log.write(Text(f"  ✗ {failure.name}", style=ERROR))
            if failure.message:
                log.write(Text(f"      {failure.message[:200]}", style=DIM))

        tail = result.stdout.strip().splitlines()[-6:]
        if tail:
            log.write(Text("  ── output tail", style=DIM))
            for line in tail:
                log.write(Text(f"  {line}", style=DIM))
        log.write(Text(""))

    def _render_ready(self, result: RunResult) -> None:
        log = self.query_one("#ready-log", RichLog)
        colour = ACCENT if result.ok else ERROR
        log.write(self._timestamped(
            f"RUN  exit={result.exit_code}  {result.duration:.1f}s", f"bold {colour}"))
        for line in (result.stdout or "").strip().splitlines()[-20:]:
            log.write(Text(f"  {line}"))
        for line in (result.stderr or "").strip().splitlines()[-10:]:
            log.write(Text(f"  {line}", style=ERROR))
        log.write(Text(""))

    def _render_test_from_dict(self, payload: dict) -> None:
        result = RunResult(
            ok=payload.get("ok", False),
            command=payload.get("command", []),
            exit_code=payload.get("exit_code", 1),
            duration=payload.get("duration", 0.0),
            stdout=payload.get("stdout", ""),
            stderr=payload.get("stderr", ""),
            summary=payload.get("summary", {}),
        )
        for item in payload.get("failures", []):
            result.failures.append(
                Failure(name=item.get("name", "?"), message=item.get("message", "")))
        self._render_test(result)

    def _render_ready_from_dict(self, payload: dict) -> None:
        self._render_ready(RunResult(
            ok=payload.get("ok", False),
            command=payload.get("command", []),
            exit_code=payload.get("exit_code", 1),
            duration=payload.get("duration", 0.0),
            stdout=payload.get("stdout", ""),
            stderr=payload.get("stderr", ""),
        ))

    def _render_demand_report(self, report: IterationReport) -> None:
        log = self.query_one("#test-log", RichLog)
        log.write(Text(""))
        if report.ok:
            log.write(Text(f"◉ EXECUTED — {report.reason}", style=f"bold {ACCENT}"))
        else:
            log.write(Text(f"◌ INCOMPLETE — {report.reason}", style=f"bold {AMBER}"))
        for attempt in report.attempts:
            log.write(Text(f"  #1  +{attempt.added}/-{attempt.removed}", style=DIM))
        log.write(Text("  no test contract — inspect pane 2 yourself", style=DIM))
        log.write(Text(""))
        self._render_code(force=True)

    # -- agent events (called from worker threads) ---------------------------

    def _on_agent_event(self, name: str, payload: dict) -> None:
        if name == "dsh":
            text = payload.get("text") or ""
            if text:
                self.call_from_thread(self._stream_chat, text)
            elif payload.get("kind") == "error":
                message = payload.get("payload", {}).get("message", "agent error")
                self.call_from_thread(self._stream_chat, f"\n[error] {message}\n")
        elif name == "status":
            self.call_from_thread(
                self._log, "#test-log", self._timestamped(payload.get("text", ""), AMBER))
        elif name == "diff":
            lines = payload.get("lines") or []
            if lines:
                self.call_from_thread(self._render_code, True)
                self.call_from_thread(
                    self._log, "#test-log",
                    self._timestamped(
                        f"patch +{payload['added']} / -{payload['removed']}", ACCENT))
        elif name == "test":
            self.call_from_thread(self._render_test_from_dict, payload)
        elif name == "ready":
            self.call_from_thread(self._render_ready_from_dict, payload)

    def _stream_chat(self, text: str) -> None:
        self.query_one("#chat-log", RichLog).write(Text(text))

    # -- shared state polling ------------------------------------------------

    def _poll(self) -> None:
        state = self.state.load()
        if state.version == self._last_state_version:
            return
        self._last_state_version = state.version
        self._render_code()

    # -- actions -------------------------------------------------------------

    def action_iterate(self, directive: str = "") -> None:
        self._log("#test-log", self._timestamped("fix loop engaged", f"bold {AMBER}"))
        self._log("#chat-log", Text("» fix loop engaged", style=AMBER))
        self._iterate_worker(directive)

    def action_demand(self, demand: str) -> None:
        self._log("#test-log", self._timestamped("executing demand", f"bold {AMBER}"))
        self._demand_worker(demand)

    def action_run_tests(self) -> None:
        self._log("#test-log", self._timestamped("test run", AMBER))
        self._test_worker()

    def action_run_ready(self) -> None:
        self._log("#ready-log", self._timestamped("ready run", AMBER))
        self._ready_worker()

    def action_clear_panes(self) -> None:
        for pane in ("#chat-log", "#code-log", "#test-log", "#ready-log"):
            self.query_one(pane, RichLog).clear()
        self._render_code(force=True)

    # -- typed commands ------------------------------------------------------

    def on_input_submitted(self, event: Input.Submitted) -> None:
        prompt = event.value.strip()
        event.input.value = ""
        if not prompt:
            return
        self._log("#chat-log", Text(f"\n» {prompt}", style=f"bold {AMBER}"))
        self._log("#chat-log", Text(""))
        self.state.append_chat("user", prompt)
        if self._dispatch_command(prompt):
            return
        self._chat_worker(prompt)

    def _dispatch_command(self, text: str) -> bool:
        """Handle slash commands. Returns True if consumed."""
        stripped = text.strip()
        if not stripped.startswith("/"):
            return False
        parts = stripped.split(maxsplit=1)
        command = parts[0].lower()
        directive = parts[1].strip() if len(parts) > 1 else ""

        if command in {"/fix", "/iterate", "/loop"}:
            self.action_iterate(directive)
        elif command in {"/do", "/demand"}:
            if not directive:
                self._log("#chat-log", Text("/do needs a demand after it", style=ERROR))
                return True
            self._log("#chat-log", Text(f"\n» /do {directive}", style=f"bold {AMBER}"))
            self._demand_worker(directive)
        elif command in {"/target", "/t"}:
            if not directive:
                self._log("#chat-log", Text("usage: /target path/to/file.py", style=DIM))
            else:
                path = Path(directive).expanduser()
                if not path.is_absolute():
                    path = self.cfg.workdir / path
                self.cfg.target = path
                self.snapshot = None
                self._render_code(force=True)
                self._log("#chat-log", Text(f"target → {path}", style=ACCENT))
        elif command in {"/tests"}:
            if not directive:
                self._log("#chat-log", Text("usage: /tests path/to/test.py", style=DIM))
            else:
                path = Path(directive).expanduser()
                if not path.is_absolute():
                    path = self.cfg.workdir / path
                self.cfg.tests = path
                self._log("#chat-log", Text(f"tests  → {path}", style=ACCENT))
        elif command in {"/test", "/tests"}:
            self.action_run_tests()
        elif command in {"/run", "/ready"}:
            self.action_run_ready()
        elif command in {"/clear"}:
            self.action_clear_panes()
        elif command in {"/help", "/?"}:
            self._log("#chat-log", Text(
                "/fix  /do  /target  /tests  /test  /run  /clear  /help", style=DIM))
        else:
            self._log("#chat-log", Text(f"unknown command {command}", style=ERROR))
        return True

    # -- workers -------------------------------------------------------------

    @work(thread=True, exclusive=True, group="chat")
    def _chat_worker(self, prompt: str) -> None:
        result = self.adapter.run(prompt, cwd=self.cfg.workdir,
                                  timeout=self.cfg.agent_timeout)
        self.state.append_chat("agent", result.output)
        if not result.ok and not result.output:
            self.call_from_thread(self._stream_chat,
                                  f"[agent exited {result.exit_code}: {result.finish_reason}]")

    @work(thread=True, exclusive=True, group="demand")
    def _demand_worker(self, demand: str) -> None:
        report = self.orchestrator.run_demand(demand)
        self.call_from_thread(self._render_demand_report, report)

    @work(thread=True, exclusive=True, group="test")
    def _test_worker(self) -> None:
        result = self.runner.run_tests(self.cfg.tests, timeout=self.cfg.test_timeout)
        self.state.update(test=result.to_dict(), status="tested")
        self.call_from_thread(self._render_test, result)

    @work(thread=True, exclusive=True, group="ready")
    def _ready_worker(self) -> None:
        result = self.runner.run_script(self.cfg.target, timeout=self.cfg.run_timeout)
        self.state.update(ready=result.to_dict(), status="ready")
        self.call_from_thread(self._render_ready, result)

    @work(thread=True, exclusive=True, group="iterate")
    def _iterate_worker(self, directive: str = "") -> None:
        report = self.orchestrator.iterate(directive)
        self.call_from_thread(self._render_report, report)

    def _render_report(self, report: IterationReport) -> None:
        log = self.query_one("#test-log", RichLog)
        log.write(Text(""))
        if report.ok:
            log.write(Text(f"◉ READY — {report.reason}", style=f"bold {ACCENT}"))
            self.call_from_thread(self._ready_worker)
        else:
            log.write(Text(f"◌ NOT READY — {report.reason}", style=f"bold {ERROR}"))
        log.write(Text(f"  rounds={report.rounds}", style=DIM))
        for attempt in report.attempts:
            after = "green" if attempt.after and attempt.after.ok else "still failing"
            log.write(Text(
                f"  #{attempt.index}  +{attempt.added}/-{attempt.removed}  "
                f"{attempt.duration:.1f}s  {after}", style=DIM))
        log.write(Text(""))
        self._render_code(force=True)

def run(pane: str | None = None, **overrides) -> None:
    cfg = Config.from_env(**overrides)
    CyberdeckApp(cfg=cfg, pane=pane).run()
```

## `cyberdeck/state.py`

```python
"""Cross-process pane state.

Lets four terminal windows (or tmux panes) behave as one environment. Every
pane tails this file and renders the sections it owns.
"""

from __future__ import annotations

import json
import threading
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

@dataclass
class SharedState:
    version: int = 0
    updated_at: float = 0.0
    chat: list[dict[str, str]] = field(default_factory=list)
    test: dict[str, Any] | None = None
    ready: dict[str, Any] | None = None
    code_revision: str = ""
    status: str = "idle"

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)

class StateStore:
    """Atomic JSON state file with a simple lock."""

    def __init__(self, directory: Path):
        self.path = directory / "state.json"
        self._lock = threading.Lock()

    def load(self) -> SharedState:
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return SharedState()
        state = SharedState()
        for key, value in raw.items():
            if hasattr(state, key):
                setattr(state, key, value)
        return state

    def _write(self, state: SharedState) -> None:
        state.version += 1
        state.updated_at = time.time()
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(state.to_json(), encoding="utf-8")
        tmp.replace(self.path)

    def update(self, **changes: Any) -> SharedState:
        with self._lock:
            state = self.load()
            for key, value in changes.items():
                if hasattr(state, key):
                    setattr(state, key, value)
            self._write(state)
            return state

    def append_chat(self, role: str, text: str) -> SharedState:
        with self._lock:
            state = self.load()
            state.chat.append({"role": role, "text": text, "ts": f"{time.time():.0f}"})
            state.chat = state.chat[-200:]
            self._write(state)
            return state
```

## `cyberdeck/theme.tcss`

```css
/* Cyberdeck phosphor theme — dark glass, green phosphor, amber accents. */

Screen {
    background: #050807;
    color: #33ff66;
}

Header {
    background: #0a1410;
    color: #33ff66;
}

Footer {
    background: #0a1410;
    color: #4f8a5f;
}

#grid {
    layout: grid;
    grid-size: 2 2;
    grid-gutter: 1;
    grid-rows: 1fr 1fr;
    grid-columns: 1fr 1fr;
    padding: 1 1 0 1;
    height: 1fr;
}

.pane {
    border: round #1f6b33;
    background: #07100a;
    padding: 0 1;
    height: 1fr;
}

.pane-title {
    color: #ffb000;
    text-style: bold;
}

#chat-log,
#code-log,
#test-log,
#ready-log {
    background: transparent;
    color: #33ff66;
    height: 1fr;
    scrollbar-size-vertical: 1;
}

#chat-input {
    background: #0b1a10;
    border: tall #1f6b33;
    color: #33ff66;
    margin-top: 1;
}

#chat-input:focus {
    border: tall #ffb000;
}

Input > .input--placeholder {
    color: #2f6b42;
}

#chat-pane {
    border: round #2f8f4a;
}
```

## `cyberdeck/__main__.py`

```python
"""CLI entry point for the Cyberdeck terminal."""

from __future__ import annotations

import argparse
from pathlib import Path

from .app import run
from .config import Config

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cyberdeck",
        description="Four-pane terminal development Ghost driving DeepSeek Harness.",
    )
    parser.add_argument("--target", type=Path, default=Path("scripts/example_target.py"),
                        help="Python script under development")
    parser.add_argument("--tests", type=Path, default=Path("tests/test_example_target.py"),
                        help="Test file or directory")
    parser.add_argument("--pane", choices=["chat", "code", "test", "ready"],
                        default=None, help="Launch a single pane (multi-window mode)")
    parser.add_argument("--model", default=None)
    parser.add_argument("--provider", default=None)
    parser.add_argument("--max-attempts", type=int, default=None)
    parser.add_argument("--dsh", dest="dsh_command", default=None)
    parser.add_argument("--dsh-home", type=Path, default=None)
    parser.add_argument("--python", dest="python_exec", default=None)
    return parser

def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    overrides = {
        "target": args.target,
        "tests": args.tests,
        "model": args.model,
        "provider": args.provider,
        "max_attempts": args.max_attempts,
        "dsh_command": args.dsh_command,
        "dsh_home": args.dsh_home,
        "python_exec": args.python_exec,
    }
    run(pane=args.pane, **{k: v for k, v in overrides.items() if v is not None})
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
```

## `scripts/example_target.py`

```python
#!/usr/bin/env python3
"""Example Cyberdeck target: index markdown notes into a JSON catalog.

Ships with one deliberate defect so the fix loop has something to close.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Split YAML-ish frontmatter from the body. Keys are lowercased."""
    if not text.startswith("---"):
        return {}, text

    lines = text.splitlines()
    meta: dict[str, str] = {}
    end = None

    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end = index
            break
        if ":" in line:
            key, _, value = line.partition(":")
            meta[key.strip().lower()] = value.strip()

    if end is None:
        return {}, text

    return meta, "\n".join(lines[end + 1:])

def note_id(relative_path: str) -> str:
    digest = hashlib.sha1(relative_path.encode("utf-8")).hexdigest()
    return digest[:12]

def index_notes(root: Path) -> list[dict[str, object]]:
    catalog: list[dict[str, object]] = []

    for path in sorted(root.rglob("*.md")):
        relative = path.relative_to(root).as_posix()
        raw = path.read_text(encoding="utf-8", errors="replace")
        meta, body = parse_frontmatter(raw)

        # DEFECT: keys are lowercased by parse_frontmatter, so "Title"
        # never exists. The fix is meta.get("title") or path.stem.
        title = meta["Title"] or path.stem

        catalog.append({
            "id": note_id(relative),
            "path": relative,
            "title": title,
            "tags": [t.strip() for t in meta.get("tags", "").split(",") if t.strip()],
            "words": len(body.split()),
        })

    return catalog

def summarize(catalog: list[dict[str, object]]) -> dict[str, object]:
    total_words = sum(int(entry["words"]) for entry in catalog)
    all_tags = sorted({t for entry in catalog for t in entry["tags"]})
    return {
        "notes": len(catalog),
        "words": total_words,
        "tags": all_tags,
        "average_words": round(total_words / len(catalog), 1) if catalog else 0.0,
    }

def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    root = Path(args[0]) if args else Path("notes")

    if not root.exists():
        print(f"no notes directory at {root}", file=sys.stderr)
        return 2

    catalog = index_notes(root)
    print(json.dumps({"catalog": catalog, "summary": summarize(catalog)}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
```

## `tests/test_example_target.py`

```python
"""Tests for the example Cyberdeck target script."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from example_target import index_notes, main, note_id, parse_frontmatter, summarize

NOTE_WITH_CAPITALISED_TITLE = """---
Title: Beowulf Cluster Notes
tags: cluster, beowulf, hardware
---

Notes about refurbished nodes.
"""

def test_parse_frontmatter_lowercases_keys():
    meta, body = parse_frontmatter(NOTE_WITH_CAPITALISED_TITLE)
    assert "title" in meta
    assert meta["title"] == "Beowulf Cluster Notes"
    assert "Notes about" in body

def test_index_notes_handles_capitalised_title(tmp_path: Path):
    (tmp_path / "cluster.md").write_text(NOTE_WITH_CAPITALISED_TITLE, encoding="utf-8")
    catalog = index_notes(tmp_path)
    assert len(catalog) == 1
    assert catalog[0]["title"] == "Beowulf Cluster Notes"

def test_index_notes_falls_back_to_filename(tmp_path: Path):
    (tmp_path / "plain.md").write_text("no frontmatter here\n", encoding="utf-8")
    assert index_notes(tmp_path)[0]["title"] == "plain"

def test_note_id_is_stable_and_short():
    assert note_id("a/b.md") == note_id("a/b.md")
    assert len(note_id("a/b.md")) == 12

def test_summarize_counts(tmp_path: Path):
    (tmp_path / "one.md").write_text(NOTE_WITH_CAPITALISED_TITLE, encoding="utf-8")
    (tmp_path / "two.md").write_text("---\ntags: rag\n---\nshort body\n", encoding="utf-8")
    report = summarize(index_notes(tmp_path))
    assert report["notes"] == 2
    assert "rag" in report["tags"]

def test_cli_returns_json(tmp_path: Path, capsys):
    (tmp_path / "one.md").write_text(NOTE_WITH_CAPITALISED_TITLE, encoding="utf-8")
    assert main([str(tmp_path)]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["summary"]["notes"] == 1
```

## Licence

MIT, matching DeepSeek Harness.
