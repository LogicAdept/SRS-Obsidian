<!--
reps: 0
priority: 0
-->
#DataFormats/Documents/CSS #SRS

# What is the difference between an ID selector and a class selector in CSS?

> [!abstract] Short answer
> **`#id` selects the one element whose `id` attribute equals the value; `.class` selects every element whose `class` attribute contains the token.** The id must be unique in the document and contributes specificity 1-0-0, while a class contributes 0-1-0 and may repeat across - and within - elements.

## Semantics and syntax

```html
<p id="intro" class="lead emphasized">First paragraph</p>
<p class="lead">Second paragraph</p>
```

```css
#intro        { border: 2px solid red; }   /* matches the single element */
.lead         { font-style: italic; }      /* matches both paragraphs */
li.spacious.elegant { margin: 2em; }       /* an element may carry several classes */
```

**Listing 1.** One id, multiple classes; the id addresses a specific node, classes address membership groups.

Syntactically - but not specificity-wise - `#demo` is equivalent to the attribute selector `[id="demo"]`, per MDN. The class attribute itself is a space-separated token list, so `.red` matches `class="red hot"`; see [[What is a CSS selector]] for the matching rules and [[What CSS attribute selectors exist]] for the raw attribute forms.

```d2
direction: right
q: "One DOM node to style?" {
  width: 250
  height: 80
  style.fill: "#e3f2fd"
}
id: "#id: unique, specificity 1-0-0\nJS hook, fragment target" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}
cls: ".class: reusable token, 0-1-0\nmany elements, many per element" {
  width: 310
  height: 90
  style.fill: "#e8f5e9"
}
q -> id: "yes"
q -> cls: "a group"
```

**Fig. 1.** The decision in one picture: a unique node versus a reusable membership group.

> [!warning] Ids in stylesheets back you into a corner
> Because an id rule out-specifies any number of class rules, an `#id` selector can only be beaten by another id, `!important`, or inline styles - the classic reason CSS codebases rot. The working convention: style with classes (and pseudo-classes/attributes, also 0-1-0), keep ids for JavaScript `getElementById` hooks, `<a href="#fragment">` targets (see [[How do you specify a hyperlink destination in HTML]]), and form-label `for` associations. HTML5 tolerates several equal ids only in the sense that the parser accepts the markup - selector, scripting, and accessibility behavior is undefined by design.

> [!tip] Interview answer
> **The id selector addresses exactly one element - ids are document-unique - and carries specificity 1-0-0; the class selector matches every element containing the token in its class list, can repeat freely, and carries 0-1-0. Style with classes; reserve ids for JS and fragment links because id specificity blocks overrides.**
