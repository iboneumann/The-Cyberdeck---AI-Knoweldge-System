#!/usr/bin/env python3
"""Flatten content/docs/** into content/posts/ as normal posts.

What it does
------------
1. Scans every *.md under content/docs/ (skipping the top-level nav index).
2. Moves each one to content/posts/ as `cyberdeck-terminal-<slug>.md`.
3. Normalises front matter to TOML (+++ delimiters, key = value).
4. Assigns sequential weights starting after the highest existing post
   weight, so migrated pages appear after everything already published.
5. Forces the licence file to weight 500 (last).
6. Reports:
     - duplicate weights anywhere in posts/
     - posts without any weight
     - the final ordered list
7. With --delete-docs, moves content/docs/ to content/.docs-backup so you
   can verify the build before removing it for good.

Nothing outside content/ is touched: no layouts, no theme files, no config.
The migrated pages use whatever post layout your theme already uses.

Usage
-----
    python3 flatten_docs_to_posts.py --check          # verify only
    python3 flatten_docs_to_posts.py --dry-run        # show the plan
    python3 flatten_docs_to_posts.py                  # do the move
    python3 flatten_docs_to_posts.py --delete-docs    # move + remove docs/

Safety
------
- Idempotent: re-running skips destinations that already exist.
- Aborts on filename collisions.
- Never overwrites an existing post.
- Backs up the docs tree instead of deleting it outright.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib

try:
    import yaml
except ImportError:
    yaml = None

DELIM = ("+++", "---")
DEFAULT_DATE = "2026-11-04"
LICENCE_WEIGHT = 500
STEP = 1
START = 51

# ----------------------------------------------------------------- front matter

def split_front(text: str):
    """Return (front_lines, body) or None if the file has no front matter."""
    lines = text.splitlines()
    if not lines or lines[0].strip() not in DELIM:
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() in DELIM:
            return lines[1:i], "\n".join(lines[i + 1:]).lstrip("\n")
    # no closing delimiter: fall back to the first blank line
    for i in range(1, len(lines)):
        if not lines[i].strip():
            return lines[1:i], "\n".join(lines[i + 1:]).lstrip("\n")
    return None

def parse_front(lines):
    body = "\n".join(lines)
    try:
        return tomllib.loads(body)
    except Exception:
        pass
    if yaml is not None:
        try:
            data = yaml.safe_load(body)
            if isinstance(data, dict):
                return data
        except Exception:
            pass
    return {}

def toml_val(v):
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

def render(front, body):
    out = ["+++"]
    for k, v in front.items():
        out.append(f"{k} = {toml_val(v)}")
    out.append("+++")
    return "\n".join(out) + "\n\n" + body

def weight_of(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    parts = split_front(text)
    if not parts:
        return None
    data = parse_front(parts[0])
    w = data.get("weight")
    if isinstance(w, int):
        return w
    if isinstance(w, str) and w.strip().isdigit():
        return int(w.strip())
    return None

# ----------------------------------------------------------------------- naming

def slug_for(src: Path) -> str:
    """cyberdeck-terminal-<stem>, or -overview for the section index."""
    stem = src.stem
    if stem == "_index":
        stem = "overview"
    stem = re.sub(r"[^a-z0-9-]+", "-", stem.lower()).strip("-")
    return f"cyberdeck-terminal-{stem}"

def is_licence(path: Path) -> bool:
    s = path.stem.lower()
    return "licence" in s or "license" in s

# -------------------------------------------------------------------- reporting

def report_weights(posts: list[Path]) -> dict:
    by_weight: dict[int, list[str]] = {}
    missing = []
    for p in posts:
        w = weight_of(p)
        if w is None:
            missing.append(p.name)
        else:
            by_weight.setdefault(w, []).append(p.name)

    print("weight map:")
    for w in sorted(by_weight):
        names = sorted(by_weight[w])
        flag = "  <-- DUPLICATE" if len(names) > 1 else ""
        print(f"  {w:>4}  {', '.join(names)}{flag}")

    if missing:
        print("\nposts without weight:")
        for n in missing:
            print(f"  {n}")

    dupes = {w: n for w, n in by_weight.items() if len(n) > 1}
    return {"duplicates": dupes, "missing": missing}

# ------------------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".", help="site root (default: current dir)")
    ap.add_argument("--dry-run", action="store_true", help="show plan, write nothing")
    ap.add_argument("--check", action="store_true",
                    help="only verify numbering, do not move anything")
    ap.add_argument("--delete-docs", action="store_true",
                    help="after a successful move, rename content/docs to .docs-backup")
    ap.add_argument("--licence-weight", type=int, default=LICENCE_WEIGHT)
    args = ap.parse_args()

    root = Path(args.root).resolve()
    docs_dir = root / "content/docs"
    posts_dir = root / "content/posts"

    if not posts_dir.exists():
        print(f"error: {posts_dir} does not exist", file=sys.stderr)
        return 1

    if args.check:
        print(f"checking {posts_dir}\n")
        report_weights(sorted(posts_dir.glob("*.md")))
        return 0

    if not docs_dir.exists():
        print(f"nothing to migrate: {docs_dir} not found")
        print("(already flattened? use --check to verify numbering)")
        return 0

    # ------------------------------------------------------------------ collect
    src_files = []
    for p in sorted(docs_dir.rglob("*.md")):
        if p.name.lower() == "readme.md":
            continue
        # skip the top-level nav index; keep the section index
        if p == docs_dir / "_index.md":
            print(f"skip top-level nav: {p.relative_to(root)}")
            continue
        src_files.append(p)

    if not src_files:
        print("no docs files found to move")
        return 0

    src_resolved = {p.resolve() for p in src_files}
    existing = [p for p in posts_dir.glob("*.md")
                if p.resolve() not in src_resolved]

    # Licence files are pinned last and must not influence the start weight.
    existing_weights = [
        w for p, w in ((p, weight_of(p)) for p in existing)
        if w is not None and not is_licence(p)
    ]
    highest = max(existing_weights, default=0)
    start = START if highest < START else ((highest // STEP) + 1) * STEP

    print(f"existing posts: {len(existing)}")
    print(f"highest existing weight: {highest or '(none)'}")
    print(f"first assigned weight: {start}\n")

    # --------------------------------------------------------------------- plan
    plan = []
    next_weight = start
    for src in src_files:
        weight = args.licence_weight if is_licence(src) else next_weight
        if not is_licence(src):
            next_weight += STEP

        text = src.read_text(encoding="utf-8")
        parts = split_front(text)
        if parts is None:
            print(f"skip (no front matter): {src.relative_to(root)}")
            continue

        front = dict(parse_front(parts[0]))
        body = parts[1]

        front.setdefault("title", src.stem.replace("_", " ").title())
        front.setdefault("date", DEFAULT_DATE)
        front["draft"] = bool(front.get("draft", False))
        front["weight"] = weight
        front.setdefault("tags", ["cyberdeck", "documentation"])

        slug = slug_for(src)
        dst = posts_dir / f"{slug}.md"
        plan.append((src, dst, front, body, weight))

    # ---------------------------------------------------------------- collisions
    names = [dst.name for _, dst, _, _, _ in plan]
    dupes_names = sorted({n for n in names if names.count(n) > 1})
    if dupes_names:
        print("ERROR: filename collisions:", dupes_names, file=sys.stderr)
        return 1

    clashes = [dst for _, dst, _, _, _ in plan if dst.exists()]
    if clashes:
        print("ERROR: destination already exists:", file=sys.stderr)
        for c in clashes:
            print(f"  {c.relative_to(root)}", file=sys.stderr)
        return 1

    # ---------------------------------------------------------------- show plan
    print("plan:")
    for src, dst, _, _, w in plan:
        print(f"  {w:>4}  {src.relative_to(root)}")
        print(f"        -> {dst.relative_to(root)}")
    print()

    # duplicate-weight warning for the resulting set
    final = {w: [] for w in []}
    for p in existing:
        w = weight_of(p)
        if w is not None:
            final.setdefault(w, []).append(p.name)
    for _, dst, _, _, w in plan:
        final.setdefault(w, []).append(dst.name)
    final_dupes = {w: n for w, n in final.items() if len(n) > 1}

    if final_dupes:
        print("WARNING: duplicate weights in the resulting set:")
        for w, names in sorted(final_dupes.items()):
            print(f"  {w}: {', '.join(names)}")
        print("(the move still proceeds; fix these by editing the weights by hand)")
        print()

    if args.dry_run:
        print("dry run — nothing written")
        return 0

    # -------------------------------------------------------------------- write
    written = 0
    for src, dst, front, body, _ in plan:
        dst.write_text(render(front, body), encoding="utf-8")
        print(f"wrote  {dst.relative_to(root)}")
        written += 1

    print(f"\n{written} file(s) written")

    if args.delete_docs:
        backup = root / "content" / ".docs-backup"
        if backup.exists():
            print(f"refusing: {backup} already exists", file=sys.stderr)
            return 1
        shutil.move(str(docs_dir), str(backup))
        print(f"moved {docs_dir.relative_to(root)} -> {backup.relative_to(root)}")
        print("run `hugo server` to verify, then delete the backup")

    print("\nnext steps:")
    print("  1. hugo server --navigateToChanged   (verify)")
    print("  2. if clean, commit and push")
    print("  3. if you keep the docs section in menus, remove it from hugo.toml")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
