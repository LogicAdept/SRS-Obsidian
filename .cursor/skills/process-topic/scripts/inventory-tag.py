#!/usr/bin/env python3
"""List live SRS cards for one tag prefix (this path or a child).

Use from /process-topic instead of writing a one-off walker.

  python .cursor/skills/process-topic/scripts/inventory-tag.py #Java/Spring
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from vault_cards import matches_prefix, normalize_prefix, repo_root_from_script, scan_cards, vault_dir


def main() -> int:
    parser = argparse.ArgumentParser(description="Inventory SRS cards for one tag prefix.")
    parser.add_argument("tag", help="Tree prefix, with or without leading #.")
    parser.add_argument(
        "--repo",
        type=str,
        default=None,
        help="Git repo root (default: inferred from this script path).",
    )
    args = parser.parse_args()
    prefix = normalize_prefix(args.tag)
    if not prefix:
        raise SystemExit("Empty tag prefix.")

    repo = Path(args.repo).resolve() if args.repo else repo_root_from_script()
    vault = vault_dir(repo)
    _scanned, cards = scan_cards(vault)
    matched = [c for c in cards if matches_prefix(c.tags, prefix)]
    n = len(matched)
    n_new = sum(1 for c in matched if c.is_new)
    n_filled = n - n_new
    leaf_counts = Counter()
    for card in matched:
        for t in card.tags:
            if t == prefix or t.startswith(prefix + "/"):
                leaf_counts[t] += 1

    print(f"prefix\t#{prefix}")
    print(f"n\t{n}")
    print(f"n_new\t{n_new}")
    print(f"n_filled\t{n_filled}")
    print("leaves")
    for leaf, count in sorted(leaf_counts.items(), key=lambda kv: (-kv[1], kv[0].lower())):
        print(f"  #{leaf}\t{count}")
    print("cues")
    for card in sorted(matched, key=lambda c: c.cue.lower()):
        flag = "new" if card.is_new else "filled"
        print(f"  [{flag}]\t{card.cue}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
