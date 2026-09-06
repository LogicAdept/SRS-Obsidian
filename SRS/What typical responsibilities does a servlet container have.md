<!--
reps: 0
priority: 0
-->
#Java/Servlet/Container #SRS

# What typical responsibilities does a servlet container have?

> [!abstract] Short answer
> The **servlet container** (engine) **owns the network**, **MIME request/response**, **URL mapping**, and **servlet lifecycle**. Jakarta Servlet **6.1 §1.2–1.3**: provide **HTTP/HTTPS** (required **HTTP/1.1 and HTTP/2**), **decode** the request, **choose** a servlet, call **`service` with request/response objects**, **flush**, and **return** to the web server. It also **`init`/`destroy`s** instances, runs the **filter chain**, holds **`ServletContext` and sessions**, and may **authenticate** and **restrict** the servlet. The servlet writes **business logic** only. Identity: [[What is a servlet container]]. What a servlet is: [[What is a servlet]]. Lifecycle: [[How does a servlet container manage the servlet lifecycle]]. Mapping: [[How is an HttpServlet request processed]]. App server vs engine: [[Why use Java EE application servers when servlet containers exist]].

## Network, mapping, lifecycle, web-app services

| Responsibility | What the container does |
| --- | --- |
| **Transport** | Listen / accept **HTTP(S)** (and optionally other request/response protocols). **6.1:** HTTP/1.1 + HTTP/2 (`h2`/`h2c`, **ALPN**). |
| **MIME** | **Decode** the incoming message; **format** the outgoing one. |
| **Dispatch** | Map the URL (and method) to a **servlet** (and **filters**). Filters: [[How would you explain servlet filters and request interception]]. |
| **Objects** | Create **`ServletRequest` / `ServletResponse`** (HTTP subtypes) and call **`service`**. |
| **Lifecycle** | Load class, **`new`**, **`init` once**, **`service` 0..n (often concurrent)**, **`destroy` once**. |
| **Completion** | **Flush** the response; hand control back to the **host HTTP server**. |
| **Application** | One **`ServletContext` per web app** (per JVM); **sessions** (`JSESSIONID` / rewrite). Sessions: [[How would you explain HTTP sessions in servlet based applications]]. |
| **Security** | May **restrict** the servlet’s environment; **login-config** mechanisms. Auth: [[What servlet authentication mechanisms exist]]. |
| **Cache** | May **alter or skip** the servlet per **HTTP caching** rules. |

Where it runs: **in** the web server, as an **add-on**, or **inside** an application server; **same process, other process, or other host** relative to the HTTP listener. Cookie session tracking **must** be supported (default name **`JSESSIONID`**). **`WEB-INF` / `META-INF`** are **not client-visible** (404); **`getResource*`** can still read them. **Welcome files / error pages** and **URI canonicalization** (mapping vs security) are container jobs. **JSP translation** is the **Pages** container, not a required Servlet-spec chapter. **JNDI pools** are **Jakarta EE**, not Chapter 1.

```d2
direction: down
net: "HTTP(S) + MIME decode/encode" {
  width: 260
  height: 40
  style.fill: "#e3f2fd"
}
map: "map URL → filters + servlet" {
  width: 240
  height: 40
  style.fill: "#fff8e1"
}
life: "init / service / destroy\ncontext + session" {
  width: 240
  height: 48
  style.fill: "#e8f5e9"
}
net -> map -> life
```

**Fig. 1.** The **servlet does application logic**. The **container does everything around it**.

```java
// Conceptual — Jakarta Servlet 6.1
@WebServlet("/ping")
public class PingServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        resp.getWriter().write("ok"); // container built req/resp, will flush
    }
}
```

**Listing 1.** The class **does not** bind a port, parse HTTP, or call **`init`**. Those are **container** jobs.

> [!warning] Caching can skip your servlet
> The engine **may answer from cache** without **`service`**. **HTTP/2** is a **6.1 container** duty, not something `doGet` implements. **Concurrent `service`** is the container’s threading model — **you** must make the instance thread-safe.

> [!warning] Container ≠ application server ≠ `ServletContext`
> A **Jakarta EE server** **includes** a servlet engine **plus** other specs. **`ServletContext`** is the **app view**, not the engine process. **Java SE 17** is the **6.1** container minimum, not a servlet author’s `javac` target by itself. **“New thread per request”** is **not** the spec — engines **pool**. **Declarative security does not apply** to **`RequestDispatcher.forward` / `include`**.

> [!tip] Interview answer
> A servlet container speaks HTTP, turns the bytes into request and response objects, maps the URL to a servlet, and drives init, service, and destroy. It also owns the filter chain, the ServletContext, sessions, and optional login. My servlet only implements the application work; the container handles the rest, including flushing the response.
