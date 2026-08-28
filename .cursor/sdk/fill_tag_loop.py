#!/usr/bin/env python3
"""Fill #New cards under a tag with one durable Cursor agent.

The orchestrator names one target per send, waits, then validates that card
before asking for the next. After fill turns it runs /refine-tags and
/dedup-tag for the same tag, then rebuilds the coverage index once. Real runs
are accepted only inside the hardened Docker workspace created by
run_fill_tag.ps1. Direct host execution is limited to --dry-run.
"""

from __future__ import annotations

import argparse
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
from typing import Any


REPO = Path(__file__).resolve().parents[2]
SCRIPTS = REPO / ".cursor" / "skills" / "process-topic" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from vault_cards import (  # noqa: E402
    card_tags,
    extract_tag_line,
    iter_card_files,
    normalize_prefix,
    parse_tree_paths,
    path_in_prefix,
    scan_cards,
    vault_dir,
)


VAULT = vault_dir(REPO)
TAGS_MD = VAULT / "Format" / "Tags.md"
FILL_SKILL = REPO / ".cursor" / "skills" / "fill-tag" / "SKILL.md"
REBUILD = SCRIPTS / "rebuild-coverage-index.py"
DEFAULT_PROGRESS = REPO / "fill-progress.json"
CONTAINER_MARKER = "SRS_FILL_ISOLATED_CONTAINER"
CONTAINER_WORKSPACE = Path("/workspace")
SYSTEM_TAGS = frozenset({"SRS", "New"})
PROGRESS_VERSION = 1

DRAFT_MARKERS = (
    "untrusted draft",
    "unverified traps",
    "dump:",
    "непроверен",
)

CONSTRAINTS = """
You are in an isolated disposable clone of the SRS vault.

This is one durable agent session. The orchestrator sends one card per turn
and waits for you to finish that card before naming the next. Do not look
ahead, invent extra cues, or start a later card on your own.

Hard constraints:
- Read and follow `.cursor/skills/fill-tag/SKILL.md` exactly except the
  coverage-index step.
- Process exactly the one target card named in the current turn.
- Invoke fill-tag with `--limit 1` on every turn.
- Use only official/original documentation as evidence.
- Do not create cards, invoke cover-tag, edit Tags.md, or modify another card.
- Do not spawn subagents.
- Do not commit, checkout, reset, clean, push, or run destructive git commands.
- Do not run rebuild-coverage-index.py. The orchestrator rebuilds once after
  refine-tags and dedup-tag for this tag.
- English only for the card and the final report.
""".strip()

POST_CONSTRAINTS = """
Fill turns are finished. Do not fill another #New card this turn.
Do not spawn subagents.
Do not commit, checkout, reset, clean, push, or run destructive git commands.
Do not run rebuild-coverage-index.py; the orchestrator rebuilds once after
refine-tags and dedup-tag for this tag.
English only.
""".strip()


@dataclass(frozen=True)
class Candidate:
    path: Path
    cue: str
    has_draft: bool


@dataclass(frozen=True)
class AgentOutcome:
    run_id: str
    report: str


class AgentRunError(RuntimeError):
    """A Cursor SDK run failed to reach the finished state."""


class WorkspaceViolation(RuntimeError):
    """An agent changed files outside its assigned card."""


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _known_tag_paths(tree_paths: list[str]) -> list[str]:
    """Tags.md leaves plus implied grouping parents the HTML tree also shows."""
    seen: set[str] = set()
    out: list[str] = []
    for path in tree_paths:
        parts = path.split("/")
        for end in range(1, len(parts) + 1):
            prefix = "/".join(parts[:end])
            if prefix in seen:
                continue
            seen.add(prefix)
            out.append(prefix)
    return out


def _tag_in_tree(requested: str, tree_paths: list[str]) -> bool:
    return any(path_in_prefix(path, requested) for path in tree_paths)


def _resolve_tag(raw: str, tree_paths: list[str]) -> str:
    requested = normalize_prefix(raw)
    if not requested:
        raise SystemExit("TAG cannot be empty")
    if _tag_in_tree(requested, tree_paths):
        return requested
    matches = [
        path
        for path in _known_tag_paths(tree_paths)
        if path.rsplit("/", 1)[-1] == requested
    ]
    if len(matches) == 1:
        return matches[0]
    if not matches:
        raise SystemExit(f"tag not found in Tags.md: #{requested}")
    raise SystemExit(
        f"ambiguous short tag #{requested}; use one of: "
        + ", ".join(f"#{path}" for path in matches)
    )


def _has_untrusted_draft(text: str) -> bool:
    lowered = text.lower()
    return any(marker in lowered for marker in DRAFT_MARKERS)


def _candidate_queue(tag: str) -> list[Candidate]:
    _scanned, cards = scan_cards(VAULT)
    candidates: list[Candidate] = []
    for card in cards:
        if not card.is_new:
            continue
        thematic = card.tags - SYSTEM_TAGS
        if not any(path_in_prefix(card_tag, tag) for card_tag in thematic):
            continue
        text = _read_text(card.path)
        candidates.append(
            Candidate(
                path=card.path,
                cue=card.cue,
                has_draft=_has_untrusted_draft(text),
            )
        )
    return sorted(
        candidates,
        key=lambda item: (not item.has_draft, item.cue.casefold()),
    )


def _card_snapshot() -> dict[str, str]:
    return {
        path.relative_to(VAULT).as_posix(): _sha256_text(_read_text(path))
        for path in iter_card_files(VAULT)
    }


def _changed_cards(before: dict[str, str], after: dict[str, str]) -> list[str]:
    names = set(before) | set(after)
    return sorted(name for name in names if before.get(name) != after.get(name))


def _card_tags(path: Path) -> set[str]:
    tag_line = extract_tag_line(_read_text(path))
    if tag_line is None:
        raise WorkspaceViolation(f"target card has no valid tag line: {path.name}")
    return card_tags(tag_line)


def _validate_filled_card(path: Path, tree_paths: list[str]) -> list[str]:
    text = _read_text(path)
    lowered = text.lower()
    problems: list[str] = []
    tag_line = extract_tag_line(text)
    tags = card_tags(tag_line) if tag_line else set()

    if not re.match(
        r"\A<!--\s*\nreps:\s*\d+\s*\npriority:\s*\d+\s*\n-->\s*\n",
        text,
    ):
        problems.append("meta block is missing or not first")
    if "SRS" not in tags:
        problems.append("tag line is missing #SRS")
    if "New" in tags:
        problems.append("tag line still contains #New")
    if not re.search(r"^> \[!abstract\] Short answer\b", text, re.MULTILINE):
        problems.append("Short answer callout is missing")
    if not re.search(r"^> \[!warning\]\b", text, re.MULTILINE):
        problems.append("warning callout is missing")
    if not re.search(r"^> \[!tip\] Interview answer\b", text, re.MULTILINE):
        problems.append("Interview answer callout is missing")
    if len(re.findall(r"\[\[[^\]\n]+\]\]", text)) < 2:
        problems.append("fewer than two wikilinks")
    if any(marker in lowered for marker in DRAFT_MARKERS):
        problems.append("untrusted-draft residue remains")
    if re.search(r"https?://", text):
        problems.append("URL remains in the card body")
    if re.search(r"\[\^[^\]]+\]", text):
        problems.append("footnote syntax remains")
    if re.search(
        r"^#{1,6}\s+(?:NOTES|SOURCES|REFERENCES|LINKS TO VERIFY|UNCERTAINTIES|CHECKLIST)\b",
        text,
        re.MULTILINE | re.IGNORECASE,
    ):
        problems.append("chat-only end matter remains in the card")

    thematic = sorted(tags - SYSTEM_TAGS)
    unknown = [item for item in thematic if item not in tree_paths]
    if unknown:
        problems.append("tag line contains unknown Tags.md paths: " + ", ".join(unknown))
    for parent in thematic:
        if any(
            child != parent and path_in_prefix(child, parent) for child in thematic
        ):
            problems.append(f"tag line contains parent and child: #{parent}")
            break
    return problems


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


def _model_selection(model: str) -> Any:
    from cursor_sdk import ModelParameterValue, ModelSelection

    if model in {"grok-4-6", "grok-4.6"}:
        return ModelSelection(
            id="grok-4.6",
            params=(ModelParameterValue(id="reasoning_effort", value="high"),),
        )
    return model


def _prompt_for(
    tag: str,
    candidate: Candidate,
    *,
    index: int,
    total: int,
    follow_up: bool,
) -> str:
    relative = candidate.path.relative_to(REPO).as_posix()
    if follow_up:
        preamble = (
            "Same durable session and the same hard constraints. "
            "Previous cards are finished. Process only the next named target."
        )
    else:
        preamble = CONSTRAINTS
    return (
        f"{preamble}\n\n"
        f"Turn {index}/{total}. The one and only target is `{relative}` "
        f"(cue: {json.dumps(candidate.cue, ensure_ascii=False)}).\n"
        "Do not process any other #New card even if the skill's normal scan would "
        "rank it first.\n\n"
        f"Invoke now:\n/fill-tag #{tag} --limit 1\n"
    )


def _post_prompt(skill: str, command: str) -> str:
    skill_file = f".cursor/skills/{skill}/SKILL.md"
    return (
        f"{POST_CONSTRAINTS}\n\n"
        f"Read and follow `{skill_file}` exactly except the coverage-index step.\n\n"
        f"Invoke now:\n{command}\n"
    )


def _run_post_phase(
    agent: Any,
    *,
    name: str,
    skill: str,
    command: str,
    max_retries: int,
    state: dict[str, Any],
    progress_path: Path,
) -> None:
    started = time.monotonic()
    print(f"\n[{name}] START {command}", flush=True)
    status = "failed"
    error: str | None = None
    run_id = ""
    report = ""
    try:
        outcome = _send(
            agent,
            _post_prompt(skill, command),
            max_retries=max_retries,
        )
        run_id = outcome.run_id
        report = outcome.report
        status = "ok"
    except AgentRunError as err:
        error = str(err)
    if report:
        print("    --- agent report ---", flush=True)
        print(report.rstrip(), flush=True)
        print("    --- end report ---", flush=True)
    elapsed = round(time.monotonic() - started, 1)
    detail = f" id={run_id}" if run_id else ""
    if error:
        detail += f" error={error}"
    print(f"[{name}] {status.upper()} {elapsed:.1f}s{detail}", flush=True)
    state["post"][name] = {
        "status": status,
        "duration_seconds": elapsed,
        "run_id": run_id or None,
        "error": error,
        "command": command,
    }
    _save_progress(progress_path, state)


def _create_agent(
    *,
    api_key: str,
    model: str,
    name: str,
    max_retries: int,
):
    from cursor_sdk import Agent, CursorAgentError, LocalAgentOptions

    last_error: BaseException | None = None
    for attempt in range(max_retries + 1):
        try:
            return Agent.create(
                model=_model_selection(model),
                api_key=api_key,
                name=name,
                local=LocalAgentOptions(
                    cwd=str(REPO),
                    setting_sources=["project"],
                ),
            )
        except CursorAgentError as err:
            last_error = err
            retryable = bool(getattr(err, "is_retryable", False))
            request_id = getattr(err, "request_id", None)
            if not retryable or attempt >= max_retries:
                raise AgentRunError(
                    f"startup failed: {err}; retryable={retryable}; "
                    f"request_id={request_id}"
                ) from err
            delay = _retry_delay(err, attempt)
            print(
                f"    startup retry {attempt + 1}/{max_retries} in {delay:.1f}s "
                f"request_id={request_id}",
                flush=True,
            )
            time.sleep(delay)
    raise AgentRunError(f"startup failed: {last_error}")


def _send(
    agent: Any,
    prompt: str,
    *,
    max_retries: int,
) -> AgentOutcome:
    from cursor_sdk import CursorAgentError

    result = None
    for attempt in range(max_retries + 1):
        try:
            run = agent.send(prompt)
            result = run.wait()
            break
        except CursorAgentError as err:
            retryable = bool(getattr(err, "is_retryable", False))
            request_id = getattr(err, "request_id", None)
            if not retryable or attempt >= max_retries:
                raise AgentRunError(
                    f"send failed: {err}; retryable={retryable}; "
                    f"request_id={request_id}"
                ) from err
            delay = _retry_delay(err, attempt)
            print(
                f"    send retry {attempt + 1}/{max_retries} in {delay:.1f}s "
                f"request_id={request_id}",
                flush=True,
            )
            time.sleep(delay)
    if result is None:
        raise AgentRunError("Cursor SDK returned no result")
    run_id = str(getattr(result, "id", "") or "")
    if result.status != "finished":
        raise AgentRunError(
            f"run did not finish: status={result.status} id={run_id}"
        )
    return AgentOutcome(
        run_id=run_id,
        report=str(getattr(result, "result", None) or ""),
    )


def _rebuild_index() -> None:
    subprocess.run([sys.executable, str(REBUILD)], cwd=str(REPO), check=True)


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
            "REFUSED: real runs require run_fill_tag.ps1; "
            "direct host execution is dry-run only"
        )
    if os.environ.get(CONTAINER_MARKER) != "1" or not Path("/.dockerenv").is_file():
        raise SystemExit("REFUSED: hardened Docker launcher marker is missing")
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
        raise SystemExit(
            "REFUSED: unexpected container mounts: " + ", ".join(sorted(unexpected))
        )


def _resolve_progress_path(raw: str) -> Path:
    path = Path(raw)
    if not path.is_absolute():
        path = REPO / path
    path = path.resolve()
    try:
        path.relative_to(REPO.resolve())
    except ValueError as err:
        raise SystemExit("--progress-file must be inside the workspace") from err
    return path


def _save_progress(path: Path, state: dict[str, Any]) -> None:
    state["updated_at"] = _utc_now()
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(state, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def _summary(items: list[dict[str, Any]], remaining: int) -> dict[str, int]:
    statuses = ("filled", "kept_new", "no_change", "failed", "invalid")
    result = {
        "attempted": len(items),
        **{status: sum(item["status"] == status for item in items) for status in statuses},
        "remaining": remaining,
    }
    return result


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Fill #New cards under one tag with one durable Cursor agent; "
            "each send names a single card. After fill turns, run "
            "/refine-tags and /dedup-tag for that tag, then rebuild the index once."
        )
    )
    parser.add_argument("tag", metavar="TAG")
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help=(
            "Maximum card attempts this run. Default 1, or every remaining "
            "#New card under the tag when --until-tag is set."
        ),
    )
    parser.add_argument(
        "--until-tag",
        action="store_true",
        help="Fill every remaining #New card under the tag, one send per card.",
    )
    parser.add_argument("--model", default="grok-4.6")
    parser.add_argument("--max-retries", type=int, default=2)
    parser.add_argument("--fail-fast", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--progress-file",
        default=str(DEFAULT_PROGRESS.relative_to(REPO)),
    )
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    if args.limit is not None and args.limit < 1:
        raise SystemExit("--limit must be at least 1")
    if args.max_retries < 0:
        raise SystemExit("--max-retries cannot be negative")
    if not TAGS_MD.is_file() or not FILL_SKILL.is_file():
        raise SystemExit("required Tags.md or fill-tag skill is missing")
    refine_skill = REPO / ".cursor" / "skills" / "refine-tags" / "SKILL.md"
    dedup_skill = REPO / ".cursor" / "skills" / "dedup-tag" / "SKILL.md"
    if not refine_skill.is_file() or not dedup_skill.is_file():
        raise SystemExit("required refine-tags or dedup-tag skill is missing")

    tree_paths = parse_tree_paths(TAGS_MD)
    tag = _resolve_tag(args.tag, tree_paths)
    available = _candidate_queue(tag)
    if args.until_tag:
        selected = available if args.limit is None else available[: args.limit]
    else:
        selected = available[: (args.limit if args.limit is not None else 1)]

    print(f"repo={REPO}", flush=True)
    limit_shown = args.limit if args.limit is not None else ("tag" if args.until_tag else 1)
    print(
        f"tag=#{tag} available={len(available)} selected={len(selected)} "
        f"limit={limit_shown} until_tag={str(args.until_tag).lower()}",
        flush=True,
    )
    print("priority=untrusted drafts, then empty stubs", flush=True)
    print(
        "agent=one durable session; one send per card; then refine-tags, "
        "dedup-tag, then one index rebuild",
        flush=True,
    )
    for index, candidate in enumerate(selected, start=1):
        kind = "draft" if candidate.has_draft else "stub"
        print(f"  [{index}/{len(selected)}] {kind}: {candidate.path.name}", flush=True)

    if args.dry_run:
        if sys.platform != "linux":
            print("note: direct host execution is dry-run only", file=sys.stderr)
        print("then /refine-tags, then /dedup-tag, then rebuild coverage index", flush=True)
        return 0

    _require_container_boundary()
    api_key = os.environ.pop("CURSOR_API_KEY", "").strip()
    if not api_key:
        raise SystemExit("set CURSOR_API_KEY (https://cursor.com/dashboard/integrations)")

    progress_path = _resolve_progress_path(args.progress_file)
    state: dict[str, Any] = {
        "version": PROGRESS_VERSION,
        "tag": tag,
        "requested_limit": args.limit,
        "until_tag": args.until_tag,
        "selected": [candidate.path.name for candidate in selected],
        "post": {},
        "agent_id": None,
        "started_at": _utc_now(),
        "updated_at": _utc_now(),
        "items": [],
        "summary": _summary([], len(available)),
    }
    _save_progress(progress_path, state)

    def record_item(
        *,
        index: int,
        candidate: Candidate,
        status: str,
        elapsed: float,
        run_id: str,
        error: str | None,
        report: str,
    ) -> None:
        if report:
            print("    --- agent report ---", flush=True)
            print(report.rstrip(), flush=True)
            print("    --- end report ---", flush=True)
        detail = f" id={run_id}" if run_id else ""
        if error:
            detail += f" error={error}"
        print(
            f"[{index}/{len(selected)}] {status.upper()} "
            f"{elapsed:.1f}s{detail}",
            flush=True,
        )
        state["items"].append(
            {
                "index": index,
                "file": candidate.path.name,
                "cue": candidate.cue,
                "input": "untrusted_draft" if candidate.has_draft else "empty_stub",
                "status": status,
                "duration_seconds": elapsed,
                "run_id": run_id or None,
                "error": error,
            }
        )
        state["summary"] = _summary(state["items"], len(_candidate_queue(tag)))
        _save_progress(progress_path, state)

    fatal = False
    try:
        with _create_agent(
            api_key=api_key,
            model=args.model,
            name=f"fill {tag}",
            max_retries=args.max_retries,
        ) as agent:
            agent_id = str(
                getattr(agent, "agent_id", None) or getattr(agent, "agentId", "") or ""
            )
            state["agent_id"] = agent_id or None
            _save_progress(progress_path, state)
            print(f"agent_id={agent_id or 'unknown'}", flush=True)
            preserve_workspace = False

            for index, candidate in enumerate(selected, start=1):
                started = time.monotonic()
                relative_card = candidate.path.relative_to(VAULT).as_posix()
                print(
                    f"\n[{index}/{len(selected)}] START {candidate.path.name}",
                    flush=True,
                )
                before_cards = _card_snapshot()
                tags_hash = _sha256_text(_read_text(TAGS_MD))
                status = "failed"
                error: str | None = None
                run_id = ""
                report = ""

                try:
                    outcome = _send(
                        agent,
                        _prompt_for(
                            tag,
                            candidate,
                            index=index,
                            total=len(selected),
                            follow_up=index > 1,
                        ),
                        max_retries=args.max_retries,
                    )
                    run_id = outcome.run_id
                    report = outcome.report

                    after_cards = _card_snapshot()
                    changed = _changed_cards(before_cards, after_cards)
                    if _sha256_text(_read_text(TAGS_MD)) != tags_hash:
                        raise WorkspaceViolation("agent modified Tags.md")
                    if any(name != relative_card for name in changed):
                        raise WorkspaceViolation(
                            "agent modified cards outside its assignment: "
                            + ", ".join(
                                name for name in changed if name != relative_card
                            )
                        )
                    if relative_card not in after_cards:
                        raise WorkspaceViolation(
                            "agent removed or renamed the target card"
                        )

                    target_tags = _card_tags(candidate.path)
                    if relative_card not in changed:
                        status = "no_change"
                    elif "New" in target_tags:
                        status = "kept_new"
                    else:
                        problems = _validate_filled_card(candidate.path, tree_paths)
                        if problems:
                            status = "invalid"
                            error = "; ".join(problems)
                            fatal = True
                        else:
                            status = "filled"
                except (
                    AgentRunError,
                    WorkspaceViolation,
                    subprocess.CalledProcessError,
                ) as err:
                    error = str(err)
                    after_cards = _card_snapshot()
                    changed = _changed_cards(before_cards, after_cards)
                    if changed:
                        error += "; workspace changed during failed run: " + ", ".join(
                            changed
                        )
                        fatal = True
                    if isinstance(err, WorkspaceViolation):
                        fatal = True
                        preserve_workspace = True

                record_item(
                    index=index,
                    candidate=candidate,
                    status=status,
                    elapsed=round(time.monotonic() - started, 1),
                    run_id=run_id,
                    error=error,
                    report=report,
                )
                if fatal or (args.fail_fast and status in {"failed", "invalid"}):
                    print(
                        "Stopping early to preserve the workspace for review.",
                        flush=True,
                    )
                    break
            if preserve_workspace:
                print(
                    "Skipping refine-tags, dedup-tag, and index rebuild "
                    "after a workspace violation.",
                    flush=True,
                )
                state["post"]["index"] = "skipped"
                _save_progress(progress_path, state)
            else:
                _run_post_phase(
                    agent,
                    name="refine",
                    skill="refine-tags",
                    command=f"/refine-tags #{tag}",
                    max_retries=args.max_retries,
                    state=state,
                    progress_path=progress_path,
                )
                _run_post_phase(
                    agent,
                    name="dedup",
                    skill="dedup-tag",
                    command=f"/dedup-tag #{tag}",
                    max_retries=args.max_retries,
                    state=state,
                    progress_path=progress_path,
                )
                print(
                    "\nRebuilding coverage index after refine-tags and dedup-tag",
                    flush=True,
                )
                try:
                    _rebuild_index()
                    state["post"]["index"] = "rebuilt"
                except subprocess.CalledProcessError as err:
                    print(f"FAILED to rebuild coverage index: {err}", file=sys.stderr, flush=True)
                    state["post"]["index"] = f"failed: {err}"
                _save_progress(progress_path, state)
    except AgentRunError as err:
        print(f"FAILED to create fill agent: {err}", file=sys.stderr, flush=True)
        state["summary"] = _summary(state["items"], len(_candidate_queue(tag)))
        state["startup_error"] = str(err)
        _save_progress(progress_path, state)
        return 1

    summary = state["summary"]
    print(
        "\nSummary: "
        + " ".join(f"{key}={value}" for key, value in summary.items()),
        flush=True,
    )
    post = state.get("post") or {}
    post_failed = any(
        (post.get(name) or {}).get("status") == "failed" for name in ("refine", "dedup")
    ) or str(post.get("index") or "").startswith("failed")
    return 2 if summary["failed"] or summary["invalid"] or post_failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
