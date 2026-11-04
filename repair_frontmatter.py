#!/usr/bin/env python3
"""Repair Hugo front matter with mismatched or missing closing delimiters.

A file with an opening '+++' and a closing '---' makes Hugo read the whole
file as TOML and fail on the first reserved character in the body. This finds
the first delimiter line after the opener (either kind) and rewrites the file
as matched +++ TOML.
"""

import argparse
import datetime
from pathlib import Path

import tomllib

try:
    import yaml
except ImportError:
    yaml = None

DELIMS = {"+++", "---"}
WINDOW = 200  # do not look for a closer past this many lines

def parse_front(body, declared):
    errors = []
    if declared == "+++":
        try:
            return tomllib.loads(body)
        except Exception as exc:
            errors.append(f"toml: {exc}")
    if yaml is not None:
        try:
            data = yaml.safe_load(body)
            if isinstance(data, dict):
                return data
            errors.append("yaml: not a mapping")
        except Exception as exc:
            errors.append(f"yaml: {exc}")
    try:
        return tomllib.loads(body)
    except Exception as exc:
        errors.append(f"toml-retry: {exc}")
    raise ValueError("; ".join(errors))

def toml_value(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, (datetime.datetime, datetime.date)):
        return v.isoformat()
    if isinstance(v, str):
        s = (v.replace("\\", "\\\\").replace('"', '\\"')
             .replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t"))
        return f'"{s}"'
    if isinstance(v, list):
        return "[" + ", ".join(toml_value(x) for x in v) + "]" if v else "[]"
    if isinstance(v, dict):
        return "{ " + ", ".join(f"{k} = {toml_value(x)}" for k, x in v.items()) + " }"
    return toml_value(str(v))

def to_toml(data):
    return "\n".join(f"{k} = {toml_value(v)}" for k, v in data.items()) + "\n"

def repair(path, dry_run):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines:
        return "empty"

    opener = lines[0].strip()
    if opener not in DELIMS:
        return "no front matter"

    close = -1
    limit = min(len(lines), WINDOW)
    for i in range(1, limit):
        if lines[i].strip() in DELIMS:
            close = i
            break

    if close == -1:
        return "UNCLOSED — no delimiter found in first {} lines".format(limit)

    closer = lines[close].strip()
    front = "\n".join(lines[1:close])
    body = "\n".join(lines[close + 1:])

    try:
        data = parse_front(front, opener)
    except ValueError as exc:
        return f"UNPARSEABLE: {exc}"

    new = "+++\n" + to_toml(data) + "+++\n"
    if body.strip():
        new += "\n" + body.lstrip("\n")

    if new == text:
        return "ok"

    if not dry_run:
        path.write_text(new, encoding="utf-8")

    if opener != closer:
        return f"repaired ({opener} opened, {closer} closed)"
    return "reformatted"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default="content")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    counts = {}
    for path in sorted(Path(args.root).rglob("*.md")):
        status = repair(path, args.dry_run)
        counts[status.split(" (")[0]] = counts.get(status.split(" (")[0], 0) + 1
        print(f"{status:40s} {path}")

    print()
    for k, v in sorted(counts.items()):
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()
