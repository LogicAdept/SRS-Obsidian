<!--
reps: 0
priority: 0
-->
#Java/Servlet #SRS

# How would you explain error context attributes in servlet error handling?

> [!abstract] Short answer
> When the container **forwards** to an **error page**, it sets **request attributes** on the **original unwrapped** request. Read them with `request.getAttribute(RequestDispatcher.ERROR_…)` (names `jakarta.servlet.error.*`). You get **status**, **exception**, **exception type**, **message**, **request URI**, **query string**, **servlet name**, and (6.1) the **original HTTP method**. The error dispatch itself is always **GET**; `getMethod()` is **not** the failing method. JSP: [[How do you handle errors on JSP pages]]. Forward shape: [[How can one servlet call or forward to another servlet]]. Filters on `ERROR`: [[How would you explain servlet filters and request interception]]. Dispatcher: [[How would you explain the servlet RequestDispatcher for forward and include]].

## What the container puts on the request

`web.xml` `<error-page>` (by **`error-code`**, by **`exception-type`**, or a **default** with neither) names a servlet or JSP. The container then behaves as a **`RequestDispatcher.forward`**: path and attributes look like a forward, **`DispatcherType.ERROR`**.

**Always set** (types as boxed objects):

| Attribute | Type | Meaning |
| --- | --- | --- |
| `jakarta.servlet.error.status_code` | `Integer` | Status that triggered `sendError`, or 500 when an exception reached the container |
| `jakarta.servlet.error.exception` | `Throwable` | The throwable (since 2.3; prefer this) |
| `jakarta.servlet.error.exception_type` | `Class` | Type of that throwable (kept for old pages) |
| `jakarta.servlet.error.message` | `String` | Message (also redundant with the throwable) |
| `jakarta.servlet.error.request_uri` | `String` | `getRequestURI()` of the **failing** request |
| `jakarta.servlet.error.query_string` | `String` | `getQueryString()` of the failing request |
| `jakarta.servlet.error.servlet_name` | `String` | Logical servlet name that failed |

**Original method.** Error pages are dispatched as **GET**. `RequestDispatcher.ERROR_METHOD` holds `getMethod()` from **immediately before** that dispatch (so a failed **POST** still reports `"POST"` here).

**How you get there.** `sendError` matches **`error-code`**. An exception that **propagates to the container** matches **`exception-type`** (closest superclass wins). For `ServletException`, if nothing matches, the container tries **`getRootCause()`** on a **second pass**. Unmatched container-level failure → **500**. **`setStatus` on 2xx/3xx does not** run this mechanism; 4xx/5xx from the **default servlet** go through **`sendError`**.

The mechanism **does not** intercept errors thrown **under** `RequestDispatcher` or `FilterChain.doFilter` — the caller can handle those. Async work on **application** threads is the application’s problem.

```d2
direction: down
fail: "sendError / uncaught exception" {
  width: 260
  height: 40
  style.fill: "#ffebee"
}
attr: "set jakarta.servlet.error.*" {
  width: 260
  height: 40
  style.fill: "#fff8e1"
}
page: "error page as GET forward\nread attributes" {
  width: 260
  height: 48
  style.fill: "#e8f5e9"
}
fail -> attr
attr -> page
```

**Fig. 1.** Attributes describe the **failed** request. The error resource is a new **GET** dispatch.

```java
// Conceptual — jakarta.servlet, Servlet 6.1
Integer status = (Integer) req.getAttribute(RequestDispatcher.ERROR_STATUS_CODE);
Throwable t = (Throwable) req.getAttribute(RequestDispatcher.ERROR_EXCEPTION);
String uri = (String) req.getAttribute(RequestDispatcher.ERROR_REQUEST_URI);
String method = (String) req.getAttribute(RequestDispatcher.ERROR_METHOD);
```

**Listing 1.** Use the `RequestDispatcher` constants, not ad-hoc strings. `exception_type` / `message` duplicate `exception`.

> [!warning] `getMethod()` on the error page is GET
> Do not treat `req.getMethod()` as the client’s original verb. Use **`ERROR_METHOD`**. URI/query on the error request are the **error location’s** path; the **failed** URI is **`ERROR_REQUEST_URI`** / **`ERROR_QUERY_STRING`**.

> [!warning] Wrappers and nested dispatch
> The error resource sees the **container’s original** request/response, not your filter wrappers. Nested `forward`/`include` errors **do not** auto-jump to `<error-page>`. Duplicate `error-code` or `exception-type` entries are illegal.

> [!tip] Interview answer
> The container forwards to the error page like a RequestDispatcher forward and sets jakarta.servlet.error attributes for status, exception, URI, query, and servlet name. I read those with RequestDispatcher constants. The error dispatch is always GET, so the original POST or PUT is only on ERROR_METHOD, and setStatus of a success code will not trigger this at all.
