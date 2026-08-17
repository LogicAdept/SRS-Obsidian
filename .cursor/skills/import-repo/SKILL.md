---
name: import-repo
description: >-
  Analyzes an interview-question GitHub repository, merges new questions into
  this SRS vault, and writes untrusted draft card bodies. Use when the user
  invokes /import-repo or pastes a GitHub URL to ingest questions.
disable-model-invocation: true
---

# Import interview repository

## Purpose

Analyze an interview-question repository, merge its questions into this vault, and fill draft cards. Goal: find questions the vault does not have yet, and capture dump answers that include traps and fine points official docs often omit. A draft is never a trusted source.

## Invoke

```
/import-repo <github-url> [--topic <name>] [--limit N]
```

- `<github-url>` required: repo or file URL.
- `--topic` optional: only questions in that area (e.g. Kafka, Spring Security).
- `--limit` optional: max **new** draft files this run. Default **40**. `0` = no cap (still batch if the dump is huge; report leftovers).

This skill creates and fills **drafts** (`#New`). It does **not** promote cards to GoldStandard. That is `/fill-tag`.

Language: English only — this skill, card files, and the chat report. Translate dump text into English when writing drafts. Do not leave Russian (or other source-language) prose in new or updated cards.

## Read first

Read these vault files before writing anything:

- `SRS/Format/Naming.md`
- `SRS/Format/Tags.md` (rules + Tree — not the copy inside FillCardPrompt)
- `SRS/Format/GoldStandard.md` (file shape only)
- `SRS/NamesHistory/md-file-names.txt`
- `SRS/NamesHistory/question-repositories.txt`

## Trust rule

The source dump is **never** a trusted source. Official docs are not required in this skill. Do **not** remove `#New`. Do **not** present dump text as interview-ready fact.

Copy dump answers into the draft so `/fill-tag` later has **claims to verify**, especially traps and fine points that vendor docs often skip (self-invocation, hash vs bucket index, `finally` vs `System.exit`, etc.).

## Pipeline

1. **Fetch** the URL (`gh`, git clone to a temp dir outside the vault, or GitHub raw). Do not add the clone to this repo.
2. **Extract** question/answer pairs from markdown/lists. Skip ads, TOC-only files, and pure multiple-choice dumps unless the user URL is that file.
3. **Normalize** each question to a Windows-safe English cue per `Naming.md` (no `? * : " < > | \ /` in the basename; sentence case; spaces).
4. **Dedupe** against:
   - existing `SRS/*.md` basenames
   - lines in `SRS/NamesHistory/md-file-names.txt`
   - **semantic** duplicates (same question, different wording) → keep one file; do not create a second cue.
5. **Skip overwrite** of cards that already lack `#New` (trusted/filled). Leave them untouched.
6. **Create or enrich** `#New` drafts for new cues and for existing `#New` files that are empty or already marked as untrusted dumps.
7. **Track**:
   - append new cues to `md-file-names.txt` as `- [+] <Cue>.md`
   - add the URL to `question-repositories.txt` with a leading `+ ` if missing
8. **Report** in chat: new / semantic-dupes / skipped-trusted / drafts-written; leftover count if `--limit` truncated.

## Draft file shape

Exact order. Nothing before the HTML comment.

```markdown
<!--
reps: 0
priority: 0
-->
#Thematic/Leaf #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

<dump answer, translated to English, trimmed; keep mechanism and examples if present>

> [!warning] Unverified traps from the dump
> - <trap or subtle point the dump claims, one bullet each>
> - <what official docs might omit: edge case, version split, popular lie>
```

- Tags: deepest honest leaf from `Tags.md`. No parent+child pair. Comparisons get both sides. `#SRS` then `#New`.
- If nothing in the tree fits: shortest honest prefix; propose a new leaf in chat; do not silently add a new top-level root. Do not edit `Tags.md` here — that is `/refine-tags`.
- Personal/HR/biography cues: meta + tags + `#New` + one line that the human must fill. No fake story.
- No URLs, source lists, or “according to …” in the `.md` file.
- English body only. `/fill-tag` still rewrites from official docs; this English dump text is only a claim list to verify.
- When enriching an older draft that still has a Russian trust warning, replace that warning with the English callouts above.

If the dump has a question and no answer: still create the file with the trust warning and empty body after it.

## Do not

- Run `/fill-tag` quality bar or strip `#New`.
- Invent answers when the dump has none.
- Treat Baeldung/interview-dump wording as correct.
- Commit the cloned upstream repo.
---
