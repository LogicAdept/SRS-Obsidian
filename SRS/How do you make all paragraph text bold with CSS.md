<!--
reps: 0
priority: 0
-->
#DataFormats/Documents/CSS #SRS

# How do you make all paragraph text bold with CSS?

> [!abstract] Short answer
> **Select the paragraphs and set `font-weight: bold` - or the numeric equivalent `font-weight: 700`:**

```css
p { font-weight: bold; }     /* keyword, equal to 700 */
p { font-weight: 700; }      /* numeric scale 1..1000 */
```

**Listing 1.** Both forms target every `<p>` in the document; the type selector needs no class.

`font-weight` is a numeric property: `400` is the keyword `normal`, `700` is `bold`, and intermediate values select intermediate faces when the font provides them - modern variable fonts expose the whole 1-1000 range. The relative keywords `bolder` and `lighter` step from the parent's weight instead of naming an absolute one.

> [!warning] bold is a request, and the font decides what renders
> The browser maps the requested weight to the closest face the loaded font actually has. A family shipped without a bold face gets **synthetic bold** - the engine smears the regular glyphs - which looks blurry and uneven against real bold type. Also, `font-weight` and `<strong>` are not interchangeable: `strong` marks *importance* in the markup semantics (see [[What is the HTML em element for]] for the emphasis sibling), while the CSS property only changes appearance - screen readers announce `strong` and ignore a styled span.

If the goal is emphasis that means something, wrap the words in `strong`; if the goal is uniform visual styling of paragraphs - a design decision - the CSS rule above is the right tool (see [[What is a CSS selector]] for how the `p` type selector matches).

## How the browser picks the face

```d2
direction: right
req: "font-weight: 700 requested" {
  width: 250
  height: 80
  style.fill: "#e3f2fd"
}
face: "Loaded font provides\na bold face?" {
  width: 250
  height: 80
  style.fill: "#fff3e0"
}
real: "Real bold face renders" {
  width: 240
  height: 80
  style.fill: "#e8f5e9"
}
synth: "Engine synthesizes bold\n(smearing regular glyphs)" {
  width: 290
  height: 90
  style.fill: "#ffebee"
}
req -> face
face -> real: yes
face -> synth: no
```

**Fig. 1.** The weight request is resolved against the loaded font; a missing bold face degrades to synthetic bold.

Also mind the inheritance angle: `font-weight` inherits, so setting it on `body` cascades everywhere and the rule for `p` only needs to deviate from that default - one more reason the property, not markup styling, is the correct place for typographic policy.

> [!tip] Interview answer
> **p { font-weight: bold } - or 700 on the 1-1000 numeric scale, with bolder/lighter relative to the parent. The rendering depends on the font's available faces: without a bold face the browser fakes it. And styling is not semantics - use strong when the text is actually important.**
