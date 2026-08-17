---
name: dedup-tag
description: >-
  Collects SRS cards for a tag, finds semantic duplicate questions, and keeps a
  distinct set. Use when the user invokes /dedup-tag or asks to cherry-pick a
  tag and remove duplicate cards.
disable-model-invocation: true
---

# Dedup cards by tag

## Purpose

Collect every card with a given tag, find semantic duplicates, make the set distinct. Do not over-engineer. Do not rewrite the tag tree.

## Invoke

```
/dedup-tag <tag> [--dry-run]
```

- `<tag>` required: tree path (`#Databases`) or short name (`Databases`). Include child paths (`#Databases/SQL`, …).
- `--dry-run` optional: report clusters only; do not delete or edit files.

Language: English only — this skill, filenames, and the chat report.

## Read first

- `SRS/Format/Tags.md`
- `SRS/Format/Naming.md` (which cue to keep)
- `SRS/NamesHistory/md-file-names.txt`
- `SRS/NamesHistory/jd-java-backend-relevant-questions.txt` if a deleted cue is listed there

## Pipeline (keep it this simple)

1. Walk `SRS/*.md`. Skip `SRS/Format/` and `SRS/NamesHistory/`.
2. Collect every card whose **tag line** contains `<tag>` or a child of it.
3. Cluster **semantic** duplicates: same interview question / same knowledge, wording differs.
4. For each true-duplicate cluster: keep one canonical file; delete the others.
5. Sync lists and wikilinks (unless `--dry-run`).
6. Chat report.

Do not retag the whole set. Do not invent taxonomy. That is `/refine-tags`.

## What is a duplicate

True duplicates — one card would answer the others:

- Several cues that all collapse to “what JOIN types exist”
- “ACID properties” vs “defining properties of a transaction” vs “ACID requirements”
- The same comparison asked twice (`UNION` vs `UNION ALL` under two names)
- Isolation-level overviews that are the same lecture with a different title

Not duplicates — different facts, keep all:

- 1NF vs 2NF vs 3NF vs “what is normalization”
- Catalog of JOIN types vs a card that is **only** LEFT vs INNER
- Generic replication vs MySQL / PostgreSQL / Oracle replication
- “How indexes work” vs “when indexes hurt” vs clustered vs non-clustered
- Hibernate isolation vs JDBC isolation vs general ACID, if they target different APIs
- Related follow-ups on the same topic

If interchangeable in an interview, they are duplicates. If a follow-up would get a different answer, they are distinct. Close calls: keep both and list them in chat. Do not guess a merge.

## Which file to keep

One survivor per cluster, in this order:

1. Filled card (no `#New`) over a stub.
2. Clearer English cue per `Naming.md` (question-shaped, Windows-safe, no `?`).
3. If still tied: denser trusted body.

Do **not** splice two GoldStandard bodies. Do **not** copy dump prose into a filled card. If the survivor is still `#New` and a deleted draft had extra unverified traps, you may append those traps under the existing untrusted-draft warning.

## After a delete

- Remove or retarget the deleted basename in `md-file-names.txt` (if the kept file is already listed, drop the extra line; else rename the line to the kept cue; preserve `[x]` / `[+]` / `[ ]`).
- Same for `jd-java-backend-relevant-questions.txt` when the cue appears there.
- Grep `[[…]]` for the deleted title; point them at the kept cue. No extra markup on the wikilink.
- Only fix a kept card’s tag line if it is an invalid path vs `Tags.md`. Do not rewrite other tags.

## Do not

- Delete merely related cards.
- Create a working folder of copies or pointers.
- Edit `Tags.md` (propose a leaf in chat if a kept card needs one).
- Fill bodies (`/fill-tag`) or import new questions.
- Commit.
---
