<!--
reps: 0
priority: 0
-->
#Java/JSP #Java/Servlet #SRS

# Why are built in JSP tags not configured in web.xml?

> [!abstract] Short answer
> **Built-in JSP tags** are the **standard actions** (`jsp:include`, `jsp:forward`, `jsp:useBean`, `jsp:setProperty`, `jsp:getProperty`, `jsp:param`, …). They are **part of the JSP language**, not a tag library. Jakarta Pages **4.0** Chapter **5**: they use the reserved prefix **`jsp:`** (JSP syntax) or the **JSP Page namespace** (XML syntax). The **translator already knows** them. **`web.xml` never registers them.** Custom tags need a **TLD** and a **`taglib` directive**; **`jsp-config/taglib`** is only an **optional URI→TLD map**. Types: [[What main JSP tag types exist]]. Descriptor: [[How is JSP configured in the web deployment descriptor]]. Custom tags: [[What do you know about authoring custom JSP tags]]. JSTL is **not** built-in: [[How would you explain JSTL the JSP Standard Tag Library]].

## Standard actions vs libraries

| Kind | How the container finds it | `web.xml` |
| --- | --- | --- |
| **Standard actions** | Grammar + reserved **`jsp:`**. Using **`jsp:`** for a **non-standard** name is a **translation error**. Prefixes **`jsp:`**, **`jspx:`**, **`java:`**, **`jakarta:`**, **`servlet:`** are **reserved**. | **No entry.** |
| **Directives** | **`<%@ page %>`, `<%@ include %>`, `<%@ taglib %>`** — syntax, not tags you map. | **No entry** to “enable” them. |
| **Custom tag library** | **`<%@ taglib uri=… prefix=… %>`** plus a **TLD**. JAR **`META-INF/*.tld` `<uri>`** fills an **implicit map**. | **Optional** **`<taglib>`** / **`<taglib-uri>`** / **`<taglib-location>`**. If present, it **wins**. |
| **Tag files** | **`tagdir="/WEB-INF/tags/…"`** — **implicit** library; **no** TLD required. | **Not** a taglib map. |
| **JSTL / others** | Separate libraries. Drop the JAR; use the **stable URI** on **`taglib`**. | Needed only to **override** that URI. |

**`jsp-config`** still has a job: **`jsp-property-group`** (EL, scripting, encoding, preludes). That **tunes pages**; it does **not** list **`jsp:include`**.

```d2
direction: down
p: "JSP translator" {
  width: 160
  height: 36
}
s: "standard actions jsp:" {
  width: 240
  height: 40
  style.fill: "#e8f5e9"
}
c: "custom prefix + TLD" {
  width: 220
  height: 40
  style.fill: "#fff3e0"
}
w: "optional web.xml taglib map" {
  width: 260
  height: 40
  style.fill: "#e3f2fd"
}
p -> s: "built in"
p -> c: "extension"
c -> w: "override URI"
```

**Fig. 1.** Built-in actions are compiled in. **`web.xml` maps custom URIs**, if you bother.

```jsp
<%-- Conceptual --%>
<jsp:include page="/f.jsp"/>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<c:out value="${x}"/>
```

**Listing 1.** **`jsp:include`** needs **no** descriptor. **`<c:out>`** needs **JSTL on the classpath** and a **`taglib`** line — not a built-in tag.

> [!warning] JSTL is not a built-in JSP tag
> **`c:forEach` / `fmt:formatDate`** are **JSTL**, a **library**. They are **not** Chapter **5** standard actions. No JAR and no **`taglib`** → **translation error**. A **`web.xml` `<taglib>`** is **optional** when the TLD already advertises its URI.

> [!warning] Do not invent a `servlet` mapping for `jsp:useBean`
> **`web.xml` `<servlet>` / `<filter>`** entries do **not** enable standard actions. **`<%@ taglib prefix="jsp" %>`** is **wrong** — **`jsp:` is reserved**. Empty or **`java:`** prefixes also fail.

> [!tip] Interview answer
> Built-in JSP tags are the standard actions. The container’s JSP translator already implements jsp:include, jsp:forward, and jsp:useBean, so web.xml has nothing to register. I put taglib maps in the descriptor only for custom libraries, and even then a TLD URI inside a JAR is usually enough. I do not call JSTL built-in.
