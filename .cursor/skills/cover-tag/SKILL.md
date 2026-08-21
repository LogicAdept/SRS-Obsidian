---
name: cover-tag
description: >-
  Widens SRS coverage for a tag by mining interview-question GitHub repos and
  compilation pages, then creating #New cards — untrusted drafts when the
  source has an answer, empty stubs when it does not. Enforces a strict
  interview-value gate and writes a structured result for orchestrated runs.
  If the tag has children, covers those leaves only — never the parent. Use when the user
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
/cover-tag <tag> [--limit N] [--per-node M] [--max-nodes K] [--flat] [--focus TEXT] [--result-file PATH]
```

- `<tag>` required: a tree path (`#Java/Collections/Map`) or a short name (`HashMap`). Resolve it in `SRS/Format/Tags.md`.
- `--limit` optional: hard maximum of **new** card files, never a target. Default **50**. Write fewer whenever fewer strong, distinct candidates survive the quality gate.
- `--per-node` optional: max new files per visited **leaf**. Default: even split of `--limit`. Unused slots stay unused.
- `--max-nodes` optional: max **leaves** to visit. Default **12**. Ignored with `--flat` on a leaf.
- `--flat` optional: if the resolved prefix is a **leaf**, cover that leaf only. If it is a **parent**, cover its descendant leaves only — never the parent node.
- `--focus` optional: prioritize one user-identified missing interview angle within
  the resolved leaf. Search specifically for distinct questions about that angle,
  but keep the normal source, ownership, duplicate, and quality gates. This may
  revisit an otherwise complete leaf; zero new cards is valid only after a real
  focused search shows the angle is already covered or has no strong candidates.
- `--result-file` optional for interactive use and **mandatory when supplied by an orchestrator**. It must be repository-local and is written through `write_cover_batch` in `write_drafts.py`, never by hand. Orchestrated use combines it with `--flat` on one leaf.

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

For the structured result, evaluate these finite dimensions without card-count
quotas: `definition` (required only if the term lacks one), `mechanism`,
`failure_version_lie`, `comparison`, `procedure_operations`, and
`missing_definition_gaps`. Each dimension records `required`, `satisfied`, and
brief evidence. A dimension can be satisfied by an existing cue; do not create a
weaker duplicate merely to tick a box.

## Candidate quality gate

Every new cue must pass all checks:

1. It comes from a real interview-question repository or question-compilation page.
2. It is independently answerable later from official documentation. Search and
   record the relevant official documentation URL in the structured result, but do
   not put URLs or source names in the card.
3. It adds a distinct definition gap, mechanism, failure/version/popular-lie,
   comparison, or procedure/operations angle.
4. It is not a semantic duplicate or near-duplicate of any existing basename or
   card created in this run.
5. It is not source-meta wording ("what does the dump/source say/equate/claim").
6. It is not an incidental vendor/product mention whose mechanism belongs elsewhere,
   obsolete trivia without current practical value, or a question better owned by
   another tag.

Candidates owned by a sibling or another tag are **deferred and reported**. Do not
create them, retag them, edit sibling cards, or mutate sibling tags during this leaf
run. Taxonomy and retagging belong exclusively to `/refine-tags`.

## Walk (do not invent a walker)

Cursor does not invoke this skill as a function. Recursion is a **leaf-only loop in this run**: cover descendant leaves, never parent nodes, never ancestors.

After `<tag>` is resolved, run (PowerShell: no leading `#`):

```
python .cursor/skills/cover-tag/scripts/subtree-order.py Java/Collections/Map
```

Pass through `--limit`, `--per-node`, `--max-nodes`, `--flat` when the user set them. The script prints `cover_next` (node + quota) and `remaining`. Follow `cover_next` in order. Do not spawn subagents.

If the name is ambiguous, pick the Tags.md path and say so in chat **before** running the script.

## Pipeline

For **each** `cover_next` node, until quotas are spent:

1. Collect existing cues for **this node and its descendants** (cards already in the vault **plus files created earlier in this run**), plus related lines in `md-file-names.txt`.
2. **Collect question/answer pairs** for this node. Record every URL in **chat** and in the structured result's source lists, never in a card file. Reuse repos/pages already fetched in this run; do not re-clone.
   - With `--focus`, begin with focused queries for that exact angle and assess
     existing cues semantically against it. Do not broaden away from the request
     merely to produce cards.
   - Open `question-repositories.txt`. Fetch `+` GitHub repos/files that match this node (raw markdown / `gh` / clone to a temp dir **outside** the vault; do not add the clone to this repo). Skip `-` URLs.
   - Search GitHub for further interview-question repos or files on this topic (`interview questions`, topic name). Same fetch rule.
   - Search the web for **compilation pages** (question lists), not generic tutorials. Official “frequently asked” pages count only as *question* sources.
   - If a new GitHub collection was actually used and is not in `question-repositories.txt`, append `+ <url>`.
3. Normalize each candidate to an English cue per `Naming.md`.
4. Apply the full Candidate quality gate above, including semantic duplicate,
   source-meta, incidental-product, obsolete-trivia, and wrong-owner rejection.
5. **Honest leaf:** `cover_next` is always a leaf. Tag the new card with that leaf. Never create a card whose thematic tag is a parent. If a child of this leaf would be a better fit, defer it and report it — do not invent a parent card.
6. Create at most this node’s **quota** files via the generator below: **draft** if any used source has an answer for that cue; **empty stub** if not. Stop the whole run when the global `--limit` is reached. Never add weak candidates to reach the quota.
7. The generator appends `- [+] <Cue>.md` to `md-file-names.txt`. Do not append by hand.

Cover must not change any existing card's tags or edit `Tags.md`. Then: write the
structured result if requested, chat report, and rebuild the coverage index once.
Do not overwrite a card that lacks `#New`. Do not rewrite an existing `#New` card
that already has a body.

## Generate files

Do **not** rewrite meta, callouts, `write()`, or the names-file append. Do not `Write()` dozens of `.md` files by hand.

1. Copy `.cursor/skills/cover-tag/scripts/_gen_tag.py` → `_gen_<slug>.py` in the **same** folder.
2. Fill `TAG`, `RESULT_FILE` (when requested), `LIMIT`, `CARDS`, `DIMENSIONS`, `SOURCES`,
   exhaustion, budget, and deferred-candidate fields. Draft = compact `body` plus
   optional concise `traps`; stub = omit both. Keep only claims and traps useful to
   a later `/fill-tag`; do not copy verbose dump prose.
3. Call `write_cover_batch(...)` exactly as the template demonstrates, then run
   (PowerShell: no leading `#`, no `&&`):

```
python .cursor/skills/cover-tag/scripts/_gen_<slug>.py
```

4. Delete `_gen_<slug>.py` after a successful run. Keep `_gen_tag.py` and `write_drafts.py`.

`write_drafts.py` refuses overwrites, checks `#SRS` / trailing `#New`, rejects
illegal/source-meta basenames, and atomically writes the result JSON after cards.
Do not hand-write JSON. Zero cards is valid through `write_cover_batch` when the
search genuinely exhausted all strong candidates.

## Structured result contract

When `--result-file` is present, a successful run must write schema version 1 with:

- exact resolved `tag`;
- `created_count` and `created_cues` (derived by the helper);
- all six `coverage_dimensions`, each with booleans `required` and `satisfied`
  plus concise non-empty `evidence`;
- `sources_searched.interview` and `.official` URL arrays;
- booleans `candidate_search_exhausted` and `budget_hit`;
- `deferred_candidates` for strong cues owned by other tags.

An unsatisfied required dimension is a valid result, but it keeps the node dirty;
record the missing angle and evidence honestly instead of inventing a weak card.
Set `candidate_search_exhausted=true` only after prescribed interview repositories
and compilation pages have no further strong, in-scope candidates. Set
`budget_hit=true` exactly when the hard limit was reached. Hitting the limit is not
proof of exhaustion. If fewer than the limit survive, write fewer. The orchestrator
fails closed when the file is absent, malformed, inconsistent with created files,
or claims the wrong budget state.

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

- One tag line: one thematic leaf, then `#SRS`, then `#New`.
- Do not invent a biography for personal cues — skip those.

If the tree has no honest leaf: do not tag a parent. Propose a new leaf in chat; do not edit `Tags.md` (use `/refine-tags`).

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
- Cover a parent node, tag a new card with a parent, or skip `subtree-order.py`.
- Spawn subagents for child tags (this run is one loop).
- Stretch a child topic onto the parent tag (or the reverse).
- Retag an existing card, edit Tags.md, or create a sibling/other-tag candidate.
- Ask what a dump, source, article, or interview list says.
- Preserve obsolete trivia or incidental vendor mentions with no practical mechanism.
- Reimplement `write_drafts.py` (meta, callouts, names-file). Copy `_gen_tag.py`.
- Commit the cloned upstream repo.
---
