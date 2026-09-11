<!--
reps: 0
priority: 0
-->
#Java/JSP #DataFormats/Documents/HTML #SRS

# Can you use JavaScript inside a JSP page?

> [!abstract] Short answer
> **Yes as client-side script in the HTML (or other) response; no as the JSP scripting language.** `<script>` markup is **template data**: the translator does not recognize it, so it is written to `out` and the **browser** runs it. `<% … %>`, `<%! … %>`, and `<%= … %>` are **Java** (JSP **4.0** `language` is only `java`). JavaScript in the page never executes in the JSP container.

## Two runtimes, one file

A JSP page is **elements** the container knows (directives, actions, scripting, EL) plus **template data** — everything else. Typical template data is text or XML/HTML fragments. At request time that text is `out.print(template)` (whitespace kept). An HTML `script` element in that stream is ordinary markup: omit `type` (or use a JavaScript MIME type) and it is a **classic script** the user agent evaluates; `src` fetches an external file instead of the element’s text. The JSP engine is finished before that happens. What a JSP is: [[What is Java Server Pages JSP]]. Java vs JavaScript as languages: [[How are JavaScript and Java related if at all]].

JSP **4.0** defines **`java`** as the only `page` `language` value (lowercase, case-sensitive). Other language names are reserved; a container may experiment, but that is **not portable**. `scripting-invalid` bans **JSP** scriptlets/declarations/expressions. It does **not** strip HTML `<script>` from the response. Scriptless pages: [[What are practical guidelines for working with JSP]].

EL (`${…}` in template text) **is** processed inside a `<script>` block: it is evaluated as a **String** when the response is rendered, then the resulting characters go to the client. `#{}` in template text is a **translation error** unless deferred syntax is turned off. Turn EL off with `isELIgnored` / `el-ignored` if the script must contain raw `${`: [[How do you disable Expression Language in JSP]].

```d2
direction: down
jsp: "*.jsp\n<template> + JSP elements" {
  width: 280
  height: 48
  style.fill: "#fff8e1"
}
out: "_jspService → out.print\nHTML including <script>" {
  width: 300
  height: 48
  style.fill: "#e8f5e9"
}
ua: "user agent\nclassic / module script" {
  width: 280
  height: 48
  style.fill: "#e3f2fd"
}
jsp -> out: "server, Java"
out -> ua: "HTTP response"
```

**Fig. 1.** JavaScript in a JSP is **payload**, not a JSP scripting element.

```jsp
<%-- Conceptual — Jakarta Pages 4.0; HTML script is template data --%>
<%@ page contentType="text/html;charset=UTF-8" %>
<script src="${pageContext.request.contextPath}/js/app.js"></script>
<script>
  const ctx = "${pageContext.request.contextPath}";
  console.log(ctx);
</script>
```

**Listing 1.** The container substitutes the EL, then prints the `<script>` tags. The browser loads `app.js` and runs the inline classic script. There is no JavaScript `language` on the `page` directive.

```jsp
<%-- Conceptual — quote JSP/EL delimiters that appear in JS --%>
<script>
  const dollar = '${'${'}';
  const open = '<\%';
</script>
```

**Listing 2.** In template text, a literal `${` is `${'${'}` (or `\$` when EL is on). A literal `<%` is `<\%`. Unquoted, those sequences are **JSP**, not JavaScript.

> [!warning] `${` and `<%` inside `<script>` are still JSP
> EL in template text runs on the **server**. `user.name` in `${user.name}` is not a JS property lookup. A JS template literal or comparison that contains `${` or `<%` can fail translation or leak server data. `scripting-invalid` does not save you: EL is a different switch. Put untrusted values through an escaping action, not raw EL inside a script.

> [!warning] `</script>` closes the HTML element
> An ASCII case-insensitive `</script>` in inline script text **ends** the `script` element, even inside a JS string. Prefer an external `src` file, or escape `<` (for example `\x3C`). `<%-- … --%>` around a script **drops** that script from the response; an HTML `<!-- … -->` comment is still template text and **still evaluates** nested EL and scriptlets.

> [!tip] Interview answer
> Yes for client-side JavaScript: it is HTML template data the servlet writes, and the browser runs the `script` element. No for JSP scripting: in JSP 4.0 that language is Java, and `<% %>` is not JavaScript. EL inside a script tag still runs on the server, so I quote `${` and `<%` or keep the JS in a static `.js` file.
