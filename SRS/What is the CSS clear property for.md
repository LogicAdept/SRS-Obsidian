<!--
reps: 0
priority: 0
-->
#DataFormats/Documents/CSS #SRS

# What is the CSS clear property for?

> [!abstract] Short answer
> **`clear` forces an element to move below ("clear") floated elements that precede it** - MDN: it specifies "whether an element must be moved below floating elements that precede it". Values: `none` (default), `left`, `right`, `both`; the property applies to floating and non-floating elements alike.

## The float-clearing mechanism

```css
img.pull { float: left; }      /* following text wraps around the image */
p.after { clear: both; }       /* this paragraph starts below any floated box */
```

**Listing 1.** A floated image lets text wrap; the cleared paragraph refuses to wrap and drops below it.

Floats are removed from normal flow: block boxes overlap the float's box while *line boxes* shorten to wrap around it. `clear` belongs to the wrapping problem - it constrains the cleared element's own box to start below the relevant floats, on the chosen side or both.

```d2
direction: right
float: "Float removed from flow\nline boxes wrap around it" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}
wrap: "Sibling without clear\ntext wraps beside the float" {
  width: 290
  height: 90
  style.fill: "#e3f2fd"
}
clearp: "Sibling with clear: both\nbox pushed below the float" {
  width: 310
  height: 90
  style.fill: "#e8f5e9"
}
float -> wrap: "no clear"
float -> clearp: "clear set"
```

**Fig. 1.** Same float, two sibling behaviors: wrapping continues unless the element clears.

> [!warning] clear prevents wrapping but does not contain floats
> A cleared *sibling* drops below the float, but the float's *parent* still collapses to zero height if it holds only floated children - the classic broken-footer layout. Containing floats needs `display: flow-root` on the parent (or the old clearfix hack), which is a different mechanism than `clear`. And remember context: floats and clears were the layout system of the 2000s; in modern flex and grid layouts children do not leave the flow, so `clear` is mostly for text-wrap-around cases (pull quotes, images in articles) - see [[What is the difference between margin and padding in CSS]] for the spacing tools that layout actually uses, and [[What is CSS]] for how floats interact with the cascade-era box model.

> [!tip] Interview answer
> **clear pushes an element below preceding floats - left, right, or both - so it stops wrapping beside them. It solves the sibling case; a collapsing parent needs flow-root or clearfix instead. It is a float-era property, still correct for wrap-around text, unnecessary in flex and grid layouts.**
