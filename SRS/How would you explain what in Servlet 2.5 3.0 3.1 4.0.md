<!--
reps: 0
priority: 0
-->
#Java/Servlet #Java/JavaEE #SRS

# How would you explain what in Servlet 2.5 3.0 3.1 4.0?

> [!abstract] Short answer
> **2.5** (Java EE 5, **JCP MR May 2006**): **J2SE 5.0** minimum; Java EE containers **inject resources** into servlets/filters/listeners — **not** `@WebServlet`. **3.0** (Java EE 6, **Dec 2009**): **`@WebServlet` / `@WebFilter` / `@WebListener`**, **`web-fragment.xml`**, programmatic **`addServlet`**, **`startAsync`**, **`login`/`logout`**, **`@MultipartConfig`**. **3.1** (Java EE 7, **May 2013**): **non-blocking I/O** (`ReadListener` / `WriteListener`) and **HTTP upgrade** (`HttpUpgradeHandler`). **4.0** (Java EE 8, **Sep 2017**): **HTTP/2 required** plus **server push** (`PushBuilder`). Servlet 3 detail: [[What features were added in the Servlet 3 specification]]. HTTP/2 in the engine: [[What typical responsibilities does a servlet container have]].

## Four Java EE servlet jumps

**2.5 — JSR 154 maintenance, not a new JSR.** Headline: containers **must** be built on **J2SE 5.0**. On a **Java EE** container, servlets, filters, and listeners get **annotations and resource injection** (`@Resource` and friends, spec SRV.14.5). That is **not** annotation-based **registration**. Also: multiple URL patterns per mapping, `filter-mapping` servlet-name `*` for all forwards, any HTTP method token in constraints, session-scope wording for portlets. `web.xml` is still the registration story.

**3.0 — JSR 315.** **Pluggability:** `META-INF/web-fragment.xml`, `ServletContainerInitializer`, `ServletContext.addServlet` / `addFilter` / `addListener`. **Ease of development:** `@WebServlet`, `@WebFilter`, `@WebListener`; `web.xml` can be omitted or used to **override**. **Async:** `ServletRequest.startAsync` / `AsyncContext` (thread returns; complete or dispatch later). **Security:** programmatic **`login` / `logout` / `authenticate`**. **Upload:** `@MultipartConfig` and `HttpServletRequest.getParts()`. **NIO did not ship here** even though the JSR proposal talked about it. Annotations: [[How would you explain servlet filters and request interception]]. Async vs `init`/`service`: [[How does a servlet container manage the servlet lifecycle]].

**3.1 — JSR 340.** **Non-blocking I/O** on `ServletInputStream` / `ServletOutputStream` **only** with async or upgrade. **Upgrade:** `HttpServletRequest.upgrade(HttpUpgradeHandler.class)` then byte streams on `WebConnection` (WebSocket handshake and similar). Also: `getContentLengthLong`, `HttpSessionIdListener`, `ServletContext.getVirtualServerName`.

**4.0 — JSR 369.** Containers **must** implement **HTTP/1.1 and HTTP/2** (`h2` / `h2c`, ALPN). **Server push:** `HttpServletRequest.newPushBuilder()` — **deprecated and optional in Servlet 6.1**. Also: `HttpFilter` / `GenericFilter`, mapping discovery (`getHttpServletMapping`), HTTP **trailers**, `ServletContext` request/response character encoding and session timeout APIs, `addJspFile`. Still **`javax.servlet`**; the **`jakarta.servlet` rename is 5.0**, not 4.0.

```d2
direction: right
v25: "2.5\nJ2SE 5 + EE injection" {
  width: 200
  height: 48
  style.fill: "#fff8e1"
}
v30: "3.0\nannotations, fragments, async, parts" {
  width: 260
  height: 48
  style.fill: "#e3f2fd"
}
v31: "3.1\nNIO + HTTP upgrade" {
  width: 220
  height: 48
  style.fill: "#fff3e0"
}
v40: "4.0\nHTTP/2 + PushBuilder" {
  width: 220
  height: 48
  style.fill: "#e8f5e9"
}
v25 -> v30
v30 -> v31
v40 <- v31
```

**Fig. 1.** Each step is a **Java EE** servlet spec. Do not fold 3.1 NIO into 3.0 async, or 5.0 `jakarta.*` into 4.0.

```java
// Conceptual — what each line needs
@WebServlet("/ok")                 // 3.0 registration, not 2.5
@MultipartConfig                   // 3.0 upload
public class ApiServlet extends HttpFilter { // HttpFilter: 4.0
    @Override
    protected void doFilter(HttpServletRequest req, HttpServletResponse res, FilterChain chain)
            throws java.io.IOException, ServletException {
        req.startAsync();          // 3.0
        req.getInputStream().setReadListener(/* 3.1 NIO, async only */);
        req.newPushBuilder();      // 4.0; may be null; 6.1 deprecated
        chain.doFilter(req, res);
    }
}
```

**Listing 1.** Mixed-era APIs. A 2.5 container has **none** of `@WebServlet`, `startAsync`, `setReadListener`, or `newPushBuilder`. Prefer **`javax.servlet`** names on a real 4.0 stack.

> [!warning] 2.5 “annotations” are not `@WebServlet`
> 2.5 injection runs on **Java EE** containers. A servlet **engine** can be 2.5-compatible **without** `@Resource`. **`@WebServlet` is 3.0.** Interview dumps that date 2.5 as “September 2005” are using a **maintenance draft**, not the **May 2006** JCP maintenance release (MR2 **Sep 2007**).

> [!warning] Async ≠ non-blocking ≠ HTTP/2
> **3.0 async** frees the container thread; the stream can still **block**. **3.1 NIO** is `isReady` / listeners, and **only** after async or upgrade. **4.0 HTTP/2** is the wire protocol; **push** is extra and **not guaranteed** (`newPushBuilder()` may return **`null`**; Servlet **6.1** makes push **optional**).

> [!tip] Interview answer
> Servlet 2.5 is Java EE 5: Java 5 and resource injection, still XML registration. 3.0 adds web fragments, @WebServlet, async, login/logout, and multipart. 3.1 adds non-blocking I/O and HTTP protocol upgrade. 4.0 requires HTTP/2 and adds server push; the jakarta rename is the later 5.0 spec.
