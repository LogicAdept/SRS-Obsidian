<!--
reps: 0
priority: 0
-->
#DataFormats/Documents/CSS #SRS

# How do you set red color for all elements with class red in CSS?

> [!abstract] Short answer
> **`.red { color: red; }` - the class selector matches every element whose `class` attribute contains the token `red`, and the `color` property sets the text color.** No element-type prefix is needed: the rule applies to paragraphs, spans, table cells, anything carrying the class.

## The rule and what it matches

```html
<p class="red">Red paragraph</p>
<span class="badge red hot">Red span, also hot</span>
<td class="red">Red cell</td>
```

```css
.red { color: red; }            /* matches all three elements */
```

**Listing 1.** The class attribute is a space-separated token list; `red` may sit anywhere in it.

`color` sets the *text* (foreground) color and inherits - so descendants without their own color turn red too. It does not touch the background (that is `background-color`, see [[Which CSS property sets the background color]]). Values may be keywords, hex, `rgb()`, or `hsl()`: `red` equals `#ff0000` and `rgb(255 0 0)`.

> [!warning] Naming a class after a color bakes paint into markup
> `.red` couples the stylesheet to the markup: a redesign that turns "red" items green either rewrites HTML or makes the class name lie. Production conventions prefer semantic names (`.error`, `.highlight`, `.danger`) that survive restyling - the class carries *meaning*, the stylesheet decides the paint. Also remember the selector matches a token, so `.red` on an element with `class="redesign"` does not match (tokens are whole words), but any element with the token does - including ones you never intended; scope with a compound selector like `.error.red` or a parent prefix when needed (see [[What is a CSS selector]] and [[What main kinds of CSS selectors exist]]).

## Why the property inherits

```d2
direction: right
rule: ".red { color: red }" {
  width: 220
  height: 80
  style.fill: "#fff3e0"
}
el: "<span class=red>" {
  width: 200
  height: 80
  style.fill: "#e3f2fd"
}
child: "child text nodes and\ndescendants inherit color" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}
rule -> el
el -> child: "inheritance"
```

**Fig. 1.** `color` inherits down the subtree, so one class colors every descendant until a more specific rule overrides it.

That inheritance is the reason a red class on a container recolors headings and links inside it - and the reason link styles from the user-agent stylesheet need their own rules to stay visible. The same inherited-property reasoning explains why [[How do you make all paragraph text bold with CSS]] works by setting one property rather than marking up each word.

> [!tip] Interview answer
> **.red { color: red } - the class selector matches any element containing the red token in its class list, and color paints the text and inherits to descendants. Prefer semantic class names over color names: the markup states what the thing is, the stylesheet states how it looks.**
