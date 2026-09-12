<!--
reps: 0
priority: 0
-->
#DataFormats/Documents/CSS #SRS

# What main kinds of CSS selectors exist?

> [!abstract] Short answer
> **The selector families are: type, class (`.x`), id (`#x`), attribute (`[attr]`), universal (`*`), pseudo-classes (`:hover`), and pseudo-elements (`::before`), plus combinators (space, `>`, `+`, `~`) that chain selectors by DOM relationships and a comma list that groups them.** Each family also carries its own specificity weight.

## The taxonomy with examples

```css
p            { }   /* type */
.menu        { }   /* class */
#main        { }   /* id */
[href]       { }   /* attribute */
*            { }   /* universal */
:hover       { }   /* pseudo-class */
::before     { }   /* pseudo-element */
nav a        { }   /* descendant combinator */
nav > a      { }   /* child combinator */
h2 + p       { }   /* next-sibling combinator */
h2 ~ p       { }   /* subsequent-sibling combinator */
h1, h2       { }   /* selector list */
```

**Listing 1.** One line per family; in practice selectors combine, as in `ul.menu > li:first-child`.

```d2
direction: right
sel: "Selectors" {
  width: 170
  height: 70
  style.fill: "#e3f2fd"
}
simple: "Simple: type, .class, #id,\n[attr], * (universal)" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}
pseudo: "Pseudo-classes :hover, :nth-child()\nPseudo-elements ::before, ::first-line" {
  width: 330
  height: 90
  style.fill: "#fff3e0"
}
comb: "Combinators: descendant, > child,\n+ next sibling, ~ subsequent sibling" {
  width: 340
  height: 90
  style.fill: "#e8f5e9"
}
sel -> simple
sel -> pseudo
sel -> comb
```

**Fig. 1.** Three groups to memorize: what an element is, what state or sub-part it has, and where it sits relative to others.

> [!warning] Specificity differs per family - id is not "a stricter class"
> The cascade weighs selectors: type = 0-0-1, class/attribute/pseudo-class = 0-1-0, id = 1-0-0. One `#id` rule beats any number of class rules, which is why utility-class systems forbid ids in stylesheets: an id rule becomes impossible to override without `!important` or another id. Combinators contribute nothing themselves - only the compound selectors they join count. See [[What is the difference between an ID selector and a class selector in CSS]] for the id-class trade and [[What is a CSS pseudo-class]] for the colon family.

> [!tip] Interview answer
> **There are simple selectors - type, class, id, attribute, universal - plus pseudo-classes for state and pseudo-elements for sub-parts, chained with combinators: descendant, child >, next sibling +, subsequent sibling ~, and grouped with commas. Remember the specificity ladder: type below class below id.**
