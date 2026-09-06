<!--
reps: 0
priority: 0
-->
#Java/JSP #SRS

# What main JSP tag types exist?

> [!abstract] Short answer
> **Three syntactic kinds of elements: directives, scripting, and actions.** Actions then split into **standard** (`jsp:`, part of the language) and **custom** (tag library: JSTL, your TLD, tag files). Custom handlers are **classic `Tag` / `IterationTag` / `BodyTag`**, **`SimpleTag`**, or a **`.tag` / `.tagx` file**. Template data and EL are **not** tag types. Built-in vs library: [[Why are built in JSP tags not configured in web.xml]]. Extension: [[How can you extend JSP functionality]]. JSTL: [[How would you explain JSTL the JSP Standard Tag Library]].

## Elements the translator knows

Jakarta Pages **4.0** §1.3: a page is **elements** plus **template data**. Elements have types the container understands. Tags are **case-sensitive**.

**1. Directives** — `<%@ … %>` (XML: `jsp:directive.*`). **Translation** only: `page`, `include`, `taglib` (tag files add `tag` / `attribute` / `variable`). No per-request output of their own.

**2. Scripting** — `<%! %>` declarations, `<% %>` scriptlets, `<%= %>` expressions. Java in JSP **4.0**. Page authors are expected to **avoid** them (`scripting-invalid`). Not actions.

**3. Actions** — XML-style tags, **request** phase. Two families:

| Family | How you get them | Examples |
| --- | --- | --- |
| **Standard** | Translator already knows `jsp:` | `jsp:include`, `jsp:forward`, `jsp:useBean`, `jsp:setProperty`, `jsp:getProperty`, `jsp:param`, `jsp:element` / `attribute` / `body`, `jsp:text`, `jsp:output`, `jsp:root`. **`jsp:invoke` / `jsp:doBody` only in tag files.** JSP **4.0** **removed** `jsp:plugin`. |
| **Custom** | `<%@ taglib %>` (or `xmlns` in a document) + **TLD** | JSTL `<c:out>`, your `<box:panel>`, tag-file `<t:header>` |

**Custom implementation types** (Ch. **7**–**8**) — how a custom action is **written**, not a fourth page syntax:

- **Classic** — `Tag` (start/end), `IterationTag` (`doAfterBody`), `BodyTag` (`BodyContent`). Container **may reuse** the instance.
- **Simple** — `SimpleTag` / `SimpleTagSupport`; **`doTag`**; body is a **`JspFragment`**; instance **not** reused; TLD `body-content` **`JSP` is illegal**.
- **Tag file** — `.tag` / `.tagx` under `/WEB-INF/tags` or JAR `META-INF/tags`. Authoring: [[What do you know about authoring custom JSP tags]]. Call-site: [[What is an example of using custom JSP tags]].

**Body-content** (`empty` / `scriptless` / `tagdependent` / `JSP`) is a **TLD constraint**, not another top-level type.

**Not a type.** **EL** `${}` / `#{}` is an expression language, not a tag. **JavaBeans** (`jsp:useBean`) hold data; they do not add tag names. **JSTL** is one **custom** library (five URIs), not a sibling of `jsp:`.

```d2
direction: down
el: "JSP elements" {
  width: 200
  height: 36
  style.fill: "#fff8e1"
}
d: "directives\n<%@ page include taglib %>" {
  width: 260
  height: 40
  style.fill: "#e8f5e9"
}
s: "scripting\n<%!  <%  <%=" {
  width: 220
  height: 40
  style.fill: "#fce4ec"
}
a: "actions" {
  width: 160
  height: 32
  style.fill: "#e3f2fd"
}
st: "standard jsp:" {
  width: 180
  height: 32
  style.fill: "#bbdefb"
}
cu: "custom\nclassic · SimpleTag · tag file" {
  width: 260
  height: 40
  style.fill: "#c8e6c9"
}
el -> d
el -> s
el -> a
a -> st
a -> cu
```

**Fig. 1.** Spec **three element types**; actions then **standard vs custom**.

```jsp
<%-- Conceptual — one of each --%>
<%@ page session="false" %>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<jsp:include page="/WEB-INF/fragments/nav.jsp"/>
<c:out value="${requestScope.title}"/>
```

**Listing 1.** Directive, standard action, custom (JSTL) action. A scriptlet would be a fourth **element** kind, not a fourth **action** kind.

> [!warning] JSTL is custom; `jsp:` is not a taglib prefix you declare
> Calling JSTL “built-in tags” confuses Chapter **5** with a **library**. `<%@ taglib prefix="jsp" %>` is a **translation error** (`jsp:` is reserved). Directives are **not** `jsp:include`. Empty vs `<x></x>` with only a JSP comment is still **empty**; whitespace in the body is **not**.

> [!tip] Interview answer
> JSP has three element types: directives at translation time, scripting, and actions at request time. Actions are either standard jsp: tags the translator already knows, or custom tags from a tag library. Custom tags are implemented as classic Tag handlers, SimpleTag, or tag files. JSTL is a portable custom library, not a third language next to standard actions.
