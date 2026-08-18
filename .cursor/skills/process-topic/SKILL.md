---
name: process-topic
description: >-
  Picks one item from topics-to-process.txt (or an explicit topic), maps it to
  Tags.md, reports coverage vs gaps, and recommends the next vault skill. Use
  when the user invokes /process-topic or asks what to do next for a queue
  topic.
disable-model-invocation: true
---

# Process one topic (propose only)

## Purpose

Hold vault context for one topic: where it lives in `Tags.md`, how covered it is, which interview themes are missing, and **which skill to run next**. You analyze and recommend. You do **not** create, fill, retag, or delete cards in this run.

## Invoke

```
/process-topic
/process-topic PostgreSQL
/process-topic PostgreSQL: performance tuning, query optimization, troubleshooting
```

- No argument: take the **first** unchecked `- [ ]` line in `SRS/NamesHistory/topics-to-process.txt`.
- A name only: that topic (queue line or ad-hoc string). Do not drain the rest of the list.
- `Name: theme1, theme2, …` (or `Topic: …`): same item, plus extra gap checks for those themes. Themes are **not** automatic new tree leaves.

Language: English only — this skill and the chat report. Vault files stay English.

This skill **names** the next slash command. Cursor does not invoke other skills as functions. Stop after the proposal. The user runs `/cover-tag`, `/fill-tag`, `/refine-tags`, or `/dedup-tag` themselves.

## Read first

- `SRS/Format/Tags.md` (tree + rules; **not** the TREE copy in `FillCardPrompt.txt`)
- `SRS/NamesHistory/topics-to-process.txt` (unless the user already named the item)
- `SRS/NamesHistory/coverage-index.md` (generated count table — fatness vs siblings)
- `SRS/NamesHistory/coverage-index.html` (same counts as a colored collapsible tree; optional to open)
- `SRS/Format/Naming.md` if you will judge cue quality / likely duplicates

**Inventory (do not invent a Python walker).** After the tag is resolved, run:

```
python .cursor/skills/process-topic/scripts/inventory-tag.py Java/Spring
```

Pass the resolved path **without** a leading `#` (PowerShell treats `#…` as a comment). Quoted `"#Java/Spring"` also works.

That script prints `n` / `n_new` / `n_filled`, child-leaf counts, and every cue. Cap the **chat** list at **~15 titles**; if there are more, summarize and name the rest as a count. Use the printed cues to judge duplicates. Read the coverage-index row for this prefix vs siblings.

If `coverage-index.md` or `coverage-index.html` is missing, or cards/`Tags.md` were just edited in this chat and the index script has not run yet, regenerate before trusting **index** counts (inventory-tag.py is always live):

```
python .cursor/skills/process-topic/scripts/rebuild-coverage-index.py
```

The index is a **cache**. Source of truth is cards + `Tags.md`. Do not increment `n` / `n_new` by hand. Do not treat a stale row as truth.

## Pipeline

1. **Pick one item.** First `- [ ]` in the queue, or the name the user typed. Quote the queue line in chat if you used the file.
2. **Resolve the tag.** Map the name to one or more `Tags.md` prefixes. Prefer the honest leaf (example: PostgreSQL → `#Databases/Relational/PostgreSQL`, never a `#PostgreSQL` root). If the name is a group of protocols (Web, HTTP, TLS, …), say which leaves you will treat as in-scope. If there is **no** honest leaf, the recommendation is `/refine-tags` — do not stretch a near-match.
3. **Inventory (live).** Run `inventory-tag.py` for the resolved prefix (see above). Do **not** write a one-off script or `python -c` card walker. Count `n` / `n_new` / `n_filled` from that output. List existing **cues** in chat (cap ~15). Read the index row for this prefix and nearby siblings for “how fat is this vs the rest of the tree.”
4. **Theme gaps.** If the user passed themes, check whether existing cues already cover them (same knowledge, not only substring match). List **covered** vs **missing**. Missing themes are cover-tag candidates, not automatic `Tags.md` leaves.
5. **Likely duplicates.** If several cues collapse to the same interview question, note clusters. Do not delete files.
6. **Recommend one Next.** Exactly one slash command (see order below). Include a realistic `--limit` when the next skill accepts one.
7. Chat report (English): item, resolved tag(s), counts, covered vs gaps, **Next:** one command. Optionally: “When that skill finishes, tick `- [x]` on this queue line” — you still do **not** edit the queue in this run.

### Recommend order (first match)

1. **`/refine-tags [prefix]`** — no honest leaf, or the item clearly belongs under a different root than cards currently use (example: Hohpe/Woolf EIP names → `#Patterns/Enterprise/Integration/...`, **not** `#Messaging/Bus` or similar).
2. **`/dedup-tag <tag> --dry-run`** — several cues look like the same question.
3. **`/fill-tag <tag> [--limit N]`** — many `#New` cards and the leaf already has enough distinct cues.
4. **`/cover-tag <tag> [--limit N]`** — thin coverage, or named themes have no matching cues. Default limit **12** unless the gap list is smaller.
5. **Skip** — well covered, distinct, mostly filled. Propose that the user tick `[x]` on the queue line. Do not invent work.

Do **not** recommend `/import-repo` for a queue **name**. Only if the user pasted a GitHub URL.

### Messaging vs Patterns

Protocols and brokers: `#Messaging` (`#Messaging/AMQP`, `#Messaging/Tools/Kafka`, …). EIP pattern names (Message Bus, Channel, Broker, Request-Reply, …): `#Patterns/Enterprise/Integration/...`. A pattern card that is also about messaging carries **both** `#Messaging` and the Patterns leaf.

## Coverage index

`SRS/NamesHistory/coverage-index.md` (grep table) and `coverage-index.html` (human tree: green ≥50% filled, yellow some filled, red cards but 0 filled, gray unused) are rewritten by:

```
python .cursor/skills/process-topic/scripts/rebuild-coverage-index.py
```

This skill may **run that script** when either file is missing or stale. It does **not** need to regenerate after a propose-only run (no card/`Tags.md` edits). Other vault skills regenerate after they mutate cards or the tree. Do not hand-edit either file.

## Do not

- Create, fill, retag, or delete cards.
- Edit `Tags.md` or tick `- [x]` on `topics-to-process.txt`.
- Run `/cover-tag`, `/fill-tag`, `/refine-tags`, or `/dedup-tag` in the same turn as this skill.
- Drain the whole P0–P2 list.
- Use `FillCardPrompt.txt` TREE as taxonomy.
- Stretch a near-match tag; if there is no leaf, recommend `/refine-tags`.
- Invent a one-off Python/`python -c` walker over `SRS/*.md`; use `inventory-tag.py`.
- Hand-edit coverage-index counts.
- Commit.
---
