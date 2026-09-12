<!--
reps: 0
priority: 0
-->
#DataFormats/Documents/CSS #SRS

# What is a CSS pseudo-class?

> [!abstract] Short answer
> **A pseudo-class is a colon-prefixed keyword that selects elements by state or by tree position without needing extra markup** - `:hover` for pointer-over state, `:first-child` for position, `:nth-child(An+B)` for patterns. Functional pseudo-classes take arguments in parentheses; the element before the colon is the anchor.

## State and structure

```css
button:hover        { background: #eee; }   /* pointer is over it */
input:focus         { outline: 2px solid; } /* keyboard focus */
li:first-child      { font-weight: 700; }
tr:nth-child(odd)   { background: #f6f6f6; } /* An+B notation: 2n+1 */
li:not(.active)     { color: gray; }         /* functional negation */
```

**Listing 1.** Interaction states, structural position, and negation - all without touching the HTML.

MDN groups pseudo-classes into families: interaction-state (`:hover`, `:active`, `:focus`), structural (`:first-child`, `:last-child`, `:only-child`, `:nth-child()`), form-related (`:checked`, `:disabled`, `:valid`), and document-level (`:root`, `:lang()`). They compose freely with other selectors - `li.menu-item:nth-child(2)` is one compound pattern (see [[What main kinds of CSS selectors exist]]).

> [!warning] A pseudo-class is not a pseudo-element
> One colon = state of an existing element (`:hover`); two colons = a manufactured sub-part of the document (`::before`, `::first-line`) introduced by the CSS3 notation change. Writing `:before` still works for legacy reasons, but the two categories are different things - and `:hover` itself is unreliable on touch screens, where there is no hover pointer: mobile browsers apply it on tap or not at all, so never hide essential actions behind hover-only affordances.

`querySelector` in JavaScript consumes the same syntax, so a selector written for CSS works for DOM queries verbatim - with the caveat that a script snapshot is not a live match the way a stylesheet rule is. For the id-versus-class trade-off see [[What is the difference between an ID selector and a class selector in CSS]], and for the matching model itself see [[What is a CSS selector]].

## Why pseudo-classes exist at all

They keep state out of the markup. Without them, every hover effect or zebra row would require JavaScript to add and remove classes as the pointer moves - exactly what the draft DOM of a naive implementation looks like. Because the browser tracks the real state, the rules stay declarative: the element's *condition* is part of the selector, not a class someone toggles. That is also the direction modern additions take - `:focus-visible` distinguishes keyboard focus from pointer focus, and `:has()` lets a selector express relationships to descendants and following siblings that CSS could not see before.

```d2
direction: right
state: "Element state changes\n(pointer, focus, checked)" {
  width: 290
  height: 90
  style.fill: "#e3f2fd"
}
match: "Pseudo-class re-evaluates\n:rule applies or stops" {
  width: 280
  height: 90
  style.fill: "#fff3e0"
}
paint: "Rendered style updates\n(no markup change)" {
  width: 270
  height: 90
  style.fill: "#e8f5e9"
}
state -> match
match -> paint
```

**Fig. 1.** The browser re-evaluates pseudo-class matches as state changes - the DOM never changes.

> [!tip] Interview answer
> **A pseudo-class is a colon keyword that matches by state or structure - hover, focus, nth-child, not() - without adding classes to markup. Functional ones take arguments in An+B or selector form; two colons mean a pseudo-element instead, which is a different category. Hover-based UI fails on touch devices.**
