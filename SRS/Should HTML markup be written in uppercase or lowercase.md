<!--
reps: 0
priority: 0
-->
#DataFormats/Documents/HTML #SRS

# Should HTML markup be written in uppercase or lowercase?

> [!abstract] Short answer
> **Functionally it does not matter for HTML itself: tag and attribute names in the HTML syntax are ASCII case-insensitive, so `<DIV>` and `<div>` are the same element.** The convention - followed by the standard's own examples and by every serializer - is lowercase, and there are places where case suddenly does matter: XML-based documents and foreign content such as inline SVG and MathML.

## What the standard actually says

The WHATWG syntax defines case-insensitivity for the HTML syntax precisely: tag names, attribute names, and unquoted/quoted attribute *names* match ASCII letters regardless of case. It is deliberately narrow - "case-insensitive" means only ASCII upper and lower alphas, not full Unicode folding.

```html
<DIV CLASS="warning">Identical to the lowercase form</DIV>
<div class="warning">Identical to the uppercase form</div>
```

**Listing 1.** Both lines parse to the same element with the same class attribute.

Values are a different story: attribute *values* are case-sensitive data. `class="Warning"` and `class="warning"` select differently in [[What is CSS]], URL paths differ by case on most servers, and `id` values are matched exactly. In documents written to the XML rules - see [[What is XHTML]] - even tag names are case-sensitive, so the freedom exists only inside the HTML syntax.

> [!warning] Three places where case is load-bearing
> 1. **Foreign elements**: inline `<svg>` uses camelCase attributes like `viewBox` and `gradientTransform` - lowercasing them breaks rendering, because foreign content is parsed with XML case rules. 2. **XHTML/XML serialization**: XML is case-sensitive, so `<DIV>` in an XHTML document is an unknown element. 3. **CSS selectors on classes and ids**: the values match byte-for-byte even though the attribute *name* does not.

## Why lowercase won

Lowercase is the convention because it survives the round trip: the HTML parser normalizes tag names to lowercase internally, the standard's `innerHTML` serializer emits lowercase, and mixed-case authoring makes diffs and code review noisy. HTML-as-shipped is written, read, and diffed by humans, so a single convention - the one the standard's own examples use - beats expressing mood through case. The one mainstream exception in style was the old XHTML-era "uppercasing makes markup easier to scan" school; it never survived contact with tooling, validators, or copy-paste from serializers.

For the same reason style guides pair this rule with quoting attribute values consistently: conventions exist so that the parser's leniency is never load-bearing in review. See [[What is HTML]] for the parsing model that makes this leniency safe.

> [!tip] Interview answer
> **HTML tag and attribute names are ASCII case-insensitive, so the browser treats DIV and div identically - but lowercase is the universal convention. Case becomes critical for attribute values (exact match), for XML/XHTML documents, and for foreign content like SVG where viewBox must keep its camelCase.**
