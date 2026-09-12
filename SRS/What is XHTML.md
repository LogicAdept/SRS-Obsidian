<!--
reps: 0
priority: 0
-->
#DataFormats/Documents/HTML #SRS

# What is XHTML?

> [!abstract] Short answer
> **XHTML is HTML written to satisfy XML rules - an XML serialization of the hypertext markup.** It enforces XML well-formedness (every element closed, quoted attributes, lowercase names, one root with a namespace) and, when served as `application/xhtml+xml`, is parsed by a strict XML parser that aborts on the first error instead of guessing.

## What becomes stricter

```html
<!-- HTML: tolerant -->
<br>
<p>Text <b>bold

<!-- XHTML: every one of these is a well-formedness error -->
<br />
<p>Text <b>bold</b></p>
```

**Listing 1.** HTML recovers from unclosed tags; the XML parser refuses the document outright.

The XML rules that bite in practice: empty elements must be self-closed (`<br />`, `<img ... />`), attribute values must be quoted, attribute names are lowercase (XML is case-sensitive), elements must nest - never overlap - and the root element must carry the XHTML namespace declaration on the `<html>` element. An XHTML file may begin with an XML declaration `<?xml version="1.0" encoding="UTF-8"?>`.

> [!warning] Serving XHTML as text/html makes it just HTML
> Most "XHTML" pages of the 2000s were served as `text/html`, which makes browsers use the ordinary HTML parser - all the XML strictness existed only in the authors' heads. Real XHTML needs the `application/xhtml+xml` MIME type (see [[What is a MIME type]]), and then any single parse error yields a yellow XML error page instead of a rendered document - the trade-off that ultimately made the tolerant HTML parser the survivor.

History in one line: XHTML 1.0 (2000) reformulated HTML 4.01 as an XML application and came in three flavors - Transitional, Strict, and Frameset; XHTML 1.1 dropped the Transitional conveniences and went fully modular, and the planned XHTML 2 was abandoned when browser vendors backed the WHATWG's tolerant living standard instead. HTML5 kept an XML serialization as a secondary syntax for tooling pipelines, but documents on the web went back to the HTML syntax. See [[What is XML]] for the base rules and [[What is HTML]] for the tolerant model that won.

## When XML serialization still makes sense

Machine-to-machine markup benefits from strictness: templates processed by XML tools, feeds consumed by parsers, or documents assembled by build systems can use the XHTML serialization and gain well-formedness checks - a typo fails the build instead of rendering a subtly wrong page in a browser. For human-facing pages the tolerant parser plus a validator delivers the same correctness with a friendlier failure mode.

> [!tip] Interview answer
> **XHTML is HTML under XML well-formedness: closed and self-closed elements, quoted lowercase attributes, namespace on the root. Served as application/xhtml+xml it is parsed strictly and fails loudly; served as text/html it degrades to plain HTML parsing. That strictness is why the industry returned to the tolerant HTML standard.**
