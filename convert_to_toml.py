#!/usr/bin/env python3
"""Convert Hugo front matter to TOML across content/.

Forgiving by design: a file with +++ delimiter but YAML body is parsed as YAML
and rewritten as proper TOML, so half-converted files repair themselves.
"""

import argparse
import datetime
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required:  pip install pyyaml")

try:
    import tomllib
except ImportError:
    import tomli as tomllib


def split_front_matter(text):
    if text.startswith("+++"):
        end = text.find("\n+++", 3)
        if end != -1:
            return "+++", text[3:end], text[end + 4:]
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return "---", text[3:end], text[end + 4:]
    if text.startswith("{"):
        end = text.find("\n}\n")
        if end != -1:
            return "{", text[: end + 2], text[end + 2:]
    return None


def parse_front(delim, body):
    errors = []

    if delim == "+++":
        try:
            return tomllib.loads(body)
        except Exception as exc:
            errors.append(f"toml: {exc}")

    if delim == "{":
        try:
            return json.loads(body if body.lstrip().startswith("{") else "{" + body)
        except Exception as exc:
            errors.append(f"json: {exc}")

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


def toml_quote(s):
    out = s.replace("\\", "\\\\").replace('"', '\\"')
    out = out.replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
    return f'"{out}"'


def toml_value(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, str):
        return toml_quote(v)
    if isinstance(v, (datetime.datetime, datetime.date)):
        return toml_quote(v.isoformat())
    if isinstance(v, list):
        if not v:
            return "[]"
        return "[" + ", ".join(toml_value(x) for x in v) + "]"
    if isinstance(v, dict):
        inner = ", ".join(f"{k} = {toml_value(val)}" for k, val in v.items())
        return "{ " + inner + " }"
    return toml_quote(str(v))


def to_toml(data):
    return "\n".join(f"{k} = {toml_value(v)}" for k, v in data.items()) + "\n"


def convert(path, dry_run=False):
    text = path.read_text(encoding="utf-8")
    parts = split_front_matter(text)
    if parts is None:
        return "no front matter"
    delim, front, body = parts
    try:
        data = parse_front(delim, front)
    except ValueError as exc:
        return f"UNPARSEABLE: {exc}"

    new_text = "+++\n" + to_toml(data) + "+++\n\n" + body.lstrip("\n")

    if new_text == text:
        return "already TOML"

    if not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return "converted" if delim != "+++" else "reformatted"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default="content")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    counts = {}
    for path in sorted(Path(args.root).rglob("*.md")):
        status = convert(path, dry_run=args.dry_run)
        counts[status] = counts.get(status, 0) + 1
        print(f"{status:22s} {path}")
    print()
    for k, v in sorted(counts.items()):
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()

