<!--
reps: 0
priority: 0
-->
#Example/Canonical #SRS

# Gold-standard SRS card

> [!abstract] What this note is
> A **sample SRS card** in Obsidian: meta → tags → body, **callouts** of several kinds, **wikilinks** `[[…]]`, a **D2** diagram, and code. How blocks look (icons, colors) is controlled by the Obsidian **theme**.

The same ideas in more detail: first **meta** and **tags** (keep order **meta → tags → body**), then **H1/H2**, text, **callouts** as needed; link related topics with **[[spaced repetition]]** and other wikilinks.

> [!tip] Quick read of the card
> By **callout type** you can tell the role: `abstract` — gist, `tip` — remember this, `warning` — pitfall; `quote` and `example` — for a quote and a worked **example inside the text**, not as a caption under a diagram or listing.

> [!note] Footnotes `[^…]` vs callouts
> A **Markdown footnote** ends up **at the bottom of the page**. A note **next to a paragraph** should be a **callout** (`info`, `note`, `tip`, …), not `[^id]`.

> [!success] Wording
> Use **clear card language** (usually neutral, conversational register): no bureaucratese, tautology, unnecessary calques, or empty “decorated” phrasing. Callout titles and **H2** headings should be **specific** to the block; if it sounds awkward aloud, rewrite it.

> [!info] Language
> **Write SRS cards in English** by default: one style across the vault, fewer mixed-language titles, and alignment with **IT** (APIs, docs, code, and interview questions are mostly English). Russian (or another language) is fine for a dedicated language-learning deck or when the learning goal is explicitly tied to that language.

## Document structure

1. **Meta** — at the top of the file, inside `<!-- … -->`: only **`reps`**, **`priority`**.
2. **Tags** — one line; **`#SRS`** is required; the rest are topic tags `#…`.
3. **Body** — **`#` / `##`**, lists, **wikilinks**, **callouts** (pick `!…` types by meaning — full list in the SRS format note), **D2**, **code**; right under a diagram or code block use a **plain Markdown caption** (“Fig. N.”, “Listing N.” and one or two sentences), **not** a callout.
4. **Wording** — same **language bar** as in the callout above: clarity over ornament; apply the same style to paragraphs and to lines like “Fig. N.” under a figure.
5. **File name** — SRS card basenames are the review **cue** (English question text). Rules: [[Naming]].

## Wikilinks (`[[…]]`)

- **No extra emphasis on linked titles** — other notes referenced in **wikilinks** must not be styled with bold, italics, inline code, or other Markdown inside or around the link. The **only** markup that marks a cross-file reference is the **pair of double square brackets** (`[[note title]]`), not decorations on the title.
- **Why link** — wikilinks exist to **compose related topic nodes** into a coherent subgraph and to **increase semantic understanding** of the vault: nearby ideas stay connected, and the graph reflects how concepts relate.

> [!warning] Common mistake
> Do **not** mix in HTML for styling in the body — Markdown and callouts are enough. A second explanatory callout or paragraph goes **below** this block at the same nesting level in the document — **do not** nest callouts inside callouts (see the SRS format note).

## Block order (diagram)

The layout is **illustrative**: file order goes left to right, so this D2 uses **`direction: right`** (see the D2 section in the format note: direction follows content and readability). Nodes set **`width` / `height`** so the preview is not too small.

```d2
direction: right
meta: "1. HTML comment\nreps · priority" {
  width: 240
  height: 130
  style.fill: "#e3f2fd"
}

tags: "2. One # line\nincludes #SRS" {
  width: 240
  height: 130
  style.fill: "#fff3e0"
}

body: "3. Markdown\nheadings, lists, code…" {
  width: 240
  height: 130
  style.fill: "#e8f5e9"
}

meta -> tags
tags -> body
```

**Fig. 1.** **Block order:** meta in `<!-- … -->` → tag line → main Markdown (callouts, D2, code).

## Mapping meta fields to code

You can mirror **`reps`** and **`priority`** from the header in code — e.g. a **`record`** and a static **`fresh()`** method.

```java
public record CardMeta(int reps, double priority) {
    public static CardMeta fresh() {
        return new CardMeta(0, 0);
    }
}
```

**Listing 1.** **`CardMeta`** matches the meta fields. **`fresh()`** is the same initial state as **`reps: 0`** and **`priority: 0`** in the comment.

> [!tip]
> **`reps` and `priority`:** **`reps`** — how many successful reviews have been recorded (exact rules live in vault policy). **`priority`** — a number for **ordering** the queue after each pass; update formula — same policy.
