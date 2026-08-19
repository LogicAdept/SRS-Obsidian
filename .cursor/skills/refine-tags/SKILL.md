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

**Do not invent a Python walker or a one-off retagger.** After the prefix is chosen, run:

```
python .cursor/skills/refine-tags/scripts/tag-audit.py Java/Spring
```

That prints unused tree paths, tags used on cards but missing from `Tags.md`, and cards that carry a parent and its child. Cue titles: `python .cursor/skills/process-topic/scripts/inventory-tag.py Java/Spring`. Pass prefixes **without** a leading `#` (PowerShell treats `#…` as a comment).

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
  - AMQP protocol → `#Messaging/AMQP` (RabbitMQ stays the broker leaf)
  - Hohpe EIP (Message Bus, Channel, Request-Reply, …) → `#Patterns/Enterprise/Integration/...`, not `#Messaging/Bus` etc.
  - JUnit / Mockito / Testcontainers / WireMock / Cucumber / Gherkin → `#Java/Testing/...`
- `#NoSQL` is not a root. Non-relational stores are `#Databases/NoSQL` and children. Store-family comparison cards use `#Databases/Relational` and `#Databases/NoSQL` (or product leaves). Language/search vs SQL stays `#Databases/SQL`. OLTP vs OLAP uses `#Databases/Relational` and `#Databases/OLAP`.
- Prefer a deeper honest leaf; do **not** put a parent and its child on the same card.
- Incomplete shorter prefix is allowed when no child is a better fit.
- New leaf only when a real topic does not fit; under a logical existing root. New **top-level** root only if no existing root can hold it — state that explicitly in chat.
- `#SRS` and `#New` stay in the System section; do not invent aliases for them.

## Do not multiply entities without need

Apply a change only if it does at least one of:

- merges two tags that mean the same thing
- moves a leaf under the parent interviewers would actually filter by
- **adds a leaf that cards already need** and currently stretch a near-match (or sit on a parent that is too coarse to filter)
- removes a tree entry that no card uses **and** that is not a planned parent of existing children

**Adding needed leaves is part of the job**, not an optional follow-up. If inventory shows a **cluster** of cards (not a single one-off) that interviewers would filter as a distinct topic, and no existing child is honest, **add the leaf to `Tags.md` and retag those cards in the same run**. Do not leave that cluster on the parent and only mention the leaf in “open questions.”

Open questions in chat are for **controversial re-parents** (two equally honest parents, synonym roots, whether two clusters are the same topic). They are not a parking lot for obvious missing filters.

Do **not**: rename for style, split a leaf because a blog has a finer heading, or create a tag for a single one-off card when the parent already names the topic.

## Pipeline

1. Inventory: run `tag-audit.py` (and `inventory-tag.py` if you need cue titles). Classify from that output: unused tree entries, used-but-missing-from-tree, synonym pairs, parent+child on the same card, stretched near-matches, **parent-only clusters that need a child**.
2. Plan a **minimal** patch: unambiguous merges/fixes **and** the needed new leaves from step 1. List only genuine taxonomy forks as options in chat — do not skip adding a leaf that the cards already require.
3. Edit `SRS/Format/Tags.md` Tree (and the short rules only if a real policy changed).
4. Retag affected **card** files with `retag-prefix.py` — not a throwaway script:

```
python .cursor/skills/refine-tags/scripts/retag-prefix.py --from Java/Spring/Framework/Boot --to Java/Spring/Boot
python .cursor/skills/refine-tags/scripts/retag-prefix.py --map Java/Spring/Framework/Boot=Java/Spring/Boot --map Java/Spring/Framework/Security=Java/Spring/Security
python .cursor/skills/refine-tags/scripts/retag-prefix.py --from Old/Leaf --to New/Leaf --only "Some cue.md"
python .cursor/skills/refine-tags/scripts/retag-prefix.py --add Java/Annotations --only "What is the Lazy annotation in Spring.md"
```

`--from/--to` also rewrites children (`Old/Leaf/X` → `New/Leaf/X`). Only cards that actually carry the old prefix are touched. The script keeps thematic → `#SRS` → `#New` and drops parent+child duplicates on the same line. Use `--dry-run` first when the mapping is easy to get wrong. Do not retag Format notes except `Tags.md`. Do not rewrite card bodies.
5. Chat report: before/after paths, files touched, unused entries left in the tree on purpose, open taxonomy questions.
6. Rebuild the coverage index (see below).

## Coverage index

After you create, fill, retag, or delete SRS cards (or edit the Tags.md tree), run:

```
python .cursor/skills/process-topic/scripts/rebuild-coverage-index.py
```

## Do not

- Invent a one-off Python/`python -c` walker or retagger; use `tag-audit.py` and `retag-prefix.py`.
- Silently create a new top-level root.
- Duplicate the whole tree into FillCardPrompt or a skill file.
- Fill or create cards (`/import-repo`, `/cover-tag`, `/fill-tag`).
- Delete semantic duplicate **cards**; that is `/dedup-tag`.
- Mass-rename wikilink titles; this skill changes **tags**, not filenames.
---
