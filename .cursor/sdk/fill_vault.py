#!/usr/bin/env python3
"""Refine and cover technical Tags.md leaves with reviewable persistent progress.

The runtime queue is rebuilt from Tags.md and the tracked
SRS/NamesHistory/coverage-progress.json file on every invocation. New or dirty
leaves run first (empty, fewer-card, deeper leaves first); branches only perform
taxonomy/aggregate validation after their relevant children complete.

Each eligible leaf gets at most one /cover-tag call per run. --cover-limit is an
upper budget, never a target. Cover must write a validated machine-readable result;
missing or malformed results fail closed. Hitting the budget marks review_required
and requires an explicit --continue-tag on a later run.

Real runs are accepted only in the hardened Docker launcher. The container root is
read-only, a disposable Git clone is the only writable host mount, Docker's socket
and the source vault are not mounted, and direct host execution is dry-run only.
The tracked progress file is reviewed and accepted or rejected with the card diff.
Do not run two instances against the same vault.
"""

from __future__ import annotations

import argparse
from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
from typing import Any, Iterable

REPO = Path(__file__).resolve().parents[2]
_SCRIPTS = REPO / ".cursor" / "skills" / "process-topic" / "scripts"
sys.path.insert(0, str(_SCRIPTS))

from vault_cards import (  # noqa: E402
    normalize_prefix,
    parse_tree_paths,
    path_in_prefix,
    scan_cards,
    vault_dir,
)

INDEX_ROW = re.compile(r"^\| `#([^`]+)` \| (\d+) \| (\d+) \| (\d+) \|")
SKILL_ROOT = REPO / ".cursor" / "skills"
TAGS_MD = vault_dir(REPO) / "Format" / "Tags.md"
COVERAGE_INDEX = vault_dir(REPO) / "NamesHistory" / "coverage-index.md"
REBUILD = _SCRIPTS / "rebuild-coverage-index.py"
DEFAULT_STATE = vault_dir(REPO) / "NamesHistory" / "coverage-progress.json"
RESULT_ROOT = REPO / ".cursor" / "sdk" / "cover-results"
STATE_VERSION = 2
RESULT_VERSION = 1
CONTAINER_MARKER = "SRS_COVER_ISOLATED_CONTAINER"
CONTAINER_WORKSPACE = Path("/workspace")

STATUSES = frozenset(
    {"pending", "blocked", "dirty", "complete", "review_required", "failed", "running"}
)
DIMENSIONS = (
    "definition",
    "mechanism",
    "failure_version_lie",
    "comparison",
    "procedure_operations",
    "missing_definition_gaps",
)
NONTECH_PREFIXES = ("Career", "EngineeringLeadership", "ProjectManagement")
SYSTEM_TAGS = frozenset({"SRS", "New"})

CONSTRAINTS = """
You are in the vault git repo (cwd). Follow the named skill exactly except that
instructions to clone or write outside cwd are superseded by these repository-only
rules. English only for reports, cards, and Tags.md.

Hard constraints:
- Do not spawn subagents or invent replacement walkers, retaggers, indexers, or writers.
- PowerShell: never pass a leading # to Python CLI arguments.
- Read and write only inside this workspace. Fetch individual source files; do not clone.
- Do not commit, checkout, reset, clean, push, or run any destructive git command.
- /cover-tag creates compact #New drafts only; never invoke /fill-tag.
- Cover may create fewer files than its limit. The limit is a hard cap, not a target.
- Cover must not retag existing cards, edit Tags.md, or mutate sibling tags.
- The structured --result-file is mandatory and must be written through write_drafts.py.
- Rebuild the coverage index after card or taxonomy changes.
""".strip()


@dataclass(frozen=True)
class Counts:
    n: int
    n_new: int
    n_filled: int


@dataclass(frozen=True)
class CoverOutcome:
    created_count: int
    created_cues: tuple[str, ...]
    dimensions: dict[str, Any]
    sources_searched: dict[str, list[str]]
    exhausted: bool
    budget_hit: bool
    deferred: tuple[str, ...]


CardAssignments = dict[str, tuple[str, ...]]


def _sha256(lines: Iterable[str]) -> str:
    payload = "\n".join(lines).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _parse_index(path: Path) -> dict[str, Counts]:
    out: dict[str, Counts] = {}
    if not path.is_file():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        match = INDEX_ROW.match(line)
        if match:
            out[match.group(1)] = Counts(
                int(match.group(2)), int(match.group(3)), int(match.group(4))
            )
    return out


def _counts_for(index: dict[str, Counts], tag: str) -> Counts:
    return index.get(tag, Counts(0, 0, 0))


def _card_assignments(repo: Path = REPO) -> CardAssignments:
    _scanned, cards = scan_cards(vault_dir(repo))
    out: CardAssignments = {}
    for card in cards:
        thematic = tuple(sorted(tag for tag in card.tags if tag not in SYSTEM_TAGS))
        # Card files are basenames in this vault. Detecting a collision is safer than
        # silently weakening a fingerprint.
        if card.path.name in out and out[card.path.name] != thematic:
            raise RuntimeError(f"duplicate card basename with different tags: {card.path.name}")
        out[card.path.name] = thematic
    return out


def _taxonomy_fingerprint(tree_paths: list[str], tag: str) -> str:
    return _sha256(sorted(path for path in tree_paths if path_in_prefix(path, tag)))


def _coverage_entries(assignments: CardAssignments, tag: str) -> list[str]:
    entries: list[str] = []
    for basename, tags in assignments.items():
        if any(path_in_prefix(card_tag, tag) for card_tag in tags):
            entries.append(f"{basename}\0{' '.join(tags)}")
    return sorted(entries)


def _coverage_fingerprint(assignments: CardAssignments, tag: str) -> str:
    return _sha256(_coverage_entries(assignments, tag))


def _direct_card_count(assignments: CardAssignments, tag: str) -> int:
    return sum(1 for tags in assignments.values() if tag in tags)


def _is_parent(path: str, tree_paths: Iterable[str]) -> bool:
    prefix = path + "/"
    return any(other != path and other.startswith(prefix) for other in tree_paths)


def _immediate_children(path: str, tree_paths: list[str]) -> list[str]:
    descendants = [
        item for item in tree_paths if item != path and path_in_prefix(item, path)
    ]
    children: list[str] = []
    for candidate in descendants:
        if not any(
            other != candidate
            and other != path
            and path_in_prefix(candidate, other)
            and path_in_prefix(other, path)
            for other in descendants
        ):
            children.append(candidate)
    return sorted(children, key=str.lower)


def _matches_any(tag: str, prefixes: Iterable[str]) -> bool:
    return any(path_in_prefix(tag, prefix) for prefix in prefixes if prefix)


def _scoped_paths(
    tree_paths: list[str],
    *,
    prefix: str,
    only: tuple[str, ...],
    excluded: tuple[str, ...],
) -> list[str]:
    return [
        path
        for path in tree_paths
        if (not prefix or path_in_prefix(path, prefix))
        and (not only or any(path_in_prefix(path, item) for item in only))
        and not _matches_any(path, excluded)
    ]


def _current_fingerprints(
    tree_paths: list[str], assignments: CardAssignments, tag: str
) -> tuple[str, str, list[str]]:
    return (
        _taxonomy_fingerprint(tree_paths, tag),
        _coverage_fingerprint(assignments, tag),
        _immediate_children(tag, tree_paths),
    )


def _dimensions_valid(dimensions: Any) -> bool:
    if not isinstance(dimensions, dict) or set(dimensions) != set(DIMENSIONS):
        return False
    for value in dimensions.values():
        if not isinstance(value, dict):
            return False
        if not isinstance(value.get("required"), bool):
            return False
        if not isinstance(value.get("satisfied"), bool):
            return False
        evidence = value.get("evidence")
        if not isinstance(evidence, list) or not all(
            isinstance(item, str) and item.strip() for item in evidence
        ):
            return False
    return True


def _dimensions_satisfied(dimensions: Any) -> bool:
    if not _dimensions_valid(dimensions):
        return False
    for value in dimensions.values():
        if value["required"] and not value["satisfied"]:
            return False
    return True


def _record_matches(
    record: Any,
    tag: str,
    tree_paths: list[str],
    assignments: CardAssignments,
) -> bool:
    if not isinstance(record, dict):
        return False
    taxonomy, coverage, children = _current_fingerprints(tree_paths, assignments, tag)
    return (
        record.get("taxonomy_fingerprint") == taxonomy
        and record.get("coverage_fingerprint") == coverage
        and record.get("children") == children
    )


def _is_complete_current(
    record: Any,
    tag: str,
    tree_paths: list[str],
    assignments: CardAssignments,
) -> bool:
    if not _record_matches(record, tag, tree_paths, assignments):
        return False
    if record.get("status") != "complete":
        return False
    if record.get("refined_taxonomy_fingerprint") != record.get(
        "taxonomy_fingerprint"
    ):
        return False
    if _is_parent(tag, tree_paths):
        return _dimensions_satisfied(record.get("coverage_dimensions"))
    return (
        record.get("candidate_search_exhausted") is True
        and record.get("budget_hit") is False
        and _dimensions_satisfied(record.get("coverage_dimensions"))
    )


def _reconcile_record(
    record: Any,
    tag: str,
    tree_paths: list[str],
    assignments: CardAssignments,
) -> dict[str, Any] | None:
    if not isinstance(record, dict):
        return None
    out = dict(record)
    if out.get("status") not in STATUSES:
        out["status"] = "dirty"
    if out.get("status") == "running":
        out["status"] = "dirty"
        out["last_error"] = "recovered stale running status"
    if not _record_matches(out, tag, tree_paths, assignments):
        out["status"] = "dirty"
        out["last_error"] = "fingerprint changed"
    return out


def _queue_sort_key(
    tag: str,
    *,
    tree_paths: list[str],
    assignments: CardAssignments,
    nodes: dict[str, Any],
) -> tuple[Any, ...]:
    parent = _is_parent(tag, tree_paths)
    direct = _direct_card_count(assignments, tag)
    status = (nodes.get(tag) or {}).get("status", "pending")
    dirty_or_new = 0 if status in {"pending", "dirty"} else 1
    if not parent:
        return (0, dirty_or_new, 0 if direct == 0 else 1, direct, -tag.count("/"), tag.lower())
    return (1, -tag.count("/"), direct, tag.lower())


def _sort_runtime_paths(
    paths: Iterable[str],
    *,
    tree_paths: list[str],
    assignments: CardAssignments,
    nodes: dict[str, Any],
) -> list[str]:
    return sorted(
        set(paths),
        key=lambda tag: _queue_sort_key(
            tag, tree_paths=tree_paths, assignments=assignments, nodes=nodes
        ),
    )


def build_runtime_queue(
    *,
    tree_paths: list[str],
    scoped_paths: list[str],
    assignments: CardAssignments,
    nodes: dict[str, Any],
    max_tags: int | None,
    continue_tags: tuple[str, ...] = (),
) -> tuple[list[str], tuple[str, ...], int]:
    """Derive the queue and max-tags seed leaves; never persist the queue."""
    continued = set(continue_tags)

    def runnable(tag: str) -> bool:
        record = nodes.get(tag)
        if _is_complete_current(record, tag, tree_paths, assignments):
            return False
        if isinstance(record, dict) and record.get("status") == "review_required":
            return tag in continued
        return True

    scoped_set = set(scoped_paths)
    leaves = [
        tag for tag in scoped_paths if not _is_parent(tag, tree_paths) and runnable(tag)
    ]
    ordered_leaves = _sort_runtime_paths(
        leaves, tree_paths=tree_paths, assignments=assignments, nodes=nodes
    )
    if max_tags is not None:
        seeds = tuple(ordered_leaves[:max_tags])
        limited_out = max(0, len(ordered_leaves) - len(seeds))
        selected = [
            path
            for path in scoped_paths
            if runnable(path)
            and any(
                path_in_prefix(path, seed) or path_in_prefix(seed, path)
                for seed in seeds
            )
        ]
    else:
        seeds = tuple(ordered_leaves)
        limited_out = 0
        selected = [path for path in scoped_paths if runnable(path)]
    return (
        _sort_runtime_paths(
            selected, tree_paths=tree_paths, assignments=assignments, nodes=nodes
        ),
        seeds,
        limited_out,
    )


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
        return {"version": STATE_VERSION, "nodes": {}}
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as err:
        raise SystemExit(f"cannot read state file {path}: {err}") from err
    if state.get("version") != STATE_VERSION or not isinstance(state.get("nodes"), dict):
        # The old ignored v1 checkpoint had no trustworthy fingerprints.
        if state.get("version") == 1:
            return {"version": STATE_VERSION, "nodes": {}}
        raise SystemExit(f"unsupported state file format: {path}")
    return state


def _save_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def _base_record(
    *,
    previous: Any,
    status: str,
    tag: str,
    tree_paths: list[str],
    assignments: CardAssignments,
) -> dict[str, Any]:
    taxonomy, coverage, children = _current_fingerprints(tree_paths, assignments, tag)
    record = dict(previous) if isinstance(previous, dict) else {}
    record.update(
        {
            "status": status,
            "taxonomy_fingerprint": taxonomy,
            "coverage_fingerprint": coverage,
            "children": children,
            "passes": int(record.get("passes", 0)),
            "last_created": int(record.get("last_created", 0)),
        }
    )
    return record


def _needs_refine(record: Any, taxonomy_fingerprint: str, skip_refine: bool) -> bool:
    if skip_refine:
        return False
    if not isinstance(record, dict):
        return True
    history = record.get("refined_taxonomy_fingerprints", [])
    return (
        record.get("refined_taxonomy_fingerprint") != taxonomy_fingerprint
        and taxonomy_fingerprint not in history
    )


def _aggregate_dimensions(children: list[dict[str, Any]]) -> dict[str, Any]:
    dimensions: dict[str, Any] = {}
    for name in DIMENSIONS:
        child_values = [child.get("coverage_dimensions", {}).get(name) for child in children]
        satisfied = bool(child_values) and all(
            isinstance(value, dict)
            and (not value.get("required", True) or value.get("satisfied") is True)
            for value in child_values
        )
        dimensions[name] = {
            "required": True,
            "satisfied": satisfied,
            "evidence": ["aggregated from complete child nodes"] if satisfied else [],
        }
    return dimensions


def _children_are_complete(
    children: list[str],
    nodes: dict[str, Any],
    tree_paths: list[str],
    assignments: CardAssignments,
) -> bool:
    return all(
        _is_complete_current(nodes.get(child), child, tree_paths, assignments)
        for child in children
    )


def _status_after_cover(outcome: CoverOutcome, *, taxonomy_refined: bool) -> str:
    if outcome.budget_hit:
        return "review_required"
    if (
        taxonomy_refined
        and outcome.exhausted
        and _dimensions_satisfied(outcome.dimensions)
    ):
        return "complete"
    return "dirty"


def _result_path(tag: str, pass_no: int) -> Path:
    digest = hashlib.sha256(tag.encode("utf-8")).hexdigest()[:16]
    return RESULT_ROOT / f"{digest}-p{pass_no}.json"


def _read_cover_result(
    path: Path,
    *,
    tag: str,
    limit: int,
    before: CardAssignments,
    after: CardAssignments,
) -> CoverOutcome:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as err:
        raise RuntimeError(f"missing/invalid structured cover result {path}: {err}") from err
    if not isinstance(raw, dict) or raw.get("version") != RESULT_VERSION:
        raise RuntimeError("structured cover result has an unsupported version")
    if normalize_prefix(str(raw.get("tag", ""))) != tag:
        raise RuntimeError("structured cover result tag does not match invocation")

    created_files = sorted(set(after) - set(before), key=str.lower)
    changed_existing = sorted(
        name for name in set(before) & set(after) if before[name] != after[name]
    )
    removed = sorted(set(before) - set(after))
    if changed_existing or removed:
        raise RuntimeError(
            "cover mutated existing card tag assignments or removed cards: "
            + ", ".join(changed_existing + removed)
        )
    for name in created_files:
        if tag not in after[name]:
            raise RuntimeError(f"cover created a card outside the current leaf: {name}")

    cues = tuple(name[:-3] if name.lower().endswith(".md") else name for name in created_files)
    declared_cues = raw.get("created_cues")
    if not isinstance(declared_cues, list) or not all(
        isinstance(item, str) for item in declared_cues
    ):
        raise RuntimeError("structured cover result created_cues must be a string list")
    if sorted(declared_cues, key=str.lower) != sorted(cues, key=str.lower):
        raise RuntimeError("structured cover result cues do not match created card files")
    created_count = raw.get("created_count")
    if not isinstance(created_count, int) or isinstance(created_count, bool):
        raise RuntimeError("structured cover result created_count must be an integer")
    if created_count != len(created_files) or created_count > limit:
        raise RuntimeError("structured cover result count violates the observed budget")

    dimensions = raw.get("coverage_dimensions")
    if not _dimensions_valid(dimensions):
        raise RuntimeError("structured cover result has invalid coverage dimensions")
    sources = raw.get("sources_searched")
    if not isinstance(sources, dict) or set(sources) != {"interview", "official"}:
        raise RuntimeError("structured cover result sources_searched is invalid")
    for kind in ("interview", "official"):
        urls = sources[kind]
        if not isinstance(urls, list) or not all(
            isinstance(url, str) and url.startswith(("https://", "http://")) for url in urls
        ):
            raise RuntimeError(f"structured cover result {kind} sources are invalid")
    if not sources["interview"]:
        raise RuntimeError("cover did not report a real interview-question source")
    if created_count and not sources["official"]:
        raise RuntimeError("created candidates lack reported official-documentation checks")

    exhausted = raw.get("candidate_search_exhausted")
    budget_hit = raw.get("budget_hit")
    if not isinstance(exhausted, bool) or not isinstance(budget_hit, bool):
        raise RuntimeError("structured cover result stop flags must be booleans")
    observed_budget_hit = created_count == limit
    if budget_hit != observed_budget_hit:
        raise RuntimeError("structured cover result budget_hit disagrees with created count")
    deferred = raw.get("deferred_candidates", [])
    if not isinstance(deferred, list) or not all(isinstance(item, str) for item in deferred):
        raise RuntimeError("structured cover result deferred_candidates is invalid")
    return CoverOutcome(
        created_count=created_count,
        created_cues=cues,
        dimensions=dimensions,
        sources_searched=sources,
        exhausted=exhausted,
        budget_hit=budget_hit,
        deferred=tuple(deferred),
    )


def _rebuild_index() -> None:
    subprocess.run([sys.executable, str(REBUILD)], cwd=str(REPO), check=True)
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
        if len(fields) >= 6:
            mounts.append(
                (Path(fields[4].replace("\\040", " ")), frozenset(fields[5].split(",")))
            )
    return mounts


def _require_container_boundary() -> None:
    if sys.platform != "linux":
        raise SystemExit(
            "REFUSED: real runs require the Docker launcher; direct host execution is dry-run only"
        )
    if os.environ.get(CONTAINER_MARKER) != "1" or not Path("/.dockerenv").is_file():
        raise SystemExit("REFUSED: hardened Docker launcher marker/environment is missing")
    if REPO.resolve() != CONTAINER_WORKSPACE:
        raise SystemExit(f"REFUSED: repository must be mounted at {CONTAINER_WORKSPACE}")
    if Path("/var/run/docker.sock").exists():
        raise SystemExit("REFUSED: Docker socket must not be mounted")
    mounts = _mount_table()
    by_path = {path: options for path, options in mounts}
    if "ro" not in by_path.get(Path("/"), frozenset()):
        raise SystemExit("REFUSED: container root is not read-only")
    if "rw" not in by_path.get(CONTAINER_WORKSPACE, frozenset()):
        raise SystemExit("REFUSED: /workspace is not a dedicated read/write mount")
    allowed = {
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
        Path("/usr/sbin/docker-init"),
    }
    prefixes = (
        CONTAINER_WORKSPACE,
        Path("/tmp"),
        Path("/home/agent"),
        Path("/proc"),
        Path("/sys"),
        Path("/dev"),
    )
    unexpected = [
        str(path)
        for path, _options in mounts
        if path not in allowed
        and not any(path != prefix and prefix in path.parents for prefix in prefixes)
    ]
    if unexpected:
        raise SystemExit("REFUSED: unexpected container mounts: " + ", ".join(sorted(unexpected)))


def _local_options() -> dict[str, Any]:
    return {"cwd": str(REPO), "setting_sources": ["project"]}


def _prompt_for(skill: str, command: str) -> str:
    skill_file = SKILL_ROOT / skill / "SKILL.md"
    return (
        f"{CONSTRAINTS}\n\nRead and follow `{skill_file.as_posix()}` exactly.\n\n"
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
                return max(
                    0.0, (retry_at - datetime.now(timezone.utc)).total_seconds()
                )
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
    from cursor_sdk import (
        Agent,
        AgentOptions,
        CursorAgentError,
        LocalAgentOptions,
        ModelParameterValue,
        ModelSelection,
    )

    model_selection: str | ModelSelection = model
    if model in {"grok-4-6", "grok-4.6"}:
        model_selection = ModelSelection(
            id="grok-4.6",
            params=(ModelParameterValue(id="reasoning_effort", value="high"),),
        )
    result = None
    for attempt in range(max_retries + 1):
        try:
            result = Agent.prompt(
                prompt,
                AgentOptions(
                    api_key=api_key,
                    model=model_selection,
                    name=name,
                    local=LocalAgentOptions(**_local_options()),
                ),
            )
            break
        except CursorAgentError as err:
            retryable = bool(getattr(err, "is_retryable", False))
            request_id = getattr(err, "request_id", None)
            if not retryable or attempt >= max_retries:
                raise AgentRunError(
                    f"startup failed: {err}; retryable={retryable}; request_id={request_id}"
                ) from err
            delay = _retry_delay(err, attempt)
            print(
                f"  startup retry {attempt + 1}/{max_retries} in {delay:.1f}s "
                f"request_id={request_id}",
                file=sys.stderr,
            )
            time.sleep(delay)
    if result is None:
        raise AgentRunError("Cursor SDK returned no result")
    text = str(getattr(result, "result", None) or "")
    print(f"  status={result.status} id={getattr(result, 'id', '')}")
    if result.status != "finished":
        raise AgentRunError(
            f"run did not finish: status={result.status} id={getattr(result, 'id', '')}"
        )
    return text


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Build a deterministic leaf-first queue from Tags.md and tracked progress. "
            "Each leaf receives at most one cover call per run."
        )
    )
    parser.add_argument("--dry-run", action="store_true", help="Print the derived queue.")
    parser.add_argument("--model", default="grok-4.6")
    parser.add_argument(
        "--cover-limit",
        type=int,
        default=50,
        help="Upper budget for new cards in one leaf call; never a target.",
    )
    parser.add_argument(
        "--max-tags",
        type=int,
        default=None,
        help="Select this many seed leaves; new descendants may join the run.",
    )
    parser.add_argument(
        "--max-passes-per-tag",
        type=int,
        default=5,
        help="Taxonomy stabilization safety cap; cover still runs at most once per leaf.",
    )
    parser.add_argument("--max-retries", type=int, default=2)
    parser.add_argument(
        "--state-file",
        default=str(DEFAULT_STATE.relative_to(REPO)),
        help="Tracked repository-local progress state.",
    )
    parser.add_argument("--fresh", action="store_true")
    parser.add_argument("--only", action="append", default=[], metavar="TAG")
    parser.add_argument(
        "--prefix",
        default="Java",
        help="Restrict to this Tags.md path and its descendants. Empty string for all technical paths.",
    )
    parser.add_argument("--exclude", action="append", default=[], metavar="PREFIX")
    parser.add_argument("--skip-refine", action="store_true")
    parser.add_argument("--skip-cover", action="store_true")
    parser.add_argument("--include-nontechnical", action="store_true")
    parser.add_argument(
        "--continue-tag",
        action="append",
        default=[],
        metavar="TAG",
        help="Explicitly continue an exact review_required leaf. Repeatable.",
    )
    parser.add_argument("--fail-fast", action="store_true")
    return parser


def _plan_line(
    tag: str,
    *,
    tree_paths: list[str],
    assignments: CardAssignments,
    nodes: dict[str, Any],
    skip_refine: bool,
    skip_cover: bool,
) -> str:
    parent = _is_parent(tag, tree_paths)
    record = nodes.get(tag)
    taxonomy = _taxonomy_fingerprint(tree_paths, tag)
    steps: list[str] = []
    if _needs_refine(record, taxonomy, skip_refine):
        steps.append("refine")
    elif not skip_refine:
        steps.append("refine skipped")
    if parent:
        steps.append("aggregate")
    elif not skip_cover:
        steps.append("cover once")
    status = (record or {}).get("status", "pending")
    return (
        f"  #{tag} direct={_direct_card_count(assignments, tag)} "
        f"[{'branch' if parent else 'leaf'} {status}] -> {' + '.join(steps) or 'validate'}"
    )


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
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
    if args.max_retries < 0:
        raise SystemExit("--max-retries must be >= 0")
    if not TAGS_MD.is_file():
        raise SystemExit(f"missing Tags.md: {TAGS_MD}")

    prefix = normalize_prefix(args.prefix)
    only = tuple(normalize_prefix(item) for item in args.only)
    continue_tags = tuple(normalize_prefix(item) for item in args.continue_tag)
    if any(not item for item in only):
        raise SystemExit("--only cannot be empty")
    if any(not item for item in continue_tags):
        raise SystemExit("--continue-tag cannot be empty")
    excluded = [normalize_prefix(item) for item in args.exclude]
    if not args.include_nontechnical:
        excluded.extend(NONTECH_PREFIXES)
    excluded_tuple = tuple(item for item in excluded if item)

    state_path = _resolve_state_path(args.state_file)
    state = _load_state(state_path, fresh=args.fresh)
    nodes: dict[str, Any] = state["nodes"]

    if not args.dry_run:
        _require_container_boundary()
        _rebuild_index()
    elif not COVERAGE_INDEX.is_file():
        raise SystemExit(f"missing coverage index: {COVERAGE_INDEX}")

    tree_paths = parse_tree_paths(TAGS_MD)
    assignments = _card_assignments()
    scoped = _scoped_paths(
        tree_paths, prefix=prefix, only=only, excluded=excluded_tuple
    )
    if not scoped:
        raise SystemExit("no Tags.md paths match the requested technical scope")
    for tag in list(nodes):
        if tag in tree_paths:
            reconciled = _reconcile_record(nodes[tag], tag, tree_paths, assignments)
            if reconciled is not None:
                nodes[tag] = reconciled

    queue_list, seed_leaves, limited_out = build_runtime_queue(
        tree_paths=tree_paths,
        scoped_paths=scoped,
        assignments=assignments,
        nodes=nodes,
        max_tags=args.max_tags,
        continue_tags=continue_tags,
    )
    resumed = sum(
        1
        for tag in scoped
        if _is_complete_current(nodes.get(tag), tag, tree_paths, assignments)
    )
    review_skipped = sum(
        1
        for tag in scoped
        if isinstance(nodes.get(tag), dict)
        and nodes[tag].get("status") == "review_required"
        and tag not in continue_tags
    )
    print(f"repo={REPO}")
    print(
        f"technical paths in scope={len(scoped)} resumed={resumed} "
        f"seed leaves={len(seed_leaves)} queued={len(queue_list)} "
        f"review_skipped={review_skipped} limited_out={limited_out}"
    )
    print(
        "completion=taxonomy refined + children complete + dimensions satisfied + "
        "candidate search exhausted + budget not hit"
    )
    if excluded_tuple:
        print("excluded=" + ", ".join(excluded_tuple))
    for tag in queue_list:
        print(
            _plan_line(
                tag,
                tree_paths=tree_paths,
                assignments=assignments,
                nodes=nodes,
                skip_refine=args.skip_refine,
                skip_cover=args.skip_cover,
            )
        )
    if args.dry_run:
        if sys.platform != "linux":
            print("note: direct host execution is dry-run only", file=sys.stderr)
        return 0
    if not queue_list:
        return 0

    api_key = os.environ.pop("CURSOR_API_KEY", "").strip()
    if not api_key:
        raise SystemExit("set CURSOR_API_KEY (https://cursor.com/dashboard/integrations)")

    queue: deque[str] = deque(queue_list)
    pending = set(queue_list)
    seed_prefixes = seed_leaves if args.max_tags is not None else None
    cover_called: set[str] = set()
    finished_this_run: set[str] = set()
    failures: set[str] = set()
    blocked: set[str] = set()
    reviews: set[str] = set()
    attempts: dict[str, int] = {}
    total_created = 0

    def currently_scoped(current_tree: list[str]) -> list[str]:
        paths = _scoped_paths(
            current_tree, prefix=prefix, only=only, excluded=excluded_tuple
        )
        if seed_prefixes is not None:
            paths = [
                path
                for path in paths
                if any(
                    path_in_prefix(path, seed) or path_in_prefix(seed, path)
                    for seed in seed_prefixes
                )
            ]
        return paths

    def refresh_queue(current_tree: list[str], current_assignments: CardAssignments) -> None:
        allowed = currently_scoped(current_tree)
        candidates: list[str] = list(queue)
        for path in allowed:
            if path in pending or path in finished_this_run or path in failures:
                continue
            record = nodes.get(path)
            if _is_complete_current(record, path, current_tree, current_assignments):
                continue
            if (
                isinstance(record, dict)
                and record.get("status") == "review_required"
                and path not in continue_tags
            ):
                continue
            candidates.append(path)
        ordered = _sort_runtime_paths(
            candidates,
            tree_paths=current_tree,
            assignments=current_assignments,
            nodes=nodes,
        )
        queue.clear()
        queue.extend(ordered)
        pending.clear()
        pending.update(ordered)

    while queue:
        tag = queue.popleft()
        pending.discard(tag)
        tree_paths = parse_tree_paths(TAGS_MD)
        assignments = _card_assignments()
        if tag not in tree_paths or tag not in currently_scoped(tree_paths):
            nodes.pop(tag, None)
            refresh_queue(tree_paths, assignments)
            continue
        existing = _reconcile_record(nodes.get(tag), tag, tree_paths, assignments)
        if existing is not None:
            nodes[tag] = existing
        if _is_complete_current(nodes.get(tag), tag, tree_paths, assignments):
            finished_this_run.add(tag)
            continue

        attempts[tag] = attempts.get(tag, 0) + 1
        if attempts[tag] > args.max_passes_per_tag:
            record = _base_record(
                previous=nodes.get(tag),
                status="failed",
                tag=tag,
                tree_paths=tree_paths,
                assignments=assignments,
            )
            record["last_error"] = "taxonomy stabilization safety cap reached"
            nodes[tag] = record
            failures.add(tag)
            _save_state(state_path, state)
            continue

        print(f"\n=== #{tag} pass {attempts[tag]}/{args.max_passes_per_tag} ===")
        existing_children = [
            child
            for child in _immediate_children(tag, tree_paths)
            if child in currently_scoped(tree_paths)
        ]
        if existing_children and not _children_are_complete(
            existing_children, nodes, tree_paths, assignments
        ):
            record = _base_record(
                previous=nodes.get(tag),
                status="blocked",
                tag=tag,
                tree_paths=tree_paths,
                assignments=assignments,
            )
            record["last_error"] = "waiting for relevant children"
            nodes[tag] = record
            blocked.add(tag)
            finished_this_run.add(tag)
            _save_state(state_path, state)
            print("BLOCKED: relevant children have not converged")
            continue
        taxonomy_before = _taxonomy_fingerprint(tree_paths, tag)
        try:
            did_refine = _needs_refine(
                nodes.get(tag), taxonomy_before, args.skip_refine
            )
            if did_refine:
                print("refine")
                _run_agent(
                    api_key=api_key,
                    model=args.model,
                    name=f"refine {tag} p{attempts[tag]}",
                    prompt=_prompt_for("refine-tags", f"/refine-tags #{tag}"),
                    max_retries=args.max_retries,
                )
                _rebuild_index()
            elif not args.skip_refine:
                print("refine skipped: taxonomy fingerprint already refined")

            tree_after = parse_tree_paths(TAGS_MD)
            assignments_after = _card_assignments()
            if tag not in tree_after:
                nodes.pop(tag, None)
                finished_this_run.add(tag)
                refresh_queue(tree_after, assignments_after)
                _save_state(state_path, state)
                continue

            taxonomy_after = _taxonomy_fingerprint(tree_after, tag)
            record = _base_record(
                previous=nodes.get(tag),
                status="dirty",
                tag=tag,
                tree_paths=tree_after,
                assignments=assignments_after,
            )
            record["passes"] += 1
            record["last_error"] = None
            if did_refine:
                history = list(record.get("refined_taxonomy_fingerprints", []))
                if taxonomy_before not in history:
                    history.append(taxonomy_before)
                record["refined_taxonomy_fingerprints"] = history
            if args.skip_refine or taxonomy_after == taxonomy_before:
                record["refined_taxonomy_fingerprint"] = taxonomy_after
            nodes[tag] = record

            if taxonomy_after != taxonomy_before:
                record["status"] = "blocked"
                record["last_error"] = "taxonomy changed; descendants must converge first"
                blocked.add(tag)
                print("taxonomy changed; blocking node and rebuilding child-first queue")
                refresh_queue(tree_after, assignments_after)
                if tag not in pending:
                    queue.append(tag)
                    pending.add(tag)
                _save_state(state_path, state)
                continue

            children = _immediate_children(tag, tree_after)
            if children:
                relevant = [child for child in children if child in currently_scoped(tree_after)]
                child_records = [nodes.get(child) for child in relevant]
                child_complete = _children_are_complete(
                    relevant, nodes, tree_after, assignments_after
                )
                if not child_complete:
                    record["status"] = "blocked"
                    record["last_error"] = "waiting for relevant children"
                    blocked.add(tag)
                    finished_this_run.add(tag)
                    print("BLOCKED: relevant children have not converged")
                else:
                    dimensions = _aggregate_dimensions(
                        [child for child in child_records if isinstance(child, dict)]
                    )
                    record["coverage_dimensions"] = dimensions
                    record["candidate_search_exhausted"] = True
                    record["budget_hit"] = False
                    if (
                        record.get("refined_taxonomy_fingerprint") == taxonomy_after
                        and _dimensions_satisfied(dimensions)
                    ):
                        record["status"] = "complete"
                        record["last_error"] = None
                        blocked.discard(tag)
                        print("COMPLETE: taxonomy and child aggregates converged")
                    else:
                        record["status"] = "dirty"
                        record["last_error"] = "branch taxonomy or dimensions incomplete"
                    finished_this_run.add(tag)
                nodes[tag] = record
                _save_state(state_path, state)
                refresh_queue(tree_after, assignments_after)
                continue

            if args.skip_cover:
                record["status"] = "dirty"
                record["last_error"] = "cover skipped; coverage not declared exhausted"
                nodes[tag] = record
                finished_this_run.add(tag)
                _save_state(state_path, state)
                continue
            if tag in cover_called:
                raise RuntimeError("internal guard prevented a second cover call in one run")
            cover_called.add(tag)
            result_path = _result_path(tag, attempts[tag])
            result_path.parent.mkdir(parents=True, exist_ok=True)
            if result_path.exists():
                result_path.unlink()
            before_cover = assignments_after
            print(f"cover (upper budget {args.cover_limit})")
            _run_agent(
                api_key=api_key,
                model=args.model,
                name=f"cover {tag} p{attempts[tag]}",
                prompt=_prompt_for(
                    "cover-tag",
                    f"/cover-tag #{tag} --limit {args.cover_limit} --flat "
                    f"--result-file {result_path.relative_to(REPO).as_posix()}",
                ),
                max_retries=args.max_retries,
            )
            _rebuild_index()
            final_tree = parse_tree_paths(TAGS_MD)
            final_assignments = _card_assignments()
            if final_tree != tree_after:
                raise RuntimeError("cover mutated Tags.md; taxonomy changes belong to refine")
            outcome = _read_cover_result(
                result_path,
                tag=tag,
                limit=args.cover_limit,
                before=before_cover,
                after=final_assignments,
            )
            total_created += outcome.created_count
            record = _base_record(
                previous=record,
                status="dirty",
                tag=tag,
                tree_paths=final_tree,
                assignments=final_assignments,
            )
            record.update(
                {
                    "last_created": outcome.created_count,
                    "coverage_dimensions": outcome.dimensions,
                    "candidate_search_exhausted": outcome.exhausted,
                    "budget_hit": outcome.budget_hit,
                    "sources_searched": outcome.sources_searched,
                    "deferred_candidates": list(outcome.deferred),
                    "last_error": None,
                }
            )
            outcome_status = _status_after_cover(
                outcome,
                taxonomy_refined=record.get("refined_taxonomy_fingerprint")
                == record.get("taxonomy_fingerprint"),
            )
            record["status"] = outcome_status
            if outcome_status == "review_required":
                record["last_error"] = "cover budget hit; explicit continuation required"
                reviews.add(tag)
                print("REVIEW REQUIRED: cover budget hit; no automatic second batch")
            elif outcome_status == "complete":
                print(f"COMPLETE: created={outcome.created_count}; candidates exhausted")
            else:
                record["last_error"] = "candidate search not exhausted"
                print(
                    f"DIRTY: created={outcome.created_count}; one-cover-call run limit reached"
                )
            nodes[tag] = record
            finished_this_run.add(tag)
            _save_state(state_path, state)
            refresh_queue(final_tree, final_assignments)
        except (AgentRunError, RuntimeError, subprocess.CalledProcessError) as err:
            current_tree = parse_tree_paths(TAGS_MD)
            current_assignments = _card_assignments()
            if tag in current_tree:
                record = _base_record(
                    previous=nodes.get(tag),
                    status="failed",
                    tag=tag,
                    tree_paths=current_tree,
                    assignments=current_assignments,
                )
                record["last_error"] = str(err)
                nodes[tag] = record
            failures.add(tag)
            finished_this_run.add(tag)
            _save_state(state_path, state)
            print(f"FAILED #{tag}: {err}", file=sys.stderr)
            if args.fail_fast:
                raise

    print(
        f"coverage batch complete: created={total_created} failed={len(failures)} "
        f"review_required={len(reviews)} blocked={len(blocked)}"
    )
    return 2 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
