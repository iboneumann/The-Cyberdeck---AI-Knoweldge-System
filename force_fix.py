#!/usr/bin/env python3
"""Fix front matter with a missing closing delimiter.

Handles: opener (--- or +++) followed by fields and a blank line, with no
closing delimiter. Uses the blank line as the boundary, parses whatever is
above it, rewrites as matched +++ TOML.
"""

import sys
from pathlib import Path

import tomllib

try:
    import yaml
except ImportError:
    yaml = None


def parse(front: str) -> dict:
    try:
        d = tomllib.loads(front)
        if d:
            return d
    except Exception:
        pass
    if yaml is not None:
        try:
            d = yaml.safe_load(front)
            if isinstance(d, dict) and d:
                return d
        except Exception:
            pass
    raise ValueError("cannot parse front matter")


def toml_val(v) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    if hasattr(v, "isoformat"):
        return v.isoformat()
    if isinstance(v, str):
        s = (v.replace("\\", "\\\\").replace('"', '\\"')
             .replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t"))
        return f'"{s}"'
    if isinstance(v, list):
        return "[" + ", ".join(toml_val(x) for x in v) + "]"
    return toml_val(str(v))


def fix(path: Path, dry: bool) -> str:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() not in ("+++", "---"):
        return "no front matter"

    front_lines = []
    body_start = None
    for i in range(1, len(lines)):
        s = lines[i].strip()
        if s in ("+++", "---"):
            body_start = i + 1
            break
        if not s:
            body_start = i + 1
            break
        front_lines.append(lines[i])

    if body_start is None:
        return "no body found"

    front = "\n".join(front_lines).strip()
    if not front:
        return "empty front matter"

    try:
        data = parse(front)
    except ValueError as exc:
        return f"UNPARSEABLE: {exc}"

    body = "\n".join(lines[body_start:]).lstrip("\n")
    new = (
        "+++\n"
        + "\n".join(f"{k} = {toml_val(v)}" for k, v in data.items())
        + "\n+++\n\n"
        + body
    )

    if new == text:
        return "ok"
    if not dry:
        path.write_text(new, encoding="utf-8")
    return "fixed"


if __name__ == "__main__":
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("content")
    dry = "--dry-run" in sys.argv
    for p in sorted(root.rglob("*.md")):
        print(f"{fix(p, dry):40s} {p}")
