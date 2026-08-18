#!/usr/bin/env python3
"""Rename a tag prefix on SRS card tag lines (children included).

Use from /refine-tags. Do not write a one-off retagger.

  python .cursor/skills/refine-tags/scripts/retag-prefix.py --from Java/Spring/Framework/Boot --to Java/Spring/Boot
  python .cursor/skills/refine-tags/scripts/retag-prefix.py --map Java/Spring/Framework/Boot=Java/Spring/Boot --map Java/Spring/Framework/Security=Java/Spring/Security
  python .cursor/skills/refine-tags/scripts/retag-prefix.py --from Java/Spring/Boot --to Java/Spring/Boot/Actuator --only "How do you monitor an application with Spring Boot Actuator.md"

Pass paths without a leading # (PowerShell treats # as a comment).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[2] / "process-topic" / "scripts"
sys.path.insert(0, str(_SCRIPTS))

from vault_cards import (  # noqa: E402
    apply_tag_maps,
    card_tags,
    extract_tag_line,
    iter_card_files,
    normalize_prefix,
    rebuild_tag_line,
    repo_root_from_script,
    vault_dir,
)


def parse_map(raw: str) -> tuple[str, str]:
    if "=" not in raw:
        raise argparse.ArgumentTypeError("expected OLD=NEW")
    old, new = raw.split("=", 1)
    old_n = normalize_prefix(old)
    new_n = normalize_prefix(new)
    if not old_n or not new_n:
        raise argparse.ArgumentTypeError("empty tag in OLD=NEW")
    return old_n, new_n


def main() -> int:
    parser = argparse.ArgumentParser(description="Retag SRS cards by prefix rename.")
    parser.add_argument("--from", dest="src", default=None, help="Old prefix (and its children).")
    parser.add_argument("--to", dest="dst", default=None, help="New prefix.")
    parser.add_argument(
        "--map",
        action="append",
        default=[],
        metavar="OLD=NEW",
        help="Extra OLD=NEW mapping. Repeatable. Applied longest-old first.",
    )
    parser.add_argument(
        "--only",
        action="append",
        default=[],
        metavar="FILE.md",
        help="Limit to these card basenames. Repeatable.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print changes; do not write files.")
    parser.add_argument("--repo", default=None, help="Git repo root.")
    args = parser.parse_args()

    mappings: list[tuple[str, str]] = []
    if bool(args.src) != bool(args.dst):
        raise SystemExit("Use --from and --to together, or only --map.")
    if args.src and args.dst:
        mappings.append((normalize_prefix(args.src), normalize_prefix(args.dst)))
    for raw in args.map:
        mappings.append(parse_map(raw))
    if not mappings:
        raise SystemExit("Need --from/--to or --map OLD=NEW.")
    mappings.sort(key=lambda pair: len(pair[0]), reverse=True)

    only = {name.strip() for name in args.only if name.strip()}
    repo = Path(args.repo).resolve() if args.repo else repo_root_from_script()
    vault = vault_dir(repo)
    changed = 0
    for path in iter_card_files(vault):
        if only and path.name not in only:
            continue
        text = path.read_text(encoding="utf-8")
        tag_line = extract_tag_line(text)
        if not tag_line:
            continue
        if not any(
            apply_tag_maps(tag, mappings) != tag
            for tag in card_tags(tag_line)
            if tag not in ("SRS", "New")
        ):
            continue
        new_line = rebuild_tag_line(tag_line, mappings)
        if new_line == tag_line:
            continue
        changed += 1
        print(f"{path.name}")
        print(f"  - {tag_line}")
        print(f"  + {new_line}")
        if not args.dry_run:
            path.write_text(text.replace(tag_line, new_line, 1), encoding="utf-8")
    print(f"{'would retag' if args.dry_run else 'retagged'} {changed} cards")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
