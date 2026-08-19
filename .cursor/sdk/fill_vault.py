#!/usr/bin/env python3
"""Converge technical Tags.md coverage with /refine-tags and /cover-tag.

Build and run from the vault repo root (PowerShell):

  $env:CURSOR_API_KEY = "cursor_..."
  ./.cursor/sdk/run_cover_vault.ps1 --dry-run --max-tags 3
  ./.cursor/sdk/run_cover_vault.ps1 --max-tags 3

Does not invoke /fill-tag. Cards stay #New drafts until a later fill pass.

Real runs are accepted only in the hardened Docker launcher. The container root is
read-only; the repository is the only host path mounted read/write; Docker's socket is
not mounted. Internet access remains enabled. Direct host execution is dry-run only.

For each path, refine and cover repeat until the tree is stable and a cover pass adds
zero cards. Newly created paths are inserted into the same post-order work queue.
Do not run two instances against the same vault.
"""

from __future__ import annotations

import argparse
from collections import deque
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import json
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[2]
_SCRIPTS = REPO / ".cursor" / "skills" / "process-topic" / "scripts"
sys.path.insert(0, str(_SCRIPTS))

from vault_cards import (  # noqa: E402
    normalize_prefix,
    parse_tree_paths,
    path_in_prefix,
    vault_dir,
)

INDEX_ROW = re.compile(r"^\| `#([^`]+)` \| (\d+) \| (\d+) \| (\d+) \|")

SKILL_ROOT = REPO / ".cursor" / "skills"
TAGS_MD = vault_dir(REPO) / "Format" / "Tags.md"
COVERAGE_INDEX = vault_dir(REPO) / "NamesHistory" / "coverage-index.md"
REBUILD = _SCRIPTS / "rebuild-coverage-index.py"
DEFAULT_STATE = REPO / ".cursor" / "sdk" / "cover-state.json"
STATE_VERSION = 1
CONTAINER_MARKER = "SRS_COVER_ISOLATED_CONTAINER"
CONTAINER_WORKSPACE = Path("/workspace")

# Experience, HR, role-fit. Technical interview coverage skips these.
NONTECH_PREFIXES = (
    "Career",
    "EngineeringLeadership",
    "ProjectManagement",
)

CONSTRAINTS = """
You are in the vault git repo (cwd). Follow the named skill file exactly except that
any instruction to clone or use temp files outside cwd is superseded by the
repository-only rules below. English only for skill reports, card files, and Tags.md.

Hard constraints:
- Do not spawn subagents. Do not invent a tag walker, retagger, or coverage script.
- PowerShell: never pass a leading # to Python CLI args.
  Example: python .cursor/skills/refine-tags/scripts/tag-audit.py Java/Spring
- Read and write only inside this workspace. Do not clone question dumps. Fetch
  individual raw files with WebFetch, WebSearch, or gh api.
- Existing vault Python scripts may be executed from cwd. Do not create replacement
  walkers, retaggers, indexers, or card writers.
- Do not run git commit, checkout, reset, clean, push, or any destructive git command.
- /cover-tag writes #New drafts from interview dumps; do not write GoldStandard bodies.
- Absolute card count is not a completion criterion. For every cover pass, check the skill's
  mechanism, failure/version/lie, comparison, procedure, and missing-definition gaps.
  A zero-card result is valid only after searching the prescribed repositories and
  compilation pages and finding no distinct non-trivia cue.
- Do not invoke /fill-tag. Leave #New in place.
- After cover, rebuild the index if the skill did not:
  python .cursor/skills/process-topic/scripts/rebuild-coverage-index.py
""".strip()


@dataclass(frozen=True)
class Counts:
    n: int
    n_new: int
    n_filled: int


def _parse_index(path: Path) -> dict[str, Counts]:
    out: dict[str, Counts] = {}
    if not path.is_file():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        m = INDEX_ROW.match(line)
        if not m:
            continue
        out[m.group(1)] = Counts(int(m.group(2)), int(m.group(3)), int(m.group(4)))
    return out


def _counts_for(index: dict[str, Counts], tag: str) -> Counts:
    return index.get(tag, Counts(0, 0, 0))


def _matches_any(tag: str, prefixes: list[str] | tuple[str, ...]) -> bool:
    return any(path_in_prefix(tag, normalize_prefix(p)) for p in prefixes if p)


def _scoped_paths(
    tree_paths: list[str],
    *,
    prefix: str,
    only: tuple[str, ...],
    excluded: tuple[str, ...],
) -> list[str]:
    out: list[str] = []
    for path in tree_paths:
        if prefix and not path_in_prefix(path, prefix):
            continue
        if only and not any(path_in_prefix(path, item) for item in only):
            continue
        if _matches_any(path, excluded):
            continue
        out.append(path)
    return out


def _is_parent(path: str, tree_paths: list[str] | set[str]) -> bool:
    child_prefix = path + "/"
    return any(other != path and other.startswith(child_prefix) for other in tree_paths)


def _sort_paths(
    paths: list[str],
    index: dict[str, Counts],
    tree_paths: list[str],
) -> list[str]:
    tree_set = set(tree_paths)

    def key(path: str) -> tuple[int, int, int, str]:
        parent = _is_parent(path, tree_set)
        if parent:
            return (1, -path.count("/"), _counts_for(index, path).n, path.lower())
        return (0, _counts_for(index, path).n, -path.count("/"), path.lower())

    return sorted(paths, key=key)


def _subtree_signature(tree_paths: list[str], tag: str) -> list[str]:
    return [path for path in tree_paths if path_in_prefix(path, tag)]


def _rebuild_index() -> None:
    subprocess.run(
        [sys.executable, str(REBUILD)],
        cwd=str(REPO),
        check=True,
    )
    if not COVERAGE_INDEX.is_file():
        raise RuntimeError(f"coverage rebuild did not create {COVERAGE_INDEX}")


def _mount_table() -> list[tuple[Path, frozenset[str]]]:
    mountinfo = Path("/proc/self/mountinfo")
    if not mountinfo.is_file():
        raise SystemExit("cannot verify Docker mounts: /proc/self/mountinfo is missing")
    mounts: list[tuple[Path, frozenset[str]]] = []
    for line in mountinfo.read_text(encoding="utf-8").splitlines():
        left, separator, _right = line.partition(" - ")
        if not separator:
            continue
        fields = left.split()
        if len(fields) < 6:
            continue
        mount_point = fields[4].replace("\\040", " ")
        mounts.append((Path(mount_point), frozenset(fields[5].split(","))))
    return mounts


def _require_container_boundary() -> None:
    if sys.platform != "linux":
        raise SystemExit(
            "REFUSED: real runs require the Docker launcher; direct host execution "
            "is dry-run only"
        )
    if os.environ.get(CONTAINER_MARKER) != "1" or not Path("/.dockerenv").is_file():
        raise SystemExit(
            "REFUSED: the hardened Docker launcher marker/environment is missing"
        )
    if REPO.resolve() != CONTAINER_WORKSPACE:
        raise SystemExit(
            f"REFUSED: repository must be mounted exactly at {CONTAINER_WORKSPACE}"
        )
    if Path("/var/run/docker.sock").exists():
        raise SystemExit("REFUSED: Docker socket must not be mounted in the container")

    mounts = _mount_table()
    by_path = {path: options for path, options in mounts}
    if "ro" not in by_path.get(Path("/"), frozenset()):
        raise SystemExit("REFUSED: container root filesystem is not read-only")
    if "rw" not in by_path.get(CONTAINER_WORKSPACE, frozenset()):
        raise SystemExit("REFUSED: /workspace is not a dedicated read/write mount")

    allowed_mounts = {
        Path("/"),
        CONTAINER_WORKSPACE,
        Path("/tmp"),
        Path("/home/agent"),
        Path("/proc"),
        Path("/sys"),
        Path("/dev"),
        Path("/etc/hostname"),
        Path("/etc/hosts"),
        Path("/etc/resolv.conf"),
    }
    allowed_mount_prefixes = (
        CONTAINER_WORKSPACE,
        Path("/tmp"),
        Path("/home/agent"),
        Path("/proc"),
        Path("/sys"),
        Path("/dev"),
    )
    unexpected: list[str] = []
    for mount_point, _options in mounts:
        if mount_point in allowed_mounts:
            continue
        if any(
            mount_point != prefix and prefix in mount_point.parents
            for prefix in allowed_mount_prefixes
        ):
            continue
        unexpected.append(str(mount_point))
    if unexpected:
        raise SystemExit(
            "REFUSED: unexpected container mounts: " + ", ".join(sorted(unexpected))
        )


def _local_options() -> dict[str, Any]:
    # The Docker mount namespace is the security boundary. A nested SDK sandbox
    # is intentionally omitted because bubblewrap is not reliably nestable.
    return {
        "cwd": str(REPO),
        "setting_sources": ["project"],
    }


def _prompt_for(skill: str, command: str) -> str:
    skill_file = SKILL_ROOT / skill / "SKILL.md"
    return (
        f"{CONSTRAINTS}\n\n"
        f"Read and follow `{skill_file.as_posix()}` exactly.\n\n"
        f"Invoke now:\n{command}\n"
    )


class AgentRunError(RuntimeError):
    """A Cursor run did not reach the finished state."""


def _retry_delay(error: BaseException, attempt: int) -> float:
    raw = getattr(error, "retry_after", None)
    if raw:
        try:
            return max(0.0, float(raw))
        except (TypeError, ValueError):
            try:
                retry_at = parsedate_to_datetime(str(raw))
                if retry_at.tzinfo is None:
                    retry_at = retry_at.replace(tzinfo=timezone.utc)
                return max(0.0, (retry_at - datetime.now(timezone.utc)).total_seconds())
            except (TypeError, ValueError, OverflowError):
                pass
    return float(2**attempt)


def _run_agent(
    *,
    api_key: str,
    model: str,
    name: str,
    prompt: str,
    max_retries: int,
) -> str:
    from cursor_sdk import Agent, AgentOptions, CursorAgentError, LocalAgentOptions

    result = None
    for attempt in range(max_retries + 1):
        try:
            result = Agent.prompt(
                prompt,
                AgentOptions(
                    api_key=api_key,
                    model=model,
                    name=name,
                    local=LocalAgentOptions(**_local_options()),
                ),
            )
            break
        except CursorAgentError as err:
            retryable = bool(getattr(err, "is_retryable", False))
            request_id = getattr(err, "request_id", None)
            if not retryable or attempt >= max_retries:
                hint = (
                    " The repository sandbox is mandatory; if it is unsupported on "
                    "native Windows, run from WSL or use a cloud agent."
                )
                raise AgentRunError(
                    f"startup failed: {err}; retryable={retryable}; "
                    f"request_id={request_id}.{hint}"
                ) from err
            delay = _retry_delay(err, attempt)
            print(
                f"  startup retry {attempt + 1}/{max_retries} in {delay:.1f}s "
                f"request_id={request_id}",
                file=sys.stderr,
            )
            time.sleep(delay)

    if result is None:
        raise AgentRunError("Cursor SDK returned no run result")
    text = getattr(result, "result", None) or ""
    preview = str(text).strip().replace("\r\n", "\n")
    if len(preview) > 800:
        preview = preview[:800] + "…"
    print(f"  status={result.status} id={getattr(result, 'id', '')}")
    if preview:
        print(preview)
    if result.status != "finished":
        raise AgentRunError(
            f"run did not finish: status={result.status} id={getattr(result, 'id', '')}"
        )
    return str(text)


def _resolve_state_path(raw: str) -> Path:
    path = Path(raw)
    if not path.is_absolute():
        path = REPO / path
    path = path.resolve()
    try:
        path.relative_to(REPO.resolve())
    except ValueError as err:
        raise SystemExit("--state-file must be inside the repository") from err
    return path


def _load_state(path: Path, *, fresh: bool) -> dict[str, Any]:
    if fresh or not path.is_file():
        return {"version": STATE_VERSION, "completed": {}}
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as err:
        raise SystemExit(f"cannot read state file {path}: {err}") from err
    if state.get("version") != STATE_VERSION or not isinstance(
        state.get("completed"), dict
    ):
        raise SystemExit(f"unsupported state file format: {path}")
    return state


def _save_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(
        json.dumps(state, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    tmp.replace(path)


def _completion_record(
    tag: str,
    index: dict[str, Counts],
    tree_paths: list[str],
) -> dict[str, Any]:
    return {
        "n": _counts_for(index, tag).n,
        "subtree": _subtree_signature(tree_paths, tag),
    }


def _state_matches(
    record: Any,
    tag: str,
    index: dict[str, Counts],
    tree_paths: list[str],
) -> bool:
    if not isinstance(record, dict):
        return False
    return record == _completion_record(tag, index, tree_paths)


def _plan_line(
    tag: str,
    counts: Counts,
    *,
    parent: bool,
    skip_refine: bool,
    skip_cover: bool,
) -> str:
    steps: list[str] = []
    if not skip_refine:
        steps.append("refine")
    if not skip_cover:
        steps.append("cover --flat")
    mode = "parent" if parent else "leaf"
    return (
        f"  #{tag}  n={counts.n} n_new={counts.n_new}  [{mode}] -> "
        f"{' + '.join(steps)} until stable"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Repeat /refine-tags and /cover-tag over technical Tags.md paths "
            "until taxonomy and question coverage converge."
        ),
    )
    parser.add_argument("--dry-run", action="store_true", help="Print the queue and exit.")
    parser.add_argument("--model", default="composer-2.5")
    parser.add_argument("--cover-limit", type=int, default=12)
    parser.add_argument(
        "--max-tags",
        type=int,
        default=None,
        help="Limit initial seed paths; children created by their refine runs are still processed.",
    )
    parser.add_argument(
        "--max-passes-per-tag",
        type=int,
        default=20,
        help="Safety cap only; hitting it leaves the tag incomplete and returns failure.",
    )
    parser.add_argument(
        "--confirm-zero-runs",
        type=int,
        default=1,
        help="Consecutive stable zero-card cover passes required for completion.",
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=2,
        help="Retries for SDK startup failures explicitly marked retryable.",
    )
    parser.add_argument(
        "--state-file",
        default=str(DEFAULT_STATE.relative_to(REPO)),
        help="Repository-local completion checkpoint.",
    )
    parser.add_argument(
        "--fresh",
        action="store_true",
        help="Discard all saved completion checkpoints before this run.",
    )
    parser.add_argument(
        "--only",
        action="append",
        default=[],
        metavar="TAG",
        help="Restrict to this path and its descendants. Repeatable.",
    )
    parser.add_argument(
        "--prefix",
        default="",
        help="Restrict to this Tags.md path and its descendants.",
    )
    parser.add_argument("--skip-refine", action="store_true")
    parser.add_argument("--skip-cover", action="store_true")
    parser.add_argument(
        "--include-nontechnical",
        action="store_true",
        help="Also queue Career, EngineeringLeadership, ProjectManagement.",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        metavar="PREFIX",
        help="Drop this prefix and its descendant paths. Repeatable.",
    )
    parser.add_argument("--fail-fast", action="store_true")
    args = parser.parse_args(argv)

    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            try:
                reconfigure(encoding="utf-8", errors="replace")
            except (OSError, ValueError):
                pass

    if args.skip_refine and args.skip_cover:
        raise SystemExit("--skip-refine and --skip-cover cannot both be set")
    if args.cover_limit < 1:
        raise SystemExit("--cover-limit must be >= 1")
    if args.max_tags is not None and args.max_tags < 1:
        raise SystemExit("--max-tags must be >= 1")
    if args.max_passes_per_tag < 1:
        raise SystemExit("--max-passes-per-tag must be >= 1")
    if args.confirm_zero_runs < 1:
        raise SystemExit("--confirm-zero-runs must be >= 1")
    if args.max_retries < 0:
        raise SystemExit("--max-retries must be >= 0")

    if not TAGS_MD.is_file():
        raise SystemExit(f"missing Tags.md: {TAGS_MD}")
    state_path = _resolve_state_path(args.state_file)
    state = _load_state(state_path, fresh=args.fresh)
    state_completed: dict[str, Any] = state["completed"]

    if not args.dry_run:
        _require_container_boundary()
        _rebuild_index()
    elif not COVERAGE_INDEX.is_file():
        raise SystemExit(f"missing coverage index: {COVERAGE_INDEX}")

    prefix = normalize_prefix(args.prefix)
    only = tuple(normalize_prefix(item) for item in args.only)
    if any(not item for item in only):
        raise SystemExit("--only cannot be empty")
    excluded = [normalize_prefix(item) for item in args.exclude]
    if not args.include_nontechnical:
        excluded.extend(NONTECH_PREFIXES)
    excluded_tuple = tuple(item for item in excluded if item)

    tree_paths = parse_tree_paths(TAGS_MD)
    index = _parse_index(COVERAGE_INDEX)
    scoped = _scoped_paths(
        tree_paths,
        prefix=prefix,
        only=only,
        excluded=excluded_tuple,
    )
    if not scoped:
        raise SystemExit("no Tags.md paths match the requested technical scope")

    resumed = {
        tag
        for tag in scoped
        if _state_matches(state_completed.get(tag), tag, index, tree_paths)
    }
    candidates = _sort_paths(
        [tag for tag in scoped if tag not in resumed],
        index,
        tree_paths,
    )
    limited_out = 0
    if args.max_tags is not None:
        limited_out = max(0, len(candidates) - args.max_tags)
        candidates = candidates[: args.max_tags]

    seed_prefixes: tuple[str, ...] | None
    seed_prefixes = tuple(candidates) if args.max_tags is not None else None

    print(f"repo={REPO}")
    print(
        f"technical paths in scope={len(scoped)}  resumed={len(resumed)}  "
        f"queued seeds={len(candidates)}  limited_out={limited_out}"
    )
    if excluded_tuple:
        print("excluded=" + ", ".join(excluded_tuple))
    print(
        f"completion=tree stable + {args.confirm_zero_runs} zero-card cover run(s); "
        "card counts only order the queue"
    )
    if args.dry_run and sys.platform != "linux":
        print(
            "note: direct host execution is dry-run only; use "
            ".cursor/sdk/run_cover_vault.ps1 for a real run",
            file=sys.stderr,
        )

    tree_set = set(tree_paths)
    for tag in candidates:
        print(
            _plan_line(
                tag,
                _counts_for(index, tag),
                parent=_is_parent(tag, tree_set),
                skip_refine=args.skip_refine,
                skip_cover=args.skip_cover,
            )
        )

    if args.dry_run or not candidates:
        return 0

    api_key = os.environ.pop("CURSOR_API_KEY", "").strip()
    if not api_key:
        raise SystemExit("set CURSOR_API_KEY (https://cursor.com/dashboard/integrations)")

    queue: deque[str] = deque(candidates)
    pending = set(candidates)
    completed = set(resumed)
    passes: dict[str, int] = {}
    zero_streak: dict[str, int] = {}
    failures: set[str] = set()
    incomplete: set[str] = set()
    total_added = 0

    def allowed_paths(current_tree: list[str]) -> list[str]:
        paths = _scoped_paths(
            current_tree,
            prefix=prefix,
            only=only,
            excluded=excluded_tuple,
        )
        if seed_prefixes is not None:
            paths = [
                path
                for path in paths
                if any(path_in_prefix(path, seed) for seed in seed_prefixes)
            ]
        return paths

    def requeue(tag: str) -> None:
        if tag not in pending and tag not in completed and tag not in failures:
            queue.appendleft(tag)
            pending.add(tag)

    def enqueue_changed(
        current_tree: list[str],
        current_index: dict[str, Counts],
        *,
        current: str,
    ) -> list[str]:
        additions: list[str] = []
        for path in allowed_paths(current_tree):
            if (
                path == current
                or path in pending
                or path in failures
                or path in incomplete
            ):
                continue
            if path in completed:
                if _state_matches(
                    state_completed.get(path),
                    path,
                    current_index,
                    current_tree,
                ):
                    continue
                completed.remove(path)
                state_completed.pop(path, None)
            additions.append(path)
        additions = _sort_paths(additions, current_index, current_tree)
        descendants = [
            path
            for path in additions
            if path != current and path_in_prefix(path, current)
        ]
        later = [path for path in additions if path not in descendants]
        for path in later:
            queue.append(path)
            pending.add(path)
        for path in reversed(descendants):
            queue.appendleft(path)
            pending.add(path)
        return additions

    while queue:
        tag = queue.popleft()
        pending.remove(tag)
        current_tree = parse_tree_paths(TAGS_MD)
        current_index = _parse_index(COVERAGE_INDEX)

        if tag not in current_tree:
            print(f"\n=== #{tag}: removed or re-parented; skipping old path ===")
            completed.discard(tag)
            state_completed.pop(tag, None)
            _save_state(state_path, state)
            enqueue_changed(current_tree, current_index, current=tag)
            continue

        pass_no = passes.get(tag, 0) + 1
        passes[tag] = pass_no
        if pass_no > args.max_passes_per_tag:
            incomplete.add(tag)
            state_completed.pop(tag, None)
            print(
                f"\nINCOMPLETE #{tag}: safety cap "
                f"{args.max_passes_per_tag} reached",
                file=sys.stderr,
            )
            continue

        print(f"\n=== #{tag} pass {pass_no}/{args.max_passes_per_tag} ===")
        subtree_before = _subtree_signature(current_tree, tag)
        try:
            if not args.skip_refine:
                print("refine")
                _run_agent(
                    api_key=api_key,
                    model=args.model,
                    name=f"refine {tag} p{pass_no}",
                    prompt=_prompt_for("refine-tags", f"/refine-tags #{tag}"),
                    max_retries=args.max_retries,
                )
                _rebuild_index()

            tree_after_refine = parse_tree_paths(TAGS_MD)
            index_after_refine = _parse_index(COVERAGE_INDEX)
            newly_queued = enqueue_changed(
                tree_after_refine,
                index_after_refine,
                current=tag,
            )

            if tag not in tree_after_refine:
                print(f"refine removed or moved #{tag}; replacement paths were queued")
                state_completed.pop(tag, None)
                _save_state(state_path, state)
                continue

            new_descendants = [
                path
                for path in newly_queued
                if path != tag and path_in_prefix(path, tag)
            ]
            if new_descendants:
                print(
                    "refine created descendant paths; deferring parent until they converge: "
                    + ", ".join(f"#{path}" for path in new_descendants)
                )
                requeue(tag)
                # enqueue_changed prepended children; putting tag back first and then
                # prepending the children again preserves children-before-parent order.
                for path in reversed(new_descendants):
                    if path in pending:
                        queue.remove(path)
                        pending.remove(path)
                    queue.appendleft(path)
                    pending.add(path)
                continue

            before_cover = _counts_for(index_after_refine, tag)
            added = 0
            if not args.skip_cover:
                print("cover")
                _run_agent(
                    api_key=api_key,
                    model=args.model,
                    name=f"cover {tag} p{pass_no}",
                    prompt=_prompt_for(
                        "cover-tag",
                        f"/cover-tag #{tag} --limit {args.cover_limit} --flat",
                    ),
                    max_retries=args.max_retries,
                )
                _rebuild_index()

            final_tree = parse_tree_paths(TAGS_MD)
            final_index = _parse_index(COVERAGE_INDEX)
            after_cover = _counts_for(final_index, tag)
            if not args.skip_cover:
                added = after_cover.n - before_cover.n
                if added < 0:
                    raise RuntimeError(
                        f"coverage count decreased during cover: "
                        f"{before_cover.n} -> {after_cover.n}"
                    )
                total_added += added
                print(
                    f"cover delta: n {before_cover.n} -> {after_cover.n}; "
                    f"created={added}"
                )

            subtree_stable = subtree_before == _subtree_signature(final_tree, tag)
            cover_stable = args.skip_cover or added == 0
            if subtree_stable and cover_stable:
                zero_streak[tag] = zero_streak.get(tag, 0) + 1
            else:
                zero_streak[tag] = 0

            requeue(tag)
            newly_queued = enqueue_changed(final_tree, final_index, current=tag)

            if zero_streak[tag] >= args.confirm_zero_runs:
                if tag in pending:
                    queue.remove(tag)
                    pending.remove(tag)
                completed.add(tag)
                state_completed[tag] = _completion_record(tag, final_index, final_tree)
                _save_state(state_path, state)
                completion_label = (
                    "stable refine pass(es)"
                    if args.skip_cover
                    else "zero-card cover run(s)"
                )
                print(
                    f"COMPLETE #{tag}: tree stable and "
                    f"{zero_streak[tag]} {completion_label}"
                )
            elif newly_queued:
                print(
                    "queued new/invalidated paths: "
                    + ", ".join(f"#{path}" for path in newly_queued)
                )
            else:
                print(
                    f"continue #{tag}: tree_stable={subtree_stable} "
                    f"created={added}"
                )
        except (AgentRunError, RuntimeError, subprocess.CalledProcessError) as err:
            failures.add(tag)
            state_completed.pop(tag, None)
            print(f"FAILED #{tag}: {err}", file=sys.stderr)
            if args.fail_fast:
                raise

    if failures or incomplete:
        print(
            f"done with failed={len(failures)} incomplete={len(incomplete)} "
            f"created={total_added}",
            file=sys.stderr,
        )
        return 2
    print(
        f"coverage batch complete: converged={len(completed - resumed)} "
        f"resumed={len(resumed)} created={total_added} limited_out={limited_out}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
