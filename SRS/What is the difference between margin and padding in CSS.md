<!--
reps: 0
priority: 0
-->
#DataFormats/Documents/CSS #SRS

# What is the difference between margin and padding in CSS?

> [!abstract] Short answer
> **Padding is the space *inside* the element - between its content and its border; margin is the space *outside* the border, pushing neighbors away.** Padding is painted by the background and included in the clickable area; margin is always transparent and never part of the box's hit area.

## Where each one lives

```css
.button {
  padding: 12px 24px;    /* content-to-border gap: grows the visible box */
  margin: 0 0 16px 0;    /* border-to-neighbor gap: reserves surrounding space */
}
```

**Listing 1.** Padding enlarges the element's own box; margin creates distance without changing its size.

```d2
direction: right
content: "content" {
  width: 150
  height: 70
  style.fill: "#e8f5e9"
}
pad: "padding\n(painted, clickable)" {
  width: 220
  height: 80
  style.fill: "#fff3e0"
}
border: "border" {
  width: 130
  height: 70
  style.fill: "#e3f2fd"
}
marg: "margin\n(transparent, not clickable)" {
  width: 260
  height: 80
  style.fill: "#ffebee"
}
content -> pad
pad -> border
border -> marg
```

**Fig. 1.** The CSS box model in one chain - margin sits outside the border, padding inside it.

Three behavioral differences follow. First, **collapsing**: adjacent vertical margins of block boxes merge into the larger of the two, while paddings never collapse - which is why spacing between stacked sections collapses but a button's padding never vanishes. Second, **signs**: negative margins are legal and pull elements together or overlap them; negative padding is impossible. Third, **auto**: `margin: auto` absorbs free space (centering), while padding has no auto value - see [[What is the difference between 0 and auto in the CSS margin property]].

> [!warning] Padding participates in the hit area and the background
> A link or button's padding belongs to its clickable region and receives its background color - padding is how you make a small text into a comfortably tappable control. Margin does neither. Misreading this produces "my margin is white but my padding is colored" confusion: the background paints the padding box (per `background-clip`, see [[Which CSS property sets the background color]]), never the margin box.

Percentages in both properties resolve against the *inline size* (width) of the containing block - even for top and bottom - a symmetry trap when people expect height-relative vertical percentages.

> [!tip] Interview answer
> **Padding is inside the border: painted by the background, part of the click area, never negative, never collapsing. Margin is outside: transparent, not clickable, can be negative, and adjacent vertical margins collapse into the larger one. Auto margins absorb free horizontal space for centering - padding has no auto.**
