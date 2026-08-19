---
name: cover-tag
description: >-
  Widens SRS coverage for a tag by mining interview-question GitHub repos and
  compilation pages, then creating #New cards — untrusted drafts when the
  source has an answer, empty stubs when it does not. If the tag has children,
  walks leaves first (post-order), then the invoked tag. Use when the user
  invokes /cover-tag or asks to expand a tag with more possible interview
  questions.
disable-model-invocation: true
---

# Cover tag with more questions

## Purpose

Widen topic coverage so interview follow-ups on that tag are less likely to be missing. **Mine questions** from collections — not blog essays and not official docs as the primary source.

Primary sources, in this order:

1. **GitHub repositories** that are interview-question dumps / cheat sheets (markdown lists, `README`, topic files). Start with `SRS/NamesHistory/question-repositories.txt` (`+` = use, `-` = skip). Search GitHub for more collections on this tag.
2. **Web pages that are question compilations** (“top interview questions”, FAQ lists, curated cheatsheets). Prefer a list of questions over a single tutorial.

This skill adds **questions**. It does **not** write trusted GoldStandard bodies (`/fill-tag` does that). If a used source includes an answer, copy it into the new card as an **untrusted draft** (same job as `/import-repo` dump text: claims and traps for later verification). If the source has only a title, leave an empty stub. Do **not** invent an answer.

Language: English only — this skill, filenames, tag lines, card bodies, and the chat report. Translate dump text into English.

## Invoke

```
/cover-tag <tag> [--limit N] [--per-node M] [--max-nodes K] [--flat]
```

- `<tag>` required: a tree path (`#Java/Collections/Map`) or a short name (`HashMap`). Resolve it in `SRS/Format/Tags.md` (leaf or parent).
- `--limit` optional: max **new** card files this run. Default **12** when the walk has children; **Maximum coverage, senior level** on a leaf or with `--flat`.
- `--per-node` optional: max new files per visited node. Default: even split of `--limit`, leftover slots on the invoked tag. If set, the invoked tag is reserved first so a wide walk does not starve it.
- `--max-nodes` optional: max tree nodes to visit. Default **12**. Ignored with `--flat`.
- `--flat` optional: cover only the resolved prefix (old behavior). Still treat child cues as already covered so you do not duplicate them on the parent.

## Read first

- `SRS/Format/Naming.md`
- `SRS/Format/Tags.md`
- `SRS/Format/GoldStandard.md` (meta → tags → body)
- `SRS/NamesHistory/question-repositories.txt`
- Existing `SRS/*.md` that already carry this tag (or a child leaf)
- `SRS/NamesHistory/md-file-names.txt`

## What “coverage” means

Interviewers do not only ask definitions. Prefer gaps in this order:

1. Mechanism / “how does it actually work”
2. Failure modes, versions, popular lies
3. Comparisons (`X` vs `Y`) that the tag still lacks
4. Procedures / “how do you …”
5. Definitions only if the vault has no card for the term

Skip trivia, company-HR, and near-duplicates of cues already in the vault.

## Walk (do not invent a walker)

Cursor does not invoke this skill as a function. Recursion is a **post-order loop in this run**: children before parents, invoked tag last.

After `<tag>` is resolved, run (PowerShell: no leading `#`):

```
python .cursor/skills/cover-tag/scripts/subtree-order.py Java/Collections/Map
```

Pass through `--limit`, `--per-node`, `--max-nodes`, `--flat` when the user set them. The script prints `cover_next` (node + quota) and `remaining`. Follow `cover_next` in order. Do not spawn subagents.

If the name is ambiguous, pick the Tags.md path and say so in chat **before** running the script.

## Pipeline

For **each** `cover_next` node, until quotas are spent:

1. Collect existing cues for **this node and its descendants** (cards already in the vault **plus files created earlier in this run**), plus related lines in `md-file-names.txt`.
2. **Collect question/answer pairs** for this node. Record every URL in **chat**, never in the card file. Reuse repos/pages already fetched in this run; do not re-clone.
   - Open `question-repositories.txt`. Fetch `+` GitHub repos/files that match this node (raw markdown / `gh` / clone to a temp dir **outside** the vault; do not add the clone to this repo). Skip `-` URLs.
   - Search GitHub for further interview-question repos or files on this topic (`interview questions`, topic name). Same fetch rule.
   - Search the web for **compilation pages** (question lists), not generic tutorials. Official “frequently asked” pages count only as *question* sources.
   - If a new GitHub collection was actually used and is not in `question-repositories.txt`, append `+ <url>`.
3. Normalize each candidate to an English cue per `Naming.md`.
4. Drop semantic duplicates of existing basenames (vault + this run).
5. **Honest leaf:** tag the new card with this node only when no child of this node is a better fit. On a **parent** node, keep comparisons, interface contracts, and “which X when” — not a child’s mechanism. No parent+child pair on the same card.
6. Create at most this node’s **quota** files via the generator below: **draft** if any used source has an answer for that cue; **empty stub** if not. Stop the whole run when the global `--limit` is reached.
7. The generator appends `- [+] <Cue>.md` to `md-file-names.txt`. Do not append by hand.

Then: chat report, then rebuild the coverage index once (see below). Do not overwrite a card that lacks `#New`. Do not rewrite an existing `#New` card that already has a body.

## Generate files

Do **not** rewrite meta, callouts, `write()`, or the names-file append. Do not `Write()` dozens of `.md` files by hand.

1. Copy `.cursor/skills/cover-tag/scripts/_gen_tag.py` → `_gen_<slug>.py` in the **same** folder.
2. Fill `CARDS` in visit order (comment `# --- Leaf ---` per node). Draft = `body` + optional `traps`. Stub = omit both.
3. Run (PowerShell: no leading `#`, no `&&`):

```
python .cursor/skills/cover-tag/scripts/_gen_<slug>.py
```

4. Delete `_gen_<slug>.py` after a successful run. Keep `_gen_tag.py` and `write_drafts.py`.

`write_drafts.py` refuses to overwrite an existing file, checks `#SRS` / trailing `#New`, and rejects `?` and other illegal basename characters.

Python quoting: triple-quote every `body`. If a trap contains `"`, wrap that item in **single** quotes (`'setAllowedOrigins("*")'`). Never nest `"` inside a double-quoted Python string.

Chat report: visit order with per-node created counts, **remaining** nodes (suggest `/cover-tag` for those), existing coverage, new cues, **drafts vs empty stubs**, skipped dupes, suggested follow-up tags, **GitHub repos and compilation pages used**.

## File shape

Exact order. Nothing before the HTML comment.

```markdown
<!--
reps: 0
priority: 0
-->
#Resolved/Leaf #SRS #New
```

- One tag line: thematic leaf/leaves, then `#SRS`, then `#New`.
- Do not invent a biography for personal cues — skip those.

If the tree has no honest leaf: use the shortest honest prefix; propose a new leaf in chat; do not edit `Tags.md` (use `/refine-tags`).

### Empty stub (no answer in the sources you opened)

Stop after the tag line. No guessed body.

### Untrusted draft (source has an answer)

Same callouts as `/import-repo`. Keep `#New`. Do not GoldStandard.

```markdown
> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

<dump answer, translated to English, trimmed; keep mechanism and examples if present>

> [!warning] Unverified traps from the dump
> - <trap or subtle point the dump claims, one bullet each>
> - <what official docs might omit: edge case, version split, popular lie>
```

Omit the traps callout if the dump has none. Prefer the source with more mechanism / traps when several lists answer the same cue. Do not merge unrelated essays. English body only. No URLs, source lists, or “according to …” in the `.md`.

## Coverage index

After you create, fill, retag, or delete SRS cards (or edit the Tags.md tree), run:

```
python .cursor/skills/process-topic/scripts/rebuild-coverage-index.py
```

## Do not

- Remove `#New` or write GoldStandard bodies.
- Invent an answer when the compilation has only a title.
- Treat dump/blog wording as correct (it is a claim list for `/fill-tag`).
- Put URLs, bibliographies, or “source:” lines in the `.md`.
- Treat a random tutorial as a question source when a GitHub list or compilation page exists.
- Stretch a near-match tag onto a different topic.
- Create more than `--limit` files, or more than a node’s quota.
- Process a parent before its listed children, or skip `subtree-order.py`.
- Spawn subagents for child tags (this run is one loop).
- Stretch a child topic onto the parent tag (or the reverse).
- Reimplement `write_drafts.py` (meta, callouts, names-file). Copy `_gen_tag.py`.
- Commit the cloned upstream repo.
---
