---
name: dedup-tag
description: >-
  Collects SRS cards for a tag, finds semantic duplicate questions, merges unique
  claims into one canonical card, then deletes the rest. Use when the user
  invokes /dedup-tag or asks to cherry-pick a tag and remove duplicate cards.
disable-model-invocation: true
---

# Dedup cards by tag

## Purpose

Collect every card with a given tag, find semantic duplicates, and leave one
canonical card per cluster. Unique knowledge from the extras must land in the
survivor **before** those files are deleted. Do not rewrite the tag tree.

## Invoke

```
/dedup-tag <tag> [--dry-run]
```

- `<tag>` required: tree path (`#Databases`) or short name (`Databases`). Include child paths (`#Databases/SQL`, …).
- `--dry-run` optional: report clusters and the merge plan; do not edit or delete files.

Language: English only — this skill, filenames, and the chat report.

## Read first

- `SRS/Format/Tags.md`
- `SRS/Format/Naming.md` (which cue to keep)
- `SRS/Format/GoldStandard.md` (shape of a filled survivor)
- `SRS/NamesHistory/md-file-names.txt`
- `SRS/NamesHistory/jd-java-backend-relevant-questions.txt` if a deleted cue is listed there

## Pipeline

1. Walk `SRS/*.md`. Skip `SRS/Format/` and `SRS/NamesHistory/`.
2. Collect every card whose **tag line** contains `<tag>` or a child of it.
3. Cluster **semantic** duplicates: same interview question / same knowledge, wording differs.
4. For each true-duplicate cluster: pick a survivor, **merge** every sibling into it, then delete the extras.
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

If interchangeable in an interview, they are duplicates. If a follow-up would get a different answer, they are distinct. Close calls: keep both and list them in chat. Do not treat “maybe related” as a cluster.

## Survivor

One survivor file per cluster:

1. Body: filled (no `#New`) over a `#New` stub or draft.
2. If several filled: denser trusted body (more specific mechanism, not more words).
3. Cue: the cluster’s best English name per `Naming.md` (question-shaped, Windows-safe, no `?`). If that name is not the survivor’s basename, **rename** the survivor to it after the merge.

The survivor is the file that remains. It is not “whichever file we keep unchanged.”

## Merge before delete

Do not delete a duplicate until its unique material has a home in the survivor or an explicit drop in the chat ledger.

For every cluster, build a **merge ledger** (chat-only) of every sibling’s substantive items:

1. direct-answer claims
2. mechanism, ordering, defaults, versions, API contracts
3. code / D2 examples and what they imply
4. traps / `always` / `never` / `cannot`
5. `[[wikilinks]]` and thematic tags

Assign each item exactly one disposition:

- **ABSORBED** — unique and on-cue; rewritten into the survivor
- **ALREADY** — survivor already states it (possibly in better words)
- **DROPPED-DUP** — same fact, worse wording
- **DROPPED-UNVERIFIED** — dump-only claim that cannot enter a filled card
- **CONFLICT** — two filled cards disagree; keep the more precise/conditional wording, quote the loser in chat; do not invent a third version

Then write the survivor:

**Filled survivor (no `#New`):** rewrite **one** GoldStandard body in place. One abstract, one interview tip, as many real `warning` pitfalls as the cue needs. Fold unique mechanism, listings, and wikilinks into that shape. Do **not** concatenate two cards. Do **not** paste dump prose, `Untrusted draft`, or a second abstract. Unverified dump traps stay out of the file and go to the ledger as `DROPPED-UNVERIFIED`. Do not put `#New` back to save a dump.

**`#New` survivor:** keep `#New`. Merge sibling drafts into **one** untrusted-draft inventory: unique claims and traps under the existing warning (or add that warning if missing). Drop only exact repeated dump sentences. `fill-tag` will audit the combined ledger later.

**Tags on the survivor:** union of thematic leaves from the cluster, then `#SRS`, then `#New` only if the survivor is still a draft. No parent+child pair. Unknown paths: do not invent a `Tags.md` leaf; propose it in chat.

**Wikilinks:** keep every on-cue `[[wikilink]]` from the cluster, pointed at surviving basenames. No styling on the title.

`--dry-run` still builds this ledger and names KEEP / RENAME / DELETE; it does not write.

A cluster is not done if a sibling had a unique on-cue fact, trap, example, or wikilink that is neither in the survivor nor listed as dropped.

## After a delete

- Remove or retarget the deleted basename in `md-file-names.txt` (if the kept file is already listed, drop the extra line; else rename the line to the kept cue; preserve `[x]` / `[+]` / `[ ]`).
- Same for `jd-java-backend-relevant-questions.txt` when the cue appears there.
- Grep `[[…]]` for every deleted **and** old-renamed title; point them at the kept cue. No extra markup on the wikilink.
- Only fix a kept card’s tag line if it is an invalid path vs `Tags.md`, or to apply the merged tag union above.

## Output (chat only)

For each cluster:

1. KEEP — survivor basename, and RENAME if the cue changed
2. DELETE — files removed
3. MERGE LEDGER — one compact line per item: `ABSORBED` / `ALREADY` / `DROPPED-DUP` / `DROPPED-UNVERIFIED` / `CONFLICT`
4. TAGS — final tag line
5. LINKS RETARGETED — old `[[title]]` → kept cue

Then lists touched (`md-file-names.txt`, JD file) and a short count: clusters merged / files deleted / close calls left distinct.

## Coverage index

After you create, fill, retag, or delete SRS cards (or edit the Tags.md tree), run:

```
python .cursor/skills/process-topic/scripts/rebuild-coverage-index.py
```

Skip this on `--dry-run`. The Docker fill orchestrator rebuilds once after
refine-tags and this dedup turn; do not rebuild during that Docker post-fill turn.

## Do not

- Delete a duplicate whose unique on-cue material has not been absorbed or explicitly dropped in the ledger.
- Concatenate two GoldStandard bodies or copy dump wording into a filled card.
- Delete merely related cards.
- Create a working folder of copies or pointers.
- Edit `Tags.md` (propose a leaf in chat if a kept card needs one).
- Fill a `#New` card to GoldStandard (`/fill-tag`) or import new questions.
- Commit.
---
