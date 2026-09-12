<!--
reps: 0
priority: 0
-->
#DataFormats/Documents/CSS #SRS

# How are comments written in CSS?

> [!abstract] Short answer
> **A CSS comment is everything between `/*` and `*/` - the only comment syntax the language has.** Comments may span lines, may sit between rules and declarations, and do **not** nest: the first `*/` closes the comment.

## Syntax and placement

```css
/* Section: buttons */
.btn {
  color: white;          /* keep contrast above 4.5:1 */
  /* background: blue;   <- disabled while the redesign lands */
  background: navy;
}
```

**Listing 1.** A comment above a rule, beside a declaration, and temporarily disabling a declaration.

Because there is no nesting, a comment containing the text `*/` - for example when commenting out a block that itself contains comments - terminates early and leaks the rest as broken syntax. The standard trick for commenting out commented code is to alternate delimiters (`/* ... */ /* ... */`) or use editor tooling; minifiers also strip every comment except ones starting with `/*!`, kept for license notices.

> [!warning] The JavaScript habits do not transfer
> There is no `//` single-line comment in CSS: typing one invalidates the declaration it appears in and, depending on position, swallows the rest of the rule until the parser can recover - a silent style break. The same applies inside the `<style>` element and the `style` attribute: the HTML parser does not treat `<!--` as a comment there (see [[How are comments written in HTML]] for where that sequence *is* a comment), and the `style` attribute accepts only declarations, so comments there are at best tolerated trivia and commonly a bug. CSS custom properties, selectors, and at-rules all expect the `/* */` form exclusively (see [[What is CSS]] for where comments sit in the stylesheet grammar).

## What comments are used for in real stylesheets

Beyond disabling declarations, comment sections carry three legitimate loads: file headers with authorship and license (`/*! ... */` survives minification), section dividers that mirror the page's component structure, and documented intent - *why* a magic number exists, which browser quirk a rule works around, which ticket introduced it. The last one matters most: CSS has no type system to express intent, so the comment is the only place the reasoning lives. Commented-out declarations are the weakest use - version control remembers - but they remain the standard way to A/B a value while iterating in the browser devtools.

One more placement rule: a comment is allowed anywhere whitespace is allowed - between declarations, inside a value between tokens (`margin: 1px /* note */ 2px;` is legal) - but not inside a string literal or an identifier, where the characters are just data. When a comment must travel with minified output, the `/*!` banner is the only survivor; everything else is build-time only.

> [!tip] Interview answer
> **Only /* ... */ - multiline allowed, no nesting, the first */ wins, and // is not a CSS comment at all: it breaks the declaration. Minifiers strip comments except /*! license banners. The HTML comment syntax inside style or the style attribute is not a comment.**
