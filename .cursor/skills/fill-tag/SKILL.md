---
name: fill-tag
description: >-
  Fills existing SRS cards for a chosen tag to GoldStandard using official
  documentation, Naming, and Tags. Use when the user invokes /fill-tag or asks
  to complete #New cards under a tag from primary docs.
disable-model-invocation: true
---

# Fill cards by tag

## Purpose

Fill cards for a chosen tag to GoldStandard, Naming, and Tags. Always rely on official documentation.

## Invoke

```
/fill-tag <tag> [--limit N]
```

- `<tag>` required: tree path or short name. Resolve via `SRS/Format/Tags.md`.
- `--limit` optional: cards to finish this run. Default **1**. Never more than **3** unless the user lists specific cues.

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

If the user names explicit cues, use those instead of scanning the tag.

## Official sources only

Before writing, **search and fetch** official/original docs for that cue. Memory is not evidence. If the web is unreachable, keep `#New` and stop.

Primary, in order:

- Language/platform spec and vendor JavaDoc (JLS, Java SE API, OpenJDK source)
- Product reference (Spring `docs.spring.io`, Kafka `kafka.apache.org`, SQL vendor docs)
- JEPs, JSRs, RFCs, ISO/SQL when they define the behavior

Not primary: Baeldung, Medium, Wikipedia, Stack Overflow, interview dumps, blogs. If only those exist, keep `#New`.

Read the defining section (contract, spec paragraph, implementation), not a snippet. Note version.

## Drafts are clues, not facts

If the card has an untrusted-draft warning (`Untrusted draft`, or a legacy Russian equivalent) or dump text:

1. Treat every claim — especially dump traps / “gotchas” — as a hypothesis.
2. Verify each against official docs or original source.
3. Keep a trap only when it is real; rewrite it as a precise `warning`.
4. Drop dump prose. The finished card must not say it was copied from a dump.
5. Fine points omitted by docs (implementation branches, self-invocation, hash vs index) are allowed **only** after reading the implementation or spec that shows them.

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

Depth: HashMap/equals gold example, not an 8-line stub. Yes/no language cues may match gold example 1.

Adversarial pass (FillCardPrompt §E): counterexample every `always`/`never`; implementation claims from real branches; listings compile or are labeled Conceptual; immutability/thresholds include preconditions.

Do not invent biographies.

## Output (chat + files)

Write the complete `.md` into `SRS/<Cue>.md` (cue already is the basename). Then in **chat only** (never inside the file):

1. Filename
2. CHECKLIST PASS/FAIL per FillCardPrompt §G line, with a short quote proving each PASS
3. LINKS TO VERIFY — every `[[wikilink]]` basename
4. TAGS — tag line plus any proposed new leaf
5. DOCS READ — official URLs actually opened, version/section. If none, the card is incomplete
6. UNCERTAINTIES — if any remain, **keep `#New`** and list them

If any checklist line is FAIL, fix before finishing. If you cannot fix without guessing, keep `#New`.

When `--limit` is 2–3: finish and self-check one card before the next.

## Coverage index

After you create, fill, retag, or delete SRS cards (or edit the Tags.md tree), run:

```
python .cursor/skills/process-topic/scripts/rebuild-coverage-index.py
```

## Do not

- Fill from dump/blog wording without official verification.
- Strip `#New` while uncertainties remain.
- Import new questions (`/import-repo`) or invent extra cues (`/cover-tag`).
- Edit `Tags.md` except proposing a leaf in chat.
---
