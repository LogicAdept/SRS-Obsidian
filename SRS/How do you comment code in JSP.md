<!--
reps: 0
priority: 0
-->
#Java/JSP #DataFormats/Documents/HTML #SRS

# How do you comment code in JSP?

> [!abstract] Short answer
> **Use `<%-- … --%>` to hide text from the translator and from the client.** Use **`<!-- … -->` in a `.jsp` page** when the comment must **appear in the response**; the container still **runs** scriptlets, actions, expressions, and EL inside it. In a **JSP document** (`.jspx`), `<!-- … -->` is an XML comment: the body is **ignored completely** and is for documenting or commenting out the page. A Java comment inside a scriptlet (`<% /* … */ %>`) lives only in the generated servlet.

## Three comment channels

Jakarta Pages **4.0** §1.5 splits comments by **syntax** (standard page vs XML document) and by **audience** (page author vs client).

**JSP comment** (`<%-- … --%>`). The body is **ignored completely**. Use it for documentation and to **comment out** a region. The grammar takes characters until the first `--%>`; **comments do not nest**. The XML view of the page **drops** this construct. `scripting-invalid` still allows JSP comments: they are not scriptlets.

**Client comment in standard syntax.** `<!-- … -->` is **uninterpreted template text**. It is written to `out` like any other HTML/XML. Dynamic content **inside** the comment is **still processed** (actions, scriptlets, `<%= … %>`). EL in that template text is still evaluated unless EL is off. HTML comments are not a sandbox: [[Can you use JavaScript inside a JSP page]], [[What is Java Server Pages JSP]].

**Scripting-language comment.** `<% /** … **/ %>` (or `//`, `/* */`) is a **scriptlet** whose Java is a comment in `_jspService`. It does not appear in the response. It **is** a scripting element: `scripting-invalid` makes it a **translation error**.

**JSP documents.** Only XML comments `<!-- … -->`. The body is **ignored completely** (documentation / comment-out). They **do not nest**. That is the opposite of the same characters on a `.jsp` page.

```d2
direction: down
src: "source comment" {
  width: 200
  height: 36
  style.fill: "#fff8e1"
}
jspc: "<%-- … --%>\nignored: no servlet, no response" {
  width: 320
  height: 56
  style.fill: "#e8f5e9"
}
htmlc: ".jsp <!-- … -->\ntemplate text → client; JSP inside still runs" {
  width: 360
  height: 56
  style.fill: "#e3f2fd"
}
xmlc: ".jspx <!-- … -->\nignored completely (XML comment)" {
  width: 320
  height: 56
}
src -> jspc
src -> htmlc
src -> xmlc
```

**Fig. 1.** Same `<!-- -->` tokens: **template output** on a standard page, **elided** on a JSP document.

```jsp
<%-- Conceptual — Jakarta Pages 4.0, standard syntax --%>
<%-- Server-only: not translated, not sent --%>
<!-- Visible in "View Source": <%= request.getRemoteUser() %> -->
<% /* Java comment in _jspService; not in the HTML */ %>
```

**Listing 1.** Three standard-syntax forms. The HTML comment still evaluates the expression and **sends** the result inside `<!-- … -->`.

```xml
<!-- Conceptual — JSP document: this whole block is ignored -->
<jsp:scriptlet>int leaked = 1;</jsp:scriptlet>
```

**Listing 2.** In `.jspx`, XML comments **comment out** markup. The scriptlet does **not** run. On a `.jsp` page the same `<!-- … -->` wrapper would **not** stop a nested `<% … %>`.

> [!warning] `<!--` does not disable JSP on a `.jsp` page
> Scriptlets, actions, and EL inside an HTML comment **still execute**. Secrets in `<!-- password=… -->` go to the browser. To disable a region, wrap it in `<%-- … --%>`, or use XML comments only in a JSP document.

> [!warning] JSP comments do not nest
> The first `--%>` ends the comment. An inner `<%--` is just text. A stray `--%>` in a Java string you thought you commented out will **reopen** the page. `<% /* … */ %>` is banned when scripting is invalid; `<%-- … --%>` is not.

> [!tip] Interview answer
> I use `<%-- --%>` for comments that must not reach the client and must not run. HTML comments on a JSP are template text: they show up in the response and the container still processes JSP inside them. In a JSP document, `<!-- -->` instead ignores the body. A `<% /* */ %>` comment is just Java in a scriptlet.
