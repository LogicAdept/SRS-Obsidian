<!--
reps: 0
priority: 0
-->
#DataFormats/Documents/HTML #SRS

# What are the HTML ol ul and li elements for?

> [!abstract] Short answer
> **`<ol>` is an ordered (numbered) list, `<ul>` an unordered (bulleted) list, and `<li>` is the list item inside either.** The choice is semantic, not visual: use `ol` when the sequence of items carries meaning - steps, rankings, procedures - and `ul` when it does not, such as navigation menus or feature lists.

## Ordered lists and their attributes

```html
<ol start="3" reversed>
  <li>Third place</li>
  <li value="7">Seventh place - jump here</li>
</ol>
```

**Listing 1.** `start` sets the first number, `reversed` counts down, and `value` on a specific `li` renumbers from that point.

Only `ol` accepts `start`, `reversed`, and the `type` numbering style; only `li` inside `ol` accepts `value`. Nesting lists means placing a whole `ol` or `ul` inside a parent `li` - a nested list is a child of the item, not a sibling.

```html
<ul>
  <li>Coffee
    <ul>
      <li>Espresso</li>
      <li>Filter</li>
    </ul>
  </li>
  <li>Tea</li>
</ul>
```

**Listing 2.** A nested unordered list; the inner list lives inside the outer li.

> [!warning] The list semantics are announced, so do not fake them
> Removing bullets with `list-style: none` does not remove the list semantics - but Safari's VoiceOver historically stopped announcing a `ul` as a list in exactly that case, which is why navigation menus sometimes need an explicit role. The inverse mistake is worse: building "lists" from `<div>`s plus dash characters loses ordering information, keyboard list navigation, and the announced item count (the same accessibility logic as [[Is the alt attribute required on an HTML img element]]).

For term-description pairs use `dl` instead - see [[What are the HTML dl dt and dd elements for]].

> [!tip] Interview answer
> **ol is for order-significant items and supports start, reversed, and per-item value; ul is for unordered groups like menus; li is the item for both. The choice is semantic - assistive technology and search engines read the difference - and nesting means putting the inner list inside an li.**
