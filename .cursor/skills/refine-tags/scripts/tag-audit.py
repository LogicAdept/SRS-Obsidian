#!/usr/bin/env python3
"""Compare Tags.md tree vs card tag lines for one prefix.

Use from /refine-tags. Do not write a one-off auditor.

  python .cursor/skills/refine-tags/scripts/tag-audit.py Java/Spring

Pass the prefix without a leading # (PowerShell treats # as a comment).
Omit the prefix to audit the whole tree.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[2] / "process-topic" / "scripts"
sys.path.insert(0, str(_SCRIPTS))

from vault_cards import (  # noqa: E402
    normalize_prefix,
    parse_tree_paths,
    repo_root_from_script,
    scan_cards,
    vault_dir,
)


def in_scope(path: str, prefix: str | None) -> bool:
    if not prefix:
        return True
    return path == prefix or path.startswith(prefix + "/")


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit Tags.md vs card tags.")
    parser.add_argument("prefix", nargs="?", default="", help="Optional tree prefix, without #.")
    parser.add_argument("--repo", default=None, help="Git repo root.")
    args = parser.parse_args()
    prefix = normalize_prefix(args.prefix) if args.prefix else None

    repo = Path(args.repo).resolve() if args.repo else repo_root_from_script()
    vault = vault_dir(repo)
    tags_md = vault / "Format" / "Tags.md"
    tree = [p for p in parse_tree_paths(tags_md) if in_scope(p, prefix)]
    tree_set = set(tree)
    _scanned, cards = scan_cards(vault)

    used: set[str] = set()
    parent_child: list[tuple[str, list[str]]] = []
    for card in cards:
        scoped = sorted(t for t in card.tags if in_scope(t, prefix) and t not in ("SRS", "New"))
        used.update(scoped)
        pairs = [t for t in scoped if any(other != t and other.startswith(t + "/") for other in scoped)]
        if pairs:
            parent_child.append((card.cue, scoped))

    unused = [p for p in tree if p not in used]
    missing = sorted(t for t in used if t not in tree_set)

    label = f"#{prefix}" if prefix else "(whole tree)"
    print(f"prefix\t{label}")
    print(f"tree_paths\t{len(tree)}")
    print(f"used_paths\t{len(used)}")
    print("unused_in_tree")
    if unused:
        for p in unused:
            print(f"  #{p}")
    else:
        print("  (none)")
    print("used_not_in_tree")
    if missing:
        for p in missing:
            print(f"  #{p}")
    else:
        print("  (none)")
    print(f"parent_and_child_cards\t{len(parent_child)}")
    for cue, tags in parent_child:
        print(f"  {cue}\t{' '.join('#' + t for t in tags)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
