<!--
reps: 0
priority: 0
-->
#Java/JSP/JSTL #Java/JSP/Tags #SRS

# What is the difference between JSTL import jsp include and the include directive?

> [!abstract] Short answer
> **`<%@ include file %>` pastes source at translation. `<jsp:include page>` dispatches in-app at request time. `<c:import url>` is the JSTL action that can do that include plus foreign context, absolute URLs, and export as `String` / `Reader`.** Directive = **static object** (text parsed here). `jsp:include` / same-context `c:import` = **dynamic object** (`RequestDispatcher.include`). JSTL: [[How would you explain JSTL the JSP Standard Tag Library]]. Dispatcher: [[How would you explain the servlet RequestDispatcher for forward and include]]. Not “HTML vs EL”: [[What is the difference between dynamic and static content in JSP]].

## Three mechanisms, two times

Jakarta Pages **4.0** Table **JSP.1-10** defines **two** language includes. Jakarta Tags **3.0** §7.2 adds **`c:import`** because `jsp:include` cannot reach **outside this web app** and is awkward as a **stream** for a nested transform.

| | `<%@ include file %>` | `<jsp:include page>` | `<c:import url>` |
| --- | --- | --- | --- |
| When | **Translation** | **Request** | **Request** |
| What is included | **Source text** (parsed into this unit) | **Output** of a dispatch | Output, or a **`var` String** / **`varReader` Reader** |
| Path | **`file`**, relative to **this JSP file** | **`page`**, relative to **this JSP page** | Relative (same or **`context`**) or **absolute** (protocol + colon) |
| Who | JSP language (no TLD) | Standard action (`jsp:`) | Core JSTL (`jakarta.tags.core`) |
| Extra | `include-prelude` / `include-coda` are the same idea | **`flush`** (default **`false`**); **`jsp:param`** for the hop only | **`c:param`**; **`charEncoding`**; throws **`JspException`** on missing dispatcher, include failure, or **non-2xx** |

**Directive.** The resource is a **static object**: its characters become part of this translation unit (JSP in the fragment is compiled **with** this page). File-relative. The container **may** recompile if the file changes; the spec **does not** give you a hook to force that. Encoding of included files is **per file**; the **response** encoding follows the **requested** page only.

**`jsp:include`.** Same **context** only. `RequestDispatcher.include` into current **`out`**. Included resource **cannot** change status or headers (cookies ignored). After it returns, this page continues. `page` is **page-relative**; a nested directive inside an included JSP still resolves against **that file**.

**`c:import`.** Same-context relative URL: **same semantics as `jsp:include`**. **`context="/other"`** (both path and context start with `/`): include into a **foreign** app on the same container — only the **request** environment is shared; **not all containers allow it**. **Absolute URL**: `URLConnection` (HTTP GET, follow redirects); **no** request/session of the importer, even if the host is “us”. Default writes to **`out`**; **`var`** caches a **String**; **`varReader`** is **nested visibility** only (must close; no nested `c:param` on that syntax). Errors: [[How does JSTL handle errors]].

**Do not.** `jsp:include` for another WAR or `https` resource. Directive for a URL that only exists at request time (`file` is not EL). Expect `<%@ include %>` of `.html` and `jsp:include` of the same file to mean the same thing: the directive **parses** it as JSP source if the container treats it as JSP text; the action **does not parse** — it includes **output**.

```d2
direction: down
dir: "<%@ include file %>\ntranslation · parse text" {
  width: 280
  height: 48
  style.fill: "#fff8e1"
}
inc: "<jsp:include page>\nsame app · RequestDispatcher" {
  width: 280
  height: 48
  style.fill: "#e3f2fd"
}
imp: "<c:import url>\nsame app · other context · absolute\noptional var / varReader" {
  width: 300
  height: 56
  style.fill: "#e8f5e9"
}
```

**Fig. 1.** Directive **merges source**. The two actions **run a resource now**; only **`c:import`** leaves this application.

```jsp
<%-- Conceptual — three includes --%>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<%@ include file="/WEB-INF/fragments/header.jspf" %>
<jsp:include page="/WEB-INF/fragments/nav.jsp" flush="false">
  <jsp:param name="tab" value="home"/>
</jsp:include>
<c:import url="/WEB-INF/fragments/footer.jsp"/>
<c:import url="/logo.html" context="/master" var="logo"/>
```

**Listing 1.** Header is **baked in**. Nav and footer **run now** in this app. `logo` is a **String** from another context (may be forbidden). Absolute URLs are legal on `c:import` only — do not put them on `jsp:include`.

> [!warning] `file` is not `page`; non-2xx fails `c:import`
> A relative `C.jsp` after `<%@ include file="dir/B.jsp" %>` then `jsp:include` inside B resolves to **`C.jsp` at the page**, not `dir/C.jsp` (spec’s A/B/C example). **`c:import`** throws if the dispatcher is missing, include throws, or the included servlet sets **status outside 2xx** — `jsp:include` does **not** treat status that way. **`varReader`** cannot be used after the `c:import` end tag. Prelude/coda in `web.xml` are **directives**, not `jsp:include`: [[How is JSP configured in the web deployment descriptor]].

> [!tip] Interview answer
> The include directive copies source into this translation unit at compile time. jsp:include is a request-time RequestDispatcher include of a resource in the same web application, writing into out. c:import can do that same-app include, and it can also pull a foreign context or an absolute URL, or export the bytes as a String or Reader. I use the directive for shared fragments I want parsed with this page, jsp:include for in-app composition, and c:import when I need another app, an external URL, or the content as an object.
