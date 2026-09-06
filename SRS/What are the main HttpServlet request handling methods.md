<!--
reps: 0
priority: 0
-->
#Java/Servlet #SRS

# What are the main HttpServlet request handling methods?

> [!abstract] Short answer
> **`HttpServlet.service` dispatches** the HTTP method to **`doGet`**, **`doPost`**, **`doPut`**, **`doDelete`**, **`doHead`**, **`doOptions`**, **`doTrace`**, and (Jakarta Servlet **6.1**) **`doPatch`**. You almost **never override `service`**. Day-to-day you override **`doGet` and `doPost`**; the rest are for people who know HTTP well. **`GET`/`HEAD` should be safe and idempotent**; **`POST`/`PUT`/`PATCH`/`DELETE` need not be**. Dispatch path: [[How is an HttpServlet request processed]]. Why the class is abstract: [[Why is HttpServlet declared as an abstract class]]. Lifecycle around `service`: [[What are the three core Servlet lifecycle methods and their roles]]. Concurrency: [[How do servlets work in a multithreaded environment]].

## `service` → `doXxx`

Public **`service(ServletRequest, ServletResponse)`** casts to HTTP and calls protected **`service(HttpServletRequest, HttpServletResponse)`**, which **switches on the method** and calls the matching **`doXxx`**. All **`doXxx`** are **`protected`**.

| Method | HTTP | Default / notes |
| --- | --- | --- |
| **`doGet`** | `GET` | Override for reads. Should be **safe** and **idempotent**. Also covers **`HEAD`** unless you override **`doHead`**. **`getLastModified`** supports **conditional GET**. |
| **`doHead`** | `HEAD` | Default **calls `doGet`**. Container implements HEAD (no body). Deprecated init-param **`jakarta.servlet.http.legacyDoHead=TRUE`** wraps the response and keeps only headers. |
| **`doPost`** | `POST` | Body of unlimited length; **not** required to be safe/idempotent. |
| **`doPut`** | `PUT` | Place/replace a resource. Keep content headers or send **501**. |
| **`doPatch`** | `PATCH` | **Partial** update (API since **6.1**). |
| **`doDelete`** | `DELETE` | Remove a resource. |
| **`doOptions`** | `OPTIONS` | Default **`Allow`** lists methods you implemented (e.g. override **`doGet`** → `GET, HEAD, TRACE, OPTIONS`). Rarely override. |
| **`doTrace`** | `TRACE` | Echoes request headers; **`isSensitiveHeader`** strips **`Authorization`**, **`Cookie`**, **`X-Forwarded*`**, **`Forwarded`**, **`Proxy-Authorization`**. Rarely override. |

**`CONNECT`** is for proxies. By default the **container rejects it with 501** and does **not** call a Filter or Servlet.

Malformed **`doGet` / `doPost` / …** requests: JavaDoc says an HTTP **Bad Request** message. Request/response types: [[How would you explain the ServletRequest interface]], [[How would you explain the ServletResponse interface]].

```d2
direction: down
svc: "service(req, res)\n→ HTTP service(...)" {
  width: 240
  height: 48
}
do: "doGet / doPost / doPut / doPatch\ndoDelete / doHead / doOptions / doTrace" {
  width: 320
  height: 56
  style.fill: "#e8f5e9"
}
svc -> do: "dispatch on HTTP method"
```

**Fig. 1.** Override **`doXxx`**, not **`service`**, unless you are replacing HTTP dispatch.

```java
// Conceptual — Jakarta Servlet 6.1
public class OrderServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        resp.setContentType("text/plain;charset=UTF-8");
        resp.getWriter().write("order " + req.getParameter("id"));
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        // not required to be idempotent
        resp.setStatus(HttpServletResponse.SC_CREATED);
    }
}
```

**Listing 1.** Typical servlet: **`doGet` + `doPost`**. **`HEAD`** follows **`doGet`** unless you override **`doHead`**.

> [!warning] Do not put work in `service` and skip `doXxx`
> Overriding **`service(HttpServletRequest, HttpServletResponse)`** bypasses **`doGet` / `doPost` / `getLastModified`**. If you do, you own **every** method, including **OPTIONS** and **TRACE**. **`doGet` must not** have user-accountable side effects; use **POST/PUT/PATCH/DELETE** to change stored data.

> [!warning] `HEAD` still runs `doGet` by default
> A slow **`doGet`** is a slow **`HEAD`**. Legacy **`LEGACY_DO_HEAD`** is **deprecated for removal**. **`doTrace`** must not echo cookies or credentials — override **`isSensitiveHeader`** if you add more. Concurrent **`doXxx`** on one instance is normal.

> [!tip] Interview answer
> HttpServlet.service looks at the HTTP method and calls doGet, doPost, doPut, doPatch, doDelete, doHead, doOptions, or doTrace. I override doGet and doPost and leave service alone. GET and HEAD should be safe and idempotent; HEAD defaults to doGet with the body omitted. OPTIONS and TRACE already have useful defaults, and CONNECT is rejected with 501 unless the container special-cases proxies.
