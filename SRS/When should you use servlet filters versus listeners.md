<!--
reps: 0
priority: 0
-->
#Java/Servlet/Filters #Java/Servlet/Listeners #SRS

# When should you use servlet filters versus listeners?

> [!abstract] Short answer
> Use a **filter** to **sit on the request path** and **adapt HTTP** (headers, body, wrapping) **before/after** a resource. Use a **listener** to **react to lifecycle or attribute events** on **`ServletContext`**, **`HttpSession`**, or **`ServletRequest`** — **not** to transform the bytes of this call. Spec filter examples: **auth, logging, compression, encryption, wrapping**. Spec listener examples: **open a DB on context start**, **session create/destroy**, **request initialized**. Filters: [[How would you explain servlet filters and request interception]]. Wrappers: [[What servlet wrapper classes exist]]. Context: [[How would you explain ServletContext in Java web applications]]. Sessions: [[How would you explain HTTP sessions in servlet based applications]].

## Chain vs notification

Jakarta Servlet **6.1 §6.1**: a **filter** is reusable code that **transforms** request/response/**headers**. It **generally does not** create the response the way a servlet does. It **may wrap** the request/response, run **before and after** `chain.doFilter`, and apply to **servlets or static content** in a **declared order**.

**§11.1–11.2:** **listeners** give control over the **lifecycle** of context, session, and request, and **factor resource management**. They are **not** a second filter chain.

| Use a **filter** when you need to… | Use a **listener** when you need to… |
| --- | --- |
| Inspect/modify **this** request or response | Know **context started / about to stop** (`ServletContextListener`) |
| **Wrap** `HttpServletRequest` / `Response` | Track **session create / invalidate / timeout** (`HttpSessionListener`) |
| **Compress, encrypt, rewrite** body or headers | Track **attribute add/replace/remove** (context/session/request) |
| **Authenticate** or **audit** on a URL pattern | Bind/unbind of an **object in the session** (`HttpSessionBindingListener` **on the object**) |
| Ordered **chain** around a resource | **Async** timeout/complete (`AsyncListener` on the **request**, not `web.xml`) |

**`ServletRequestListener`:** request **began / finished** being processed — good for **timing or per-request state**, **not** for wrapping the entity. **`ReadListener` / `WriteListener`** are **3.1 NIO** callbacks, not Chapter 11 app listeners. Attributes: [[What are servlet attributes for and how do they work]].

```d2
direction: down
f: "Filter.doFilter\nwrap → chain → unwrap" {
  width: 260
  height: 48
  style.fill: "#e8f5e9"
}
l: "Listener\ncontextInitialized / sessionCreated / …" {
  width: 300
  height: 48
  style.fill: "#fff8e1"
}
f -> l: "both may see a request\nonly the filter can wrap it" {
  style.stroke-dash: 3
}
```

**Fig. 1.** **Filters intercept I/O.** **Listeners observe events.**

```java
// Conceptual — Jakarta Servlet 6.1
@WebFilter("/*")
public class GzipFilter implements Filter {
    public void doFilter(ServletRequest req, ServletResponse resp, FilterChain chain) throws IOException, ServletException {
        chain.doFilter(req, new HttpServletResponseWrapper((HttpServletResponse) resp) { /* wrap getOutputStream */ });
    }
}

@WebListener
public class PoolListener implements ServletContextListener {
    public void contextInitialized(ServletContextEvent e) { /* open pool, setAttribute */ }
    public void contextDestroyed(ServletContextEvent e) { /* close pool */ }
}
```

**Listing 1.** **Compression = filter.** **Application-scoped resource = context listener.**

> [!warning] A request listener is not a filter
> **`requestInitialized`** cannot **replace** the response writer or **stop** the servlet the way **not calling `chain.doFilter`** can. Opening JDBC in a **filter** on every request instead of **`contextInitialized`** is the spec’s listener example **inverted**.

> [!warning] Logging overlaps both
> Spec lists **logging filters** and **request listeners**. Prefer a **filter** if you need **URL mapping, wrappers, or post-resource body**. Prefer a **listener** if you need **session destroy** or **context shutdown** (no current `doFilter`). Attribute listeners may fire **concurrently**; the container **need not** serialize them.

> [!tip] Interview answer
> I use a filter when I need to wrap or transform the HTTP request or response on the way in and out — auth, gzip, headers. I use a listener when something is created or destroyed: the ServletContext, an HttpSession, or a request lifecycle event. Filters are a chain around a resource; listeners are callbacks, not a second chain.
