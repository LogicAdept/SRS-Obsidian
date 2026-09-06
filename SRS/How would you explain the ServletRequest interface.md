<!--
reps: 0
priority: 0
-->
#Java/Servlet #SRS

# How would you explain the ServletRequest interface?

> [!abstract] Short answer
> **`ServletRequest` is the protocol-neutral view of one incoming request.** The container **creates** it and passes it into **`Servlet.service`** and **`Filter.doFilter`**. From it you read **parameters**, **attributes**, **body** (`getInputStream` **or** `getReader`), **scheme / protocol / remote and local address**, **locale**, and **`isSecure`**. HTTP extras — URI path, headers, cookies, session, `getParts` — live on **`HttpServletRequest`**. Lifetime: **this `service` / `doFilter` only**, unless **`startAsync`**. Pair: [[How would you explain the ServletResponse interface]]. Mapping into `service`: [[How is an HttpServlet request processed]]. Attributes across a dispatch: [[How would you explain the servlet RequestDispatcher for forward and include]].

## Parameters, body, attributes, lifetime

**Parameters.** `getParameter` / `getParameterValues` / `getParameterNames` / `getParameterMap` (`Map<String,String[]>`, **immutable**). `getParameter` is the **first** of `getParameterValues`. For HTTP, the map is **query string then POST body** (`a=hello` plus body `a=goodbye&a=world` → `hello, goodbye, world`). **Form body** joins that map only for **HTTP POST** + **`application/x-www-form-urlencoded`** (or multipart when the servlet has **`@MultipartConfig` / `<multipart-config>`**) after the **first** `getParameter*` call — then the **body stream is consumed**. Otherwise read the body yourself. Missing name → **`null`**. Path parameters (`;jsessionid=`) are **not** in this API.

**Body.** **`getInputStream()` XOR `getReader()`** — the second throws **`IllegalStateException`**. Same exclusive pair on the response: [[Can a servlet use PrintWriter and ServletOutputStream on the same response]]. **`setCharacterEncoding`** (String, or **`Charset` since 6.1**) must run **before** parameters or `getReader`, or it is a **no-op**. If the client omitted charset: **`getCharacterEncoding()` is `null`**; the container still parses **urlencoded** as **US-ASCII** (`%nn` → ISO-8859-1) and other types as **ISO-8859-1** unless app/container config says otherwise. **`getContentLength`** is `-1` if unknown or **> `Integer.MAX_VALUE`**; use **`getContentLengthLong`** (Servlet 3.1).

**Attributes.** Request-scoped objects for the container (SSL, dispatcher) or for you before a **`RequestDispatcher`**. **One value per name**; `setAttribute(name, null)` is **`removeAttribute`**. Names **`jakarta.*` are reserved**. HTTPS: **`isSecure()`**, plus `jakarta.servlet.request.cipher_suite`, `key_size`, `ssl_session_id`, `secure_protocol`, and **`jakarta.servlet.request.X509Certificate`**. [[What are servlet attributes for and how do they work]]

**Also on this interface:** `getProtocol` / `getScheme` / `getServerName` / `getServerPort`; `getRemoteAddr` (client **or last proxy**, maybe RFC 7239) / `getRemoteHost` / `getRemotePort`; `getLocalAddr` / `getLocalName` / `getLocalPort`; `getLocale` / `getLocales` (`Accept-Language`, else container default); `getRequestDispatcher` (path **relative to this request**); `getDispatcherType`; `getServletContext`; `startAsync` (3.0). Client address: [[How do you get the client IP address in a servlet]]. Filters: [[How would you explain servlet filters and request interception]].

**Lifetime.** Valid only in **`service` / `doFilter`**, unless **`startAsync`** — then until **`AsyncContext.complete`**. Containers **recycle** the object; keeping a reference afterward is undefined.

```d2
direction: down
c: "container" {
  width: 160
  height: 36
  style.fill: "#fff8e1"
}
r: "ServletRequest\nparams · attrs · body" {
  width: 260
  height: 48
  style.fill: "#e3f2fd"
}
h: "HttpServletRequest\nURI · headers · cookies · session" {
  width: 300
  height: 48
  style.fill: "#e8f5e9"
}
c -> r
r -> h: "HTTP"
```

**Fig. 1.** The container hands you `ServletRequest`. For HTTP you almost always downcast to `HttpServletRequest`.

```java
// Conceptual — jakarta.servlet, Servlet 6.1
@Override
public void service(ServletRequest req, ServletResponse resp) throws IOException {
    String q = req.getParameter("q");           // first value, or null
    req.setCharacterEncoding(java.nio.charset.StandardCharsets.UTF_8); // too late if getParameter already ran
    try (var in = req.getInputStream()) {       // IllegalStateException if getReader() was used
        in.readAllBytes();
    }
}
```

**Listing 1.** `getParameter` parses the body. Call **`setCharacterEncoding` first**, and pick **stream or reader**, not both.

> [!warning] Parameter parse eats the POST body
> The first `getParameter*` on a urlencoded POST **reads the entity**. A later `getInputStream` / `getReader` will not see those bytes. The reverse also breaks parameter parsing. **`getParameter` is not `getAttribute`.**

> [!warning] Do not stash the request
> After `service` / `doFilter` returns (no `startAsync`), the object may be **reused for another client**. `getRemoteAddr` is **not** “the browser” behind a proxy unless a protocol mapping (for example RFC 7239) is in play.

> [!tip] Interview answer
> ServletRequest is the container’s protocol-neutral request: parameters, attributes, body, addresses, locale, and isSecure. I use getParameter for query and urlencoded POST, getAttribute for request-scoped objects, and either getInputStream or getReader, never both. HTTP headers and the URI live on HttpServletRequest; the object is only valid for this service call unless I start async.
