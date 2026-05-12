# SRS file naming rules

This note is the **canonical specification** for how SRS flashcard files are named in this vault. Other format notes (for example [[GoldStandard]]) **link here** instead of duplicating rules.

## Purpose

- **Spaced repetition (SRS)** — during review, the **cue** you see first should be the **question**.
- The **file basename** (name without `.md`) is that cue: an **English interrogative or question-shaped line**, not a generic topic slug.
- **Obsidian wikilinks** `[[…]]` resolve to note titles (usually the basename unless you override the display title). Match the **link text** to how the note is titled in your vault so links do not break after renames.

## Scope

- These rules apply to **SRS flashcard notes** (cards you drill with `#SRS` and the meta/tags/body layout from [[GoldStandard]]).
- They do **not** require this policy file’s own filename to equal its H1; `Naming.md` is documentation, not a drill card.

## Language

- **Basename: English only.** No Cyrillic or other non-Latin scripts in the filename.
- Card **body** language follows [[GoldStandard]] (English by default).

## Word separator

- Use **spaces** in the basename (Obsidian-style), for example `What is a hash map.md`.

## Basename and cue

- The **basename** (without `.md`) is the **review cue** in the file list and matches the default note title in Obsidian. The **first `#` heading** in the body **does not** have to duplicate the basename — use it for a short in-note title, a section label, or structure as you prefer.
- **Imperative history lines** (e.g. Russian «Расскажи про X», «Опиши X») should become an **English question cue** when you create the file, not a literal “Tell me about X” filename, unless you explicitly want that register for a deck (not the default here).

## Punctuation and Windows filenames

- On Windows, these characters **must not** appear in a basename: `\ / : * ? " < > |`
- Therefore the ASCII **`?` must not** appear in the basename (or anywhere in it). Question shape comes from words: **What / How / Why / When / Which**, etc.

## Case

- Use **sentence case** for the full line (first word capitalized; proper nouns and acronyms as in English: `JVM`, `SQL`, `Dijkstra's algorithm`).

## Question-shaped templates (by knowledge type)

Pick **one** primary pattern per card type so the deck feels consistent. Trailing `?` is omitted everywhere (see above).

| Type | Primary basename pattern | Examples (basename only) |
|------|-------------------------|---------------------------|
| Definition | `What is …` | `What is a hash map`, `What is idempotency` |
| Mechanism / behavior | `How does … work` or `What happens when …` | `How does HashMap get work`, `What happens when you call wait without holding the monitor` |
| Comparison | `What is the difference between X and Y` | `What is the difference between final and static` |
| Rationale / trade-off | `Why …` or `When should you use …` | `Why is String immutable`, `When should you use a LinkedList` |
| Procedure / how-to | `How do you …` | `How do you configure a DataSource in Spring` |

If two patterns both fit, prefer **definition** (`What is …`) for “term explains” cards and **mechanism** for runtime or step-by-step behavior.

## Glossary and named patterns (narrow exception)

- For **widely fixed names** (for example **Enterprise Integration Patterns** channel/pattern names), you may use a **short canonical English title** as basename **without** a `What is` prefix, **only** when the cue you want in review is **recognition of that name** (e.g. `Dead Letter Channel`, `Request-Reply`).
- Treat this as an **exception class**: add new short names here sparingly; prefer `What is the Dead Letter Channel pattern` if you want a verbal question cue instead.
- Keep **official spelling and hyphens** from the source (e.g. `Event-Driven Consumer`, `Content-Based Router`).

## “X vs Y” cues

- Default: use a full question, e.g. `What is the difference between HashMap and TreeMap`.
- A short `X vs Y` basename is allowed **only** if you document it as an intentional cue style for a subset of cards; otherwise avoid it.

## Length and readability

- Aim for roughly **80–120 characters** in the basename as a soft limit; shorten by removing filler words while keeping the question unambiguous.
- No leading/trailing spaces; avoid a trailing `.` before `.md`.

## Duplicates and collisions

- If two history lines map to the **same** English question: **one file**; merge or drop the duplicate line in your tracking list.
- If two different cards need similar titles: add a **short English disambiguator** in parentheses, e.g. `What does this code print (2)` — ASCII digits and parentheses are fine on Windows.

## Code and APIs in the basename

- **Do not** put Markdown backticks in the filename.
- Write readable English around the API, e.g. `What does equals and hashCode contract require` instead of `` `equals()` `` in the filename.

## Typos in the source list

- The **canonical English basename fixes** obvious typos from `SRS/NamesHistory/md-file-names.txt` (or any import list). Optionally note the original typo once in the card body.

## Workflow: adding a card from a history line

1. Open a line in `SRS/NamesHistory/md-file-names.txt` (or your export of it).
2. Decide **which question** that line is asking — that is the SRS **cue**.
3. Write the **same question in English**, following the templates and punctuation rules above.
4. Search the vault for an existing `.md` with that basename to avoid duplicates.
5. Create **`English question.md`** with meta/tags and body per [[GoldStandard]]; the first `#` heading does **not** need to repeat the basename.
6. On **rename**, use Obsidian’s option to **update wikilinks** (or fix links manually). Renames break `[[old title]]` if not updated.

## Examples (history line → basename)

| Source line (from history) | Canonical basename (no `.md`) |
|----------------------------|-------------------------------|
| Расскажи про HashMap | What is a HashMap |
| В чём разница между ArrayList и LinkedList | What is the difference between ArrayList and LinkedList |
| What is Merge Sort | What is merge sort |
| Dead Letter Channel | Dead Letter Channel *(glossary exception)* or What is the Dead Letter Channel pattern *(preferred if you want a verbal cue)* |

## Risks

- **Renaming** files breaks existing `[[links]]` — batch-rename with care and backups.
- Too many different question openers without a pattern can make the deck feel noisy; stick to the table above unless you extend this note.

## See also

- [[GoldStandard]] — card language, structure, and wikilink usage.
