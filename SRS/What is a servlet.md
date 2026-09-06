<!--
reps: 0
priority: 0
-->
#Java/Servlet #SRS

# What is a servlet?

> [!abstract] Short answer
> A **servlet** is a **Jakarta web component**: a **platform-independent Java class**, **managed by a container** (servlet engine), that **generates dynamic content** using a **request/response** model. You implement **`jakarta.servlet.Servlet`**, almost always by extending **`HttpServlet`**. The **interface is the contract**, not the component. The container **loads** the class, calls **`init`**, then **`service`** (HTTP: **`doGet` / `doPost` / …**), then **`destroy`**. **`getServletConfig` / `getServletInfo`** are extra **`Servlet`** methods, not a second life cycle. It is **not** a `main` program and **not** CGI. Container: [[What is a servlet container]]. Duties: [[What typical responsibilities does a servlet container have]]. Three methods: [[What are the three core Servlet lifecycle methods and their roles]]. HTTP dispatch: [[What are the main HttpServlet request handling methods]]. Vs CGI: [[What are the advantages of servlets over CGI]].

## Web component, not a standalone process

Jakarta Servlet **6.1 §1.1**: like other Jakarta components, a servlet is compiled to **bytecode**, **loaded dynamically** into a **Jakarta-enabled web server**, and run **inside** a **container**. The container **owns the socket**, **MIME request/response**, and **lifecycle**. Clients talk HTTP (required) to the **server**; the **engine** picks a servlet and passes **`ServletRequest` / `ServletResponse`** (HTTP: **`HttpServletRequest` / `HttpServletResponse`**). Request path: [[How is an HttpServlet request processed]].

**`Servlet`** is the central API type. Implement it **directly**, or extend **`GenericServlet`** (protocol-neutral) or **`HttpServlet`** (usual). Developers **override `doXxx`**, not **`service`**, for HTTP.

Servlets sit **above CGI** and **below** frameworks such as **Jakarta Faces**. JSP/Faces still **run as servlets** under the hood.

```d2
direction: down
client: "HTTP client" {
  width: 140
  height: 36
}
box: "servlet container\n(engine in web/app server)" {
  width: 260
  height: 48
  style.fill: "#fff8e1"
}
s: "HttpServlet\ninit / service / destroy" {
  width: 220
  height: 48
  style.fill: "#e8f5e9"
}
client -> box: "request"
box -> s: "HttpServletRequest"
s -> box: "HttpServletResponse"
box -> client: "response"
```

**Fig. 1.** The **container** calls the servlet. The class does **not** listen on a port itself.

```java
// Conceptual — Jakarta Servlet 6.1
@WebServlet("/hello")
public class HelloServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        resp.setContentType("text/plain;charset=UTF-8");
        resp.getWriter().write("hello");
    }
}
```

**Listing 1.** A servlet is an **`HttpServlet`** the container **maps** and **invokes**. **`@WebServlet` is 3.0+**; XML `<servlet>` is the older form.

> [!warning] The container multithreaded `service`
> One instance (non-distributed) can run **`service` on many threads**. Instance fields are **shared**. Do not treat a servlet like a **per-request process**. Do not call **`init` / `service` / `destroy` yourself**.

> [!warning] `javax.servlet` vs `jakarta.servlet`
> Through **4.0** the package is **`javax.servlet`**. **Jakarta Servlet 5.0** renamed it to **`jakarta.servlet`**. A class with **`main`** or a raw **`ServerSocket`** is **not** a servlet even if it speaks HTTP. Implementing **`Servlet` by hand** still needs a **container** to call **`service`**.

> [!tip] Interview answer
> A servlet is a Java class the web container manages to produce dynamic responses. I implement Servlet, almost always by extending HttpServlet and overriding doGet or doPost. Init, service, and destroy are the lifecycle; getServletConfig and getServletInfo are extra Servlet methods. The container handles HTTP and drives those calls. It is a component inside an engine, not a standalone HTTP server.
