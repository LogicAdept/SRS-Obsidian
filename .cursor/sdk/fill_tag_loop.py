#!/usr/bin/env python3
"""Fill #New cards under a tag with one durable Cursor agent.

The orchestrator warms the durable session, asks the model to cluster remaining
#New cards by shared official docs, then fills one cluster per send. Shape
failures (missing warning, leftover URL, skipped file) get a repair send on
the same agent instead of stopping the tag. --until-tag walks every remaining
cluster until the tag is empty; --one-cluster stops after the first cluster.
Real runs are accepted only inside the hardened Docker workspace created by
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
GOLD_STANDARD = VAULT / "Format" / "GoldStandard.md"
NAMING_MD = VAULT / "Format" / "Naming.md"
FORMAT_MD = VAULT / "Format" / "Format.md"
FILL_PROMPT = VAULT / "Format" / "FillCardPrompt.txt"
FILL_SKILL = REPO / ".cursor" / "skills" / "fill-tag" / "SKILL.md"
REBUILD = SCRIPTS / "rebuild-coverage-index.py"
DEFAULT_PROGRESS = REPO / "fill-progress.json"
CONTAINER_MARKER = "SRS_FILL_ISOLATED_CONTAINER"
CONTAINER_WORKSPACE = Path("/workspace")
SYSTEM_TAGS = frozenset({"SRS", "New"})
PROGRESS_VERSION = 1
SHAPE_REPAIR_CLUSTER = "orchestrator-shape-repair"

DRAFT_MARKERS = (
    "untrusted draft",
    "unverified traps",
    "dump:",
    "непроверен",
)

CONSTRAINTS = """
You are in an isolated disposable clone of the SRS vault.

This is one durable agent session. After warm-up the orchestrator asks you to
cluster the remaining #New cards, then sends one of those clusters per turn.
Finish every listed card in a fill turn before you reply. Do not look ahead to
a later cluster, invent extra cues, or start a card that is not listed.

Hard constraints:
- Read and follow `.cursor/skills/fill-tag/SKILL.md` on fill turns.
- Process every listed target this fill turn; no other cards.
- Invoke fill-tag with `--limit N` matching the listed count. The listed cues
  are an explicit assignment, so do not stop after the first card and do not
  apply the skill's usual cap of 3.
- Use only official/original documentation as evidence.
- Do not create cards, invoke cover-tag, edit Tags.md, or modify a card that
  is not listed this turn.
- Do not spawn subagents.
- Do not commit, checkout, reset, clean, push, or run destructive git commands.
- Do not run rebuild-coverage-index.py; the orchestrator rebuilds the index.
- English only for the cards and the final report.

Session cache:
- After warm-up, do not re-read GoldStandard, Naming, Tags, Format, or the skill
  unless the orchestrator asks.
- Fetch official docs for this cluster's mechanism once. Reuse those pages
  for every card in this turn. Do not WebFetch a URL you already opened.
- Previous cluster pages may not apply to a new cluster.

Chat report override on fill turns (this orchestrator only; not the card file):
- One line per file: FILENAME | CHECKLIST PASS or FAIL.
- DRAFT AUDIT: one line per file (not per ledger item).
- DOCS READ: official URLs only, comma-separated. Repeat URLs you reused.
- Omit LINKS TO VERIFY, TAGS, and long checklist quotes unless FAIL.

Repair turns:
- The orchestrator may send a repair turn listing validator failures.
- Fix only those listed files. Add a real `> [!warning]` pitfall; do not
  restore `#New` to dodge a missing warning.
- URLs belong in the chat DOCS READ line, never in the card body.
""".strip()


@dataclass(frozen=True)
class Candidate:
    path: Path
    cue: str
    has_draft: bool
    cluster: str


@dataclass(frozen=True)
class AgentOutcome:
    run_id: str
    report: str


class AgentRunError(RuntimeError):
    """A Cursor SDK run failed to reach the finished state."""


class WorkspaceViolation(RuntimeError):
    """An agent changed files outside its assigned cluster."""


class ClusterPlanError(RuntimeError):
    """The clustering turn did not return a usable partition of the queue."""


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
        thematic = set(card.tags) - SYSTEM_TAGS
        if not any(path_in_prefix(card_tag, tag) for card_tag in thematic):
            continue
        text = _read_text(card.path)
        candidates.append(
            Candidate(
                path=card.path,
                cue=card.cue,
                has_draft=_has_untrusted_draft(text),
                cluster="",
            )
        )
    candidates.sort(key=lambda item: (not item.has_draft, item.cue.casefold()))
    return candidates


def _filled_sibling(tag: str) -> Path | None:
    _scanned, cards = scan_cards(VAULT)
    for card in cards:
        if card.is_new:
            continue
        thematic = set(card.tags) - SYSTEM_TAGS
        if any(path_in_prefix(card_tag, tag) for card_tag in thematic):
            return card.path
    return None


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


def _warmup_prompt(tag: str, sibling: Path | None) -> str:
    reads = [
        ".cursor/skills/fill-tag/SKILL.md",
        "SRS/Format/GoldStandard.md",
        "SRS/Format/Naming.md",
        "SRS/Format/Tags.md",
        "SRS/Format/Format.md",
        "SRS/Format/FillCardPrompt.txt (sections C, E, F, G, H only)",
    ]
    if sibling is not None:
        reads.append(
            sibling.relative_to(REPO).as_posix() + " (filled sibling, density only)"
        )
    listed = "\n".join(f"- `{path}`" for path in reads)
    return (
        f"{CONSTRAINTS}\n\n"
        "This is a warm-up turn. Do not fill any card, do not edit any vault "
        "card, and do not edit Tags.md.\n\n"
        f"Tag for this run: #{tag}\n\n"
        "Read now (do not restate them at length):\n"
        f"{listed}\n\n"
        "Reply with exactly: WARMUP_OK\n"
    )


def _cluster_prompt(tag: str, cards: list[Candidate]) -> str:
    lines: list[str] = []
    for offset, card in enumerate(cards, start=1):
        relative = card.path.relative_to(REPO).as_posix()
        kind = "untrusted_draft" if card.has_draft else "empty_stub"
        lines.append(
            f"{offset}. {card.path.name} | {json.dumps(card.cue, ensure_ascii=False)} "
            f"| {kind} | {relative}"
        )
    listed = "\n".join(lines)
    return (
        "Same durable session. Warm-up is done. This is a clustering turn, not a "
        "fill turn. Do not fill any card, do not edit any vault card, and do not "
        "edit Tags.md. Do not WebSearch or WebFetch.\n\n"
        f"Partition every listed #New card under #{tag} into tight clusters.\n"
        "A cluster is a set of cards that share the same official documentation "
        "pages (same mechanism, annotation family, or spec section). "
        "Prefer multi-card clusters. Use a singleton only when no other listed "
        "card shares that mechanism. Do not put the whole tag in one cluster. "
        "Do not invent files. Each listed file must appear in exactly one cluster.\n\n"
        f"Cards ({len(cards)}):\n{listed}\n\n"
        "Reply with JSON only, no markdown fences, no prose:\n"
        '{"clusters":[{"label":"short mechanism name","files":["Exact.md"]}]}'
    )


def _extract_json(report: str) -> Any:
    text = report.strip()
    fenced = re.search(
        r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL | re.IGNORECASE
    )
    if fenced:
        text = fenced.group(1).strip()
    decoder = json.JSONDecoder()
    for index, char in enumerate(text):
        if char not in "{[":
            continue
        try:
            value, _end = decoder.raw_decode(text[index:])
            return value
        except json.JSONDecodeError:
            continue
    raise ClusterPlanError("no JSON object in clustering report")


def _lookup_card(raw: str, available: list[Candidate]) -> Candidate | None:
    token = str(raw).strip().strip("`").replace("\\", "/")
    name = Path(token).name
    for card in available:
        relative_repo = card.path.relative_to(REPO).as_posix()
        relative_vault = card.path.relative_to(VAULT).as_posix()
        if card.path.name == name or relative_repo == token or relative_vault == token:
            return card
        if card.cue == token:
            return card
    return None


def _parse_cluster_plan(
    report: str, available: list[Candidate]
) -> list[list[Candidate]]:
    payload = _extract_json(report)
    if isinstance(payload, dict):
        raw_clusters = payload.get("clusters")
    else:
        raw_clusters = payload
    if not isinstance(raw_clusters, list) or not raw_clusters:
        raise ClusterPlanError("clustering JSON must contain a non-empty clusters list")

    seen: set[str] = set()
    batches: list[list[Candidate]] = []
    for offset, item in enumerate(raw_clusters, start=1):
        if not isinstance(item, dict):
            raise ClusterPlanError(f"cluster {offset} is not an object")
        label = str(item.get("label") or "").strip() or f"cluster-{offset}"
        files = item.get("files") or item.get("cards") or []
        if not isinstance(files, list) or not files:
            raise ClusterPlanError(f"cluster {label!r} has no files")
        group: list[Candidate] = []
        for name in files:
            card = _lookup_card(name, available)
            if card is None:
                raise ClusterPlanError(f"clustering named unknown file: {name}")
            if card.path.name in seen:
                raise ClusterPlanError(
                    f"clustering listed {card.path.name} more than once"
                )
            seen.add(card.path.name)
            group.append(
                Candidate(
                    path=card.path,
                    cue=card.cue,
                    has_draft=card.has_draft,
                    cluster=label,
                )
            )
        batches.append(group)
    missing = [card.path.name for card in available if card.path.name not in seen]
    if missing:
        raise ClusterPlanError(
            "clustering omitted files: " + ", ".join(missing)
        )
    return batches


def _cluster_retry_prompt(err: ClusterPlanError, cards: list[Candidate]) -> str:
    names = "\n".join(f"- {card.path.name}" for card in cards)
    return (
        "Same durable session. Clustering JSON was unusable: "
        f"{err}. Do not fill cards. Reply with JSON only.\n\n"
        "Put every listed file in exactly one cluster:\n"
        f"{names}\n"
    )


def _prompt_for(tag: str, cards: list[Candidate], *, index: int, total: int) -> str:
    label = cards[0].cluster
    lines: list[str] = []
    for offset, card in enumerate(cards, start=1):
        relative = card.path.relative_to(REPO).as_posix()
        kind = "untrusted_draft" if card.has_draft else "empty_stub"
        lines.append(
            f"{offset}. `{relative}` "
            f"(cue: {json.dumps(card.cue, ensure_ascii=False)}; {kind})"
        )
    listed = "\n".join(lines)
    count = len(cards)
    return (
        "Same durable session and the same hard constraints. "
        "Warm-up and clustering are done. Previous clusters are finished.\n\n"
        f"Turn {index}/{total}. Fill this entire tight cluster in this one turn. "
        "Fetch official docs for this mechanism once, then write every listed card "
        "before you reply. Do not stop after the first card. Do not pick any other "
        "#New card from a tag scan.\n\n"
        f"Cluster `{label}` ({count} cards):\n{listed}\n\n"
        "These cues are named explicitly, so the skill's default --limit 1 and the "
        "usual cap of 3 do not apply.\n\n"
        f"Invoke now:\n/fill-tag #{tag} --limit {count}\n"
    )


def _repair_prompt(
    tag: str,
    cards: list[Candidate],
    problems: dict[str, str],
    *,
    attempt: int,
    max_repairs: int,
) -> str:
    lines: list[str] = []
    for offset, card in enumerate(cards, start=1):
        relative = card.path.relative_to(REPO).as_posix()
        issue = problems.get(card.path.name, "GoldStandard shape failed")
        lines.append(f"{offset}. `{relative}` — {issue}")
    listed = "\n".join(lines)
    count = len(cards)
    return (
        "Same durable session and the same hard constraints. "
        "This is a repair turn, not a new cluster.\n\n"
        f"Repair {attempt}/{max_repairs}. The orchestrator validator rejected "
        "these files after the fill turn. Patch the listed shape failures in "
        "place. Do not restore #New to dodge a missing warning. Do not touch "
        "any other card.\n\n"
        "Required GoldStandard shape (all of these):\n"
        "- `> [!abstract] Short answer`\n"
        "- at least one `> [!warning]` pitfall (a real trap, not a heading)\n"
        "- `> [!tip] Interview answer`\n"
        "- at least two `[[wikilinks]]`\n"
        "- no URLs in the .md (put them in DOCS READ in chat)\n"
        "- no footnotes, no NOTES/SOURCES/REFERENCES in the file\n"
        "- no untrusted-draft residue\n\n"
        f"Rejected files ({count}):\n{listed}\n\n"
        "Reuse official docs already fetched for this cluster. Fetch again "
        "only if you need a pitfall you did not already read.\n\n"
        f"Invoke now:\n/fill-tag #{tag} --limit {count}\n"
    )


def _print_agent_report(report: str) -> None:
    if not report.strip():
        return
    print("    --- agent report ---", flush=True)
    print(report.rstrip(), flush=True)
    print("    --- end report ---", flush=True)


def _assert_assigned_edits(
    *,
    assigned: set[str],
    before_cards: dict[str, str],
    tags_hash: str,
) -> list[str]:
    after_cards = _card_snapshot()
    changed = _changed_cards(before_cards, after_cards)
    if _sha256_text(_read_text(TAGS_MD)) != tags_hash:
        raise WorkspaceViolation("agent modified Tags.md")
    extra = [name for name in changed if name not in assigned]
    if extra:
        raise WorkspaceViolation(
            "agent modified cards outside its assignment: " + ", ".join(extra)
        )
    missing = [name for name in assigned if name not in after_cards]
    if missing:
        raise WorkspaceViolation(
            "agent removed or renamed target cards: " + ", ".join(missing)
        )
    return changed


def _evaluate_cards(
    cards: list[Candidate],
    changed: list[str],
    tree_paths: list[str],
    *,
    previous: dict[str, tuple[str, str | None]] | None = None,
) -> list[tuple[Candidate, str, str | None]]:
    out: list[tuple[Candidate, str, str | None]] = []
    for card in cards:
        relative = card.path.relative_to(VAULT).as_posix()
        status, error = _card_fill_status(card, relative, changed, tree_paths)
        if previous is not None and status == "no_change":
            prev_status, prev_error = previous[card.path.name]
            out.append((card, prev_status, prev_error))
            continue
        out.append((card, status, error))
    return out


def _repair_targets(
    per_card: list[tuple[Candidate, str, str | None]],
) -> list[tuple[Candidate, str]]:
    targets: list[tuple[Candidate, str]] = []
    for card, status, error in per_card:
        if status == "invalid":
            targets.append((card, error or "GoldStandard shape failed"))
        elif status == "no_change":
            targets.append((card, "listed card was not modified this turn"))
    return targets


def _evaluate_from_disk(
    cards: list[Candidate],
    tree_paths: list[str],
) -> list[tuple[Candidate, str, str | None]]:
    out: list[tuple[Candidate, str, str | None]] = []
    for card in cards:
        if "New" in _card_tags(card.path):
            out.append((card, "kept_new", None))
            continue
        problems = _validate_filled_card(card.path, tree_paths)
        if problems:
            out.append((card, "invalid", "; ".join(problems)))
        else:
            out.append((card, "filled", None))
    return out


def _invalid_from_progress(
    progress_path: Path,
    tag: str,
    tree_paths: list[str],
) -> list[Candidate]:
    if not progress_path.is_file():
        return []
    try:
        data = json.loads(_read_text(progress_path))
    except json.JSONDecodeError:
        return []
    if data.get("tag") != tag:
        return []
    found: list[Candidate] = []
    seen: set[str] = set()
    for item in data.get("items", []):
        if item.get("status") != "invalid":
            continue
        name = str(item.get("file") or "").strip()
        if not name or name in seen:
            continue
        path = VAULT / name
        if not path.is_file():
            continue
        if "New" in _card_tags(path):
            continue
        problems = _validate_filled_card(path, tree_paths)
        if not problems:
            continue
        seen.add(name)
        found.append(
            Candidate(
                path=path,
                cue=str(item.get("cue") or path.stem),
                has_draft=_has_untrusted_draft(_read_text(path)),
                cluster=SHAPE_REPAIR_CLUSTER,
            )
        )
    return found


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


def _select_clusters(
    groups: list[list[Candidate]],
    *,
    until_tag: bool,
    one_cluster: bool,
    limit: int | None,
) -> list[list[Candidate]]:
    if not groups:
        return []
    if until_tag and one_cluster:
        raise SystemExit("use either --until-tag or --one-cluster, not both")
    if one_cluster:
        return groups[:1]
    if until_tag:
        if limit is not None:
            return groups[:limit]
        return groups
    return groups[: (limit if limit is not None else 1)]


def _card_fill_status(
    card: Candidate,
    relative: str,
    changed: list[str],
    tree_paths: list[str],
) -> tuple[str, str | None]:
    if relative not in changed:
        return "no_change", None
    if "New" in _card_tags(card.path):
        return "kept_new", None
    problems = _validate_filled_card(card.path, tree_paths)
    if problems:
        return "invalid", "; ".join(problems)
    return "filled", None


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Fill #New cards under one tag with one durable Cursor agent; "
            "the model clusters remaining cards, then one cluster is filled per send."
        )
    )
    parser.add_argument("tag", metavar="TAG")
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help=(
            "Maximum clusters this run. Default 1, or every remaining cluster "
            "under the tag when --until-tag is set."
        ),
    )
    parser.add_argument(
        "--until-tag",
        action="store_true",
        help=(
            "Walk every model cluster under the tag until no #New remain "
            "(one send fills the whole current cluster, then the next cluster)."
        ),
    )
    parser.add_argument(
        "--one-cluster",
        action="store_true",
        help="Fill only the first model cluster, then stop.",
    )
    parser.add_argument("--model", default="grok-4.6")
    parser.add_argument("--max-retries", type=int, default=2)
    parser.add_argument(
        "--max-repairs",
        type=int,
        default=2,
        help=(
            "Repair sends per cluster after shape validation fails "
            "(missing warning, leftover URL, skipped file). Default 2. "
            "The run continues to the next cluster unless --fail-fast."
        ),
    )
    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="Stop after a cluster that is still failed/invalid after repairs.",
    )
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
    if args.max_repairs < 0:
        raise SystemExit("--max-repairs cannot be negative")
    required = (
        TAGS_MD,
        GOLD_STANDARD,
        NAMING_MD,
        FORMAT_MD,
        FILL_PROMPT,
        FILL_SKILL,
    )
    missing = [path.name for path in required if not path.is_file()]
    if missing:
        raise SystemExit("required fill files missing: " + ", ".join(missing))

    tree_paths = parse_tree_paths(TAGS_MD)
    tag = _resolve_tag(args.tag, tree_paths)
    available = _candidate_queue(tag)
    if args.until_tag and args.one_cluster:
        raise SystemExit("use either --until-tag or --one-cluster, not both")

    print(f"repo={REPO}", flush=True)
    if args.until_tag:
        limit_shown = args.limit if args.limit is not None else "tag"
    elif args.one_cluster:
        limit_shown = "cluster"
    else:
        limit_shown = args.limit if args.limit is not None else 1
    print(
        f"tag=#{tag} available={len(available)} "
        f"limit={limit_shown} until_tag={str(args.until_tag).lower()} "
        f"one_cluster={str(args.one_cluster).lower()}",
        flush=True,
    )
    print("clustering=model (shared official docs), then one cluster per send", flush=True)
    print(
        f"repairs=up to {args.max_repairs} shape-fix sends per cluster "
        "(missing warning, leftover URL, skipped file)",
        flush=True,
    )
    print("index=rebuild once at end of run", flush=True)
    for card in available:
        kind = "draft" if card.has_draft else "stub"
        print(f"  {kind}: {card.path.name}", flush=True)

    if args.dry_run:
        if sys.platform != "linux":
            print("note: direct host execution is dry-run only", file=sys.stderr)
        return 0

    _require_container_boundary()
    api_key = os.environ.pop("CURSOR_API_KEY", "").strip()
    if not api_key:
        raise SystemExit("set CURSOR_API_KEY (https://cursor.com/dashboard/integrations)")

    progress_path = _resolve_progress_path(args.progress_file)
    leftover_invalid = _invalid_from_progress(progress_path, tag, tree_paths)
    if leftover_invalid:
        print(
            f"leftover_invalid={len(leftover_invalid)} from prior progress "
            "(will repair before new clusters)",
            flush=True,
        )
        for card in leftover_invalid:
            print(f"  invalid: {card.path.name}", flush=True)
    if not available and not leftover_invalid:
        return 0
    state: dict[str, Any] = {
        "version": PROGRESS_VERSION,
        "tag": tag,
        "requested_limit": args.limit,
        "until_tag": args.until_tag,
        "one_cluster": args.one_cluster,
        "max_repairs": args.max_repairs,
        "clustering": "pending",
        "clusters": 0,
        "selected": [card.path.name for card in available],
        "selected_clusters": [],
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
        print_report: bool = False,
        repair_attempts: int = 0,
    ) -> None:
        if print_report and report:
            _print_agent_report(report)
        detail = f" id={run_id}" if run_id else ""
        if repair_attempts:
            detail += f" repairs={repair_attempts}"
        if error:
            detail += f" error={error}"
        print(
            f"    {status.upper()} {candidate.path.name} {elapsed:.1f}s{detail}",
            flush=True,
        )
        state["items"].append(
            {
                "index": index,
                "file": candidate.path.name,
                "cue": candidate.cue,
                "cluster": candidate.cluster,
                "input": "untrusted_draft" if candidate.has_draft else "empty_stub",
                "status": status,
                "duration_seconds": elapsed,
                "run_id": run_id or None,
                "repair_attempts": repair_attempts,
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

            sibling = _filled_sibling(tag)
            warmup_before = _card_snapshot()
            warmup_tags = _sha256_text(_read_text(TAGS_MD))
            print("\n[warmup] START read format + skill", flush=True)
            try:
                warmup = _send(
                    agent,
                    _warmup_prompt(tag, sibling),
                    max_retries=args.max_retries,
                )
                if _sha256_text(_read_text(TAGS_MD)) != warmup_tags:
                    raise WorkspaceViolation("warm-up modified Tags.md")
                warmup_changed = _changed_cards(warmup_before, _card_snapshot())
                if warmup_changed:
                    raise WorkspaceViolation(
                        "warm-up modified cards: " + ", ".join(warmup_changed)
                    )
            except (AgentRunError, WorkspaceViolation) as err:
                print(f"FAILED warmup: {err}", file=sys.stderr, flush=True)
                state["startup_error"] = f"warmup: {err}"
                _save_progress(progress_path, state)
                return 1
            print(
                f"[warmup] OK id={warmup.run_id or 'unknown'}",
                flush=True,
            )
            if warmup.report.strip():
                print(warmup.report.rstrip(), flush=True)

            planned: list[list[Candidate]] = []
            clustered_id = "skipped"
            clustered_report = ""
            if available:
                print("\n[cluster] START model partition", flush=True)
                cluster_before = _card_snapshot()
                cluster_tags = _sha256_text(_read_text(TAGS_MD))
                try:
                    clustered = _send(
                        agent,
                        _cluster_prompt(tag, available),
                        max_retries=args.max_retries,
                    )
                    if _sha256_text(_read_text(TAGS_MD)) != cluster_tags:
                        raise WorkspaceViolation("clustering modified Tags.md")
                    cluster_changed = _changed_cards(cluster_before, _card_snapshot())
                    if cluster_changed:
                        raise WorkspaceViolation(
                            "clustering modified cards: " + ", ".join(cluster_changed)
                        )
                    try:
                        planned = _parse_cluster_plan(clustered.report, available)
                    except ClusterPlanError as err:
                        print(f"[cluster] retry: {err}", flush=True)
                        clustered = _send(
                            agent,
                            _cluster_retry_prompt(err, available),
                            max_retries=args.max_retries,
                        )
                        if _sha256_text(_read_text(TAGS_MD)) != cluster_tags:
                            raise WorkspaceViolation("clustering retry modified Tags.md")
                        cluster_changed = _changed_cards(cluster_before, _card_snapshot())
                        if cluster_changed:
                            raise WorkspaceViolation(
                                "clustering retry modified cards: "
                                + ", ".join(cluster_changed)
                            )
                        planned = _parse_cluster_plan(clustered.report, available)
                except (
                    AgentRunError,
                    WorkspaceViolation,
                    ClusterPlanError,
                ) as err:
                    print(f"FAILED clustering: {err}", file=sys.stderr, flush=True)
                    state["startup_error"] = f"clustering: {err}"
                    state["clustering"] = "failed"
                    _save_progress(progress_path, state)
                    return 1
                clustered_id = clustered.run_id or "unknown"
                clustered_report = clustered.report
            else:
                print("\n[cluster] SKIP no remaining #New", flush=True)

            batches = _select_clusters(
                planned,
                until_tag=args.until_tag,
                one_cluster=args.one_cluster,
                limit=args.limit,
            )
            if leftover_invalid:
                if args.one_cluster:
                    batches = [leftover_invalid]
                else:
                    batches = [leftover_invalid] + batches
            state["clustering"] = "ok" if available else "skipped"
            state["clusters"] = len(batches)
            state["selected"] = [card.path.name for batch in batches for card in batch]
            state["selected_clusters"] = [
                {
                    "label": batch[0].cluster,
                    "files": [card.path.name for card in batch],
                }
                for batch in batches
            ]
            _save_progress(progress_path, state)
            print(
                f"[cluster] OK id={clustered_id} "
                f"clusters={len(planned)} selected={len(batches)}",
                flush=True,
            )
            if clustered_report.strip():
                print("    --- cluster report ---", flush=True)
                print(clustered_report.rstrip(), flush=True)
                print("    --- end report ---", flush=True)
            for index, cards in enumerate(batches, start=1):
                print(
                    f"  [{index}/{len(batches)}] cluster={cards[0].cluster} "
                    f"cards={len(cards)}",
                    flush=True,
                )
                for card in cards:
                    if cards[0].cluster == SHAPE_REPAIR_CLUSTER:
                        kind = "invalid"
                    else:
                        kind = "draft" if card.has_draft else "stub"
                    print(f"      {kind}: {card.path.name}", flush=True)
            if not batches:
                print("No clusters selected after model partition.", flush=True)
                return 0

            index_dirty = False
            card_index = 0
            for index, cards in enumerate(batches, start=1):
                started = time.monotonic()
                label = cards[0].cluster
                assigned = {
                    card.path.relative_to(VAULT).as_posix() for card in cards
                }
                print(
                    f"\n[{index}/{len(batches)}] START cluster={label} "
                    f"cards={len(cards)}",
                    flush=True,
                )
                before_cards = _card_snapshot()
                tags_hash = _sha256_text(_read_text(TAGS_MD))
                run_id = ""
                report = ""
                cluster_error: str | None = None
                per_card: list[tuple[Candidate, str, str | None]] = []
                repair_attempts = 0

                try:
                    if label == SHAPE_REPAIR_CLUSTER:
                        per_card = _evaluate_from_disk(cards, tree_paths)
                    else:
                        outcome = _send(
                            agent,
                            _prompt_for(
                                tag,
                                cards,
                                index=index,
                                total=len(batches),
                            ),
                            max_retries=args.max_retries,
                        )
                        run_id = outcome.run_id
                        report = outcome.report
                        _print_agent_report(report)
                        report = ""

                        changed = _assert_assigned_edits(
                            assigned=assigned,
                            before_cards=before_cards,
                            tags_hash=tags_hash,
                        )
                        if changed:
                            index_dirty = True
                        per_card = _evaluate_cards(cards, changed, tree_paths)

                    targets = _repair_targets(per_card)
                    while targets and repair_attempts < args.max_repairs:
                        repair_attempts += 1
                        repair_cards = [card for card, _reason in targets]
                        problems = {
                            card.path.name: reason for card, reason in targets
                        }
                        print(
                            f"  [repair {repair_attempts}/{args.max_repairs}] "
                            f"START cluster={label} cards={len(repair_cards)}",
                            flush=True,
                        )
                        for card, reason in targets:
                            print(
                                f"      {card.path.name}: {reason}",
                                flush=True,
                            )
                        repair_before = _card_snapshot()
                        repair_tags = _sha256_text(_read_text(TAGS_MD))
                        repair_assigned = {
                            card.path.relative_to(VAULT).as_posix()
                            for card in repair_cards
                        }
                        outcome = _send(
                            agent,
                            _repair_prompt(
                                tag,
                                repair_cards,
                                problems,
                                attempt=repair_attempts,
                                max_repairs=args.max_repairs,
                            ),
                            max_retries=args.max_retries,
                        )
                        run_id = outcome.run_id
                        _print_agent_report(outcome.report)
                        repair_changed = _assert_assigned_edits(
                            assigned=repair_assigned,
                            before_cards=repair_before,
                            tags_hash=repair_tags,
                        )
                        if repair_changed:
                            index_dirty = True
                        previous = {
                            card.path.name: (status, error)
                            for card, status, error in per_card
                        }
                        repaired = _evaluate_cards(
                            repair_cards,
                            repair_changed,
                            tree_paths,
                            previous=previous,
                        )
                        by_name = {
                            card.path.name: (card, status, error)
                            for card, status, error in per_card
                        }
                        for card, status, error in repaired:
                            by_name[card.path.name] = (card, status, error)
                        per_card = [by_name[card.path.name] for card in cards]
                        print(
                            f"  [repair {repair_attempts}/{args.max_repairs}] "
                            f"DONE cluster={label} id={run_id or 'unknown'}",
                            flush=True,
                        )
                        targets = _repair_targets(per_card)

                    leftover = _repair_targets(per_card)
                    if leftover and repair_attempts >= args.max_repairs:
                        suffix = (
                            "stopping (--fail-fast)."
                            if args.fail_fast
                            else "continuing with remaining clusters."
                        )
                        print(
                            "  Repair budget exhausted for this cluster; "
                            + suffix,
                            flush=True,
                        )
                except (
                    AgentRunError,
                    WorkspaceViolation,
                    subprocess.CalledProcessError,
                ) as err:
                    cluster_error = str(err)
                    after_cards = _card_snapshot()
                    changed = _changed_cards(before_cards, after_cards)
                    if changed:
                        cluster_error += (
                            "; workspace changed during failed run: "
                            + ", ".join(changed)
                        )
                        fatal = True
                        index_dirty = True
                    if isinstance(err, WorkspaceViolation):
                        fatal = True
                    if per_card:
                        per_card = [
                            (card, "failed", cluster_error)
                            if status in {"invalid", "no_change"}
                            else (card, status, error)
                            for card, status, error in per_card
                        ]
                    else:
                        per_card = [
                            (card, "failed", cluster_error) for card in cards
                        ]
                    _print_agent_report(report)

                elapsed = round(time.monotonic() - started, 1)
                print(
                    f"[{index}/{len(batches)}] DONE cluster={label} {elapsed:.1f}s "
                    f"id={run_id or 'unknown'}",
                    flush=True,
                )
                cluster_failed = False
                for card, status, error in per_card:
                    card_index += 1
                    record_item(
                        index=card_index,
                        candidate=card,
                        status=status,
                        elapsed=elapsed,
                        run_id=run_id,
                        error=error,
                        report="",
                        repair_attempts=repair_attempts,
                    )
                    if status in {"failed", "invalid"}:
                        cluster_failed = True
                if fatal:
                    print(
                        "Stopping early to preserve the workspace for review.",
                        flush=True,
                    )
                    break
                if args.fail_fast and cluster_failed:
                    print("Stopping early (--fail-fast).", flush=True)
                    break
            if index_dirty:
                print("\nRebuilding coverage index at end of run", flush=True)
                _rebuild_index()
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
    return 2 if summary["failed"] or summary["invalid"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
