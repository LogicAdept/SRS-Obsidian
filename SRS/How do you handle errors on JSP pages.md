<!--
reps: 0
priority: 0
-->
#Java/JSP #Java/Servlet #SRS

# How do you handle errors on JSP pages?

> [!abstract] Short answer
> **Uncaught throwables go to the page’s `errorPage`, or to servlet `error-page` mappings if the page did not set one.** Mark the target with `isErrorPage="true"` so the `exception` implicit object (`Throwable`) is defined. You can still `try`/`catch` in the page. Translation failures are HTTP 500.

## Page directive, then the deployment descriptor

At **request** time, a runtime failure in the page (or in code it calls) is a Java exception. You may catch it in a scriptlet. Anything still uncaught is **forwarded** to the URL in `<%@ page errorPage="…" %>`. The throwable is stored on the request as `jakarta.servlet.error.exception` (and the older `jakarta.servlet.jsp.jspException`). If the page has **no** `errorPage`, the container’s default applies — including **`web.xml` `<error-page>`** for an `exception-type` or HTTP `error-code` ([[How is JSP configured in the web deployment descriptor]], [[What is Java Server Pages JSP]]).

If the page **does** set `errorPage`, **`web.xml` error pages are not used** for that page’s uncaught throwables.

A JSP is an error page only when `isErrorPage="true"`. Then the scripting variable `exception` is the originating `Throwable`. If `isErrorPage` is `false` (the default), naming `exception` is a **translation error**. `web.xml` dispatch to a JSP does **not** by itself define that variable — the target still needs `isErrorPage="true"`. EL can use `${pageContext.exception}` and `${pageContext.errorData.statusCode}` ([[Which implicit JSP objects are unavailable on a plain JSP page]], [[How would you explain the JSP page lifecycle]]).

By default the error page sets the response status from `errorData.statusCode` (typically 500). A page must not set `errorPage` to **itself** (translation error). If `autoFlush` is true and the buffer has already been flushed, forwarding to `errorPage` may fail.

Translation-time failures (the page will not compile) are not `errorPage`; for HTTP they surface as status **500**.

```d2
direction: down
page: "JSP (uncaught Throwable)" {
  width: 280
  height: 50
}
ep: "page errorPage URL\n(isErrorPage target)" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
dd: "web.xml error-page\n(only if no errorPage)" {
  width: 300
  height: 70
  style.fill: "#fff8e1"
}
page -> ep
page -> dd
```

**Fig. 1.** Page-level `errorPage` wins over deployment-descriptor error pages for that JSP.

```jsp
<%-- work.jsp --%>
<%@ page errorPage="error.jsp" %>
<%
    int n = 1 / 0;
%>

<%-- error.jsp --%>
<%@ page isErrorPage="true" %>
<p>${pageContext.errorData.statusCode}</p>
<p><%= exception.getMessage() %></p>
```

**Listing 1.** Uncaught `ArithmeticException` is forwarded to `error.jsp`. Without `isErrorPage="true"`, `exception` does not compile.

```xml
<error-page>
  <exception-type>java.lang.Throwable</exception-type>
  <location>/error.jsp</location>
</error-page>
<error-page>
  <error-code>404</error-code>
  <location>/notfound.jsp</location>
</error-page>
```

**Listing 2.** Servlet `error-page` for exceptions and status codes. The JSP at `/error.jsp` still needs `isErrorPage="true"` to use `exception`. Unused when `work.jsp` already declared `errorPage`.

> [!warning] `errorPage` on the JSP turns off `web.xml` error pages for that page
> Uncaught throwables go only to the page directive URL. Status-code pages in the descriptor still apply to `sendError` / 404-style cases, not as a second handler for that JSP’s throw.

> [!warning] `exception` exists only on `isErrorPage="true"`
> A descriptor location is not enough. Referencing `exception` on a normal page is a fatal translation error. After a flush, the forward to `errorPage` may not run.

> [!tip] Interview answer
> **Put `errorPage` on the page and `isErrorPage="true"` on the handler so `exception` is the uncaught `Throwable`.** If you omit `errorPage`, `web.xml` `<error-page>` can map types and status codes. A page that sets `errorPage` does not use those descriptor mappings for its uncaught exceptions.
