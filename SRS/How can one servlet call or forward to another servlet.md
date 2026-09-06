<!--
reps: 0
priority: 0
-->
#Java/Servlet #SRS

# How can one servlet call or forward to another servlet?

> [!abstract] Short answer
> Use a **`RequestDispatcher`**, not a direct `service` / `doGet` call and not a client redirect. **`forward`** hands the **same request/response** to another resource and that target **finishes the response**. **`include`** runs another resource **into the same response**, then the caller continues. Obtain the dispatcher by **context path**, **request-relative path**, or **servlet name**. Browser-visible URL change is **`sendRedirect`**, a different mechanism: [[How does sendRedirect differ from forward in servlets]]. API split: [[How would you explain the servlet RequestDispatcher for forward and include]].

## Obtain a dispatcher, then `forward` or `include`

The container’s **`RequestDispatcher`** wraps a servlet, JSP, or static resource. You get one from:

| Source | Path / key | Notes |
| --- | --- | --- |
| `ServletContext.getRequestDispatcher(path)` | Must be **context-relative**, start with **`/`**, or be empty | Mapped with the usual servlet path rules. If no servlet matches, you still get a dispatcher for **that path’s content**. May return **`null`**. |
| `ServletRequest.getRequestDispatcher(path)` | May be **relative to the current request** | `header.html` on `/garden/tools.html` behaves like context `"/garden/header.html"`. |
| `ServletContext.getNamedDispatcher(name)` | Deployment **servlet name** (`ServletConfig.getServletName()`) | **`null`** if that name is unknown. Does **not** set the `jakarta.servlet.forward.*` / `include.*` path attributes. |

You may append a **query string** to a path (`"/other?id=5"`). Those parameters **win** over same-named request parameters and last **only** for that `include` / `forward`.

Pass the **`request` and `response` the container gave `service`**, or wrappers that wrap those objects. Dispatch runs on the **same thread and JVM** as the original request ([[How can a servlet deadlock]], [[How is an HttpServlet request processed]]).

**`forward`** — caller must **not** have committed the response. Uncommitted buffer content is **cleared**, then the target’s `service` runs. Path elements on the request become the dispatcher path (except **named** dispatch, which keeps the original path). On a normal return the container **commits and closes** the response unless the request went async. If already committed: **`IllegalStateException`**.

**`include`** — legal **anytime**. The target may write to the existing `ServletOutputStream` / `PrintWriter` and may commit by overflowing the buffer or `flushBuffer`. It **must not** set response headers (attempts are ignored). `getSession` that would add a session cookie throws **`IllegalStateException`** if the response is already committed.

For another **web application**, `getRequestDispatcher` on **this** context is not enough: `ServletContext.getContext(uripath)` then `getRequestDispatcher` on that foreign context.

`sendRedirect` is **not** a servlet-to-servlet call. It sets redirect headers (relative URLs are allowed; the container may absolutize them), **commits and ends** the response, and the **client** issues a **new** request. After it, further output is ignored; if the response was already committed, **`IllegalStateException`**.

```d2
direction: down
src: "servlet A in service()" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
rd: "RequestDispatcher" {
  width: 240
  height: 40
  style.fill: "#fff8e1"
}
fwd: "forward\nsame request, target owns response" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
inc: "include\nwrite into response, A continues" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
redir: "sendRedirect\nHTTP to the client, new request" {
  width: 280
  height: 50
  style.fill: "#ffebee"
}
src -> rd
rd -> fwd
rd -> inc
src -> redir: "not a dispatcher"
```

**Fig. 1.** Server-side `forward` / `include` versus a client redirect.

```java
// Conceptual — jakarta.servlet.http, Servlet 6.1
protected void doGet(HttpServletRequest req, HttpServletResponse resp)
        throws ServletException, IOException {
    req.setAttribute("from", "A");
    if ("include".equals(req.getParameter("mode"))) {
        req.getRequestDispatcher("/b").include(req, resp);
        resp.getWriter().write("A after include");
        return;
    }
    getServletContext()
            .getRequestDispatcher("/b?via=forward")
            .forward(req, resp);
    // do not write the body after a successful forward
}

protected void doPost(HttpServletRequest req, HttpServletResponse resp)
        throws ServletException, IOException {
    RequestDispatcher named = getServletContext().getNamedDispatcher("servletB");
    if (named == null) {
        resp.sendError(HttpServletResponse.SC_NOT_FOUND);
        return;
    }
    named.forward(req, resp);
}
```

**Listing 1.** Path dispatch (`/`-relative or request-relative) versus **named** dispatch. `include` returns to the caller; `forward` should not be followed by more body writes.

> [!warning] `forward` after commit, or writing after `forward`
> Any flush / buffer overflow **commits**. `forward` then throws **`IllegalStateException`**. A successful `forward` **closes** the response on return (unless async). Later `getWriter().write(...)` is the wrong follow-up; use `include` if the caller must still write.

> [!warning] Context `getRequestDispatcher` is not a sandbox
> The path **must** start with `/` (or be empty). The lookup **bypasses** implicit `WEB-INF` / `META-INF` hiding and explicit security constraints. Do not build the path from unsanitized client data. `getNamedDispatcher` / `getRequestDispatcher` can return **`null`** — do not call `forward` on that.

> [!warning] `include` cannot fix headers, and named dispatch hides path attributes
> The included servlet cannot change status/headers. `jakarta.servlet.include.*` / `forward.*` are **not** set for **`getNamedDispatcher`**. Filters still run according to dispatcher type (`FORWARD` / `INCLUDE`).

> [!tip] Interview answer
> One servlet reaches another with RequestDispatcher: forward transfers the same request and the target completes the response; include runs the target into the current response and then the caller continues. Get the dispatcher from the context with a slash path, from the request with a possibly relative path, or by servlet name. sendRedirect is a client round-trip, not a server-side call, and you do not invoke another servlet’s service method yourself.
