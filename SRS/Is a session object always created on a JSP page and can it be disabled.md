<!--
reps: 0
priority: 0
-->
#Java/JSP #Java/Servlet/Sessions #SRS

# Is a session object always created on a JSP page and can it be disabled?

> [!abstract] Short answer
> **No.** The **`page` directive `session` defaults to `true`**, so the generated servlet **joins or creates** an **`HttpSession`** (`request.getSession()`, i.e. **`getSession(true)`**) and exposes it as the implicit **`session`**. Set **`<%@ page session="false" %>`** and that page **does not participate**: the implicit **`session` is gone**, and **any use of it is a fatal translation error**. An HTTP session created by **another** servlet or JSP can still exist. Servlet sessions: [[How would you explain HTTP sessions in servlet based applications]]. JSP as a servlet: [[What is Java Server Pages JSP]]. Tracking without cookies: [[How would you explain URL rewriting for session tracking]].

## Default `true`, opt out with `session="false"`

Jakarta Pages **4.0** `page` directive attribute **`session`**:

| Value | Effect |
| --- | --- |
| **`true` (default)** | Implicit **`session`** (`jakarta.servlet.http.HttpSession`) is the **current or new** session for this page. |
| **`false`** | The page is **not session-aware**. Implicit **`session` is unavailable**. A reference in the page body is **illegal** → **fatal translation error** (HTTP **500** on later requests). |

The spec sample `_jspService` for a session-aware page does `HttpSession session = request.getSession();` and `JspFactory.getPageContext(..., needsSession=true, ...)`. **`getSession()` creates** a session if the client has none (cookie / URL id). That is why a **default JSP can create sessions for crawlers** that never come back.

**`session="false"` is per translation unit**, not a container kill-switch. It does **not** call `invalidate()`. **`jsp:useBean` / objects with `scope="session"` are illegal** on a page that is not session-aware. Application scope still works. EL **`sessionScope`** remains a named map; it is **not** the scripting variable `session`. Some tag actions that store into session scope throw **`IllegalStateException` at runtime** if the calling page does not participate.

Need a session only if one already exists: **`request.getSession(false)`** in a scriptlet (that identifier is **`request`**, not **`session`**). Creating one on purpose: **`getSession(true)`** or the default directive. Protecting endpoints: [[How do you restrict servlet endpoints to users with a valid session]].

```d2
direction: down
dir: "page session=true|false\n(default true)" {
  width: 260
  height: 48
  style.fill: "#fff8e1"
}
yes: "getSession() / needsSession=true\nimplicit session" {
  width: 280
  height: 48
  style.fill: "#e8f5e9"
}
no: "no implicit session\nusing session → translation error" {
  width: 280
  height: 48
  style.fill: "#fff3e0"
}
dir -> yes: "true"
dir -> no: "false"
```

**Fig. 1.** Disable participation on **this JSP**. Other pages in the same app can still create **`HttpSession`**.

```jsp
<%-- Conceptual — Jakarta Pages 4.0 --%>
<%@ page session="false" %>
<%-- session.setAttribute("x", 1);  illegal: fatal translation error --%>
<%
    HttpSession existing = request.getSession(false); // OK: not the implicit session
    if (existing != null) {
        existing.getAttribute("user");
    }
%>
```

**Listing 1.** **`session="false"`** drops the implicit variable. **`request.getSession(false)`** reads an existing session **without creating** one.

> [!warning] Default `true` creates sessions
> Omit the directive and the implementation still calls **`getSession()`**. That can set **`JSESSIONID`** on the first hit. Static-ish pages and bots should use **`session="false"`**.

> [!warning] `session="false"` is not `session.invalidate()`
> The implicit name **`session` cannot appear** in that page — including in a branch you think is dead. A **`forward`** to a **`session="true"`** page can still **create** a session. Duplicate `session` attributes in one translation unit with **different** values are a **translation error**.

> [!tip] Interview answer
> By default a JSP is session-aware: the generated servlet calls getSession and exposes HttpSession as session, which creates a session if needed. I turn that off with page session false; then using the session implicit object is a translation error. That does not wipe a session another component already created; for a maybe-session I use request.getSession false.
