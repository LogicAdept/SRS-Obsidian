<!--
reps: 0
priority: 0
-->
#Java/Servlet/Sessions #Networking/Web/Protocols/HTTP #SRS

# How would you explain HTTP sessions in servlet based applications?

> [!abstract] Short answer
> HTTP is **stateless**. The container gives you an **`HttpSession`**: a **per-`ServletContext`** bag of named attributes plus a **session id**. Tracking is **cookies first** (`JSESSIONID`, required); **URL rewriting** (`;jsessionid=` path parameter) is the fallback when cookies are off. Call **`request.getSession()`** to **create or join**; **`getSession(false)`** returns **`null`** if none is valid. The session is **`isNew()`** until the client **joins** (sends the id back). Gate with a valid session: [[How do you restrict servlet endpoints to users with a valid session]]. Login is separate: [[What servlet authentication mechanisms exist]]. Path params: [[How is an HttpServlet request processed]]. Listeners on bind/timeout: [[Why do servlets use listeners]].

## Associate requests without pretending HTTP has memory

**Create / look up.** `getSession()` creates a session if needed. `getSession(false)` only returns one that already exists and is still valid. Until the client **joins**, the next request **may not** share this session — cookies refused, first response not yet seen. `changeSessionId()` rotates the id after login (fixation). `isRequestedSessionIdValid()` is false when **no** id was sent or it is dead.

**How the id travels.** Cookie `JSESSIONID` is mandatory in every container (name may be customized; that name is also the URI parameter). Containers **must** let you mark it **`HttpOnly`**. `;jsessionid=` in the path is **URL rewriting** — use `encodeURL` / `encodeRedirectURL` so links carry the id. Prefer cookies or SSL session tracking; rewriting **leaks** the id (logs, referer, bookmarks).

**Scope.** One `HttpSession` object **per web application**. Another context (including a cross-context dispatch) sees a **different** session even if the cookie is shared. The object from `getSession` is valid **only for this request**; to touch it later use **`HttpSession.getAccessor()`**.

**Attributes.** `setAttribute` / `getAttribute` are visible to every servlet in this context on later requests in the **same** session. Implement **`HttpSessionBindingListener`** (`valueBound` / `valueUnbound`) if the object must notice bind/unbind. The container **thread-safes the attribute map**, not your **values**. Many threads may share one session.

**Timeout.** No HTTP “goodbye.” Idle limit: `ServletContext` session timeout is **minutes**; `HttpSession.setMaxInactiveInterval` is **seconds**. **≤ 0** means **never expire**. Invalidation waits until in-flight `service` methods exit; then new requests must not see that session. `invalidate()` unbinds attributes. `getLastAccessedTime` is the previous access, not this request.

**Distributed app:** one JVM at a time per session; attributes should be **`Serializable`**. **`HttpSessionActivationListener`** around passivation. Assume **all browser windows** share one session.

```d2
direction: down
http: "stateless HTTP" {
  width: 200
  height: 36
  style.fill: "#fff8e1"
}
id: "session id\ncookie or ;jsessionid=" {
  width: 240
  height: 48
  style.fill: "#e3f2fd"
}
hs: "HttpSession\nattributes in this context" {
  width: 240
  height: 48
  style.fill: "#e8f5e9"
}
http -> id
id -> hs
```

**Fig. 1.** The id is the correlation token. The object is application-scoped state.

```java
// Conceptual — jakarta.servlet.http, Servlet 6.1
HttpSession session = req.getSession(); // creates if needed
session.setAttribute("cart", cart);
if (session.isNew()) { /* client has not joined yet */ }
```

**Listing 1.** Creating a session is not “the user is logged in.” Check `getSession(false)` when you only want an existing one.

> [!warning] `getSession()` is not a login check
> No-arg `getSession()` **mints** a session for anonymous traffic. `isNew()` can stay **true** every request if cookies are off and you never rewrite URLs. Call `getSession` **before the response is committed** if a cookie must be set.

> [!warning] Do not stash the `HttpSession` on another thread
> Using the object after `service` returns is undefined unless you go through **`getAccessor()`**. Attribute **values** still need their own concurrency story. URL rewriting plus mixed HTTP/HTTPS is a leak; prefer cookies and `HttpOnly`.

> [!tip] Interview answer
> HTTP has no session, so the container tracks a client with a JSESSIONID cookie, or with a jsessionid path parameter if cookies are off. getSession creates or returns that HttpSession; getSession false returns null when there isn’t a valid one. The session is new until the client sends the id back, it is scoped to one ServletContext, and a session object is not the same thing as an authenticated user.
