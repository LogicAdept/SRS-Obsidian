---
name: fill-tag
description: >-
  Fills existing SRS cards for a chosen tag to GoldStandard using official
  documentation, Naming, and Tags, auditing any untrusted dump draft
  claim-by-claim before replacing it. Use when the user invokes /fill-tag or
  asks to complete #New cards under a tag from primary docs.
disable-model-invocation: true
---

# Fill cards by tag

## Purpose

Fill cards for a chosen tag to GoldStandard, Naming, and Tags. Input may be an
empty stub or an untrusted draft produced by `/cover-tag`; always rely on
official documentation.

## Invoke

```
/fill-tag <tag> [--limit N]
/fill-tag @SRS/<Cue>.md
```

- `<tag>` required when no file is named: tree path or short name. Resolve via `SRS/Format/Tags.md`. A grouping parent is valid even if it has no own bullet, as long as a child leaf exists (`#Java/Spring/Framework` covers `.../WebMvc`, `.../WebFlux`, …).
- `@SRS/<Cue>.md` (or another vault-relative card path): fill **that** card only. Coverage index **#New** tab copies this form.
- `--limit` optional: cards to finish this run when filling by tag. Default **1**. Never more than **3** unless the user lists specific cues or the Docker fill orchestrator names a cluster from its clustering turn.

Accuracy beats coverage. A wrong card is worse than leaving `#New`.

Language: English only — this skill, finished card bodies, and the chat report. Translate any leftover dump-language prose; do not keep it.

## Read first

- `SRS/Format/GoldStandard.md`
- `SRS/Format/Naming.md`
- `SRS/Format/Tags.md` (Tree lives here)
- `SRS/Format/Format.md` (D2: no `layoutEngine` in diagram source)
- `SRS/Format/FillCardPrompt.txt` sections **C, E, F, G, H** for quality bar, gold density, checklist, and chat-only output. Ignore its preamble (“you do not have the vault”) and its TREE — use `Tags.md`.
- The target card(s), including any draft dump text
- A filled sibling on the same tag when one exists (density reference)

## Which files to fill

Prefer `#New` cards whose tag line matches `<tag>` or a child of it.

Skip personal/HR/biography cues: leave the stub; human fills those.

If the user names explicit cues, attaches `@SRS/<Cue>.md`, or the orchestrator
lists a tight cluster of files, fill **every named card** this turn. Do not
stop after the first file. Coverage index **#New** tab still copies a single
`@SRS/<Cue>.md`.

Otherwise process cards with an `Untrusted draft` body before empty stubs. A
draft contains more claims that can be lost or accidentally trusted; auditing
it is part of filling the card, not optional cleanup.

## Official sources only

Before writing, **search and fetch** official/original docs for that cue. Memory is not evidence. If the web is unreachable, keep `#New` and stop.

Primary, in order:

- Language/platform spec and vendor JavaDoc (JLS, Java SE API, OpenJDK source)
- Product reference (Spring `docs.spring.io`, Kafka `kafka.apache.org`, SQL vendor docs)
- JEPs, JSRs, RFCs, ISO/SQL when they define the behavior

Not primary: Baeldung, Medium, Wikipedia, Stack Overflow, interview dumps, blogs. If only those exist, keep `#New`.

Read the defining section (contract, spec paragraph, implementation), not a snippet. Note version.

## Draft-aware workflow

A `#New` card has one of two inputs:

- **Empty stub:** meta + tags, with no proposed answer. Research the cue from
  scratch.
- **Untrusted draft:** an `Untrusted draft` warning (or a legacy Russian
  equivalent), dump prose/code, and possibly `Unverified traps from the dump`.
  This is a **claim inventory**, never a source.

For an untrusted draft, do not erase or rewrite it before auditing it. First
make a scratch **claim ledger** (chat-only, never in the card) containing every
substantive item:

1. direct-answer claims
2. mechanism or ordering claims
3. defaults, thresholds, versions, and API contracts
4. code examples and their implied behavior
5. traps, gotchas, and every `always` / `never` / `cannot` statement

Research the cue **and each ledger item** in official docs or original source.
Assign exactly one disposition:

- **VERIFIED** — official text/source establishes the claim and its conditions
- **CORRECTED** — the draft has a useful idea but wrong wording, scope,
  default, version, or mechanism
- **REJECTED** — contradicted, irrelevant to the cue, or a popular falsehood
- **UNRESOLVED** — primary evidence was not found

Then build the GoldStandard body:

1. Rewrite verified material in precise card language; do not preserve dump
   wording or attribution.
2. Replace corrected claims with the evidenced version.
3. Remove rejected claims. Do not hedge them into the finished answer.
4. A verified trap becomes a specific normal `> [!warning] ...` block.
   Rejected traps disappear.
5. Re-check draft code against the stated version. Replace or fix it; never
   carry an uncompiled dump listing forward.
6. Fine points omitted by reference docs (implementation branches,
   self-invocation, hash vs index) are allowed only after reading original
   implementation/spec text that shows them.
7. If an **essential** claim is unresolved, keep `#New`. A nonessential,
   unresolved aside may be dropped only when the remaining official evidence
   fully answers the cue; report the omission in chat.

When `#New` is removed, no draft residue may remain: delete the `Untrusted
draft` / `Unverified traps` callouts, legacy equivalents, `Dump:` labels, and
sentences saying text came from a dump.

## File shape (finished card)

Exact order. Nothing before the HTML comment.

1. Meta only:

```html
<!--
reps: 0
priority: 0
-->
```

Preserve existing `reps` / `priority` if already non-zero.

2. One tag line: thematic leaves from `Tags.md`, then `#SRS`. **No `#New`** iff the checklist passes. No parent+child pair. Comparisons get both sides. If no leaf fits: honest shorter prefix + propose a new leaf in chat; do not silently add a top-level root (taxonomy edits are `/refine-tags`).

3. English body per GoldStandard + FillCardPrompt §C:

- `> [!abstract] Short answer` — answers the cue; does not restate the title
- Mechanism (APIs, steps, version when it matters)
- At least one real `warning` pitfall
- ≥2 `[[wikilinks]]` to question-shaped English titles; no styling on the title; never link tag paths
- Code and/or D2 for mechanisms; **Fig. N.** / **Listing N.** captions as plain Markdown under the fence, not callouts
- `> [!tip] Interview answer` — 2–4 spoken sentences

Forbidden in the `.md`: nested callouts, `[^footnotes]`, HTML styling, URLs, “according to the JLS”, NOTES/SOURCES/REFERENCES, cite tokens, empty “it depends”.

Draft-clean gate: a card cannot lose `#New` if a substantive draft claim lacks
a ledger disposition, an essential item is unresolved, or any untrusted-draft
marker remains.

Depth: HashMap/equals gold example, not an 8-line stub. Yes/no language cues may match gold example 1.

Adversarial pass (FillCardPrompt §E): counterexample every `always`/`never`; implementation claims from real branches; listings compile or are labeled Conceptual; immutability/thresholds include preconditions.

Do not invent biographies.

## Output (chat + files)

Write the complete `.md` into `SRS/<Cue>.md` (cue already is the basename). Then in **chat only** (never inside the file):

1. Filename
2. CHECKLIST PASS/FAIL per FillCardPrompt §G line, with a short quote proving each PASS
3. DRAFT AUDIT — one compact line per ledger item:
   `VERIFIED`, `CORRECTED`, `REJECTED`, or `UNRESOLVED`, plus what changed.
   For an empty stub, write `DRAFT AUDIT — empty stub; no inherited claims`.
4. LINKS TO VERIFY — every `[[wikilink]]` basename
5. TAGS — tag line plus any proposed new leaf
6. DOCS READ — official URLs actually opened, version/section. If none, the card is incomplete
7. UNCERTAINTIES — if any remain, **keep `#New`** and list them

If any checklist line is FAIL, fix before finishing. If you cannot fix without guessing, keep `#New`.

When the Docker fill orchestrator sends a **repair** turn with validator
problems, treat that as the same FAIL: patch the listed files now. A missing
`> [!warning]` is a real failure — add a documented pitfall; do not restore
`#New` to bypass it. URLs belong in chat DOCS READ, not in the `.md`. The
orchestrator re-validates and either accepts or sends another repair; it does
not stop the tag for a shape miss.

When `--limit` is 2–3, or a named cluster is larger: fetch the shared official
docs once, then finish and self-check one card before writing the next. Do not
stop after the first card.

## Coverage index

After you create, fill, retag, or delete SRS cards (or edit the Tags.md tree), run:

```
python .cursor/skills/process-topic/scripts/rebuild-coverage-index.py
```

## Do not

- Fill from dump/blog wording without official verification.
- Treat a draft as evidence, silently omit one of its substantive claims, or
  report only the claims retained in the final answer.
- Leave `Untrusted draft`, `Unverified traps`, `Dump:`, or legacy draft markers
  after removing `#New`.
- Strip `#New` while uncertainties remain.
- Import new questions (`/import-repo`) or invent extra cues (`/cover-tag`).
- Edit `Tags.md` except proposing a leaf in chat.
---
