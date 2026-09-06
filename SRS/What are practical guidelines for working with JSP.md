<!--
reps: 0
priority: 0
-->
#Java/JSP #Java/Servlet #SRS

# What are practical guidelines for working with JSP?

> [!abstract] Short answer
> **Treat the page as presentation: template + standard/custom actions + EL; keep Java off the page.** Spec **page authors** are expected **not** to use scripting. Enforce that with **`scripting-invalid`**. Put work in a **servlet** (or bean), **`setAttribute`**, **`forward`** to a JSP under **`/WEB-INF/`**. Use **JSTL** for loops/conditionals/output. Do **not** write to `response.getWriter()` — only **`out`**. Scriptlets: [[Why should JSP scriptlets be avoided in modern applications]]. MVC hop: [[How does JSP servlet JSP interaction work]]. Errors: [[How do you handle errors on JSP pages]].

## Page author vs developer

Jakarta Pages **4.0** splits **roles**. **Authors** compose HTML/XML presentations; they **need not know Java**. **Developers** write components that talk to server-side objects. Authors should stay on **standard actions, custom actions (JSTL, tag files), and EL**. **Advanced** authors who know Java are still told to **avoid scripting where possible**. EL exists so pages can be **scriptless**; **`scripting-invalid`** makes `<%` / `<%!` / `<%=` a **translation error**. JSTL: [[How would you explain JSTL the JSP Standard Tag Library]]. Hide views: [[How do you prevent direct browser access to a JSP page]].

**Do this in practice**

- **One job per file.** Controller servlet (or equivalent) does I/O and rules; the JSP **renders**. Forward on the **same request**; do not `sendRedirect` into `WEB-INF`.
- **Declare libraries once, before first use.** `taglib` at the top, or **`include-prelude`** for the taglibs every page shares. A `taglib` **after** an action that uses that prefix is a **fatal translation error**.
- **EL for data**, **`c:out`** (default XML escaping) for text that came from users. Qualify scopes (`requestScope`, `pageContext.request`) so names do not `findAttribute` the wrong bag.
- **`session="false"`** when the view does not participate in a session (`session` defaults to **`true`** and will create/join one).
- **Know the two includes.** `<%@ include %>` pastes **source** into this translation unit (even another JSP — it is **not** “static files only”). `<jsp:include>` **invokes** the resource at **request** time.
- **JSP comments for authors.** `<%-- … --%>` is dropped at translation. `<!-- … -->` is template and **reaches the client**; EL and actions **inside** it still run: [[How do you comment code in JSP]].
- **Fail loud.** `error-on-undeclared-namespace` so a mistyped prefix is not silent template text. Wire **`errorPage` / `isErrorPage`**.
- **Lifecycle is a servlet’s.** Optional **`jspInit` / `jspDestroy`** in declarations; never **`_jspService`**. Lifecycle: [[How would you explain the JSP page lifecycle]]. Config: [[How is JSP configured in the web deployment descriptor]].

**Do not**

- Scriptlets for business rules, JDBC, or flow the tags already cover.
- Call **`response.getWriter()`** or **`getOutputStream()`** from the page — the spec **prohibits** that; **`out`** is the `JspWriter`.
- Use **`page extends`** unless you can honour the `HttpJspPage` contract; it blocks container superclasses.
- Treat **`<%= %>`** as a substitute for **`c:out`**.
- Use **`isThreadSafe`** — it rides deprecated **`SingleThreadModel`**.
- Treat CSS/JS file layout as a JSP rule. It is not.

```d2
direction: down
dev: "developer\nservlet, beans, tags" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
auth: "page author\ntemplate + actions + EL" {
  width: 260
  height: 40
  style.fill: "#fff8e1"
}
page: "JSP under WEB-INF" {
  width: 220
  height: 36
  style.fill: "#e8f5e9"
}
dev -> page: "forward + attributes"
auth -> page: "no scriptlets"
```

**Fig. 1.** Practical split: **Java on the server side of the forward**, **markup on the JSP**.

```jsp
<%-- Conceptual — Jakarta Pages 4.0, scriptless view --%>
<%@ page session="false" contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<p><c:out value="${requestScope.user.name}"/></p>
```

**Listing 1.** A view with **no** session, **no** scriptlets, **escaped** output.

```xml
<!-- Conceptual — enforce the guideline in web.xml -->
<jsp-property-group>
  <url-pattern>/WEB-INF/jsp/*</url-pattern>
  <scripting-invalid>true</scripting-invalid>
  <error-on-undeclared-namespace>true</error-on-undeclared-namespace>
</jsp-property-group>
```

**Listing 2.** Descriptor: a stray `<%` or unknown tag prefix is a **translation error**.

> [!warning] `out` is not `response.getWriter()`
> Writing the servlet streams **breaks** JSP buffering and is **forbidden** for page authors. A scriptlet that “works” on one container can still flush the buffer and kill `errorPage` forwarding.

> [!warning] Guidelines are not optional style
> Without **`scripting-invalid`**, scriptlets compile. **`session` defaults to `true`**. An unknown `c:out` without a **`taglib`** is not JSTL. A JSP in the document root is a **public URL**. HTML comments **do not** comment out JSP.

> [!warning] `include` directive is not “static files only”
> It pastes **text** into this page (even another JSP). `jsp:include` runs that resource **now**. Mixing them without knowing which translation unit you are in is the usual bug.

> [!tip] Interview answer
> I keep JSPs as views: actions and EL, no Java in the page, scripting-invalid in the descriptor. The servlet does the work and forwards to a page under WEB-INF. I use the include directive when I want source baked in at translation, and jsp include when I want another resource executed on the request. I set session false when I do not need a session, and I never write to getWriter from the page.
