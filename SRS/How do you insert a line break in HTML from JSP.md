<!--
reps: 0
priority: 0
-->
#Java/JSP #Networking/Web/HTML #SRS

# How do you insert a line break in HTML from JSP?

> [!abstract] Short answer
> **Emit an HTML `br` element** (`<br>` in a `.jsp`, well-formed `<br/>` in a JSP document). That element **represents a line break** in the document the browser renders. A Java `'\n'`, `out.println`, or a newline in the JSP **source** only writes the platform **line separator** into the HTML **text**; it is not a `br`. Template data: [[What is Java Server Pages JSP]]. `out`: [[What is the difference between JspWriter and servlet PrintWriter]].

## Markup vs a newline character

Jakarta Pages **4.0** treats HTML as **template data**: the translator does not interpret `<br>`, so it becomes `out.print(…)` like any other text (whitespace in that text is kept). The implicit `out` is a `JspWriter`. `println` / `newLine` terminate the current **output line** with `line.separator` (not necessarily `'\n'`). That character is still just text in the HTML serialization.

HTML: **`br` represents a line break.** Use it when the break is **part of the content** (address, poem). Do **not** use `br` to split thematic groups — that is another `p` (or similar). A `p` that contains only `br` is a placeholder blank line, not a layout tool. Inside `pre`, structure can be **preformatted** (newlines in the text matter); that is a different element, not a substitute for scattering `br` for page layout.

`System.out.println` is **not** `out`. It does not write the response. Client-side script in the page is also template data; it does not create HTML `br` for you: [[Can you use JavaScript inside a JSP page]].

```d2
direction: down
jsp: "JSP template / scriptlet" {
  width: 240
  height: 40
  style.fill: "#fff8e1"
}
html: "response bytes" {
  width: 280
  height: 40
  style.fill: "#e8f5e9"
}
br: "<br> → line-break element" {
  width: 260
  height: 40
  style.fill: "#e3f2fd"
}
nl: "line.separator → source newline" {
  width: 280
  height: 40
}
jsp -> html
html -> br
html -> nl
```

**Fig. 1.** A visual break in HTML is the **`br` element** (or preformatted text). `JspWriter.println` only ends a **line of markup**.

```jsp
<%-- Conceptual — Jakarta Pages 4.0, HTML template data --%>
<%@ page contentType="text/html;charset=UTF-8" %>
<p>P. Sherman<br>
42 Wallaby Way<br>
Sydney</p>
```

**Listing 1.** Content line breaks as `br`, same pattern as a postal address. In a `.jspx` document use `<br/>` so the XML is well-formed.

```jsp
<%-- Conceptual — these are not HTML line breaks --%>
<%
    out.println("P. Sherman");
    out.println("42 Wallaby Way");
%>
```

**Listing 2.** Each `println` writes text plus `line.separator`. The browser still sees one phrasing run unless you also emit `br` or wrap the text in `pre`.

> [!warning] `out.println` is not `<br>`
> It writes a **line separator**, not a line-break **element**. The page may look like one line in the browser while “View Source” shows wraps. `System.out.println` never reaches the client. Do not stuff `<%= "\n" %>` and expect a visual break in a normal `p`.

> [!warning] `br` is content, not layout
> Do not insert `br` between links or form fields to fake a list or a stack of blocks — use separate `p` (or other grouping) elements. Do not put renderable content inside `br`. A JSP document cannot use a raw `<br>` start tag without a well-formed empty-element form.

> [!tip] Interview answer
> I put a `br` in the JSP template, or I print the `br` markup through `out`. A Java newline or `out.println` only wraps the HTML source. I use `br` for real content breaks like an address, not to lay out the page, and I never confuse `System.out` with the JSP `out`.
