<!--
reps: 0
priority: 0
-->
#Java/JSP/ImplicitObjects #Java/Servlet #SRS

# What is PageContext and what are its benefits?

> [!abstract] Short answer
> **`jakarta.servlet.jsp.PageContext` is the servlet-aware context for one JSP request.** It stores **page-scoped** objects, unifies the **four scopes**, exposes implicits (`request`, `out`, session, …), and adds **`forward` / `include` / `handlePageException`**. Benefit: the generated servlet (and your tags) call a **portable API** while the container supplies an implementation-specific `JspWriter` and can **reuse** the instance. Scopes: [[What variable scopes exist in JSP]]. `out`: [[What is the difference between JspWriter and servlet PrintWriter]].

## One object instead of four bags plus the servlet APIs

Jakarta Pages **4.0** §1.8.4: a `PageContext` **holds references** used by the page, **hides implementation**, and offers **convenience methods**. `_jspService` obtains it from **`JspFactory.getPageContext`** and **`releasePageContext`s** it when the request ends — the container **may recycle** the instance. It is itself a **page-scoped** implicit (`pageContext` in scriptlets; EL **`${pageContext}`**). What JSP is: [[What is Java Server Pages JSP]]. Lifecycle: [[How would you explain the JSP page lifecycle]].

**`JspContext` vs `PageContext`.** `PageContext` **extends** `JspContext`. The base is **not** servlet-specific (`SimpleTag` only needs `JspContext`): **`setAttribute` / `getAttribute` / `findAttribute` / `removeAttribute`**, `getOut()`, `getELContext()`, `pushBody` / `popBody`. `PageContext` adds the **servlet environment**: `getRequest()`, `getResponse()`, `getSession()`, `getServletConfig()`, `getServletContext()`, `getPage()`, `getException()`, **`getErrorData()`**, **`forward`**, **`include`**, **`handlePageException`**. Classic `Tag` handlers receive a `PageContext`; SimpleTag receives a `JspContext`.

**Benefits the API actually lists**

- **One API for four namespaces** — `PAGE_SCOPE` (default, this `PageContext` until `_jspService` returns), `REQUEST_SCOPE`, `SESSION_SCOPE`, `APPLICATION_SCOPE`. `findAttribute(name)` walks **page → request → session (if valid) → application**.
- **Convenience getters** for every scripting implicit, so tags do not thread `ServletRequest` by hand.
- **`getOut()`** — the interposed **`JspWriter`** (possibly a faster container subclass).
- **Session policy** from the `page` directive (`needsSession` at `initialize`).
- **Forward / include** of the current request (paths starting `/` are context-root; others are relative to this JSP). `include(path)` **flushes `out` first**; `include(path, false)` does not.
- **Error-page wiring** — `handlePageException(Throwable)` forwards to this page’s error page, or rethrows into servlet error handling. **`getErrorData()`** is meaningful only when **`isErrorPage="true"`**.

**Not for page authors:** `initialize` / `release` (container / `JspFactory` only). Nested `BodyContent` uses `pushBody()`.

EL implicits wrap the same scopes: [[What are the implicit EL scope objects in JSP and how do they differ from servlet scoped objects]]. Request method via this object: [[How do you read the HTTP method with JSP EL]]. Context vs config: [[What is the difference between ServletContext and ServletConfig]].

```d2
direction: down
pc: "PageContext\n(JspContext + servlet APIs)" {
  width: 280
  height: 48
  style.fill: "#fff8e1"
}
scopes: "page / request / session / application\nfindAttribute" {
  width: 300
  height: 48
  style.fill: "#e3f2fd"
}
io: "getOut · getRequest · forward/include\nhandlePageException" {
  width: 300
  height: 48
  style.fill: "#e8f5e9"
}
pc -> scopes
pc -> io
```

**Fig. 1.** `PageContext` is the **hub**: scopes plus servlet I/O, so the page implementation stays portable.

```jsp
<%-- Conceptual — EL on the implicit pageContext --%>
<p>${pageContext.request.contextPath}</p>
<p>${pageContext.errorData.statusCode}</p>
```

**Listing 1.** Bean path through `PageContext`. `errorData` is only meaningful on an error page.

```java
// Conceptual — same object in a tag or scriptlet
Object user = pageContext.findAttribute("user");
pageContext.setAttribute("label", "ok", PageContext.REQUEST_SCOPE);
pageContext.include("/WEB-INF/jsp/footer.jsp", false);
```

**Listing 2.** `findAttribute` searches all four scopes; `getAttribute("user")` is **page scope only**. `include(..., false)` does not flush `out`.

> [!warning] After `forward`, do not write; `initialize` is not yours
> Successful **`forward`** makes further **`ServletResponse`** changes **undefined** — return from `_jspService`. Do not call **`initialize` / `release`**. **`SESSION_SCOPE`** throws **`IllegalStateException`** if the page is `session="false"` (or the session is dead). **`getException()`** is typed **`Exception`**, not `Throwable`. **`getErrorData()`** on a normal page is **meaningless**.

> [!tip] Interview answer
> PageContext is the per-request JSP context: page scope lives on it, and it unifies request, session, and application attributes behind one API. It also hands me the implicits, the JspWriter, and forward, include, and error-page handling. The container creates it through JspFactory so the generated servlet stays portable and can use a faster JspWriter. I look up a name with findAttribute when I mean any scope, and I do not call initialize or write to the response after forward.
