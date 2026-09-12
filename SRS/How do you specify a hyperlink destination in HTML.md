<!--
reps: 0
priority: 0
-->
#DataFormats/Documents/HTML #SRS

# How do you specify a hyperlink destination in HTML?

> [!abstract] Short answer
> **The destination of a hyperlink is the value of the `href` attribute on an `<a>` element** - any URL: absolute, relative, or a fragment reference to an id on the same page. An `<a>` without `href` is not a link; with `href` it becomes focusable and navigable.

## Absolute, relative, and fragment destinations

```html
<a href="https://example.com/docs">Absolute URL</a>
<a href="about/team.html">Relative URL</a>
<a href="/prices">Root-relative URL</a>
<a href="#contacts">Fragment: scroll to id="contacts"</a>
<p id="contacts">Contact block</p>
```

**Listing 1.** Four destination kinds; the fragment navigates within the document to the element with a matching id.

The target of a fragment link is any element whose `id` equals the fragment. The legacy way to define an in-page target was the `name` attribute on `<a>`; modern HTML uses `id` on any element, and the `name` attribute is obsolete for this purpose.

> [!warning] href is what makes the anchor a link
> An `<a>` element without `href` is a "placeholder link": it is not focusable, not activated by Enter, and screen readers announce it as plain text. Adding `href` gives the element link semantics; `target="_blank"` then opens the destination in a new browsing context. Relative destinations resolve against the document's base URL, which `<base href>` can override.

## How the browser resolves the destination

For a relative value the browser resolves it against the current document URL, then navigates (see [[What happens when you type a URL into a browser and press Enter]] for the full pipeline). The same `<a>` element also carries other URL schemes: `mailto:` opens the mail client (see [[How do you create a mailto link in HTML]]) and `tel:` dials a number.

```d2
direction: right
click: "User activates <a href>" {
  width: 240
  height: 80
  style.fill: "#e3f2fd"
}
kind: "Destination form?" {
  width: 210
  height: 70
  style.fill: "#fff3e0"
}
abs: "absolute/relative URL\nnavigate to document" {
  width: 250
  height: 90
  style.fill: "#e8f5e9"
}
frag: "#fragment\nscroll to element id" {
  width: 220
  height: 90
  style.fill: "#e8f5e9"
}
click -> kind
kind -> abs
kind -> frag
```

**Fig. 1.** One attribute, two resolution paths: full navigation or in-page scroll.

> [!tip] Interview answer
> **The link destination lives in the href attribute of an anchor: absolute or relative URL for navigation, #fragment for jumping to an element by id on the same page. Without href an anchor is not a link at all - no focus, no activation. Legacy name-based anchors are replaced by id.**
