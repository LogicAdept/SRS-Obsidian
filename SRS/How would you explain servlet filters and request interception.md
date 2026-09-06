<!--
reps: 0
priority: 0
-->
#Java/Servlet/Filters #SRS

# How would you explain servlet filters and request interception?

> [!abstract] Short answer
> A **filter** is a container-managed interceptor for a **servlet or static resource**: it can **read** the request, **wrap** request/response, **call the next hop**, or **stop** and write the response itself. It **does not usually create** the response the way a servlet does. You implement **`jakarta.servlet.Filter`** (or subclass **`HttpFilter`**). The container builds a **`FilterChain`** and calls **`doFilter`**. Skipping **`chain.doFilter`** means the servlet **never runs**. Mapping then chain: [[How is an HttpServlet request processed]]. Wrappers: [[What servlet wrapper classes exist]]. Filters vs listeners vs MVC interceptors: [[How do servlet filters Spring MVC interceptors and web listeners differ]]. Vs `forward`/`include`: [[How would you explain the servlet RequestDispatcher for forward and include]].

## `doFilter`, chain, wrap, or stop

Implement **`Filter`** with a **public no-arg constructor**. The container **`init(FilterConfig)`**s **exactly once** per **`<filter>`** declaration (per JVM) **before** any `doFilter`. `init` **happens-before** later `doFilter` calls. **`destroy`** runs before the instance is taken out of service. **`init`/`destroy` are default no-ops** since Servlet 4.0; **`HttpFilter`** (also 4.0) is the HTTP convenience base: override **`doFilter(HttpServletRequest, HttpServletResponse, FilterChain)`**. Two declarations of the **same class** → **two instances**.

On each matching request the container calls the first filter with the request, response, and a **`FilterChain`**. A typical `doFilter`:

1. Inspect the request.
2. Optionally wrap with **`HttpServletRequestWrapper`** / **`HttpServletResponseWrapper`** (decorator; methods default to the wrapped object).
3. Either **`chain.doFilter(requestOrWrapper, responseOrWrapper)`** — next filter, or the **resource** if this is last — **or omit that call** and **complete the response yourself**.
4. After the nested call returns, inspect or finish the response (headers after the chain only if it is **not already committed**).

The container **must** pass **the same objects** you passed into `chain.doFilter` to the next entity. **`Servlet.service` and every filter on that chain share one thread.** `doFilter` is **concurrent** across requests: one instance, many threads — protect instance fields yourself.

Typical uses named in the API: **authentication, logging, compression, encryption**, image conversion, XSLT, caching.

**Register.** `@WebFilter` (Servlet 3.0) on a `Filter` class, **`web.xml` `<filter>` + `<filter-mapping>`**, or **`ServletContext.addFilter`** during application init. `@WebFilter` **must** name **`urlPatterns`**, **`servletNames`**, or **`value`** (not **`value` and `urlPatterns` together**). Default filter name is the **FQCN**. **`dispatcherTypes` defaults to `REQUEST` only.** Context from **`FilterConfig.getServletContext()`**: [[How would you explain ServletContext in Java web applications]].

**Chain order (deployment descriptor).** After the container maps the **target resource**: matching **`<url-pattern>`** mappings **first**, in **declaration order**, then matching **`<servlet-name>`** mappings, then the resource. A mapping with both expands into one mapping per pattern/name, keeping that inner order. **`@WebFilter` invocation order is unspecified** — put the chain in **`web.xml` / `web-fragment.xml`** if order matters.

**Dispatchers.** No `<dispatcher>` (or only `REQUEST`) → **client requests**, **not** `RequestDispatcher.forward` / `include`, error pages, or async `dispatch`. Name **`FORWARD`**, **`INCLUDE`**, **`ERROR`**, **`ASYNC`** when those hops must be filtered. Named-dispatcher `*` + `FORWARD` applies to **all** forwards. Dispatch API: [[How would you explain the servlet RequestDispatcher for forward and include]].

```d2
direction: down
client: "client request" {
  width: 180
  height: 36
  style.fill: "#fff8e1"
}
urlf: "url-pattern filters\n(declaration order)" {
  width: 260
  height: 48
  style.fill: "#e3f2fd"
}
namef: "servlet-name filters\n(declaration order)" {
  width: 260
  height: 48
  style.fill: "#e3f2fd"
}
res: "servlet or static resource" {
  width: 240
  height: 40
  style.fill: "#e8f5e9"
}
client -> urlf
urlf -> namef
namef -> res
res -> namef: "return"
namef -> urlf: "return"
```

**Fig. 1.** Inbound: URL-pattern filters, then servlet-name filters, then the resource. After `chain.doFilter` returns, the same stack unwinds. A filter that never calls the chain never reaches the resource.

```java
// Conceptual — jakarta.servlet.http, Servlet 6.1
@WebFilter(urlPatterns = "/secure/*")
public class AuthFilter extends HttpFilter {
    @Override
    protected void doFilter(HttpServletRequest req, HttpServletResponse res, FilterChain chain)
            throws IOException, ServletException {
        if (req.getUserPrincipal() == null) {
            res.sendError(HttpServletResponse.SC_UNAUTHORIZED);
            return; // no chain.doFilter → target never runs
        }
        chain.doFilter(new HttpServletRequestWrapper(req), res);
    }
}
```

**Listing 1.** Interception is **`doFilter` + `FilterChain`**. Wrap **before** `chain.doFilter` if the rest of the chain must see the wrapper. Default `@WebFilter` dispatcher is **`REQUEST`**.

> [!warning] Default mapping is not `forward`
> `@WebFilter("/products/*")` or a `<filter-mapping>` with **no** `<dispatcher>` runs on **direct client** hits only. A servlet **`forward`** to `/products/…` **skips** that filter unless you add **`DispatcherType.FORWARD`** (or `<dispatcher>FORWARD</dispatcher>`). Spec “before the resource is invoked” means **`service` / static file**, **not** **`Servlet.init`**. Filter **`init` already ran** at deploy (or first use).

> [!warning] Skip the chain, own the response
> If you return without **`chain.doFilter`**, later filters and the servlet **do not run**. You must write status and body. Response **body** wrapping must be in place **before** the nested call; after `service` the buffer may already be **committed**.

> [!tip] Interview answer
> A servlet filter sits on the container chain around a servlet or static file: init once, then doFilter on each matching request. I can wrap the request or response, call chain.doFilter to continue, or skip it and write the response myself. URL-pattern mappings run before servlet-name mappings; by default the filter is REQUEST-only, so forwards and includes do not hit it unless I say so.
