<!--
reps: 0
priority: 0
-->
#DataFormats/Documents/CSS #SRS

# How do you remove underlines from all links with CSS?

> [!abstract] Short answer
> **`a { text-decoration: none; }` removes the underline from every link.** The property is the shorthand for the line-decoration longhands; the underline itself comes from the browser's user-agent stylesheet for `a[href]`, and the declaration overrides it.

## The property family

```css
a { text-decoration: none; }          /* remove the line */

a { text-decoration-line: underline;
    text-decoration-color: red;
    text-decoration-style: wavy;
    text-decoration-thickness: 2px; } /* the longhands the shorthand composes */
```

**Listing 1.** The shorthand and its parts; `line-through` for strikethrough and `overline` come from the same property.

The `text-decoration` shorthand resets all four longhands - the same reset trap as the `background` shorthand (see [[Which CSS property sets the background color]]): a later `text-decoration: underline;` also resets color and style to their initial values.

```d2
direction: right
ua: "User-agent stylesheet\na { text-decoration: underline }" {
  width: 320
  height: 90
  style.fill: "#e3f2fd"
}
author: "Author rule\na { text-decoration: none }" {
  width: 290
  height: 90
  style.fill: "#fff3e0"
}
cascade: "Cascade: same origin, same specificity\nsource order decides" {
  width: 320
  height: 90
  style.fill: "#e8f5e9"
}
paint: "Link renders without the line" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
ua -> cascade
author -> cascade
cascade -> paint
```

**Fig. 1.** No magic: the author rule wins by source order in the cascade, not by being "stronger".

> [!warning] The underline is a usability signal, not decoration
> Users scan for underlined text as the cue for clickability - links are distinguished by underline plus color (see [[Which CSS property sets the background color]] for how the background stays untouched here; `text-decoration` draws a line, `color` changes the text). Removing the underline without replacing the signal (distinct color, weight, or hover treatment) measurably harms usability and accessibility, and never remove it from body-text links in prose. Style links in `:hover`/`:focus` states too, or the affordance disappears exactly when users reach for it.

Note the selector: a bare `a` also matches anchors without `href` - placeholder links that render nothing link-like; `a[href]` or `a:link` is the precise target, see [[What is a CSS pseudo-class]] for the state pseudo-classes.

> [!tip] Interview answer
> **a { text-decoration: none } - the shorthand resets its longhands, so later shorthand rules drop custom color and style. The underline comes from the user-agent stylesheet, so this is a plain cascade override. Keep some other clickable signal, and target a[href] rather than a bare a.**
