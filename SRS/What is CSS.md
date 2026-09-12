<!--
reps: 0
priority: 0
-->
#DataFormats/Documents/CSS #SRS

# What is CSS?

> [!abstract] Short answer
> **CSS (Cascading Style Sheets) is the declarative style-sheet language that describes the presentation of documents written in a markup language such as HTML.** Rules pair selectors with declarations, and the *cascade* - plus specificity and inheritance - resolves conflicts when several rules target the same element. HTML carries structure; CSS carries appearance.

## Rules, declarations, and where they live

```css
p {
  color: #222;
  line-height: 1.6;
}
```

**Listing 1.** A ruleset: the selector `p` followed by declarations - each a property, a colon, and a value.

Stylesheets reach the document three ways: an external file linked from the head (see [[What is the HTML head element for]]), an embedded `<style>` block, and the per-element `style` attribute. The external stylesheet is the standard choice because one file can style every page of a site and the browser can cache it.

```d2
direction: right
html: "HTML document\nstructure only" {
  width: 230
  height: 90
  style.fill: "#e3f2fd"
}
css: "CSS rules\npresentation" {
  width: 210
  height: 90
  style.fill: "#fff3e0"
}
dom: "Styled rendering\nstyle -> element match" {
  width: 260
  height: 90
  style.fill: "#e8f5e9"
}
html -> dom
css -> dom: "selector matches"
```

**Fig. 1.** CSS attaches to the parsed document: each selector matches DOM elements and applies its declarations.

## The cascade

When multiple rules set the same property on the same element, the winner is decided by origin and importance, then by specificity, then by source order - the mechanism that gives the language its name. Inheritance spreads values (mostly typographic ones) down the tree so you set a font once on the root. Beyond author styles there is a **user-agent stylesheet**: the browser's built-in defaults, which is why an unstyled heading is large and bold (see [[What is the difference between div and span]] for elements whose only default is display type).

> [!warning] CSS is presentation, not structure
> Two related lies: "CSS is easy" (the cascade and layout models are genuinely intricate) and "style it with HTML attributes" (presentational markup like `bgcolor` is obsolete). Markup carries meaning - [[What is the HTML em element for]] stresses words whether or not CSS loads - and the stylesheet should never be the only carrier of information; a document without its stylesheet must still read coherently.

> [!tip] Interview answer
> **CSS is the style-sheet language of the web: selectors match elements, declarations set properties, and the cascade resolves conflicts by origin, specificity, and order, with inheritance spreading typographic values. It describes only presentation - the HTML stays structural, and the browser's user-agent stylesheet supplies the defaults.**
