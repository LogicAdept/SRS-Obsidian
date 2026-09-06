<!--
reps: 0
priority: 0
-->
#Java/Servlet #SRS

# What is the difference between GenericServlet and HttpServlet?

> [!abstract] Short answer
> **`GenericServlet`** is a **protocol-independent** helper: it implements **`Servlet`** and **`ServletConfig`**, stores the config, and leaves **`service(ServletRequest, ServletResponse)` abstract**. **`HttpServlet` extends `GenericServlet`** and implements **`service`** by **dispatching HTTP methods** to **`doGet` / `doPost` / …**. For the Web you **extend `HttpServlet`**, not `GenericServlet`. This is **not Java generics** (`List<T>`). What a servlet is: [[What is a servlet]]. Why `HttpServlet` is abstract: [[Why is HttpServlet declared as an abstract class]]. `doXxx`: [[What are the main HttpServlet request handling methods]]. No-arg `init()`: [[Why override the no argument init method in a servlet]].

## Protocol-neutral base vs HTTP subclass

Jakarta Servlet **6.1 §2**: the two API classes that implement **`Servlet`** are **`GenericServlet`** and **`HttpServlet`**. **Most developers extend `HttpServlet`.**

| | **`GenericServlet`** | **`HttpServlet`** |
| --- | --- | --- |
| **Role** | Generic, **protocol-independent** servlet | HTTP servlet for the Web |
| **Extends** | `Object` | **`GenericServlet`** |
| **Implements** | `Servlet`, `ServletConfig`, `Serializable` | same, plus HTTP helpers |
| **`service`** | **`abstract`** — you write it | **Implemented** — looks at the method, calls **`doXxx`**. Almost **never override**. |
| **Request/response** | `ServletRequest` / `ServletResponse` | **`HttpServletRequest` / `HttpServletResponse`** |
| **Extra** | `init()` convenience, `log`, `getInitParameter` via stored config | **`doGet`…`doTrace`/`doPatch`**, **`getLastModified`**, **`isSensitiveHeader`** |

To write a **generic** servlet you **only override `service`**. To write an **HTTP** servlet you **override `doGet`/`doPost`** (and friends). Constructor vs `init`: [[Should you define a constructor for a servlet and how should you initialize it]]. Lifecycle: [[What are the three core Servlet lifecycle methods and their roles]].

```d2
direction: down
s: "interface Servlet" {
  width: 180
  height: 36
}
g: "GenericServlet\nabstract service(req, res)" {
  width: 260
  height: 48
  style.fill: "#fff8e1"
}
h: "HttpServlet\nservice → doGet / doPost / …" {
  width: 280
  height: 48
  style.fill: "#e8f5e9"
}
you: "YourServlet" {
  width: 140
  height: 36
}
s -> g -> h -> you
```

**Fig. 1.** **HTTP work belongs on `HttpServlet`.** `GenericServlet` is the **shared** config/lifecycle base.

```java
// Conceptual — Jakarta Servlet 6.1
public class PingServlet extends HttpServlet { // not GenericServlet
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        resp.getWriter().write("pong");
    }
}
```

**Listing 1.** Web servlet: **`HttpServlet` + `doGet`**. Extending **`GenericServlet`** would force you to implement **`service`** and cast to HTTP yourself.

> [!warning] `GenericServlet` is not `List<E>`
> Interview dumps that answer **type erasure** here mixed up **generic types** with **`GenericServlet`**. **`HttpServlet` is still a `GenericServlet`**: you inherit **`init()`** and **`getServletContext()`**. Skip **`super.init(config)`** only if you override the **no-arg** `init()`.

> [!warning] Do not override `HttpServlet.service` to “be generic”
> That **bypasses `doGet` / `doPost` / `getLastModified`**. If the protocol is not HTTP, **`GenericServlet.service`** is the hook — a **servlet container still must speak HTTP/HTTPS** for web apps; non-HTTP servlets are rare.

> [!tip] Interview answer
> GenericServlet is the protocol-independent base that implements Servlet and ServletConfig and leaves service abstract. HttpServlet extends it and implements service by calling doGet, doPost, and the other HTTP methods. For a web app I extend HttpServlet. The name GenericServlet has nothing to do with Java generics.
