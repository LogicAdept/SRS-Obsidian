<!--
reps: 0
priority: 0
-->
#Java/JSP #Java/Servlet #SRS

# How does JSP servlet JSP interaction work?

> [!abstract] Short answer
> A JSP **is a servlet** (`JspPage` / `_jspService`). Interaction is **the same request**: a **controller servlet** reads parameters, puts **request attributes**, then **`RequestDispatcher.forward`** to a **view JSP**. The JSP reads those attributes with **EL** (`${…}`) or **`<jsp:useBean>`** in **request** scope. The other direction is a **form `action`** (new HTTP hit) or **`<jsp:forward>`** / `pageContext.forward` to a servlet. **`include`** stitches output into the current response; **`sendRedirect`** is a **new** request and **drops** those attributes. Dispatcher: [[How can one servlet call or forward to another servlet]]. Beans from the request: [[How do you populate a JavaBean or object attributes from a request]]. Redirect vs forward: [[How does sendRedirect differ from forward in servlets]]. Page lifecycle: [[How would you explain the JSP page lifecycle]]. EL scopes: [[What are the implicit EL scope objects in JSP and how do they differ from servlet scoped objects]].

## Same request, two roles

**View JSP → HTTP → servlet.** A page renders a form whose `action` is the servlet’s URL. That is a **new** client request (parameters in the query or body). The servlet is the **controller**.

**Servlet → forward → JSP.** After work, `request.setAttribute("name", value)` (one value per name). `getRequestDispatcher("/WEB-INF/views/result.jsp").forward(request, response)` runs the JSP as the **view on this same request**. `forward` **clears an uncommitted buffer**, then the target **finishes and commits** the response. Path elements on the target reflect the dispatcher path (unless you used `getNamedDispatcher`). A JSP under **`WEB-INF`** is not a public URL; the dispatcher can still reach it.

**Why two JSPs.** The inbound page is the **form**; the outbound page is the **result**. They can be the same file if you forward back to it, but the **servlet still sits in the middle**. `<jsp:forward>` from a JSP to a servlet is the **server-side** equivalent of “go run the controller.”

**JSP → JSP or JSP → servlet (server-side).** `<jsp:forward page="…"/>` (or `PageContext.forward`) **stops** the current page and dispatches in-context to a static file, JSP, or servlet. `<jsp:include>` runs another resource **into** this response (included page **cannot** set status/headers). `<jsp:param>` **augments** request parameters for the duration of that include/forward (new values **precede** old ones).

The JSP implementation class still goes through servlet `init` / `service` / `destroy`; authors hook **`jspInit` / `jspDestroy`**, never `_jspService`.

```d2
direction: down
form: "form JSP\nHTML + action=servlet" {
  width: 220
  height: 48
  style.fill: "#fff8e1"
}
ctl: "HttpServlet\nparameters + setAttribute" {
  width: 240
  height: 48
  style.fill: "#e3f2fd"
}
view: "view JSP\nEL / useBean request scope" {
  width: 240
  height: 48
  style.fill: "#e8f5e9"
}
redir: "sendRedirect\nnew request, attributes gone" {
  width: 260
  height: 48
  style.fill: "#ffebee"
}
form -> ctl
ctl -> view
ctl -> redir
```

**Fig. 1.** Attribute hand-off needs **forward/include**, not a client redirect.

```java
// Conceptual — jakarta.servlet.http, Servlet 6.1
@Override
protected void doPost(HttpServletRequest req, HttpServletResponse resp)
        throws ServletException, IOException {
    String name = req.getParameter("name");
    req.setAttribute("greeting", "Hello, " + name);
    req.getRequestDispatcher("/WEB-INF/views/hello.jsp").forward(req, resp);
}
```

**Listing 1.** Controller does not write the page. Forward before the response is committed.

```jsp
<%-- Conceptual — request attribute from the servlet --%>
<p>${greeting}</p>
<jsp:useBean id="customer" class="com.example.Customer" scope="request"/>
```

**Listing 2.** EL sees request attributes. `jsp:useBean` / `jsp:getProperty` still need the bean **introduced** on this page even if the servlet stored it.

> [!warning] Committed output blocks `forward`
> If the buffer **flushed** or the page is **unbuffered** and has **written**, `forward` / `<jsp:forward>` throws **`IllegalStateException`**. After a successful `PageContext.forward`, do not touch the response; return from `_jspService`. Do not `new` the other servlet and call `service`.

> [!warning] Redirect is not this pattern
> `sendRedirect` tells the **browser** to request another URL. Request attributes from the servlet are **gone**. Session or query string survive; that is a different contract. `jsp:include` is for **fragments**, not for handing off the whole view.

> [!warning] MVC is the nickname, not an interface
> The Servlet and Pages specs do **not** define Model/View/Controller types. They define **`RequestDispatcher`**, **request attributes**, and JSP actions. Faces (and Spring MVC) are **other** controller stacks on the same container.

> [!tip] Interview answer
> The usual JSP-servlet-JSP flow is a form posting to a servlet, which sets request attributes and forwards to a JSP that renders them. Interview shorthand calls that MVC — JSPs are views, the servlet is the controller — but the API is still forward plus request attributes. Forward keeps the same request; sendRedirect does not. A JSP is itself a servlet, so the dispatcher, not a direct method call, is how they share that request.
