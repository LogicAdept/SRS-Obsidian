#!/usr/bin/env python3
"""Resolve Accept cherry-pick conflicts from parallel cover/fill clones.

Shared files always diverge across clones that forked from the same source tip.
This merger keeps the source vault's accumulated Accept history and overlays the
incoming clone's contributions without leaving conflict markers.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


MARKER_RE = re.compile(
    r"<<<<<<<[^\n]*\n(.*?)=======\n(.*?)>>>>>>>[^\n]*",
    re.DOTALL,
)


def run(repo: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return completed.stdout


def unmerged_paths(repo: Path) -> list[str]:
    out = run(repo, "diff", "--name-only", "--diff-filter=U")
    return [line.strip().replace("\\", "/") for line in out.splitlines() if line.strip()]


def show_stage(repo: Path, stage: int, path: str) -> str | None:
    try:
        return run(repo, "show", f":{stage}:{path}")
    except subprocess.CalledProcessError:
        return None


def write_text(path: Path, text: str) -> None:
    if not text.endswith("\n"):
        text += "\n"
    path.write_text(text, encoding="utf-8", newline="\n")


def merge_progress(ours: str, theirs: str) -> str:
    left = json.loads(ours)
    right = json.loads(theirs)
    nodes = dict(left.get("nodes") or {})
    for key, value in (right.get("nodes") or {}).items():
        nodes[key] = value
    merged = dict(left)
    merged["nodes"] = nodes
    return json.dumps(merged, ensure_ascii=False, indent=2) + "\n"


def merge_line_union(ours: str, theirs: str) -> str:
    left = ours.splitlines()
    right = theirs.splitlines()
    seen = set(left)
    out = list(left)
    for line in right:
        if line not in seen:
            out.append(line)
            seen.add(line)
    return "\n".join(out) + "\n"


def merge_tags_keep_both(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        head = match.group(1).rstrip("\n")
        theirs = match.group(2).rstrip("\n")
        if not head:
            return theirs
        if not theirs:
            return head
        if head == theirs:
            return head
        # Source already has later refine/Accept history; keep it on overlap.
        return head

    merged = MARKER_RE.sub(repl, text)
    if "<<<<<<<" in merged or ">>>>>>>" in merged:
        raise RuntimeError("Tags.md still has unresolved conflict markers")
    return merged if merged.endswith("\n") else merged + "\n"


def stage_add(repo: Path, path: str) -> None:
    subprocess.run(
        ["git", "-C", str(repo), "add", "--", path],
        check=True,
    )


def resolve(repo: Path) -> int:
    paths = unmerged_paths(repo)
    if not paths:
        print("No unmerged paths.")
        return 0

    leftover: list[str] = []
    for rel in paths:
        path = repo / Path(*rel.split("/"))
        ours = show_stage(repo, 2, rel)
        theirs = show_stage(repo, 3, rel)

        if rel == "SRS/NamesHistory/coverage-progress.json":
            if ours is None or theirs is None:
                leftover.append(rel)
                continue
            write_text(path, merge_progress(ours, theirs))
            stage_add(repo, rel)
            print(f"merged {rel}")
            continue

        if rel in {
            "SRS/NamesHistory/md-file-names.txt",
            "SRS/NamesHistory/question-repositories.txt",
        }:
            if ours is None and theirs is None:
                leftover.append(rel)
                continue
            write_text(path, merge_line_union(ours or "", theirs or ""))
            stage_add(repo, rel)
            print(f"merged {rel}")
            continue

        if rel == "SRS/Format/Tags.md":
            raw = path.read_text(encoding="utf-8")
            if "<<<<<<<" in raw:
                write_text(path, merge_tags_keep_both(raw))
            elif theirs is not None and ours is not None:
                # No markers left in the worktree; prefer combining via stages
                # only when one side is empty of the other. Fall back to ours.
                write_text(path, ours if "<<<<<<<" not in ours else merge_tags_keep_both(ours))
            elif theirs is not None:
                write_text(path, theirs)
            elif ours is not None:
                write_text(path, ours)
            else:
                leftover.append(rel)
                continue
            stage_add(repo, rel)
            print(f"merged {rel}")
            continue

        if rel.startswith("SRS/") and rel.endswith(".md"):
            # Source already has earlier Accept retags; keep ours for card edits.
            if ours is not None:
                write_text(path, ours)
            elif theirs is not None:
                write_text(path, theirs)
            else:
                leftover.append(rel)
                continue
            stage_add(repo, rel)
            print(f"kept source for {rel}")
            continue

        leftover.append(rel)

    if leftover:
        print("Unresolved conflicts:", file=sys.stderr)
        for rel in leftover:
            print(f"  {rel}", file=sys.stderr)
        return 1

    remaining = unmerged_paths(repo)
    if remaining:
        print("Still unmerged after merge:", file=sys.stderr)
        for rel in remaining:
            print(f"  {rel}", file=sys.stderr)
        return 1
    return 0


def main() -> int:
    repo = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    return resolve(repo)


if __name__ == "__main__":
    raise SystemExit(main())
