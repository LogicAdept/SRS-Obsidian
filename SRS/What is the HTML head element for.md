<!--
reps: 0
priority: 0
-->
#DataFormats/Documents/HTML #SRS

# What is the HTML head element for?

> [!abstract] Short answer
> **`<head>` is the machine-readable metadata container of the document** - it must be the first child of `<html>`, before `<body>`, and its content is not rendered as page content. It holds the title, character-set declaration, viewport configuration, stylesheet and script references, favicon, and base URL.

## What belongs inside

```html
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Checkout - Shop</title>
  <link rel="stylesheet" href="/styles/main.css">
  <script src="/js/app.js" defer></script>
  <base href="/shop/">
</head>
```

**Listing 1.** Typical head: charset first, then viewport, the required title, and resource references.

The `<title>` element is the one head member users actually see - as the browser tab text, bookmarks, and search-result headline; the document must have exactly one. `<meta charset>` declares the character encoding and should sit within the first 1024 bytes so the parser can decode the rest of the file correctly.

> [!warning] head is not a header
> The visible page header - logo, navigation banner - is `<header>`, a body element. `<head>` renders nothing itself; confusing the two is a classic interview slip. Also, `<meta charset>` placed too late or a duplicated title are real conformance errors, and stylesheets loaded in head block rendering until fetched, which is why scripts usually take the `defer` attribute there.

## Why the head/body split exists

The split separates **information about the document** from **the document's content**. Machine consumers - the rendering engine, search crawlers, social-media link previewers - read head metadata; the human reads the body. See [[What is HTML]] for the document tree and [[What is a MIME type]] for how the delivered document declares its type.

```d2
direction: right
html: "<html>" {
  width: 160
  height: 70
  style.fill: "#e3f2fd"
}
head: "<head>: title, meta, link, script, base" {
  width: 330
  height: 80
  style.fill: "#fff3e0"
}
body: "<body>: rendered content" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
html -> head: "first child"
html -> body: "second"
```

**Fig. 1.** The skeleton split: head carries metadata for machines, body carries content for people.

> [!tip] Interview answer
> **head is the metadata container: title (required, exactly one), charset and viewport metas, stylesheet and script references, favicon, base URL. It must precede body, renders nothing, and is not the same element as the visible header. Scripts in head typically use defer to avoid blocking parsing.**
