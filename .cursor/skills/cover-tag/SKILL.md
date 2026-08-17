---
name: cover-tag
description: >-
  Searches the web for interview questions matching an SRS tag and creates new
  #New stub cards to widen topic coverage. Use when the user invokes /cover-tag
  or asks to expand a tag with more possible interview questions.
disable-model-invocation: true
---

# Cover tag with more questions

## Purpose

Search the web for interview questions on a given tag and create stub cards. Goal: widen topic coverage so interview follow-ups on that tag are less likely to be missing.

## Invoke

```
/cover-tag <tag> [--limit N]
```

- `<tag>` required: a tree path (`#Java/Collections/Map/HashMap`) or a short name (`HashMap`). Resolve it to a leaf in `SRS/Format/Tags.md`.
- `--limit` optional: max **new** card files this run. Default **12**.

This skill adds **questions** (stubs). It does **not** write trusted answers. That is `/fill-tag`.

Language: English only — this skill, filenames, tag lines, and the chat report.

## Read first

- `SRS/Format/Naming.md`
- `SRS/Format/Tags.md`
- `SRS/Format/GoldStandard.md` (meta → tags → body)
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

## Pipeline

1. Resolve `<tag>` to one or more tree prefixes. If the name is ambiguous, pick the Tags.md leaf and say so in chat.
2. Collect existing cues: grep the tag (and child paths) in `SRS/`, plus related lines in `md-file-names.txt`.
3. **Search the web** for interview questions on that topic (question lists, official “frequently asked” only as *question* sources). Record URLs in **chat**, never in the card file.
4. Normalize each candidate to an English cue per `Naming.md`.
5. Drop semantic duplicates of existing basenames.
6. Keep the best `--limit` gaps. Create one stub file each.
7. Append `- [+] <Cue>.md` to `md-file-names.txt` for new cues.
8. Chat report: existing coverage count, new cues, skipped dupes, suggested follow-up tags, URLs used as question sources.

## Stub file shape

```markdown
<!--
reps: 0
priority: 0
-->
#Resolved/Leaf #SRS #New
```

- Nothing before the HTML comment.
- One tag line: thematic leaf/leaves, then `#SRS`, then `#New`.
- **Empty body.** Do not paste blog answers, dump answers, or guessed facts.
- Do not invent a biography for personal cues — skip those.

If the tree has no honest leaf: use the shortest honest prefix; propose a new leaf in chat; do not edit `Tags.md` (use `/refine-tags`).

## Do not

- Remove `#New` or write GoldStandard bodies.
- Copy interview-dump answers into the card (untrusted, and this skill is coverage not ingest).
- Put URLs, bibliographies, or “source:” lines in the `.md`.
- Stretch a near-match tag onto a different topic.
- Create more than `--limit` files.
---
