<!--
reps: 0
priority: 0
-->
#DataFormats/Documents/HTML #SRS

# What are the HTML dl dt and dd elements for?

> [!abstract] Short answer
> **`<dl>` builds a description list: `<dt>` marks a term and `<dd>` marks its description.** It is the element pair for glossaries, metadata key-value display, FAQs, and any term-association structure - semantically an association list, not a visual table.

## Structure

```html
<dl>
  <dt>HTTP</dt>
  <dd>An application protocol for distributed hypermedia systems.</dd>

  <dt>URL</dt>
  <dt>URI</dt>
  <dd>A character string locating a resource.</dd>
</dl>
```

**Listing 1.** One term with one description, then two terms sharing one description - both groupings are legal.

The rules the parser enforces: `dt` must precede its `dd` or `dt` siblings inside the `dl`; a `dt` group may have several consecutive terms and several descriptions per group. What a `dl` must *not* be used for is marking up dialogue or plain content that is not a term-description association - the standard spells out that a conversation is not a description list.

> [!warning] dl is not a layout grid
> A common abuse is wrapping generic label-value UI in `dl` because it indents nicely. Screen readers announce the list semantics, so a checkout form assembled from `dl`/`dt`/`dd` reads out as a glossary. Form controls belong in a `<form>` with `<label>`; `dl` is for publishing associations, such as specification metadata (see [[What is a MIME type]] for a real registry of name-value pairs) or glossaries alongside [[What is an HTML character entity]]-style terminology.

Browsers render `dt` bold and `dd` indented by default - which is pure stylesheet legacy, not semantics; reset it freely with CSS.

```d2
direction: right
dl: "<dl> association list" {
  width: 240
  height: 80
  style.fill: "#e3f2fd"
}
dt: "<dt> term\n(HTTP)" {
  width: 190
  height: 80
  style.fill: "#fff3e0"
}
dt2: "<dt> term\n(URL, URI)" {
  width: 190
  height: 80
  style.fill: "#fff3e0"
}
dd: "<dd> description" {
  width: 200
  height: 80
  style.fill: "#e8f5e9"
}
dl -> dt
dl -> dt2
dt -> dd
dt2 -> dd: "one description\nfor two terms"
```

**Fig. 1.** Terms and descriptions associate in order: each dd describes the dt or dt-group before it.

> [!tip] Interview answer
> **dl is the description-list element: dt holds a term, dd holds its description, and several of each may group together. It encodes term-association semantics for glossaries and metadata; it is not a layout device and not for dialogue.**
