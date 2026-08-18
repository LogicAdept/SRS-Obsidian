"""Shared SRS card/tag scanning for vault skills (process-topic, refine-tags)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

TREE_BULLET_RE = re.compile(r"^\s*\*\s+`#([^`]+)`")
TAG_TOKEN_RE = re.compile(r"#([A-Za-z][A-Za-z0-9]*(?:/[A-Za-z0-9]+)*)")
SKIP_DIR_NAMES = frozenset({"Format", "NamesHistory", ".obsidian"})


@dataclass(frozen=True)
class Card:
    path: Path
    tags: frozenset[str]
    is_new: bool

    @property
    def cue(self) -> str:
        name = self.path.name
        return name[:-3] if name.lower().endswith(".md") else name


def repo_root_from_script() -> Path:
    # .cursor/skills/process-topic/scripts/this.py → repo root
    return Path(__file__).resolve().parents[4]


def vault_dir(repo: Path | None = None) -> Path:
    root = repo.resolve() if repo else repo_root_from_script()
    return root / "SRS"


def normalize_prefix(raw: str) -> str:
    text = raw.strip().strip("`").strip()
    if text.startswith("#"):
        text = text[1:]
    return text.strip()


def parse_tree_paths(tags_md: Path) -> list[str]:
    """Return Tags.md Tree paths in file order (without leading #)."""
    text = tags_md.read_text(encoding="utf-8")
    in_tree = False
    paths: list[str] = []
    seen: set[str] = set()
    for line in text.splitlines():
        if line.startswith("## Tree"):
            in_tree = True
            continue
        if in_tree and line.startswith("## "):
            break
        if not in_tree:
            continue
        m = TREE_BULLET_RE.match(line)
        if not m:
            continue
        path = m.group(1).strip()
        if path in ("SRS", "New") or path in seen:
            continue
        seen.add(path)
        paths.append(path)
    return paths


def extract_tag_line(text: str) -> str | None:
    """First tag line: starts with # and is not a markdown heading with spaces."""
    in_comment = False
    for raw in text.splitlines():
        line = raw.strip()
        if not in_comment and line.startswith("<!--"):
            if "-->" not in line[4:]:
                in_comment = True
            continue
        if in_comment:
            if "-->" in line:
                in_comment = False
            continue
        if not line:
            continue
        if line.startswith("#") and TAG_TOKEN_RE.search(line):
            heading_prefix = line.split("#SRS")[0].rstrip()
            if " " not in heading_prefix or heading_prefix.startswith("#"):
                if all(part.startswith("#") or not part for part in line.split()):
                    return line
        if not line.startswith("#"):
            return None
    return None


def card_tags(tag_line: str) -> set[str]:
    return {m.group(1) for m in TAG_TOKEN_RE.finditer(tag_line)}


def iter_card_files(cards_root: Path) -> list[Path]:
    files: list[Path] = []
    for path in cards_root.rglob("*.md"):
        rel = path.relative_to(cards_root)
        if any(part in SKIP_DIR_NAMES for part in rel.parts):
            continue
        files.append(path)
    return files


def matches_prefix(tags: set[str] | frozenset[str], prefix: str) -> bool:
    for t in tags:
        if t == prefix or t.startswith(prefix + "/"):
            return True
    return False


def scan_cards(vault: Path) -> tuple[int, list[Card]]:
    """Return (files scanned, cards that had a tag line)."""
    files = iter_card_files(vault)
    cards: list[Card] = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        tag_line = extract_tag_line(text)
        if not tag_line:
            continue
        tags = card_tags(tag_line)
        if not tags:
            continue
        cards.append(Card(path=path, tags=frozenset(tags), is_new="New" in tags))
    return len(files), cards


def rewrite_one_tag(tag: str, old: str, new: str) -> str:
    """Rename old and old/... children to new / new/... . Does not match oldFoo."""
    if tag == old:
        return new
    if tag.startswith(old + "/"):
        return new + tag[len(old) :]
    return tag


def apply_tag_maps(tag: str, mappings: list[tuple[str, str]]) -> str:
    for old, new in mappings:
        tag = rewrite_one_tag(tag, old, new)
    return tag


def drop_parent_child_tags(tags_in_order: list[str]) -> list[str]:
    """If both T and T/child are present, keep the child only."""
    present = set(tags_in_order)
    out: list[str] = []
    seen: set[str] = set()
    for tag in tags_in_order:
        if tag in seen:
            continue
        if any(other != tag and other.startswith(tag + "/") for other in present):
            continue
        seen.add(tag)
        out.append(tag)
    return out


def rebuild_tag_line(tag_line: str, mappings: list[tuple[str, str]]) -> str:
    """Rewrite thematic tags, drop parent+child dupes, keep #SRS then #New last."""
    ordered = [m.group(1) for m in TAG_TOKEN_RE.finditer(tag_line)]
    has_srs = "SRS" in ordered
    has_new = "New" in ordered
    thematic: list[str] = []
    seen: set[str] = set()
    for tag in ordered:
        if tag in ("SRS", "New"):
            continue
        tag = apply_tag_maps(tag, mappings)
        if tag in seen:
            continue
        seen.add(tag)
        thematic.append(tag)
    thematic = drop_parent_child_tags(thematic)
    parts = [f"#{t}" for t in thematic]
    if has_srs:
        parts.append("#SRS")
    if has_new:
        parts.append("#New")
    return " ".join(parts)
