<!--
reps: 0
priority: 0
-->
#Java/Servlet #SRS

# How is an HttpServlet request processed?

> [!abstract] Short answer
> The container **picks the web app** (longest matching **context path**), **maps the remaining path** to a servlet (exact, then longest prefix `…/*`, then `*.ext`, then the **default** servlet `/`), runs the **filter chain**, then calls **`Servlet.service`**. **`HttpServlet.service`** turns the HTTP method into **`doGet` / `doPost` / `doPut` / `doDelete` / `doHead` / `doOptions` / `doTrace`**. Mapping uses **case-sensitive** comparisons; path parameters such as `;jsessionid=` are **stripped** before the match. Lifecycle (when `init` ran): [[How does a servlet container manage the servlet lifecycle]]. Why `doXxx`: [[Why is HttpServlet declared as an abstract class]]. Filters: [[How would you explain servlet filters and request interception]]. Request API: [[How would you explain the ServletRequest interface]].

## Map, wrap, dispatch, `doXxx`

**1. Which application.** Decode the request URL as **UTF-8**. Choose the `ServletContext` whose **context path** is the **longest prefix** of that URL.

**2. Which servlet.** Mapping path = URL **minus** context path and **path parameters**. First hit wins:

1. **Exact** pattern (`/catalog`).
2. **Longest path prefix** (`/foo/bar/*`).
3. **Extension** on the last segment (`*.jsp`, `*.bop`). An application `*.jsp` mapping **beats** the container’s implicit JSP mapping.
4. **Default** servlet, pattern `/` — servlet path is the rest of the URI, **path info is `null`**.

Pattern `""` is the **context root**; servlet path is `""`, path info is `"/"`. The same `url-pattern` on **two** servlets after merge → **deployment fails**.

**3. Filters, then `service`.** Matching filters run **`doFilter`** in order (they may wrap request/response or **stop** the chain). The last `chain.doFilter` is the servlet. **Filters and `service` share one thread.** `HttpServlet.service` rejects a non-HTTP pair and otherwise calls the matching **`doXxx`**. Default **`doHead`** calls **`doGet`** (legacy header-only wrap is deprecated). **`CONNECT`** is for proxies: the container **must** answer **501** and **must not** invoke a filter or servlet (unless a vendor option says otherwise).

**4. Path pieces on `HttpServletRequest`.** After mapping: **context path**, **servlet path**, **path info**, plus query string. `getHttpServletMapping()` describes **this** activation (not for `getNamedDispatcher`). These objects are valid **only** for this `service` / `doFilter` (unless `startAsync`).

```d2
direction: down
url: "request URL" {
  width: 200
  height: 36
  style.fill: "#fff8e1"
}
ctx: "longest context path" {
  width: 220
  height: 36
  style.fill: "#e3f2fd"
}
map: "exact → prefix → *.ext → /" {
  width: 260
  height: 36
  style.fill: "#e3f2fd"
}
fil: "FilterChain.doFilter" {
  width: 220
  height: 36
  style.fill: "#fff8e1"
}
svc: "HttpServlet.service → doXxx" {
  width: 260
  height: 40
  style.fill: "#e8f5e9"
}
url -> ctx
ctx -> map
map -> fil
fil -> svc
```

**Fig. 1.** Mapping finishes before any `doGet`. Filters can still block the servlet.

```java
// Conceptual — jakarta.servlet.http, Servlet 6.1
@Override
protected void doGet(HttpServletRequest req, HttpServletResponse resp)
        throws IOException {
    String ctx = req.getContextPath();   // /shop
    String servlet = req.getServletPath(); // /catalog
    String extra = req.getPathInfo();    // /items/42 or null
    resp.getWriter().write(ctx + servlet + (extra == null ? "" : extra));
}
```

**Listing 1.** Override **`doGet`**, not `service`, unless you must intercept every method. Prefix `/catalog` does **not** own `/catalog/index.html` if `/catalog` was an **exact** map.

> [!warning] Prefix vs exact vs extension
> `/foo/bar/index.bop` matches **`/foo/bar/*`**, not `*.bop`. `/catalog` as an **exact** pattern does not take `/catalog/racecar.bop`. Comparisons are **case-sensitive**. Do not keep the request object after `service` returns.

> [!warning] `service` is concurrent
> The container may call `service` on **many threads** for one instance. Shared fields need their own locking; do not synchronize `service` as a policy. If a filter never calls `chain.doFilter`, **`doXxx` never runs**.

> [!tip] Interview answer
> The container matches the longest context path, then maps the rest of the path with exact, longest prefix, extension, then the default servlet. Filters wrap that target on the same thread, then HttpServlet.service calls doGet or doPost for the HTTP method. I read context path, servlet path, and path info from the request, and I remember an exact map does not steal extra path segments.
