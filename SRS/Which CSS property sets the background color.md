<!--
reps: 0
priority: 0
-->
#DataFormats/Documents/CSS #SRS

# Which CSS property sets the background color?

> [!abstract] Short answer
> **`background-color` sets the background color of an element's box** - it accepts color values (named, hex, `rgb()`, `hsl()`), its initial value is `transparent`, and the painted area extends under the padding and border by default (controlled by `background-clip`).

## Values and painting area

```css
.callout {
  background-color: coral;              /* named */
  background-color: #ff7f50;            /* hex 6-digit */
  background-color: #ff7f5080;          /* hex with alpha */
  background-color: rgb(255 127 80 / 50%);
  background-color: hsl(16 100% 66%);
}
```

**Listing 1.** The same color in four notations; the 4- and 8-digit hex forms and the slash syntax carry alpha.

The color is painted behind the element's content and padding and - unless `background-clip: padding-box` says otherwise - beneath a translucent border. For the visible result remember the layering: `background-color` sits at the bottom of the background stack, under `background-image` layers, and the `background` shorthand resets every background property, including the color, to its initial value when not specified.

> [!warning] The background shorthand silently resets the color
> `background: url(bg.png);` does not "add an image" - it resets `background-color` to `transparent` and every other longhand to its initial value, so a color set by an earlier, weaker rule disappears the moment this rule wins. Either include the color in the shorthand (`background: url(bg.png) no-repeat #fff;`) or write the longhand. The same reset-on-shorthand trap applies to the `font` shorthand (see [[How do you make all paragraph text bold with CSS]]).

For the text itself the property is `color`; the pair `color` + `background-color` must keep sufficient contrast for readability and accessibility - the same reasoning that makes [[Is the alt attribute required on an HTML img element]] matter: information must not live in styling alone.

## Which box area gets painted

```d2
direction: right
content: "content box" {
  width: 200
  height: 80
  style.fill: "#e8f5e9"
}
padding: "padding - painted" {
  width: 220
  height: 80
  style.fill: "#fff3e0"
}
border: "border - painted\nunless clipped" {
  width: 230
  height: 80
  style.fill: "#fff3e0"
}
margin: "margin - never painted" {
  width: 240
  height: 80
  style.fill: "#ffebee"
}
content -> padding
padding -> border
border -> margin
```

**Fig. 1.** The background color fills content and padding by default and reaches under the border; the margin area stays transparent.

> [!tip] Interview answer
> **background-color is the property; it takes named, hex, rgb(), or hsl() colors, defaults to transparent, and paints under content, padding, and border per background-clip. The classic trap: the background shorthand resets the color - include it in the shorthand or use longhands.**
