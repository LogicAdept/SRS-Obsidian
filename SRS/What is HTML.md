<!--
reps: 0
priority: 0
-->
#DataFormats/Documents/HTML #SRS

# What is HTML?

> [!abstract] Short answer
> **HTML (HyperText Markup Language) is the markup language that describes the meaning and structure of web content.** Elements such as headings, paragraphs, lists, links, and images tell the browser what each piece of content *is*; the browser parses them into the DOM tree and renders them. Presentation is delegated to [[What is CSS]]-style styling and behavior to JavaScript, so HTML by itself carries no layout or logic.

## Elements, tags, and attributes

An HTML document is a tree of **elements** written with **tags**. A start tag may carry **attributes** - name-value pairs that configure the element. Void elements such as `<img>` or `<br>` have no end tag and no children.

```html
<a href="https://example.com" target="_blank">Go</a>
<img src="logo.png" alt="Company logo">
```

**Listing 1.** A normal element with two attributes and a void element with required attributes.

The document skeleton is fixed: a `<!DOCTYPE html>` preamble, one root `<html>` element, and its two children `<head>` and `<body>` (see [[What is the HTML head element for]]).

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Page title</title>
  </head>
  <body>
    <p>Visible content.</p>
  </body>
</html>
```

**Listing 2.** The minimal skeleton every HTML document shares.

## Hypertext and the document model

"Hypertext" refers to the links that connect documents - the `<a>` element is the founding feature of the Web. The browser does not render the markup text directly: the parser tokenizes tags, builds the **DOM** tree, and the rendering engine lays out that tree. This is why malformed markup still renders - the HTML parser has a defined error-recovery algorithm, unlike an XML parser that aborts on the first well-formedness error.

> [!warning] HTML is not a programming language
> HTML has no control flow, variables, or computation - it declares structure and semantics. Cards like [[What is the difference between methods GET and POST]] describe transport semantics that HTML links merely trigger; the logic lives in JavaScript on top of the DOM.

## Where HTML sits

HTML defines **what content means**: a heading, a list, tabular data, a quotation. How it looks is the job of CSS, and what it does is the job of scripts - the classic separation of structure, presentation, and behavior. The current language is the living WHATWG HTML standard, commonly called **HTML5** and after it simply "HTML".

> [!tip] Interview answer
> **HTML is the declarative markup language of the Web: it describes the structure and semantics of a document as a tree of elements. The browser parses it into the DOM and renders it; CSS styles it and JavaScript makes it interactive. It is not a programming language, and its parser is deliberately error-tolerant.**
