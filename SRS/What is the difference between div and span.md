<!--
reps: 0
priority: 0
-->
#DataFormats/Documents/HTML #SRS

# What is the difference between div and span?

> [!abstract] Short answer
> **Both are generic containers with no built-in meaning; the difference is content model and default rendering. `<div>` is a flow (block-level) container that starts its own line and may hold paragraphs, lists, and other divs; `<span>` is a phrasing (inline-level) container for text inside a paragraph.** Use them only when no semantic element fits.

## Block versus inline

```html
<div class="card">
  <h2>Plan</h2>
  <p>Use the <span class="keyword">flex</span> layout for this row.</p>
</div>
```

**Listing 1.** The div groups a whole block of content; the span marks a fragment inside the sentence.

MDN defines `div` as "the generic container for flow content" with "no effect on the content or layout until styled in some way using CSS", and `span` as "the generic inline container for phrasing content" that "should be used only when no other semantic element is appropriate". Wrapping a paragraph inside a `span` is invalid - phrasing content cannot contain flow content - while a `div` inside a `<p>` implicitly closes the paragraph.

```d2
direction: right
card: "<div class=card>\nblock container" {
  width: 260
  height: 90
  style.fill: "#e3f2fd"
}
h2: "<h2> heading" {
  width: 170
  height: 70
  style.fill: "#e8f5e9"
}
p: "<p> paragraph" {
  width: 170
  height: 70
  style.fill: "#e8f5e9"
}
span: "<span> keyword\ninline fragment" {
  width: 190
  height: 80
  style.fill: "#fff3e0"
}
card -> h2
card -> p
p -> span
```

**Fig. 1.** Nesting shapes the choice: div holds blocks, span lives inside text flow.

> [!warning] Generic does not mean first-resort
> Both elements are the last stop, not the default: the standard's own guidance is to prefer semantic elements - `<article>`, `<nav>`, `<header>`, `<strong>`, `em` - and reach for div/span when nothing matches. Div-soup makes stylesheets brittle and the document unreadable for assistive technology, because a class name carries none of the semantics an element would.

See [[What is the HTML em element for]] for inline semantics and [[What is HTML]] for how these containers sit in the document tree.

> [!tip] Interview answer
> **div and span are both semantically empty hooks for styling and scripting; div is block-level flow content, span is inline phrasing content. Span cannot legally wrap block content. Reach for semantic elements first and use these two only when nothing else represents the grouping.**
