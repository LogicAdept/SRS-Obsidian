<!--
reps: 0
priority: 0
-->
#Java/Servlet/Sessions #Security/Authentication #SRS

# How do you restrict servlet endpoints to users with a valid session?

> [!abstract] Short answer
> **Do not call `getSession()`** (that **creates** a session). Use **`getSession(false)`**: **`null`** means this request has **no valid `HttpSession`** — refuse (redirect to login, 401/403). Optionally require a login **attribute** on that session. **`isRequestedSessionIdValid()`** is `false` if the client sent **no** id or the id is **dead**. Container **`security-constraint` + `auth-constraint`** requires **authentication** (role or `**` = any authenticated user), which is **not** the same as “a session object exists.” Sessions: [[How would you explain HTTP sessions in servlet based applications]]. Auth mechanisms: [[What servlet authentication mechanisms exist]]. Filters: [[How would you explain servlet filters and request interception]].

## Check the session, or let the container demand a principal

HTTP is stateless. The container associates requests via **`JSESSIONID`** (cookie, required) or URL rewriting (`;jsessionid=…` — avoid when cookies work). Until the client **joins** (sends tracking info back), `isNew()` is **true** and the next request may **not** be the same session.

**Programmatic gate** (servlet or `Filter` on the URL pattern):

1. `HttpSession s = request.getSession(false);`
2. If `s == null` — no valid session for this request. Do **not** `chain.doFilter`.
3. If you store login as `s.getAttribute("…")` and it is `null`, treat as logged out even if a session exists (empty/anonymous session).
4. On logout: `s.invalidate()` (unbinds attributes). Timeout: `setMaxInactiveInterval` / context session timeout; after the idle interval the container **invalidates**.

Call `getSession` **before the response is committed** if you might **create** a session (cookie path). Creating after commit → **`IllegalStateException`**.

**Declarative gate:** `web.xml` `security-constraint` on `url-pattern` + `auth-constraint`. Named roles, `*` (all declared roles), or `**` (**any authenticated user**, independent of role). **Empty** `auth-constraint` **denies everyone**. No auth-constraint → request accepted **without** login. FORM login stores the original URL, authenticates, then redirects; use CONFIDENTIAL on login and constrained resources. `@ServletSecurity` / `setServletSecurity` map to the same model.

A Filter is the usual place to apply the `getSession(false)` rule to many servlets without repeating it in every `doGet`.

```d2
direction: down
req: "request" {
  width: 200
  height: 36
  style.fill: "#fff8e1"
}
gs: "getSession(false)" {
  width: 200
  height: 36
  style.fill: "#e3f2fd"
}
ok: "session + login attribute\nchain.doFilter" {
  width: 220
  height: 48
  style.fill: "#e8f5e9"
}
no: "null or expired id\nredirect / 401" {
  width: 220
  height: 48
  style.fill: "#ffebee"
}
req -> gs
gs -> ok
gs -> no
```

**Fig. 1.** Restrict means **look up**, not **create**.

```java
// Conceptual — jakarta.servlet.http, Servlet 6.1
public class SessionFilter implements Filter {
    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {
        HttpServletRequest req = (HttpServletRequest) request;
        HttpServletResponse resp = (HttpServletResponse) response;
        HttpSession session = req.getSession(false);
        if (session == null || session.getAttribute("user") == null) {
            resp.sendRedirect(req.getContextPath() + "/login");
            return;
        }
        chain.doFilter(request, response);
    }
}
```

**Listing 1.** `false` avoids minting a session for anonymous hits. A session **without** your login attribute is not “signed in.”

```xml
<!-- Conceptual — any authenticated user, all methods -->
<security-constraint>
  <web-resource-collection>
    <web-resource-name>app</web-resource-name>
    <url-pattern>/app/*</url-pattern>
  </web-resource-collection>
  <auth-constraint>
    <role-name>**</role-name>
  </auth-constraint>
</security-constraint>
```

**Listing 2.** Container authentication, not `getSession(false)`. Combine with `login-config` (FORM, BASIC, …).

> [!warning] `getSession()` is the opposite of a gate
> No-arg `getSession()` **creates** a session if none exists. Every visitor then “has a session.” `isRequestedSessionIdValid()` is **false** when **no** id was sent — not a substitute for “user logged in.” `isNew()` can stay **true** every request if the client **refuses cookies** and you rely on cookies only.

> [!warning] Session ≠ authenticated principal
> `security-constraint` checks **roles / authenticated user**. An application session can exist with **no** principal. After FORM login, prefer **`changeSessionId()`** so a pre-login id is not reused. Sessions are **per `ServletContext`**; they are not shared across apps.

> [!warning] URL rewriting leaks the id
> `;jsessionid=` in the path shows up in logs, referers, and bookmarks. Prefer cookies (`HttpOnly` is a container capability). Do not treat “I see a session cookie” as authorization without the `getSession(false)` / constraint check.

> [!tip] Interview answer
> I gate protected URLs with getSession false and reject when it returns null, often also requiring a login attribute. I never use no-arg getSession for that check because it would create a session. For container-managed access I declare a security-constraint with an auth-constraint, using `**` for any authenticated user, and I remember that is not the same as merely having an HttpSession.
