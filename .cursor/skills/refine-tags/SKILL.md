---
name: refine-tags
description: >-
  Refines the SRS tag taxonomy in Tags.md and retags cards when a path must
  change. Use when the user invokes /refine-tags or asks to tidy, merge, or
  restructure the tag tree without proliferating synonyms.
disable-model-invocation: true
---

# Refine tag tree

## Purpose

Refine the tag tree. Goal: a convenient, logical taxonomy. Do not multiply entities without need.

## Invoke

```
/refine-tags [prefix]
```

- `prefix` optional: only that root or path (e.g. `#Java/Spring`, `#Messaging`). Default: whole tree, but still prefer small honest edits over a rewrite.

Language: English only — this skill, `Tags.md` edits, and the chat report.

## Read first

- `SRS/Format/Tags.md` (canonical rules + Tree)
- Grep actual tag lines in `SRS/*.md` (skip `SRS/Format/` and `SRS/NamesHistory/`)

Do not use the TREE copy inside `SRS/Format/FillCardPrompt.txt`. If it disagrees with `Tags.md`, `Tags.md` wins; mention the drift in chat only.

## Principles (from Tags.md — do not violate)

- Composite paths `Root/.../Leaf`; each segment Capitalized; abbreviations UPPERCASE.
- Extend existing roots; **do not** add parallel synonym roots (`#REST` vs `#API/REST`, `#Kubernetes` vs `#DevOps/Tools/Kubernetes`, `#SQL` vs `#Databases/SQL`).
- Established mappings:
  - REST → `#API/REST`
  - SQL language → `#Databases/SQL/...` (no `#SQL` root)
  - Relational RDBMS → `#Databases/Relational/...` (SQL stays the language)
  - OLAP / columnar → `#Databases/OLAP/...` (ClickHouse, Snowflake, Druid, Pinot)
  - Kubernetes → `#DevOps/Tools/Kubernetes`
  - Kafka → `#Messaging/Tools/Kafka`
- `#NoSQL` is not a root. Non-relational stores are `#Databases/NoSQL` and children. Store-family comparison cards use `#Databases/Relational` and `#Databases/NoSQL` (or product leaves). Language/search vs SQL stays `#Databases/SQL`. OLTP vs OLAP uses `#Databases/Relational` and `#Databases/OLAP`.
- Prefer a deeper honest leaf; do **not** put a parent and its child on the same card.
- Incomplete shorter prefix is allowed when no child is a better fit.
- New leaf only when a real topic does not fit; under a logical existing root. New **top-level** root only if no existing root can hold it — state that explicitly in chat.
- `#SRS` and `#New` stay in the System section; do not invent aliases for them.

## Do not multiply entities without need

Apply a change only if it does at least one of:

- merges two tags that mean the same thing
- moves a leaf under the parent interviewers would actually filter by
- adds a leaf that cards already need and currently stretch a near-match
- removes a tree entry that no card uses **and** that is not a planned parent of existing children

Do **not**: rename for style, split a leaf because a blog has a finer heading, or create a tag for a single one-off card when the parent already names the topic.

## Pipeline

1. Inventory: tags in `Tags.md` vs tags used on cards.
2. Classify: unused tree entries, used-but-missing-from-tree, synonym pairs, parent+child on the same card, stretched near-matches.
3. Plan a **minimal** patch. If several layouts are reasonable, apply only the unambiguous merges/fixes and list the rest as options in chat — do not guess a controversial re-parent.
4. Edit `SRS/Format/Tags.md` Tree (and the short rules only if a real policy changed).
5. Retag affected **card** files: replace old paths, keep thematic → `#SRS` → `#New` order, drop parent+child duplicates.
6. Do not retag Format notes except `Tags.md`. Do not rewrite card bodies.
7. Chat report: before/after paths, files touched, unused entries left in the tree on purpose, open taxonomy questions.

## Do not

- Silently create a new top-level root.
- Duplicate the whole tree into FillCardPrompt or a skill file.
- Fill or create cards (`/import-repo`, `/cover-tag`, `/fill-tag`).
- Delete semantic duplicate **cards**; that is `/dedup-tag`.
- Mass-rename wikilink titles; this skill changes **tags**, not filenames.
---
