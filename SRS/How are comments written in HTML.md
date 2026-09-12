<!--
reps: 0
priority: 0
-->
#DataFormats/Documents/HTML #SRS

# How are comments written in HTML?

> [!abstract] Short answer
> **An HTML comment is delimited by `<!--` and `-->`.** The parser ignores everything between them, so comments can annotate markup or temporarily remove elements. The syntax has exact rules: the opening is the four-character string `<!--`, the closing is `-->`, comments never nest, and the text inside may not contain the sequence `-->` or `--!>`.

## Syntax and rules

```html
<!-- One-line comment -->
<!--
  Multi-line comment:
  <p>This paragraph is disabled.</p>
-->
<p>Visible text</p>
```

**Listing 1.** Commenting out markup - the commented-out element is not parsed into the DOM.

The WHATWG syntax prescribes the format precisely: the text must not start with `>` or `->`, must not contain `<!--`, `-->`, or `--!>`, and must not end with `<!-`. Notably, the text *is* allowed to end with `<!` - a legal oddity from the standard.

> [!warning] Comments do not nest and are not stripped everywhere
> A nested `<!--` inside a comment closes it early at the first `-->`, and the rest becomes visible markup. Also, inside **raw-text elements** (`<script>`, `<style>`) and RCDATA elements (`<title>`, `<textarea>`) the parser treats `<!--` as ordinary text - CSS and JavaScript have their own comment syntax (`/* */` and `//`), which is why [[How do you comment code in JSP]]-style server-side templating needs different care in generated scripts. For escaping visible characters see [[What is an HTML character entity]].

## What comments are for

Comments are authoring aids: section markers, removal notes, TODOs. They travel to the client - the browser never strips them from the delivered source, so anything placed in a comment is visible via View Source. Conditional comments of the IE era (`<!--[if IE]>`) are dead: modern parsers treat them as plain comments and ignore the content in every browser.

```d2
direction: right
src: "Source: <!-- draft --> <p>Hi</p>" {
  width: 300
  height: 80
  style.fill: "#e3f2fd"
}
state: "Tokenizer in comment state" {
  width: 270
  height: 80
  style.fill: "#fff3e0"
}
dom: "DOM: only the <p> element" {
  width: 270
  height: 80
  style.fill: "#e8f5e9"
}
src -> state
state -> dom: "at first -->"
```

**Fig. 1.** The comment ends at the first `-->` and never becomes a DOM node; everything after it parses normally.

## Practical limits

Because comments ship to the client, they must not carry secrets, internal hostnames, or review notes you would not show users. Build tools and minifiers strip them from production bundles, which is why license headers and version markers placed in comments are the ones that survive - and why debugging a stripped page differs from debugging the source you wrote.

> [!tip] Interview answer
> **HTML comments are <!-- ... --> blocks the parser skips. They cannot nest, cannot contain -->, and everything inside stays in the delivered source. Inside script, style, title, and textarea the sequence is not a comment at all - those elements have their own text-processing rules.**
