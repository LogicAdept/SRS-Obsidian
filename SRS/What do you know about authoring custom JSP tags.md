<!--
reps: 0
priority: 0
-->
#Java/JSP/Tags #SRS

# What do you know about authoring custom JSP tags?

> [!abstract] Short answer
> **You author a custom action as a TLD description plus a handler: a Java class (`Tag` / `IterationTag` / `BodyTag` or `SimpleTag`) or a `.tag` / `.tagx` file.** Declare the name, `body-content`, and attributes. Pages import the library with `<%@ taglib %>`. Tag files use `tag` / `attribute` / `variable` directives — **`page` is a translation error**. Extension mechanism: [[How can you extend JSP functionality]]. Built-in `jsp:` is not this: [[Why are built in JSP tags not configured in web.xml]].

## TLD first, then a handler

Jakarta Pages **4.0** Chapter **7** is the authoring contract. The **TLD** (`.tld`) is an XML document the translator reads **without** loading your handler: library docs, JSP/`tlib` versions, each action’s **name**, **handler class** or **tag-file path**, **attributes** (required? request-time expression? type?), optional **scripting variables**, optional **`TagLibraryValidator`** / **`TagExtraInfo`**. Drop a JAR in `WEB-INF/lib` or a `.tld` under `WEB-INF` (not `WEB-INF/classes`, not `WEB-INF/lib` as a loose file, and **not** under `WEB-INF/tags` unless it is the reserved **`implicit.tld`**). The `uri` in the TLD feeds the taglib map; `web.xml` can override the URI→path. Types of tags on a page: [[What main JSP tag types exist]]. A worked call-site: [[What is an example of using custom JSP tags]].

**Java handler.** Implement `jakarta.servlet.jsp.tagext.Tag` (plus `IterationTag` / `BodyTag` if you need `doAfterBody` / `BodyContent`) or **`SimpleTag`**. Base classes: `TagSupport` / `BodyTagSupport` / `SimpleTagSupport`. Bean-style setters receive attributes **before** `doStartTag` / `doTag`. **Classic** instances **may be reused**; **SimpleTag** is **construct → inject → set properties → `doTag` → discard**. SimpleTag body is a **`JspFragment`**; TLD `body-content` of **`JSP` is illegal**. Extra attribute names: implement **`DynamicAttributes`**. Nested classic-inside-simple: container wraps with **`TagAdapter`**. Resource injection (`@Resource`, …) applies to **Java handlers and TLD listeners**, not to pages or tag files.

**Tag file (Chapter 8).** Same custom-action surface, authored in **JSP syntax** (`.tag`) or **XML** (`.tagx`). Live only in **`/WEB-INF/tags/`** (or a subdir) or **`/META-INF/tags/`** inside a `WEB-INF/lib` JAR. Anywhere else the container **ignores** them as tags (docroot `.tag` is just content). Directories under `/WEB-INF/tags/` are **implicit libraries** imported with **`tagdir`** (no hand-written TLD). A JAR **must** list each file in a TLD **`tag-file`** (`path` starts with `/META-INF/tags`); unlisted JAR tag files are ignored. Directives: **`tag`**, **`attribute`**, **`variable`**, plus `taglib` / `include`. **`jsp:doBody`** / **`jsp:invoke`** exist **only** here. Default `body-content` is **`scriptless`** (`empty` / `tagdependent` allowed; **`JSP` is a translation error**). `attribute` **`rtexprvalue` defaults to `true`** (the TLD element does not). Each directory is its own library; `a.tag` and `a.tagx` in the same folder is an **invalid** library.

**`body-content` values you actually write:** `empty`, `scriptless`, `tagdependent`, or (classic Java tags only) `JSP`. Scriptless bodies cannot contain scriptlets; that is what SimpleTag / tag files assume.

```d2
direction: down
auth: "author\nTLD + handler" {
  width: 260
  height: 40
  style.fill: "#fff8e1"
}
java: "Java\nTag / SimpleTag class\nWEB-INF/classes or lib" {
  width: 280
  height: 48
  style.fill: "#e3f2fd"
}
file: "tag file\n.tag / .tagx\nWEB-INF/tags or JAR META-INF/tags" {
  width: 300
  height: 48
  style.fill: "#e8f5e9"
}
use: "page\n<%@ taglib uri|tagdir %>" {
  width: 260
  height: 40
  style.fill: "#f3e5f5"
}
auth -> java
auth -> file
java -> use: "uri → TLD"
file -> use: "tagdir or tag-file in TLD"
```

**Fig. 1.** Authoring is **declaring the contract**, then implementing it in **Java or JSP**. JSTL is one library you consume, not the authoring API: [[How would you explain JSTL the JSP Standard Tag Library]].

```jsp
<%-- Conceptual — /WEB-INF/tags/panel.tag --%>
<%@ tag body-content="scriptless" %>
<%@ attribute name="title" required="true" %>
<section>
  <h2>${title}</h2>
  <jsp:doBody/>
</section>
```

**Listing 1.** Tag-file authoring: `tag` + `attribute`, body as a fragment via `jsp:doBody`. Do **not** put `<%@ page %>` here.

```xml
<!-- Conceptual TLD fragment — Jakarta Pages 4.0 -->
<taglib version="4.0">
  <tlib-version>1.0</tlib-version>
  <short-name>box</short-name>
  <uri>urn:example:box</uri>
  <tag>
    <name>panel</name>
    <tag-class>example.PanelTag</tag-class>
    <body-content>scriptless</body-content>
    <attribute>
      <name>title</name>
      <required>true</required>
      <rtexprvalue>true</rtexprvalue>
    </attribute>
  </tag>
</taglib>
```

**Listing 2.** Java-handler authoring: the TLD names the class and the attribute contract. URI map / `jsp-config`: [[How is JSP configured in the web deployment descriptor]].

> [!warning] `page` in a tag file, or `body-content` `JSP` on SimpleTag, fails translation
> A tag file is not a page: **`<%@ page %>` is illegal**; use **`<%@ tag %>`**. Tag-file `body-content` may be `empty`, `scriptless` (default), or `tagdependent` — never `JSP`. The same `JSP` value on a **SimpleTag** TLD entry makes any using page **invalid**. `implicit.tld` may set only JSP version and `tlib-version`; extra elements are a translation error.

> [!tip] Interview answer
> I author a custom JSP tag as a TLD entry plus a handler. The handler is a Java Tag or SimpleTag class, or a tag file under WEB-INF/tags. Tag files declare the contract with tag, attribute, and variable directives; Java handlers declare it in the TLD. I import with taglib uri or tagdir, and I never treat standard jsp: actions as something I register myself.
