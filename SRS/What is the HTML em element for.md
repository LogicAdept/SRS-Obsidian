<!--
reps: 0
priority: 0
-->
#DataFormats/Documents/HTML #SRS

# What is the HTML em element for?

> [!abstract] Short answer
> **`<em>` marks stress emphasis - the words that would be spoken with emphasis - and its meaning moves with placement: "I *love* HTML" and "I love *HTML*" say different things.** It is phrasing-content semantics, not decoration; browsers render it in italics, but italics are a side effect, not the definition.

## Emphasis changes the sentence

```html
<p>I <em>love</em> code review.</p>   <!-- whoever says it, loves it -->
<p><em>I</em> love code review.</p>   <!-- contrasts with someone else who does not -->
```

**Listing 1.** Same words, moved emphasis, different meaning - the reason the element exists at the phrase level.

The standard contrasts `em` with `<i>`: `i` marks text in an alternative voice or mood - a term being defined, a taxonomic name, a foreign phrase, a ship name - where the italics are typographic convention rather than spoken stress. Neither is a heading; neither conveys importance, which is `<strong>` (severity and urgency), a different axis again. Choosing between them is a semantic decision the CSS cannot make retroactively: a span styled italic announces nothing to a screen reader or a search indexer.

```d2
direction: right
text: "Text to mark up" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
em: "<em>: spoken stress" {
  width: 230
  height: 80
  style.fill: "#fff3e0"
}
i: "<i>: alternative voice\n(foreign word, term)" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
strong: "<strong>: importance" {
  width: 240
  height: 80
  style.fill: "#e8f5e9"
}
text -> em
text -> i
text -> strong
```

**Fig. 1.** Three italic-adjacent marks with different meanings; the choice is about semantics, not the visual result.

> [!warning] Nested em multiplies the stress level
> Emphasis nests: an `em` inside an `em` increases the relative stress, per the standard. The common abuses - using `em` for entire paragraphs (no emphasis survives when everything is emphasized) or styling italics manually with CSS while stripping the element - both destroy the semantics that screen readers and text-to-speech rely on to modulate delivery.

The same structure-over-decoration principle drives the rest of phrasing content: prefer `em`, `strong`, `i`, and friends over spans plus CSS whenever the text has a voice (see [[What is the difference between div and span]] for the generic container fallback and [[What is HTML]] for where phrasing content sits in the tree).

> [!tip] Interview answer
> **em conveys stress emphasis whose meaning depends on which words it wraps; the italic rendering is incidental. Use i for alternative-voice typographic italics like foreign terms, strong for importance, and em for the word a speaker would stress - nesting em raises the stress level.**
