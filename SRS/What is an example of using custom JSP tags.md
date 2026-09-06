<!--
reps: 0
priority: 0
-->
#Java/JSP/Tags #SRS

# What is an example of using custom JSP tags?

> [!abstract] Short answer
> **Declare the library, then write `prefix:action` like any other action.** Standard-syntax pages: `<%@ taglib prefix="t" tagdir="/WEB-INF/tags" %>` then `<t:panel title="${title}">…</t:panel>`. URI-mapped libraries (your TLD or JSTL) use `uri` instead of `tagdir`. That is **using** tags; writing the handler is separate: [[What do you know about authoring custom JSP tags]]. `jsp:` is not this: [[Why are built in JSP tags not configured in web.xml]].

## Import, then invoke

Jakarta Pages **4.0**: custom actions enter a page only after a **`taglib`** (or, in a JSP document, an `xmlns` that resolves to a TLD or `urn:jsptagdir:…`). The prefix you pick becomes the XML prefix on every invocation. **`taglib` must appear before** the first action that uses that prefix. **`uri` and `tagdir` cannot both** appear. `tagdir` must be an existing directory under **`/WEB-INF/tags`**. Empty prefixes, and prefixes `jsp:`, `jspx:`, `java:`, `jakarta:`, `servlet:`, are **illegal**. Unknown `prefix:Name` is a **translation error**. Mechanism: [[How can you extend JSP functionality]]. Types: [[What main JSP tag types exist]].

**Three call-sites you actually write**

1. **Tag file** — implicit library, no TLD of your own: `tagdir="/WEB-INF/tags"` → `<t:panel>`.
2. **Java handler** — TLD `uri` (or a relative path to a `.tld`): `<box:panel title="…">`.
3. **Portable library** — same `uri` + prefix pattern; JSTL core is `<c:forEach>` / `<c:out>` after `uri="jakarta.tags.core"`: [[How would you explain JSTL the JSP Standard Tag Library]].

Attributes follow the TLD: required names must be present; **`${}`** is legal only if `rtexprvalue` is true (tag-file `attribute` defaults to true). Body content must match `empty` / `scriptless` / `tagdependent` / `JSP`. Nested custom actions cooperate via `setParent` / `findAncestorWithClass`, or via scoped variables the inner tag reads. URI map in `web.xml`: [[How is JSP configured in the web deployment descriptor]].

In **JSP documents**, you do **not** write `taglib`; you bind the same libraries with **`xmlns:prefix`**. A tagdir library is the URN form **`urn:jsptagdir:`** plus the `/WEB-INF/tags/…` path.

```d2
direction: down
dir: "<%@ taglib prefix uri|tagdir %>" {
  width: 280
  height: 40
  style.fill: "#fff8e1"
}
act: "<prefix:name attr=\"${…}\">\n  body / nested actions\n</prefix:name>" {
  width: 300
  height: 56
  style.fill: "#e3f2fd"
}
out: "handler runs\nSimpleTag.doTag or Tag.doStartTag" {
  width: 280
  height: 48
  style.fill: "#e8f5e9"
}
dir -> act: "prefix bound"
act -> out: "translation + request"
```

**Fig. 1.** Using a custom tag is **bind prefix, then invoke**. The page never names the Java class.

```jsp
<%-- Conceptual — page using a tag file and JSTL --%>
<%@ taglib prefix="t" tagdir="/WEB-INF/tags" %>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<t:panel title="${requestScope.heading}">
  <c:forEach var="m" items="${requestScope.movies}">
    <c:out value="${m.title}"/>
  </c:forEach>
</t:panel>
```

**Listing 1.** `t:panel` is a local tag file; `c:forEach` / `c:out` are custom actions from JSTL. Both are **used** the same way. Assume `/WEB-INF/tags/panel.tag` exists (see authoring card).

```jsp
<%-- Conceptual — URI-mapped Java tag, empty body --%>
<%@ taglib prefix="box" uri="urn:example:box" %>
<box:panel title="Best movies"/>
```

**Listing 2.** Same invocation shape; the TLD’s `<uri>` is `urn:example:box` and `<name>` is `panel`. A relative `uri="/WEB-INF/tlds/box.tld"` also works as a fallback during development.

> [!warning] `taglib` after the first `<t:…>`, or `jsp:` as a custom prefix, fails translation
> Put **`taglib` first**. Do not combine **`uri` and `tagdir`**. A mistyped prefix is not HTML — it is a **translation error** (unless undeclared namespaces are left silent; prefer `error-on-undeclared-namespace`). **`<jsp:include>`** is a **standard** action; you do **not** `taglib` it. `<c:forEach>` without importing `jakarta.tags.core` is also an error.

> [!tip] Interview answer
> I use a custom JSP tag by importing its library with taglib, then writing prefix:name with attributes and an optional body. tagdir points at WEB-INF/tags for tag files; uri points at a TLD or a well-known library such as JSTL. The call site never names the handler class. I keep taglib above the first use, I never reuse the reserved jsp prefix, and I pass data with EL attributes rather than scriptlets.
