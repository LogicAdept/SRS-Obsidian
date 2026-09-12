<!--
reps: 0
priority: 0
-->
#DataFormats/Documents/CSS #SRS

# What is a CSS selector?

> [!abstract] Short answer
> **A CSS selector is the pattern at the start of a rule that determines which elements the declarations apply to** - MDN defines selectors as "patterns used to match, or select, the elements you want to style". The engine evaluates the pattern against every element in the DOM; the same syntax also drives `querySelector` in JavaScript.

## Anatomy of matching

```css
li.spacious.elegant { margin: 2em; }
```

**Listing 1.** A compound selector: it matches an `li` whose class attribute contains both `spacious` and `elegant` - the order of tokens in the attribute is irrelevant.

Selectors range from a simple type (`p`), class (`.x`), or id (`#x`) to complex patterns joined by **combinators**: a descendant combinator (space), child `>`, next-sibling `+`, and subsequent-sibling `~`. A selector list separated by commas applies one rule to several patterns. The full catalog - more than sixty selector kinds - lives in the selectors module; see [[What main kinds of CSS selectors exist]] for the taxonomy and [[What CSS attribute selectors exist]] for one family in detail.

```d2
direction: right
rule: "Ruleset" {
  width: 170
  height: 70
  style.fill: "#e3f2fd"
}
sel: "Selector pattern" {
  width: 230
  height: 80
  style.fill: "#fff3e0"
}
dom: "DOM tree walk\nmatch test per element" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}
decl: "Declarations apply\n(cascade decides conflicts)" {
  width: 270
  height: 80
  style.fill: "#e8f5e9"
}
rule -> sel
sel -> dom
dom -> decl: "matched"
```

**Fig. 1.** The selector is a filter between the stylesheet and the DOM; only matched elements receive the declarations.

> [!warning] A class selector matches tokens, not "the class"
> `.red` matches every element whose `class` attribute *contains the token* `red` among its space-separated list - `class="red hot"` matches, and so does a `<div>` as well as a `<p>`. Newcomers expect the selector to name a kind of element or a unique object; it names a token in an attribute. Specificity, not order of appearance alone, decides which competing selector wins.

> [!tip] Interview answer
> **A selector is the matching pattern of a CSS rule - simple selectors like type, class, and id, optionally chained by combinators into complex patterns. The engine matches it against every DOM element and applies the declarations to the hits; the same mini-language is reused by querySelector.**
