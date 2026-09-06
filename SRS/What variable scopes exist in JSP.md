<!--
reps: 0
priority: 0
-->
#Java/JSP/ImplicitObjects #Java/Servlet #SRS

# What variable scopes exist in JSP?

> [!abstract] Short answer
> **Four: `page`, `request`, `session`, and `application`.** Each named object lives in one namespace until that scope ends. **Page** is JSP-only (`PageContext`). The other three are the servlet bags (`ServletRequest`, `HttpSession`, `ServletContext`). Default for `jsp:useBean` / `c:set` is **page**. Hub: [[What is PageContext and what are its benefits]]. EL maps: [[What are the implicit EL scope objects in JSP and how do they differ from servlet scoped objects]]. Session on/off: [[Is a session object always created on a JSP page and can it be disabled]].

## Where the name lives, and when it dies

Jakarta Pages **4.0** §1.8.2: created objects (implicits, actions, scriptlets) have a **scope** — who can see the name, and when the **reference is released**.

| Scope | Stored on | Visible to | Released |
| --- | --- | --- | --- |
| **`page`** | `pageContext` | **This** JSP only | After the **response is sent**, or the request is **forwarded** elsewhere |
| **`request`** | `request` | Every resource on **this request** (includes **forward**) | After the **request** finishes |
| **`session`** | `session` | Pages in the **same HttpSession** | When the **session ends**. **Illegal** on a page with `session="false"` |
| **`application`** | `application` (`ServletContext`) | The **whole web app** (works **without** a session) | When the container **reclaims** the context |

`PageContext` constants: `PAGE_SCOPE` (default), `REQUEST_SCOPE`, `SESSION_SCOPE`, `APPLICATION_SCOPE`. `findAttribute(name)` walks **page → request → session (if valid) → application**. A **name should** behave as **one namespace** across those four; the container **need not** enforce uniqueness (performance). Servlet attributes: [[What are servlet attributes for and how do they work]]. Context: [[How would you explain ServletContext in Java web applications]].

**Object scope ≠ scripting variable.** `jsp:useBean id="cust"` puts the bean in the chosen scope **and** declares a Java variable whose **lexical** life follows Java block rules — the object can still sit on `pageContext` after the variable is out of scope. JSTL `c:set` / `c:remove` use **`var` + `scope`** (page default) and **no** scripting variable: [[What is the difference between the JSTL set tag and jsp useBean]].

**Implicits have scopes too** (Table JSP.1-6): e.g. `out`, `config`, `pageContext`, `response`, `page` are **page**; `request` is **request**; `session` is **session**; `application` is **application**. `exception` on an error page is **page**.

```d2
direction: down
p: "page\nthis JSP / PageContext" {
  width: 240
  height: 40
  style.fill: "#fff8e1"
}
r: "request\nthis request / ServletRequest" {
  width: 260
  height: 40
  style.fill: "#e3f2fd"
}
s: "session\nHttpSession" {
  width: 200
  height: 36
  style.fill: "#e8f5e9"
}
a: "application\nServletContext" {
  width: 220
  height: 36
  style.fill: "#f3e5f5"
}
p -> r: "forward keeps request, drops page"
r -> s: "later hits"
s -> a: "all users of the app"
```

**Fig. 1.** Narrowest **page** (gone on **forward**). Widest **application**.

```jsp
<%-- Conceptual — four scopes --%>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<c:set var="label" value="here" scope="page"/>
<c:set var="user" value="${requestScope.user}" scope="request"/>
<jsp:useBean id="prefs" class="example.Prefs" scope="session"/>
<c:set var="appName" value="shop" scope="application"/>
<p>${pageScope.label} ${requestScope.user.name}</p>
```

**Listing 1.** Unqualified `${user}` is **`findAttribute`**, not “request only.” Qualify when the same name might exist in two bags.

> [!warning] Page attributes die on `forward`; session scope needs a session
> After **`jsp:forward` / `RequestDispatcher.forward`**, **page** names from the caller are **gone**; **request** names remain. `scope="session"` on `session="false"` is a **translation** or **runtime** failure (`IllegalStateException` on `PageContext` session ops). Do not treat **`response`** as request-scoped — the implicit is **page**. `${session.profile}` is **not** the session object.

> [!tip] Interview answer
> JSP has four scopes: page, request, session, and application. Page lives on PageContext for this JSP only and is released when the response is sent or the request is forwarded. Request, session, and application are the servlet request, HttpSession, and ServletContext. Default for useBean and c:set is page, and findAttribute searches from page outward.
