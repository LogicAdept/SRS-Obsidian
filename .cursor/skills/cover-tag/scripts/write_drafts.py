#!/usr/bin/env python3
"""Write #New untrusted-draft or empty-stub SRS cards for /cover-tag.

Do not copy this file into a one-off generator. Import it:

  from write_drafts import write_all

See `_gen_tag.py` for the CARDS shape. Refuses to overwrite existing files.
Appends `- [+] Cue.md` to `SRS/NamesHistory/md-file-names.txt`.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

_PROCESS = Path(__file__).resolve().parents[2] / "process-topic" / "scripts"
if str(_PROCESS) not in sys.path:
    sys.path.insert(0, str(_PROCESS))

from vault_cards import vault_dir  # noqa: E402

META = """<!--
reps: 0
priority: 0
-->
"""

DRAFT = """> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

"""

_FORBIDDEN_IN_NAME = '\\/:*?"<>|'


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


def _check_tags(tags: str) -> None:
    parts = tags.split()
    if "#SRS" not in parts or parts[-1] != "#New":
        raise SystemExit(f"tags must include #SRS and end with #New: {tags!r}")


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


def write_all(cards: list[dict[str, Any]]) -> int:
    """Write a batch of drafts/stubs. Omit `body` (and `traps`) for a stub."""
    if not cards:
        raise SystemExit(
            "CARDS is empty - copy _gen_tag.py to _gen_<slug>.py and fill CARDS"
        )
    vault, _names = _vault_and_names()
    seen: set[str] = set()
    for card in cards:
        name = card["name"]
        _check_name(name)
        _check_tags(card["tags"])
        if name in seen:
            raise SystemExit(f"duplicate in CARDS: {name}")
        seen.add(name)
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
