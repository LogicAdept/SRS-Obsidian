<!--
reps: 0
priority: 0
-->
#Java/Servlet #SRS

# How would you explain the servlet RequestDispatcher for forward and include?

> [!abstract] Short answer
> **`RequestDispatcher` is a server-side hand-off** to another servlet, JSP, or static resource **in the same request**. **`forward`** transfers **the whole response** (caller must not have **committed**; the buffer is **cleared**; when `forward` returns the container **commits and closes** unless async). **`include`** **splices body** into the current response (headers from the include are **ignored**). Neither is **`sendRedirect`**: no new client round trip. Redirect contrast: [[How does sendRedirect differ from forward in servlets]]. Wrappers you may pass: [[What servlet wrapper classes exist]]. Filters on these hops: [[How would you explain servlet filters and request interception]].

## Obtain, `forward`, `include`

**Obtain.** `ServletContext.getRequestDispatcher(path)` — path is **context-relative**, **`/`**-prefixed or **empty**. `ServletRequest.getRequestDispatcher(path)` — **relative to this request** (`header.html` under `/garden/tools.html` → `/garden/header.html`). Matching uses the usual servlet rules; if no servlet matches, you still get a dispatcher for **that path’s content**. `getNamedDispatcher(name)` binds a **servlet name**, or **`null`**. Query string on the path is allowed; those params **win** over same-named request params **only for the duration** of that `forward` / `include`.

**Same thread, same JVM.** Pass the **`service` request/response** or **wrappers of them**. `forward` sets **`DispatcherType.FORWARD`**; `include` is **`INCLUDE`**. Default filters are **`REQUEST` only**, so they **skip** these hops unless mapped for `FORWARD` / `INCLUDE`. **Declarative security does not apply** to dispatcher `forward` / `include`.

**`forward`.** Legal only if the response is **not committed**; otherwise **`IllegalStateException`**. Uncommitted buffer is **cleared**. The target’s **`getRequestURI` / servlet path / …** become the **dispatcher path** (except **named** dispatch: paths stay the **original** request). Original client path is in **`jakarta.servlet.forward.*`** (`RequestDispatcher.FORWARD_REQUEST_URI`, …) — **not** set for named dispatch; they **keep reflecting the first client request** through later forwards/includes. On normal return the container **sends, commits, and closes** the response (unless async). Do not write after `forward`.

**`include`.** Callable **anytime**. The include may **write the body** and **flush**; **set-header attempts are ignored**. `getSession` that would add a **Cookie** header throws **`IllegalStateException`** if the response is already committed. The include’s own path is in **`jakarta.servlet.include.*`** (replaced on nested include; **not** set for named dispatch). Missing static target via the **default servlet** → **`FileNotFoundException`**, and **500** if uncaught and the response is not committed.

**Exceptions** from the target (`RuntimeException`, `ServletException`, `IOException`) propagate to the caller; other checked exceptions become **`ServletException`** with the original as root cause.

```d2
direction: down
client: "client request" {
  width: 180
  height: 36
  style.fill: "#fff8e1"
}
a: "servlet A" {
  width: 140
  height: 36
  style.fill: "#e3f2fd"
}
fwd: "forward\nclears buffer, target owns response" {
  width: 280
  height: 48
  style.fill: "#fff3e0"
}
inc: "include\nwrites body, A continues" {
  width: 260
  height: 48
  style.fill: "#e8f5e9"
}
b: "servlet or static B" {
  width: 200
  height: 36
  style.fill: "#e8f5e9"
}
client -> a
a -> fwd
fwd -> b
a -> inc
inc -> b
```

**Fig. 1.** `forward` is a transfer of the response. `include` is a nested write. Both stay on the **server**; the browser URL does not change.

```java
// Conceptual — jakarta.servlet.http, Servlet 6.1
RequestDispatcher view = req.getRequestDispatcher("/WEB-INF/view.jsp");
view.forward(req, resp); // after this, do not write; response will be closed

RequestDispatcher nav = req.getRequestDispatcher("/WEB-INF/nav.jsp");
nav.include(req, resp);  // body spliced; then this servlet may write more
```

**Listing 1.** Path-based dispatchers. After **`forward`**, read the **original** URI from **`RequestDispatcher.FORWARD_REQUEST_URI`**, not `getRequestURI()`. Another servlet: [[How can one servlet call or forward to another servlet]]. Mapping: [[How is an HttpServlet request processed]].

> [!warning] Committed response kills `forward`
> Any **flush** (full buffer, `flushBuffer`, writing past the buffer) **commits**. Then `forward` throws **`IllegalStateException`**. `include` still runs but **cannot change headers**. Do not treat `forward` like `sendRedirect`: the client never sees a new URL.

> [!warning] Named dispatch hides the path attributes
> `getNamedDispatcher("ReportServlet").forward(...)` does **not** set `jakarta.servlet.forward.*`, and **path getters stay on the original request**. Dispatcher query params are **temporary**. Filters and **security constraints** on the target URL often **do not run** on this hop.

> [!tip] Interview answer
> RequestDispatcher is a server-side call to another resource in the same request. Forward clears the uncommitted buffer and lets the target finish the response, then the container commits and closes it; include writes into the current body and the caller continues. I get a dispatcher by path or servlet name, and I remember that getRequestURI after a path forward is the target, while the original client URI sits in the forward request attributes.
