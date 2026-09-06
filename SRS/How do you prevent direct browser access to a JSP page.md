<!--
reps: 0
priority: 0
-->
#Java/JSP #Java/Servlet #Security/AppSec #SRS

# How do you prevent direct browser access to a JSP page?

> [!abstract] Short answer
> **Put the page under `/WEB-INF/`** (for example `/WEB-INF/jsp/result.jsp`). The container **must not serve** `WEB-INF` to a client (`404`). Reach it only with a **server-side** `RequestDispatcher.forward` or `include` from a servlet (or another JSP). A **redirect** asks the **browser** for that URL and fails. Structure: [[What does a typical Java web application project structure look like]]. Dispatcher: [[How would you explain the servlet RequestDispatcher for forward and include]]. MVC hop: [[How does JSP servlet JSP interaction work]].

## `WEB-INF` is not the public tree

Jakarta Servlet **6.1** §10.5: the web app hierarchy has a **document root** (public files) and a special **`WEB-INF`** directory for everything that is **not** in that tree. **Most of `WEB-INF` is not public.** Except static resources and JSPs packaged under **`META-INF/resources`** of a JAR in **`WEB-INF/lib`**, **no other `WEB-INF` file may be served directly**. Client requests for `WEB-INF` (including odd casing such as `/WEb-iNf/foo`) must **not** return those files or a listing. Other client hits on `WEB-INF/` are **`SC_NOT_FOUND` (404)** — except that JAR-packaged static/`META-INF/resources` case.

Servlet code can still **see** those files via `ServletContext.getResource` / `getResourceAsStream`, and can **expose** them with **`RequestDispatcher`**. That is the intended view path: controller servlet, `setAttribute`, `forward("/WEB-INF/jsp/…")`. JSP: [[What is Java Server Pages JSP]]. `jsp-file` mapping: [[How is JSP configured in the web deployment descriptor]].

`getResource` on a `.jsp` returns the **JSP source**, and it **bypasses** both the implicit WEB-INF/META-INF rule and explicit `security-constraint`s. Do not stream that URL to the client. Use a dispatcher so the container **runs** the page.

A **`<servlet>` + `<jsp-file>/WEB-INF/…`** plus a **`<servlet-mapping>`** publishes the page at that **URL pattern**. The file is still under `WEB-INF`, but the **mapping** is a public address. Omit the mapping if the page must stay internal. `web.xml` `<security-constraint>` is **authorization** on a URL, not a substitute for moving views out of the document root.

```d2
direction: down
browser: "GET /WEB-INF/jsp/result.jsp" {
  width: 280
  height: 40
  style.fill: "#fff8e1"
}
nf: "container 404" {
  width: 200
  height: 36
}
ctrl: "servlet /app" {
  width: 200
  height: 36
  style.fill: "#e8f5e9"
}
jsp: "RequestDispatcher.forward\n/WEB-INF/jsp/result.jsp" {
  width: 300
  height: 48
  style.fill: "#e3f2fd"
}
browser -> nf
ctrl -> jsp: "same request"
```

**Fig. 1.** Direct URL to `WEB-INF` is **404**. A **forward** is not a client request for that path.

```
/index.html
/WEB-INF/web.xml
/WEB-INF/classes/…/ReportServlet.class
/WEB-INF/jsp/result.jsp
```

**Listing 1.** Conceptual WAR tree. `result.jsp` is not in the document root.

```java
// Conceptual — Servlet 6.1 RequestDispatcher; JSP under WEB-INF
request.setAttribute("report", report);
request.getRequestDispatcher("/WEB-INF/jsp/result.jsp")
    .forward(request, response);
```

**Listing 2.** Server-side hand-off. `response.sendRedirect("/WEB-INF/jsp/result.jsp")` would make the **browser** request that path and get **404**.

> [!warning] `META-INF/resources` in `WEB-INF/lib` JARs is public
> JSPs and static files there **may be served directly**. Case tricks (`/WEb-iNf/`) must still **not** leak `WEB-INF`. A `jsp-file` **servlet-mapping** re-exposes a hidden page at a public URL.

> [!warning] `getResource` is source, not a rendered page
> It skips implicit and explicit URL constraints. Never write that stream to the client as “the JSP”. `include`/`forward` execute it. Do not use a client redirect into `WEB-INF`.

> [!tip] Interview answer
> I keep view JSPs under WEB-INF so the container returns 404 for a direct browser URL. The servlet forwards or includes that path on the same request. A redirect cannot reach WEB-INF, and mapping the page with jsp-file would publish it again.
