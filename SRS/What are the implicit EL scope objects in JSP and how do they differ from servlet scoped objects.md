<!--
reps: 0
priority: 0
-->
#Java/JSP/EL #Java/Servlet #SRS

# What are the implicit EL scope objects in JSP and how do they differ from servlet scoped objects?

> [!abstract] Short answer
> EL’s **scope maps** are **`pageScope`**, **`requestScope`**, **`sessionScope`**, **`applicationScope`**: each is a **`Map` of attribute name → value**. They wrap the **same four JSP scopes** as servlet attributes, except **page** (JSP-only, stored on **`PageContext`**). They are **not** the servlet objects. In **scriptlets**, **`request` / `session` / `application`** **are** `HttpServletRequest` / `HttpSession` / `ServletContext`. In EL those names are **not** implicits; you use the **`*Scope` maps** or **`${pageContext.request}`**. Bare **`${product}`** is **`PageContext.findAttribute`**: page, then request, then session, then application. Attributes: [[What are servlet attributes for and how do they work]]. Session on/off: [[Is a session object always created on a JSP page and can it be disabled]]. Context: [[How would you explain ServletContext in Java web applications]]. JSP scopes: [[What variable scopes exist in JSP]].

## Maps vs the servlet objects

Jakarta Pages **4.0 §2.4** — EL implicits, **always** named:

| EL name | Type | Backs |
| --- | --- | --- |
| `pageScope` | `Map` | **Page** attributes (`PageContext`) — **no servlet API twin** |
| `requestScope` | `Map` | `ServletRequest` attributes |
| `sessionScope` | `Map` | `HttpSession` attributes |
| `applicationScope` | `Map` | `ServletContext` attributes |
| `pageContext` | `PageContext` | The page; **`${pageContext.request}`** reaches the servlet request |

Also EL (not scopes): **`param` / `paramValues`**, **`header` / `headerValues`**, **`cookie`**, **`initParam`** (`ServletContext.getInitParameter`, **not** context **attributes**).

Scripting implicits (**§1.8.3**): **`request`**, **`session`**, **`application`**, **`pageContext`**, **`out`**, **`config`**, **`page`**, **`exception`**. EL does **not** define **`request`**, **`session`**, or **`application`**. **`${sessionScope.profile}`** is **`session.getAttribute("profile")`**. **`${session.profile}`** does **not** mean that: **`session`** is resolved as a **scoped attribute name** (or stays unknown → **`null`**).

**`${product}`** (no map prefix): **`ScopedAttributeELResolver`** → **`findAttribute("product")`** in **page → request → session → application**. Same name in two scopes: the **narrower** wins unless you qualify **`${requestScope.product}`**.

```d2
direction: down
el: "EL *Scope Maps" {
  width: 220
  height: 40
  style.fill: "#e3f2fd"
}
script: "scriptlet request / session / application" {
  width: 280
  height: 40
  style.fill: "#fff8e1"
}
srv: "ServletRequest / HttpSession / ServletContext" {
  width: 300
  height: 40
  style.fill: "#e8f5e9"
}
el -> srv: "getAttribute via Map"
script -> srv: "the objects themselves"
```

**Fig. 1.** EL **scope objects are maps**. Scripting implicits **are** the servlet (or JSP) objects.

```jsp
<%-- Conceptual — Jakarta Pages 4.0 --%>
<% request.setAttribute("order", order); %>
${requestScope.order}          <%-- Map of request attributes --%>
${pageContext.request.method}  <%-- the HttpServletRequest --%>
<%-- ${request.method} is not the scripting implicit "request" --%>
${sessionScope.user}           <%-- HttpSession.getAttribute("user") --%>
${applicationScope.cache}      <%-- ServletContext.getAttribute("cache") --%>
${pageScope.scratch}           <%-- PageContext only; not on the request --%>
${initParam.dsn}               <%-- context-param, not an attribute --%>
```

**Listing 1.** Qualify with **`*Scope`** (or **`pageContext`**) so EL does not walk **`findAttribute`**.

> [!warning] `${session.x}` is not `session.getAttribute("x")`
> **`session` is a scriptlet variable**, not an EL implicit. Unqualified names search **four** scopes and can **shadow**. **`param.q` is not `requestScope.q`**: parameters vs attributes. **`initParam` is not `applicationScope`**.

> [!warning] Page scope never leaves this JSP
> A **forwarded servlet** sees **request / session / context** attributes, not **`pageScope`**. **`session="false"`** still leaves the EL name **`sessionScope`**; it does **not** create a session. Defining **session-scoped** objects on that page is still **illegal**.

> [!tip] Interview answer
> EL gives me four maps — pageScope, requestScope, sessionScope, applicationScope — plus pageContext. Those maps are the attribute bags; the servlet scoped objects are Request, Session, and ServletContext themselves, which scriptlets call request, session, and application. Page scope exists only on PageContext. I write requestScope.foo when I mean the request attribute so findAttribute cannot pick a page-scoped name by mistake.
