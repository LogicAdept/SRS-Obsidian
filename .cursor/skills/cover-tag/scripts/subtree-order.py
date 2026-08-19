#!/usr/bin/env python3
"""Post-order tag walk for /cover-tag. Do not invent a one-off walker.

  python .cursor/skills/cover-tag/scripts/subtree-order.py Java/Collections/Map
  python .cursor/skills/cover-tag/scripts/subtree-order.py Java/Collections/Map --flat
  python .cursor/skills/cover-tag/scripts/subtree-order.py Java --limit 12 --max-nodes 12

Pass the prefix without a leading # (PowerShell treats # as a comment).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[2] / "process-topic" / "scripts"
sys.path.insert(0, str(_SCRIPTS))

from vault_cards import (  # noqa: E402
    assign_visit_quotas,
    node_role,
    normalize_prefix,
    parse_tree_paths,
    repo_root_from_script,
    subtree_post_order,
    truncate_visit,
    vault_dir,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Post-order Tags.md walk for /cover-tag.")
    parser.add_argument("tag", help="Tree prefix, with or without leading #.")
    parser.add_argument("--flat", action="store_true", help="Visit only the resolved prefix.")
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Max new cards this run. Default: 12 if the walk has children, else unlimited.",
    )
    parser.add_argument(
        "--per-node",
        type=int,
        default=None,
        metavar="M",
        help="Max new cards per visited node. Extra unused slots stay unused.",
    )
    parser.add_argument(
        "--max-nodes",
        type=int,
        default=12,
        metavar="K",
        help="Max nodes to visit (default 12). Ignored with --flat.",
    )
    parser.add_argument("--repo", default=None, help="Git repo root.")
    args = parser.parse_args()
    prefix = normalize_prefix(args.tag)
    if not prefix:
        raise SystemExit("Empty tag prefix.")
    if args.max_nodes < 1:
        raise SystemExit("max_nodes must be >= 1.")
    if args.per_node is not None and args.per_node < 1:
        raise SystemExit("per_node must be >= 1.")
    if args.limit is not None and args.limit < 0:
        raise SystemExit("limit must be >= 0.")

    repo = Path(args.repo).resolve() if args.repo else repo_root_from_script()
    tags_md = vault_dir(repo) / "Format" / "Tags.md"
    if not tags_md.is_file():
        raise SystemExit(f"Tags.md not found: {tags_md}")

    tree = parse_tree_paths(tags_md)
    order = subtree_post_order(tree, prefix)
    if prefix not in order:
        order = [prefix]
    full_count = len(order)
    has_children = full_count > 1

    if args.flat or not has_children:
        visit, remaining = [prefix], [p for p in order if p != prefix]
        mode = "flat"
    else:
        visit, remaining = truncate_visit(order, prefix, args.max_nodes)
        mode = "post-order"

    limit = args.limit
    if limit is None and mode == "post-order":
        limit = 12

    quotas = assign_visit_quotas(visit, limit, args.per_node)
    roles = {path: node_role(path, order) for path in order}
    skip = [path for path, q in zip(visit, quotas) if q == 0]
    active = [(path, q) for path, q in zip(visit, quotas) if q != 0]

    print(f"prefix\t#{prefix}")
    print(f"mode\t{mode}")
    print(f"node_count\t{full_count}")
    print(f"visit_count\t{len(visit)}")
    print(f"limit\t{limit if limit is not None else 'unlimited'}")
    print(f"per_node\t{args.per_node if args.per_node is not None else 'auto'}")
    print(f"max_nodes\t{args.max_nodes}")
    print("visit")
    for path, quota in zip(visit, quotas):
        qlabel = "unlimited" if quota is None else str(quota)
        print(f"  #{path}\t{roles.get(path, node_role(path, visit))}\tquota\t{qlabel}")
    print("skip_zero_quota")
    if skip:
        for path in skip:
            print(f"  #{path}")
    else:
        print("  (none)")
    print("remaining")
    leftover = remaining + skip
    if leftover:
        for path in leftover:
            print(f"  #{path}")
    else:
        print("  (none)")
    print("cover_next")
    for path, quota in active:
        print(f"  #{path}\t{quota if quota is not None else 'unlimited'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
