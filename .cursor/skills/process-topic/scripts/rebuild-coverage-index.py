#!/usr/bin/env python3
"""Rebuild coverage-index.md (table) and coverage-index.html (colored tree + #New tab).

Counts for each tree path T:
  n        — cards whose tag line has T or a child T/...
  n_new    — subset that also has #New
  n_filled — n - n_new

The HTML also has a **#New** tab: searchable list of unfinished cards with a
Fill button that copies `/fill-tag @SRS/<Cue>.md` for chat.

Do not edit the generated files by hand. Re-run this script after card or Tags.md changes.
"""

from __future__ import annotations

import argparse
import html
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from vault_cards import (
    matches_prefix,
    parse_tree_paths,
    repo_root_from_script,
    scan_cards,
)

Node = dict[str, Any]

NOTES_MARKER = "<!-- process-topic-notes -->"
REBUILD_INDEX_CMD = (
    "python ./.cursor/skills/process-topic/scripts/rebuild-coverage-index.py"
)
COVER_TAG_RE = re.compile(r"[A-Za-z0-9]+(?:/[A-Za-z0-9]+)*")
COVER_TARGET_TAG_RE = re.compile(r'"tag"\s*:\s*"(' + COVER_TAG_RE.pattern + r')"')
FOCUSED_PLAN_RE = re.compile(
    r"^=== focused taxonomy plan for #(" + COVER_TAG_RE.pattern + r") ===",
    re.MULTILINE,
)
COVER_PASS_RE = re.compile(
    r"^=== #(" + COVER_TAG_RE.pattern + r") pass", re.MULTILINE
)


def _normalize_clone_tag(raw: Any) -> str:
    tag = str(raw or "").strip().lstrip("#")
    return tag if COVER_TAG_RE.fullmatch(tag) else ""


def _read_agent_target_tag(meta: Path) -> str:
    """Launched tag from an agent target file."""
    try:
        raw = meta.read_text(encoding="utf-8-sig")
    except OSError:
        return ""
    try:
        tag = _normalize_clone_tag(json.loads(raw).get("tag", ""))
        if tag:
            return tag
    except json.JSONDecodeError:
        pass
    match = COVER_TARGET_TAG_RE.search(raw)
    return _normalize_clone_tag(match.group(1) if match else "")


def _clone_tag(run_dir: Path, kind: str) -> str | None:
    meta = run_dir / f"{kind}-target.json"
    if meta.is_file():
        tag = _read_agent_target_tag(meta)
        if tag:
            return tag
    log = run_dir / f"{kind}-run.log"
    if log.is_file():
        text = log.read_text(encoding="utf-8", errors="replace")
        if kind == "fill":
            match = re.search(
                r"^tag=#(" + COVER_TAG_RE.pattern + r")\b",
                text,
                re.MULTILINE,
            )
        else:
            match = FOCUSED_PLAN_RE.search(text) or COVER_PASS_RE.search(text)
        if match:
            return match.group(1)
    return None


def scan_agent_clones(repo: Path, kind: str) -> dict[str, str]:
    """Newest cover or fill clone directory name per launched tag."""
    if kind not in {"cover", "fill"}:
        raise ValueError(f"unsupported agent kind: {kind}")
    runs = repo / ".cursor" / "sdk" / "runs"
    if not runs.is_dir():
        return {}
    ranked: list[tuple[float, str, str]] = []
    for path in runs.iterdir():
        if not path.is_dir() or not (path / ".git").exists():
            continue
        tag = _clone_tag(path, kind)
        if not tag:
            continue
        ranked.append((path.stat().st_mtime, tag, path.name))
    ranked.sort()
    return {tag: name for _, tag, name in ranked}


def write_agent_clones_js(
    vault: Path,
    cover_clones: dict[str, str],
    fill_clones: dict[str, str],
) -> Path:
    path = vault / "NamesHistory" / "coverage-clones.js"
    path.parent.mkdir(parents=True, exist_ok=True)
    cover_payload = json.dumps(cover_clones, ensure_ascii=False, indent=2)
    fill_payload = json.dumps(fill_clones, ensure_ascii=False, indent=2)
    path.write_text(
        f"window.COVER_CLONES = {cover_payload};\n"
        f"window.FILL_CLONES = {fill_payload};\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def load_preserved_notes(out_path: Path) -> str:
    if not out_path.is_file():
        return ""
    text = out_path.read_text(encoding="utf-8")
    idx = text.find(NOTES_MARKER)
    if idx < 0:
        return ""
    return text[idx:].rstrip() + "\n"


def fill_status(n: int, n_filled: int) -> str:
    """unused | red (0% filled) | yellow (<50%) | green (>=50%)."""
    if n <= 0:
        return "unused"
    ratio = n_filled / n
    if ratio <= 0:
        return "red"
    if ratio < 0.5:
        return "yellow"
    return "green"


def fill_pct(n: int, n_filled: int) -> int:
    if n <= 0:
        return 0
    return round(100 * n_filled / n)


def expand_with_ancestors(tree_paths: list[str]) -> list[str]:
    """Insert missing parent prefixes so HTML can nest Tags.md leaves.

    Tags.md often lists only leaves (``#Java/Spring/Framework/WebSocket``) and
    skips the grouping node (``#Java/Spring/Framework``). Without that parent in
    the node map, ``build_tree`` would promote the leaf to a root.
    """
    seen: set[str] = set()
    out: list[str] = []

    def add(path: str) -> None:
        if path in seen:
            return
        parent, sep, _ = path.rpartition("/")
        if sep:
            add(parent)
        seen.add(path)
        out.append(path)

    for path in tree_paths:
        add(path)
    return out


def build_tree(rows: list[tuple[str, int, int, int]]) -> list[Node]:
    nodes: dict[str, Node] = {}
    order: list[str] = []
    for path, n, n_new, n_filled in rows:
        nodes[path] = {
            "path": path,
            "name": path.rsplit("/", 1)[-1],
            "n": n,
            "n_new": n_new,
            "n_filled": n_filled,
            "children": [],
        }
        order.append(path)
    roots: list[Node] = []
    for path in order:
        parent = path.rsplit("/", 1)[0] if "/" in path else None
        if parent and parent in nodes:
            nodes[parent]["children"].append(nodes[path])
        else:
            roots.append(nodes[path])
    return _sort_nodes_by_n(roots)


def _sort_nodes_by_n(nodes: list[Node]) -> list[Node]:
    """Siblings: more cards first; ties by path."""
    nodes.sort(key=lambda node: (-node["n"], node["path"].lower()))
    for node in nodes:
        _sort_nodes_by_n(node["children"])
    return nodes


def count_statuses(rows: list[tuple[str, int, int, int]]) -> dict[str, int]:
    out = {"unused": 0, "red": 0, "yellow": 0, "green": 0}
    for _path, n, _n_new, n_filled in rows:
        out[fill_status(n, n_filled)] += 1
    return out


def render_index(
    *,
    generated_at: str,
    tree_paths: list[str],
    cards_scanned: int,
    cards_with_tags: int,
    rows: list[tuple[str, int, int, int]],
    notes: str,
) -> str:
    lines = [
        "# Coverage index",
        "",
        "Human view: open **[coverage-index.html](coverage-index.html)** in a browser "
        "(collapsible tree, green / yellow / red by how much of `n` is filled).",
        "",
        "Generated by `.cursor/skills/process-topic/scripts/rebuild-coverage-index.py`. "
        "Do not hand-edit these files. Re-run the script after card or `Tags.md` changes.",
        "",
        f"Generated: {generated_at}",
        f"Tree paths: {len(tree_paths)}. Cards scanned: {cards_scanned}. Cards with a tag line: {cards_with_tags}.",
        "",
        "`n` = cards tagged with this path or a child. `n_new` = subset with `#New`. `n_filled` = `n - n_new`.",
        "",
        "Implied parent paths (a Tags.md leaf whose grouping node has no bullet, "
        "e.g. `Java/Spring/Framework` above `.../WebSocket`) are inserted so the HTML "
        "tree nests. They are counted like any other prefix.",
        "",
        "Row color in the HTML tree: **green** ≥50% filled · **yellow** some filled · **red** cards exist but none filled · **gray** unused (`n=0`).",
        "",
        "Order: siblings (HTML) and this table are sorted by `n` descending. "
        "HTML tabs: **Tags** (tree) and **#New** (unfinished cards; **Fill** copies "
        "`/fill-tag @SRS/<Cue>.md`). "
        "HTML row buttons: **Cover agent** opens General / Focused. **Fill agent** starts "
        "a fill on one durable agent (one #New card per send until the tag is empty). "
        "**Fill clone → Finalize** runs `/refine-tags` and `/dedup-tag` once, then one "
        "index rebuild — not after every tag fill. "
        "Toolbar **Rebuild index** copies "
        f"`{REBUILD_INDEX_CMD}`. "
        "Clone menus appear "
        "only when the corresponding cover or fill clone exists. **…** hides "
        "Process/Cover/Fill/Dedup/Refine chat commands.",
        "",
        "## Counts",
        "",
        "| Tag | n | n_new | n_filled |",
        "| --- | ---: | ---: | ---: |",
    ]
    for path, n, n_new, n_filled in sorted(rows, key=lambda r: (-r[1], r[0].lower())):
        lines.append(f"| `#{path}` | {n} | {n_new} | {n_filled} |")
    lines.append("")
    if notes:
        lines.append(notes if notes.endswith("\n") else notes + "\n")
    return "\n".join(lines)


def _copy_btn(label: str, cmd: str, path: str, extra: str = "") -> str:
    return (
        f'<button type="button" class="copy{extra}" data-cmd="{html.escape(cmd, quote=True)}" '
        f'data-tag="{html.escape(path, quote=True)}" title="{html.escape(cmd, quote=True)}">{label}</button>'
    )


def _menu(summary: str, buttons: str, extra: str, path: str, hidden: bool = False) -> str:
    hide = " hidden" if hidden else ""
    return (
        f'<details class="menu{extra}" data-tag="{html.escape(path, quote=True)}"{hide}>'
        f"<summary>{html.escape(summary)}</summary>"
        f'<div class="menu-list">{buttons}</div>'
        f"</details>"
    )


def _html_node(node: Node, depth: int) -> str:
    n = node["n"]
    n_new = node["n_new"]
    n_filled = node["n_filled"]
    status = fill_status(n, n_filled)
    pct = fill_pct(n, n_filled)
    path = node["path"]
    name = html.escape(node["name"])
    full = html.escape("#" + path)
    kids = node["children"]
    meta = f"{n_filled} / {n} filled · {n_new} new · {pct}%"
    if n == 0:
        meta = "unused"
    bar = f'<span class="bar" title="{html.escape(meta)}"><i style="width:{pct}%"></i></span>'
    tag = "#" + path
    launch = f"./.cursor/sdk/run_cover_vault.ps1 {path}"
    review = f"./.cursor/sdk/switch_review.ps1 -Kind Cover {path}"
    accept = f"./.cursor/sdk/switch_review.ps1 -Kind Cover -Accept {path}"
    drop = f"./.cursor/sdk/switch_review.ps1 -Kind Cover -Drop {path}"
    agent_menu = _menu(
        "Cover agent",
        "".join(
            (
                _copy_btn("General", launch, path),
                _copy_btn("Focused", f"{launch} --focus ''", path, " focused"),
            )
        ),
        " agent-menu",
        path,
    )
    fill_launch = f"./.cursor/sdk/run_fill_tag.ps1 {path}"
    fill_agent_menu = ""
    if n_new:
        fill_agent_menu = _menu(
            "Fill agent",
            "".join(
                (
                    _copy_btn("Start", f"{fill_launch} --until-tag", path),
                )
            ),
            " fill-agent-menu",
            path,
        )
    clone_menu = _menu(
        "Cover clone",
        "".join(
            (
                _copy_btn("Open", review, path),
                _copy_btn("Continue", launch, path, " continue"),
                _copy_btn("Focused", f"{launch} --focus ''", path, " focused"),
                _copy_btn("Accept", accept, path),
                _copy_btn("Drop", drop, path),
            )
        ),
        " clone-menu",
        path,
        hidden=True,
    )
    fill_review = f"./.cursor/sdk/switch_review.ps1 -Kind Fill {path}"
    fill_accept = f"./.cursor/sdk/switch_review.ps1 -Kind Fill -Accept {path}"
    fill_drop = f"./.cursor/sdk/switch_review.ps1 -Kind Fill -Drop {path}"
    fill_clone_menu = _menu(
        "Fill clone",
        "".join(
            (
                _copy_btn("Open", fill_review, path),
                _copy_btn("Log", "", path, " fill-log"),
                _copy_btn("Progress", "", path, " fill-progress"),
                _copy_btn("Continue", "", path, " fill-continue"),
                _copy_btn("Finalize", "", path, " fill-finalize"),
                _copy_btn("Accept", fill_accept, path),
                _copy_btn("Drop", fill_drop, path),
            )
        ),
        " fill-clone-menu",
        path,
        hidden=True,
    )
    chat_menu = _menu(
        "…",
        "".join(
            (
                _copy_btn("Process", f"/process-topic {tag}", path),
                _copy_btn("Cover", f"/cover-tag {tag} --limit 12", path),
                _copy_btn("Fill", f"/fill-tag {tag} --limit 1", path),
                _copy_btn("Dedup", f"/dedup-tag {tag} --dry-run", path),
                _copy_btn("Refine", f"/refine-tags {tag}", path),
            )
        ),
        " chat-menu",
        path,
    )
    cmds = agent_menu + fill_agent_menu + clone_menu + fill_clone_menu + chat_menu
    label = (
        f'<span class="swatch" aria-hidden="true"></span>'
        f'<code class="name" title="{full}">{name}</code>'
        f"{bar}"
        f'<span class="meta">{html.escape(meta)}</span>'
        f'<span class="cmds">{cmds}</span>'
    )
    attrs = (
        f'class="node" data-status="{status}" data-path="{html.escape(path, quote=True)}" '
        f'data-name="{html.escape(node["name"].lower(), quote=True)}" data-depth="{depth}"'
    )
    if not kids:
        return f"<li {attrs}><div class=\"row leaf\">{label}</div></li>"
    open_attr = " open" if depth == 0 else ""
    inner = "".join(_html_node(child, depth + 1) for child in kids)
    return (
        f"<li {attrs}><details{open_attr}>"
        f"<summary class=\"row\">{label}</summary>"
        f"<ul>{inner}</ul>"
        f"</details></li>"
    )


def new_card_rows(cards: list) -> list[dict[str, Any]]:
    """Compact payload for the HTML #New tab (drafts first, then cue)."""
    rows: list[dict[str, Any]] = []
    for card in cards:
        if not card.is_new:
            continue
        thematic = sorted(t for t in card.tags if t not in {"SRS", "New"})
        rows.append(
            {
                "cue": card.cue,
                "tags": thematic,
                "draft": bool(card.has_draft),
            }
        )
    rows.sort(key=lambda r: (not r["draft"], r["cue"].lower()))
    return rows


def render_html(
    *,
    generated_at: str,
    tree_paths: list[str],
    cards_scanned: int,
    cards_with_tags: int,
    rows: list[tuple[str, int, int, int]],
    new_cards: list[dict[str, Any]],
) -> str:
    roots = build_tree(rows)
    tallies = count_statuses(rows)
    body = "".join(_html_node(node, 0) for node in roots)
    new_json = json.dumps(new_cards, ensure_ascii=False).replace("<", "\\u003c")
    n_new_total = len(new_cards)
    n_draft = sum(1 for c in new_cards if c["draft"])
    rebuild_cmd = html.escape(REBUILD_INDEX_CMD, quote=True)
    rebuild_cmd_html = html.escape(REBUILD_INDEX_CMD)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SRS coverage index</title>
<style>
:root {{
  --bg: #111113;
  --panel: #1c1c21;
  --text: #ececf1;
  --muted: #9b9ba8;
  --line: #2e2e36;
  --unused: #3f3f46;
  --unused-text: #a1a1aa;
  --red: #7f1d1d;
  --red-bar: #f87171;
  --yellow: #713f12;
  --yellow-bar: #fbbf24;
  --green: #14532d;
  --green-bar: #4ade80;
  --accent: #818cf8;
}}
@media (prefers-color-scheme: light) {{
  :root {{
    --bg: #f6f6f8;
    --panel: #fff;
    --text: #18181b;
    --muted: #71717a;
    --line: #e4e4e7;
    --unused: #e4e4e7;
    --unused-text: #52525b;
    --red: #fecaca;
    --red-bar: #dc2626;
    --yellow: #fde68a;
    --yellow-bar: #d97706;
    --green: #bbf7d0;
    --green-bar: #16a34a;
    --accent: #4f46e5;
  }}
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0;
  font: 14px/1.45 system-ui, Segoe UI, sans-serif;
  background: var(--bg);
  color: var(--text);
}}
header {{
  position: sticky; top: 0; z-index: 2;
  background: var(--panel);
  border-bottom: 1px solid var(--line);
  padding: 12px 20px 14px;
}}
.toolbar {{ display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }}
input[type="search"] {{
  flex: 1; min-width: 180px;
  background: var(--bg); color: var(--text);
  border: 1px solid var(--line); border-radius: 8px;
  padding: 6px 10px;
}}
button, label.chk {{
  background: var(--bg); color: var(--text);
  border: 1px solid var(--line); border-radius: 8px;
  padding: 6px 10px; cursor: pointer; font: inherit;
}}
label.chk {{ display: inline-flex; align-items: center; gap: 6px; user-select: none; }}
.legend {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px; font-size: 12px; color: var(--muted); }}
.legend b {{ font-weight: 600; color: var(--text); }}
.hints {{
  margin: 8px 0 10px;
  font-size: 12px;
  color: var(--muted);
  max-width: 72rem;
}}
.hints > summary {{
  cursor: pointer;
  list-style: none;
  color: var(--text);
  font-weight: 650;
  user-select: none;
}}
.hints > summary::-webkit-details-marker {{ display: none; }}
.hints > summary::before {{ content: "▸ "; color: var(--muted); }}
.hints[open] > summary::before {{ content: "▾ "; }}
.skills {{
  display: grid;
  grid-template-columns: 5.5rem 1fr;
  gap: 2px 12px;
  margin: 6px 0 0;
  font-size: 12px;
  color: var(--muted);
}}
.skills dt {{ font-weight: 650; color: var(--text); }}
.skills dd {{ margin: 0; }}
.skills code {{ font-size: 11px; }}
.pill {{ display: inline-flex; align-items: center; gap: 6px; }}
.dot {{ width: 10px; height: 10px; border-radius: 3px; display: inline-block; }}
.dot.unused {{ background: var(--unused); }}
.dot.red {{ background: var(--red-bar); }}
.dot.yellow {{ background: var(--yellow-bar); }}
.dot.green {{ background: var(--green-bar); }}
main {{ padding: 12px 16px 40px; }}
ul {{ list-style: none; margin: 0; padding-left: 16px; }}
main > ul {{ padding-left: 0; }}
li.node {{ margin: 3px 0; }}
.row {{
  display: flex; align-items: center; gap: 10px;
  padding: 5px 10px; border-radius: 8px;
}}
summary.row {{ cursor: pointer; list-style: none; }}
summary.row::-webkit-details-marker {{ display: none; }}
summary.row::before {{ content: "▸"; color: var(--muted); width: 1em; flex: none; }}
details[open] > summary.row::before {{ content: "▾"; }}
.leaf {{ padding-left: 26px; }}
li.node[data-status="unused"] > .row,
li.node[data-status="unused"] > details > summary.row {{ background: var(--unused); }}
li.node[data-status="red"] > .row,
li.node[data-status="red"] > details > summary.row {{ background: var(--red); }}
li.node[data-status="yellow"] > .row,
li.node[data-status="yellow"] > details > summary.row {{ background: var(--yellow); }}
li.node[data-status="green"] > .row,
li.node[data-status="green"] > details > summary.row {{ background: var(--green); }}
code.name {{
  font: 13px/1.3 ui-monospace, Consolas, monospace;
  color: var(--text); min-width: 8rem;
}}
.bar {{
  flex: 1; min-width: 48px; max-width: 160px; height: 7px;
  background: var(--line); border-radius: 99px; overflow: hidden;
}}
.bar i {{ display: block; height: 100%; background: var(--accent); }}
li.node[data-status="red"] > .row .bar i,
li.node[data-status="red"] > details > summary .bar i {{ background: var(--red-bar); }}
li.node[data-status="yellow"] > .row .bar i,
li.node[data-status="yellow"] > details > summary .bar i {{ background: var(--yellow-bar); }}
li.node[data-status="green"] > .row .bar i,
li.node[data-status="green"] > details > summary .bar i {{ background: var(--green-bar); }}
li.node[data-status="unused"] > .row .bar i,
li.node[data-status="unused"] > details > summary .bar i {{ width: 0 !important; }}
.meta {{ color: var(--muted); font-size: 12px; white-space: nowrap; }}
.cmds {{ display: flex; flex-wrap: wrap; gap: 4px; flex: none; align-items: center; }}
button.copy {{
  padding: 2px 7px; font-size: 11px; line-height: 1.3;
  background: var(--panel);
}}
button.copy:hover {{ border-color: var(--accent); color: var(--accent); }}
button.copy.copied, button.nav.copied {{ border-color: var(--green-bar); color: var(--green-bar); }}
button.nav,
.menu.agent-menu > summary,
.menu.fill-agent-menu > summary,
.menu.clone-menu > summary,
.menu.fill-clone-menu > summary {{ font-weight: 600; }}
.menu {{ position: relative; display: inline-block; }}
.menu > summary {{
  list-style: none; cursor: pointer; user-select: none;
  padding: 2px 7px; font-size: 11px; line-height: 1.3;
  border: 1px solid var(--line); border-radius: 8px;
  background: var(--panel); color: var(--text);
}}
.menu > summary::-webkit-details-marker {{ display: none; }}
.menu > summary::after {{ content: " ▾"; color: var(--muted); font-weight: 400; }}
.menu[open] > summary {{ border-color: var(--accent); color: var(--accent); }}
.menu[open] > summary::after {{ content: " ▴"; color: var(--accent); }}
.menu-list {{
  position: absolute; right: 0; z-index: 6;
  display: flex; flex-direction: column; gap: 2px;
  margin-top: 4px; padding: 4px; min-width: 7.5rem;
  background: var(--panel); border: 1px solid var(--line); border-radius: 8px;
  box-shadow: 0 8px 24px rgba(0,0,0,.35);
}}
.menu-list .copy {{ width: 100%; text-align: left; }}
.menu.clone-menu[hidden], .menu.fill-clone-menu[hidden] {{ display: none !important; }}
li.node.hidden {{ display: none; }}
.empty-msg {{ display: none; color: var(--muted); padding: 24px; }}
.tabs {{ display: flex; gap: 6px; margin: 10px 0 0; }}
.tab {{
  background: var(--bg); color: var(--muted);
  border: 1px solid var(--line); border-radius: 8px;
  padding: 6px 12px; cursor: pointer; font: inherit; font-weight: 650;
}}
.tab[aria-selected="true"] {{
  color: var(--text); border-color: var(--accent); color: var(--accent);
}}
.panel {{ display: none; }}
.panel.active {{ display: block; }}
.panel-toolbar {{
  display: flex; flex-wrap: wrap; gap: 8px; align-items: center;
  margin-bottom: 10px;
}}
.panel-toolbar .count {{ color: var(--muted); font-size: 12px; }}
#new-list {{ list-style: none; margin: 0; padding: 0; }}
#new-list li {{
  display: flex; flex-wrap: wrap; gap: 8px; align-items: center;
  padding: 8px 10px; border-bottom: 1px solid var(--line);
}}
#new-list .cue {{
  flex: 1; min-width: 12rem;
  font: 13px/1.35 ui-monospace, Consolas, monospace;
}}
#new-list .tags {{ color: var(--muted); font-size: 12px; flex: 1 1 100%; }}
@media (min-width: 900px) {{
  #new-list .tags {{ flex: 1 1 auto; }}
}}
.badge {{
  font-size: 11px; font-weight: 650; padding: 2px 7px; border-radius: 99px;
  border: 1px solid var(--line); color: var(--muted); flex: none;
}}
.badge.draft {{
  border-color: var(--yellow-bar); color: var(--yellow-bar);
}}
.badge.stub {{ opacity: 0.85; }}
</style>
</head>
<body>
<header>
  <details class="hints">
    <summary>Подсказки про теги</summary>
    <dl class="skills">
    <dt>Cover agent</dt>
    <dd><b>General</b> — обычный refine + cover листа или листьев под родителем. <b>Focused</b> — копирует ту же команду с <code>--focus ''</code>; в терминале допишите, какого покрытия не хватает. Агент сопоставит запрос с честным листом (при необходимости создаст его) и покроет именно его. В shell нужен <code>CURSOR_API_KEY</code>.</dd>
    <dt>Fill agent</dt>
    <dd><b>Start</b> — изолированный fill на одном Cursor-агенте. Один ход = одна <code>#New</code> карточка, затем следующая, пока под тегом не кончатся <code>#New</code>. Refine, dedup и индекс сюда не входят. В shell нужен <code>CURSOR_API_KEY</code>.</dd>
    <dt>Cover clone</dt>
    <dd>Меню только у тега с живым агент-клоном. <b>Open</b> — второе окно на клон. <b>Continue</b> — продолжить незавершённое состояние. <b>Focused</b> — шаблон с <code>--focus ''</code> для того же клона, даже если лист уже complete. <b>Accept</b> — cherry-pick в исходный vault и удалить клон. <b>Drop</b> — удалить без переноса.</dd>
    <dt>Fill clone</dt>
    <dd>Управление fill-клоном: <b>Open</b>, просмотр <b>Log</b> / <b>Progress</b>, <b>Continue</b> — оставшиеся <code>#New</code> в том же клоне по одной карточке. <b>Finalize</b> — один раз в конце: <code>/refine-tags</code>, <code>/dedup-tag</code>, затем индекс. <b>Accept</b> или <b>Drop</b>.</dd>
    <dt>Source</dt>
    <dd>Копирует <code>./.cursor/sdk/switch_review.ps1 -Source</code> — вернуться в исходный vault.</dd>
    <dt>Rebuild index</dt>
    <dd>Копирует <code>{rebuild_cmd_html}</code> — пересобрать HTML/MD индекс из текущего vault (вставить в терминал из корня репозитория).</dd>
    <dt>…</dt>
    <dd>Process / Cover / Fill / Dedup / Refine — slash-команды для чата Cursor, не Docker-флоу.</dd>
    <dt>#New</dt>
    <dd>Вкладка со всеми карточками <code>#New</code>. <b>Fill</b> копирует <code>/fill-tag @SRS/&lt;Cue&gt;.md</code> — в чат вставляете конкретный файл. Drafts (untrusted dump) выше stubs. Фильтр ищет по cue и тегам.</dd>
    </dl>
  </details>
  <div class="tabs" role="tablist">
    <button type="button" class="tab" role="tab" id="tab-tags" aria-selected="true" data-panel="panel-tags">Tags</button>
    <button type="button" class="tab" role="tab" id="tab-new" aria-selected="false" data-panel="panel-new">#New ({n_new_total})</button>
  </div>
  <div class="toolbar" id="tags-toolbar">
    <input type="search" id="q" placeholder="Filter tags…" autocomplete="off">
    <button type="button" id="expand">Expand all</button>
    <button type="button" id="collapse">Collapse all</button>
    <button type="button" id="open-source" class="copy nav" data-cmd="./.cursor/sdk/switch_review.ps1 -Source">Source</button>
    <button type="button" id="rebuild-index" class="copy nav" data-cmd="{rebuild_cmd}" title="{rebuild_cmd}">Rebuild index</button>
    <label class="chk"><input type="checkbox" id="hide-unused"> Hide unused</label>
  </div>
  <div class="legend" id="tags-legend">
    <span class="pill"><span class="dot green"></span><b>{tallies["green"]}</b> ≥50% filled</span>
    <span class="pill"><span class="dot yellow"></span><b>{tallies["yellow"]}</b> some filled</span>
    <span class="pill"><span class="dot red"></span><b>{tallies["red"]}</b> cards, 0 filled</span>
    <span class="pill"><span class="dot unused"></span><b>{tallies["unused"]}</b> unused (n=0)</span>
  </div>
</header>
<main>
  <section class="panel active" id="panel-tags" role="tabpanel">
    <p class="empty-msg" id="empty">No tags match.</p>
    <ul>{body}</ul>
  </section>
  <section class="panel" id="panel-new" role="tabpanel" hidden>
    <div class="panel-toolbar">
      <input type="search" id="new-q" placeholder="Filter #New by cue or tag…" autocomplete="off">
      <label class="chk"><input type="checkbox" id="drafts-only"> Drafts only</label>
      <span class="count" id="new-count">{n_draft} drafts · {n_new_total} total</span>
      <button type="button" class="copy nav" data-cmd="{rebuild_cmd}" title="{rebuild_cmd}">Rebuild index</button>
    </div>
    <p class="empty-msg" id="new-empty">No #New cards match.</p>
    <ul id="new-list"></ul>
  </section>
</main>
<script type="application/json" id="new-cards-data">{new_json}</script>
<script src="coverage-clones.js"></script>
<script>
document.querySelectorAll(".clone-menu").forEach((el) => {{
  const id = (window.COVER_CLONES || {{}})[el.dataset.tag];
  el.hidden = !id;
  if (id) {{
    const cmd = "./.cursor/sdk/run_cover_vault.ps1 --workspace .cursor/sdk/runs/" + id + " " + el.dataset.tag;
    const cont = el.querySelector("button.continue");
    if (cont) {{
      cont.dataset.cmd = cmd;
      cont.title = cmd;
    }}
    const focused = el.querySelector("button.focused");
    if (focused) {{
      const fcmd = cmd + " --focus ''";
      focused.dataset.cmd = fcmd;
      focused.title = fcmd;
    }}
  }}
}});
document.querySelectorAll(".fill-clone-menu").forEach((el) => {{
  const id = (window.FILL_CLONES || {{}})[el.dataset.tag];
  el.hidden = !id;
  if (!id) return;
  const workspace = ".cursor/sdk/runs/" + id;
  const base = "./.cursor/sdk/run_fill_tag.ps1 " + el.dataset.tag +
    " --workspace " + workspace;
  const cont = el.querySelector("button.fill-continue");
  if (cont) {{
    const cmd = base + " --until-tag";
    cont.dataset.cmd = cmd;
    cont.title = cmd;
  }}
  const fin = el.querySelector("button.fill-finalize");
  if (fin) {{
    const cmd = base + " --finalize";
    fin.dataset.cmd = cmd;
    fin.title = cmd;
  }}
  const log = el.querySelector("button.fill-log");
  if (log) {{
    const cmd = 'Get-Content "' + workspace + '/fill-run.log" -Wait';
    log.dataset.cmd = cmd;
    log.title = cmd;
  }}
  const progress = el.querySelector("button.fill-progress");
  if (progress) {{
    const cmd = 'Get-Content "' + workspace + '/fill-progress.json"';
    progress.dataset.cmd = cmd;
    progress.title = cmd;
  }}
}});
document.querySelectorAll(".menu").forEach((menu) => {{
  menu.addEventListener("click", (e) => e.stopPropagation());
  menu.addEventListener("toggle", () => {{
    if (!menu.open) return;
    document.querySelectorAll(".menu").forEach((other) => {{
      if (other !== menu) other.open = false;
    }});
  }});
}});
const nodes = [...document.querySelectorAll("li.node")];
const empty = document.getElementById("empty");
function applyFilter() {{
  const q = document.getElementById("q").value.trim().toLowerCase();
  const hideUnused = document.getElementById("hide-unused").checked;
  for (const li of nodes) {{
    const unused = li.dataset.status === "unused";
    const textMatch = !q || li.dataset.path.toLowerCase().includes(q) || li.dataset.name.includes(q);
    li.dataset.match = (textMatch && !(hideUnused && unused)) ? "1" : "0";
  }}
  if (q) {{
    for (const li of nodes) {{
      if (li.dataset.match !== "1") continue;
      let p = li.parentElement;
      while (p) {{
        if (p.matches && p.matches("li.node")) p.dataset.match = "1";
        p = p.parentElement;
      }}
    }}
  }}
  let shown = 0;
  for (const li of nodes) {{
    const hide = li.dataset.match !== "1";
    li.classList.toggle("hidden", hide);
    if (!hide) shown++;
  }}
  if (q) {{
    for (const li of nodes) {{
      if (li.classList.contains("hidden")) continue;
      const d = li.querySelector(":scope > details");
      if (d) d.open = true;
    }}
  }}
  empty.style.display = shown ? "none" : "block";
}}
document.getElementById("q").addEventListener("input", applyFilter);
document.getElementById("hide-unused").addEventListener("change", applyFilter);
document.getElementById("expand").addEventListener("click", () => {{
  document.querySelectorAll("li.node > details").forEach((d) => d.open = true);
}});
document.getElementById("collapse").addEventListener("click", () => {{
  document.querySelectorAll("li.node > details").forEach((d) => d.open = false);
}});
async function copyCmd(cmd) {{
  try {{
    await navigator.clipboard.writeText(cmd);
    return true;
  }} catch (e) {{
    const ta = document.createElement("textarea");
    ta.value = cmd;
    ta.setAttribute("readonly", "");
    ta.style.position = "fixed";
    ta.style.left = "-9999px";
    document.body.appendChild(ta);
    ta.select();
    const ok = document.execCommand("copy");
    ta.remove();
    return ok;
  }}
}}
document.querySelectorAll("header, main").forEach((root) => {{
  root.addEventListener("click", async (e) => {{
    const btn = e.target.closest("button.copy");
    if (!btn) return;
    e.preventDefault();
    e.stopPropagation();
    const cmd = btn.dataset.cmd;
    if (!cmd) return;
    const prev = btn.textContent;
    const ok = await copyCmd(cmd);
    btn.textContent = ok ? "Copied" : "Failed";
    btn.classList.toggle("copied", ok);
    setTimeout(() => {{
      btn.textContent = prev;
      btn.classList.remove("copied");
    }}, 1600);
  }}, true);
}});

const PAGE = 150;
const newData = JSON.parse(document.getElementById("new-cards-data").textContent || "[]");
const newList = document.getElementById("new-list");
const newEmpty = document.getElementById("new-empty");
const newCount = document.getElementById("new-count");
let newRendered = 0;
let newFiltered = [];

function fillCmd(cue) {{
  return "/fill-tag @SRS/" + cue + ".md";
}}

function renderNewPage(reset) {{
  if (reset) {{
    newList.innerHTML = "";
    newRendered = 0;
  }}
  const slice = newFiltered.slice(newRendered, newRendered + PAGE);
  for (const row of slice) {{
    const li = document.createElement("li");
    const badge = document.createElement("span");
    badge.className = "badge " + (row.draft ? "draft" : "stub");
    badge.textContent = row.draft ? "draft" : "stub";
    const cue = document.createElement("code");
    cue.className = "cue";
    cue.textContent = row.cue;
    const tags = document.createElement("span");
    tags.className = "tags";
    tags.textContent = (row.tags || []).map((t) => "#" + t).join(" ");
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "copy";
    btn.textContent = "Fill";
    btn.dataset.cmd = fillCmd(row.cue);
    btn.title = btn.dataset.cmd;
    li.append(badge, cue, btn, tags);
    newList.appendChild(li);
  }}
  newRendered += slice.length;
  const more = newFiltered.length - newRendered;
  let moreBtn = document.getElementById("new-more");
  if (more > 0) {{
    if (!moreBtn) {{
      moreBtn = document.createElement("button");
      moreBtn.type = "button";
      moreBtn.id = "new-more";
      moreBtn.textContent = "Load more";
      moreBtn.addEventListener("click", () => renderNewPage(false));
      newList.after(moreBtn);
    }}
    moreBtn.style.display = "";
    moreBtn.textContent = "Load more (" + more + " left)";
  }} else if (moreBtn) {{
    moreBtn.style.display = "none";
  }}
  newEmpty.style.display = newFiltered.length ? "none" : "block";
  newCount.textContent =
    newFiltered.length + " shown of " + newData.length +
    " · " + newData.filter((r) => r.draft).length + " drafts";
}}

function applyNewFilter() {{
  const q = document.getElementById("new-q").value.trim().toLowerCase();
  const draftsOnly = document.getElementById("drafts-only").checked;
  newFiltered = newData.filter((row) => {{
    if (draftsOnly && !row.draft) return false;
    if (!q) return true;
    if (row.cue.toLowerCase().includes(q)) return true;
    return (row.tags || []).some((t) => t.toLowerCase().includes(q));
  }});
  renderNewPage(true);
}}

document.getElementById("new-q").addEventListener("input", applyNewFilter);
document.getElementById("drafts-only").addEventListener("change", applyNewFilter);

function setTab(panelId) {{
  document.querySelectorAll(".tab").forEach((tab) => {{
    const on = tab.dataset.panel === panelId;
    tab.setAttribute("aria-selected", on ? "true" : "false");
  }});
  document.querySelectorAll(".panel").forEach((panel) => {{
    const on = panel.id === panelId;
    panel.classList.toggle("active", on);
    panel.hidden = !on;
  }});
  const tagsChrome = panelId === "panel-tags";
  document.getElementById("tags-toolbar").style.display = tagsChrome ? "" : "none";
  document.getElementById("tags-legend").style.display = tagsChrome ? "" : "none";
  if (panelId === "panel-new" && !newList.childElementCount) applyNewFilter();
}}
document.querySelectorAll(".tab").forEach((tab) => {{
  tab.addEventListener("click", () => setTab(tab.dataset.panel));
}});
</script>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Rebuild coverage-index.md and coverage-index.html.")
    parser.add_argument(
        "--repo",
        type=Path,
        default=None,
        help="Git repo root (default: inferred from this script path).",
    )
    parser.add_argument(
        "--clones-js-only",
        action="store_true",
        help="Rewrite cover/fill clone mappings without rebuilding the index.",
    )
    args = parser.parse_args()
    root = args.repo.resolve() if args.repo else repo_root_from_script()
    vault = root / "SRS"
    cover_clones = scan_agent_clones(root, "cover")
    fill_clones = scan_agent_clones(root, "fill")
    clones_js = write_agent_clones_js(vault, cover_clones, fill_clones)
    if args.clones_js_only:
        print(
            f"Wrote {clones_js} "
            f"({len(cover_clones)} cover, {len(fill_clones)} fill clones)"
        )
        return 0
    tags_md = vault / "Format" / "Tags.md"
    out_md = vault / "NamesHistory" / "coverage-index.md"
    out_html = vault / "NamesHistory" / "coverage-index.html"
    if not tags_md.is_file():
        raise SystemExit(f"Tags.md not found: {tags_md}")

    tree_paths = parse_tree_paths(tags_md)
    if not tree_paths:
        raise SystemExit(f"No tree paths parsed from {tags_md}")
    index_paths = expand_with_ancestors(tree_paths)

    cards_scanned, cards = scan_cards(vault)
    cards_with_tags = len(cards)

    rows: list[tuple[str, int, int, int]] = []
    for prefix in index_paths:
        n = 0
        n_new = 0
        for card in cards:
            if matches_prefix(card.tags, prefix):
                n += 1
                if card.is_new:
                    n_new += 1
        rows.append((prefix, n, n_new, n - n_new))

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    notes = load_preserved_notes(out_md)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(
        render_index(
            generated_at=generated_at,
            tree_paths=index_paths,
            cards_scanned=cards_scanned,
            cards_with_tags=cards_with_tags,
            rows=rows,
            notes=notes,
        ),
        encoding="utf-8",
        newline="\n",
    )
    out_html.write_text(
        render_html(
            generated_at=generated_at,
            tree_paths=index_paths,
            cards_scanned=cards_scanned,
            cards_with_tags=cards_with_tags,
            rows=rows,
            new_cards=new_card_rows(cards),
        ),
        encoding="utf-8",
        newline="\n",
    )
    print(f"Wrote {out_md} and {out_html} ({len(rows)} paths, {cards_with_tags} tagged cards)")
    print(
        f"Wrote {clones_js} "
        f"({len(cover_clones)} cover, {len(fill_clones)} fill clones)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
