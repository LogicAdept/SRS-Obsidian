#!/usr/bin/env python3
"""Validate and write the leaf selected for an orchestrated focused cover run."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

REPO = Path(__file__).resolve().parents[4]
_PROCESS_SCRIPTS = REPO / ".cursor" / "skills" / "process-topic" / "scripts"
sys.path.insert(0, str(_PROCESS_SCRIPTS))

from vault_cards import normalize_prefix, parse_tree_paths, path_in_prefix, vault_dir  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Write a validated focused-cover target leaf."
    )
    parser.add_argument("--root", required=True)
    parser.add_argument("--target", required=True)
    parser.add_argument("--result-file", required=True, type=Path)
    args = parser.parse_args()

    root = normalize_prefix(args.root)
    target = normalize_prefix(args.target)
    tree = parse_tree_paths(vault_dir(REPO) / "Format" / "Tags.md")
    if root not in tree and not any(path_in_prefix(path, root) for path in tree):
        raise SystemExit(f"focused root is not in Tags.md: {root}")
    if target not in tree:
        raise SystemExit(f"focused target is not in Tags.md: {target}")
    if not path_in_prefix(target, root):
        raise SystemExit(f"focused target {target} is outside root {root}")
    if any(path != target and path_in_prefix(path, target) for path in tree):
        raise SystemExit(f"focused target must be a leaf: {target}")

    result = args.result_file
    if not result.is_absolute():
        result = REPO / result
    result = result.resolve()
    try:
        result.relative_to(REPO.resolve())
    except ValueError as err:
        raise SystemExit("--result-file must be inside the repository") from err

    result.parent.mkdir(parents=True, exist_ok=True)
    payload = {"version": 1, "root": root, "target_leaf": target}
    temporary = result.with_name(result.name + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    temporary.replace(result)
    print(f"focus_target={target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
