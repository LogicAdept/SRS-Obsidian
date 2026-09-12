<!--
reps: 0
priority: 0
-->
#DataFormats/Documents/CSS #SRS

# What CSS attribute selectors exist?

> [!abstract] Short answer
> **Attribute selectors match elements by the presence or value of any attribute: `[attr]` exists, `[attr=v]` exact, `[attr~=v]` whitespace-separated word, `[attr|=v]` hyphen-prefix, `[attr^=v]` starts-with, `[attr$=v]` ends-with, `[attr*=v]` contains - optionally with an `i` or `s` flag for case handling.**

## The seven forms

```css
[disabled]            { opacity: .6; }        /* has the attribute */
[type="checkbox"]     { accent-color: red; }  /* exact value */
[class~="logo"]       { padding: 2px; }       /* one word in a space-separated list */
[lang|="en"]          { font-variant: east-asian; }  /* en or en-* */
[href^="https://"]    { }                     /* value starts with */
[href$=".pdf"]        { }                     /* value ends with */
[title*="error"]      { }                     /* value contains the substring */
[href$=".org" i]      { font-style: italic; } /* case-insensitive match */
```

**Listing 1.** All forms; `[attr|=v]` matches `en` or `en-US` but not `enu` - the hyphen boundary matters.

The `~=` form is the semantic sibling of the class selector: the class attribute is just a space-separated list, so `.logo` is syntactically sugar for `[class~="logo"]` (see [[What is a CSS selector]]). The case flags are appended before the closing bracket: `i` makes the comparison case-insensitive, `s` forces case-sensitivity.

> [!warning] ^= and *= look alike and behave differently
> `[href^="/docs"]` anchors the match at the start of the whole value; `[href*="/docs"]` finds the substring anywhere - including in a query parameter, which is usually not what you meant. Attribute selectors also see *markup*, not state: they match whatever the HTML (or JavaScript) has written into the attribute, so they cannot observe user interaction - that is the job of pseudo-classes like `:checked`, see [[What is a CSS pseudo-class]].

Attribute selectors carry class-level specificity (0-1-0) in the cascade, same as classes and pseudo-classes.

```d2
direction: right
attr: "href="/docs/intro.html"" {
  width: 280
  height: 80
  style.fill: "#e3f2fd"
}
starts: "[href^="/docs"] matches\n(anchor at start)" {
  width: 290
  height: 90
  style.fill: "#e8f5e9"
}
contains: "[href*="docs"] matches\n(substring anywhere)" {
  width: 290
  height: 90
  style.fill: "#fff3e0"
}
ends: "[href$=".html"] matches\n(anchor at end)" {
  width: 280
  height: 90
  style.fill: "#fff3e0"
}
attr -> starts
attr -> contains
attr -> ends
```

**Fig. 1.** One attribute value, three positional tests: the caret anchors at the start, the dollar at the end, the star searches anywhere.

> [!tip] Interview answer
> **Seven forms: presence, exact =, word ~=, hyphen-prefix |=, starts-with ^=, ends-with $=, contains *=, plus the i/s case flags. The ~= variant matches one word of a space-separated list - it is what the class selector compiles to - and ^= anchors at the start while *= searches anywhere.**
