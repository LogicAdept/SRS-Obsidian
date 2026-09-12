<!--
reps: 0
priority: 0
-->
#DataFormats/Documents/CSS #SRS

# What is the difference between 0 and auto in the CSS margin property?

> [!abstract] Short answer
> **`0` is a fixed zero margin; `auto` means "compute from the free space".** In normal block flow, horizontal `auto` margins absorb the leftover width (this is how a fixed-width block gets centered with `margin: 0 auto`), while vertical `auto` resolves to `0`. In flex and grid layouts, `auto` margins absorb free space along the corresponding axis - including vertically.

## The resolution rules

```css
.card {
  width: 600px;
  margin: 0 auto;   /* left and right margins split the free space */
}
.hero {
  margin-top: auto; /* normal block flow: computes to 0 */
}
```

**Listing 1.** The classic centering idiom and the vertical case that surprises people.

The math for horizontal centering: the used width of the containing block minus `width` minus borders and paddings leaves free space; `margin-left: auto; margin-right: auto` distributes it equally between the two sides. If `width` is also `auto` - the default - there is no free space to distribute, and auto margins compute to zero: auto centering only works on a box with a definite width (or a fitting `fit-content` size), which is exactly the nuance the draft phrasing "auto means 0 when width is also auto" captures.

```d2
direction: right
mode: "Layout context?" {
  width: 220
  height: 80
  style.fill: "#e3f2fd"
}
block: "Block flow\nhorizontal auto: split free space\nvertical auto: 0" {
  width: 330
  height: 100
  style.fill: "#fff3e0"
}
flex: "Flex / grid\nauto absorbs free space\non its axis (both directions)" {
  width: 330
  height: 100
  style.fill: "#e8f5e9"
}
mode -> block
mode -> flex
```

**Fig. 1.** The same keyword resolves differently by context - and the flex case is the modern interview follow-up.

> [!warning] margin: auto is not "the centering property"
> In a flex container, `margin-left: auto` on an item pushes it to the far end of the main axis - auto margins become an alignment tool that can even beat `justify-content`, because alignment distributes space between items while auto margins concentrate it inside the item's own margins. And `margin: 0 auto` does nothing on an element whose width fills the container: no free space, nothing to distribute. Vertical centering in normal flow needs other tools (flex `align-items`, grid `place-items`) - auto margins alone cannot do it there. For the box geometry behind the computation see [[What is the difference between margin and padding in CSS]], and for where the containing-block width comes from see [[What is the difference between div and span]].

> [!tip] Interview answer
> **0 is a literal zero; auto means resolve from free space. In block flow that only works horizontally - auto side margins split the remaining width and center a fixed-width box, vertical auto is 0. In flex and grid, auto margins absorb free space along their axis, so margin-top: auto actually pushes an item down.**
