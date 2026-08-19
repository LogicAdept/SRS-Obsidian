#!/usr/bin/env python3
"""Write #New untrusted-draft or empty-stub SRS cards for /cover-tag.

Do not copy this file into a one-off generator. Import it:

  from write_drafts import write_all

See `_gen_tag.py` for the CARDS shape. Refuses to overwrite existing files.
Appends `- [+] Cue.md` to `SRS/NamesHistory/md-file-names.txt`.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

_PROCESS = Path(__file__).resolve().parents[2] / "process-topic" / "scripts"
if str(_PROCESS) not in sys.path:
    sys.path.insert(0, str(_PROCESS))

from vault_cards import node_role, parse_tree_paths, vault_dir  # noqa: E402

META = """<!--
reps: 0
priority: 0
-->
"""

DRAFT = """> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

"""

_FORBIDDEN_IN_NAME = '\\/:*?"<>|'
_SOURCE_META = (
    "according to ",
    "what does the dump ",
    "what does a dump ",
    "what does the source ",
    "what does the interview ",
    "what does the article ",
)
RESULT_VERSION = 1
DIMENSIONS = (
    "definition",
    "mechanism",
    "failure_version_lie",
    "comparison",
    "procedure_operations",
    "missing_definition_gaps",
)


def traps(items: list[str]) -> str:
    lines = "\n".join(f"> - {t}" for t in items)
    return f"""
> [!warning] Unverified traps from the dump
{lines}
"""


def _vault_and_names() -> tuple[Path, Path]:
    vault = vault_dir()
    names = vault / "NamesHistory" / "md-file-names.txt"
    if not names.is_file():
        raise SystemExit(f"missing names file: {names}")
    return vault, names


def _check_name(name: str) -> None:
    if Path(name).name != name or not name.endswith(".md"):
        raise SystemExit(f"name must be a .md basename: {name!r}")
    stem = name[:-3]
    if any(ch in stem for ch in _FORBIDDEN_IN_NAME):
        raise SystemExit(f"illegal character in cue: {name!r}")
    lowered = stem.casefold()
    if any(fragment in lowered for fragment in _SOURCE_META):
        raise SystemExit(f"source-meta cue is not an independent question: {name!r}")


def _check_tags(tags: str) -> None:
    parts = tags.split()
    if "#SRS" not in parts or parts[-1] != "#New":
        raise SystemExit(f"tags must include #SRS and end with #New: {tags!r}")


def _cue_key(name: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", name[:-3].casefold()))


def _append_name(names: Path, name: str) -> None:
    with names.open("a", encoding="utf-8") as f:
        f.write(f"- [+] {name}\n")


def write_stub(name: str, tags: str) -> None:
    """Empty stub: meta + tag line only."""
    _check_name(name)
    _check_tags(tags)
    vault, names = _vault_and_names()
    path = vault / name
    if path.exists():
        raise SystemExit(f"exists: {name}")
    path.write_text(META + tags + "\n", encoding="utf-8")
    _append_name(names, name)
    print(name)


def write(name: str, tags: str, body: str) -> None:
    """Untrusted draft. `body` may already include traps() output."""
    _check_name(name)
    _check_tags(tags)
    vault, names = _vault_and_names()
    path = vault / name
    if path.exists():
        raise SystemExit(f"exists: {name}")
    text = META + tags + "\n\n" + DRAFT + body.strip() + "\n"
    path.write_text(text, encoding="utf-8")
    _append_name(names, name)
    print(name)


def write_all(cards: list[dict[str, Any]], *, allow_empty: bool = False) -> int:
    """Write a batch of drafts/stubs. Omit `body` (and `traps`) for a stub."""
    if not cards and not allow_empty:
        raise SystemExit(
            "CARDS is empty - copy _gen_tag.py to _gen_<slug>.py and fill CARDS"
        )
    vault, _names = _vault_and_names()
    seen: set[str] = set()
    seen_keys: set[str] = set()
    existing_keys = {
        _cue_key(path.name)
        for path in vault.rglob("*.md")
        if path.name.lower().endswith(".md")
    }
    for card in cards:
        name = card["name"]
        _check_name(name)
        _check_tags(card["tags"])
        if name in seen:
            raise SystemExit(f"duplicate in CARDS: {name}")
        key = _cue_key(name)
        if key in existing_keys:
            raise SystemExit(f"normalized duplicate of an existing cue: {name}")
        if key in seen_keys:
            raise SystemExit(f"normalized duplicate in CARDS: {name}")
        seen.add(name)
        seen_keys.add(key)
        if (vault / name).exists():
            raise SystemExit(f"exists: {name}")
    for card in cards:
        name = card["name"]
        tags = card["tags"]
        body = card.get("body")
        trap_items = card.get("traps") or []
        if body is None:
            if trap_items:
                raise SystemExit(f"stub cannot have traps: {name}")
            write_stub(name, tags)
            continue
        text = body
        if trap_items:
            text = text.rstrip() + traps(list(trap_items))
        write(name, tags, text)
    print(f"done ({len(cards)})")
    return len(cards)


def _check_dimensions(dimensions: dict[str, Any]) -> None:
    if set(dimensions) != set(DIMENSIONS):
        raise SystemExit(
            "coverage dimensions must be exactly: " + ", ".join(DIMENSIONS)
        )
    for name, value in dimensions.items():
        if not isinstance(value, dict):
            raise SystemExit(f"dimension {name!r} must be an object")
        if not isinstance(value.get("required"), bool):
            raise SystemExit(f"dimension {name!r} requires boolean required")
        if not isinstance(value.get("satisfied"), bool):
            raise SystemExit(f"dimension {name!r} requires boolean satisfied")
        evidence = value.get("evidence")
        if not isinstance(evidence, list) or not all(
            isinstance(item, str) and item.strip() for item in evidence
        ):
            raise SystemExit(f"dimension {name!r} requires non-empty string evidence")


def _result_path(raw: str | Path) -> Path:
    repo = Path(__file__).resolve().parents[4]
    path = Path(raw)
    if not path.is_absolute():
        path = repo / path
    path = path.resolve()
    try:
        path.relative_to(repo)
    except ValueError as err:
        raise SystemExit("result_file must stay inside the repository") from err
    return path


def write_cover_batch(
    cards: list[dict[str, Any]],
    *,
    result_file: str | Path,
    tag: str,
    limit: int,
    coverage_dimensions: dict[str, Any],
    sources_searched: dict[str, list[str]],
    candidate_search_exhausted: bool,
    budget_hit: bool,
    deferred_candidates: list[str] | None = None,
) -> int:
    """Write cards and then atomically emit the orchestrator's result contract."""
    if not isinstance(limit, int) or isinstance(limit, bool) or limit < 1:
        raise SystemExit("limit must be a positive integer")
    if len(cards) > limit:
        raise SystemExit(f"card batch exceeds limit {limit}")
    if budget_hit != (len(cards) == limit):
        raise SystemExit("budget_hit must be true exactly when the card limit is reached")
    normalized_tag = tag.lstrip("#")
    tags_md = vault_dir(Path(__file__).resolve().parents[4]) / "Format" / "Tags.md"
    if tags_md.is_file() and node_role(normalized_tag, parse_tree_paths(tags_md)) == "parent":
        raise SystemExit(f"cover never writes cards for parent tag {normalized_tag}")
    for card in cards:
        if f"#{normalized_tag}" not in card["tags"].split():
            raise SystemExit(f"card is not assigned to current leaf {normalized_tag}: {card['name']}")
    _check_dimensions(coverage_dimensions)
    if set(sources_searched) != {"interview", "official"}:
        raise SystemExit("sources_searched must contain interview and official")
    for kind, urls in sources_searched.items():
        if not isinstance(urls, list) or not all(
            isinstance(url, str) and url.startswith(("https://", "http://"))
            for url in urls
        ):
            raise SystemExit(f"{kind} sources must be URL strings")
    if not sources_searched["interview"]:
        raise SystemExit("at least one real interview-question source is required")
    if cards and not sources_searched["official"]:
        raise SystemExit("created cards require official-documentation checks")
    if not isinstance(candidate_search_exhausted, bool) or not isinstance(
        budget_hit, bool
    ):
        raise SystemExit("candidate_search_exhausted and budget_hit must be booleans")
    deferred = deferred_candidates or []
    if not all(isinstance(item, str) for item in deferred):
        raise SystemExit("deferred_candidates must be strings")

    count = write_all(cards, allow_empty=True)
    result = {
        "version": RESULT_VERSION,
        "tag": normalized_tag,
        "created_count": count,
        "created_cues": [card["name"][:-3] for card in cards],
        "coverage_dimensions": coverage_dimensions,
        "sources_searched": sources_searched,
        "candidate_search_exhausted": candidate_search_exhausted,
        "budget_hit": budget_hit,
        "deferred_candidates": deferred,
    }
    path = _result_path(result_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)
    print(f"result: {path}")
    return count
