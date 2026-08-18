---
name: cover-tag
description: >-
  Widens SRS coverage for a tag by mining interview-question GitHub repos and
  compilation pages, then creating #New cards — untrusted drafts when the
  source has an answer, empty stubs when it does not. Use when the user invokes
  /cover-tag or asks to expand a tag with more possible interview questions.
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
/cover-tag <tag> [--limit N]
```

- `<tag>` required: a tree path (`#Java/Collections/Map/HashMap`) or a short name (`HashMap`). Resolve it to a leaf in `SRS/Format/Tags.md`.
- `--limit` optional: max **new** card files this run. Default **Maximum coverage, senior level**.

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

## Pipeline

1. Resolve `<tag>` to one or more tree prefixes. If the name is ambiguous, pick the Tags.md leaf and say so in chat.
2. Collect existing cues: grep the tag (and child paths) in `SRS/`, plus related lines in `md-file-names.txt`.
3. **Collect question/answer pairs.** Record every URL in **chat**, never in the card file.
   - Open `question-repositories.txt`. Fetch `+` GitHub repos/files that match this tag (raw markdown / `gh` / clone to a temp dir **outside** the vault; do not add the clone to this repo). Skip `-` URLs.
   - Search GitHub for further interview-question repos or files on this topic (`interview questions`, topic name). Same fetch rule.
   - Search the web for **compilation pages** (question lists), not generic tutorials. Official “frequently asked” pages count only as *question* sources.
   - If a new GitHub collection was actually used and is not in `question-repositories.txt`, append `+ <url>`.
4. Normalize each candidate to an English cue per `Naming.md`.
5. Drop semantic duplicates of existing basenames.
6. Keep the best `--limit` gaps. Create one file each: **draft** if any used source has an answer for that cue; **empty stub** if not.
7. Append `- [+] <Cue>.md` to `md-file-names.txt` for new cues.
8. Chat report: existing coverage count, new cues, **drafts vs empty stubs**, skipped dupes, suggested follow-up tags, **GitHub repos and compilation pages used**.
9. Rebuild the coverage index (see below).

Do not overwrite a card that lacks `#New`. Do not rewrite an existing `#New` card that already has a body.

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
- Create more than `--limit` files.
- Commit the cloned upstream repo.
---
