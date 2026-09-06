<!--
reps: 0
priority: 0
-->
#Java/JSP #Java/Servlet #SRS

# How would you explain principles work with JSP?

> [!abstract] Short answer
> Treat a JSP as the **presentation** layer: **template + actions + EL**, compiled to a **servlet**. Spec page authors are expected to **avoid scripting** (`<% %>`); use **standard/custom actions** and **EL**, or **`scripting-invalid`**. Put **work in a servlet**, **`setAttribute`**, **`forward`** to the page. **`session` defaults to `true`** (that page **joins/creates** a session) — set **`session="false"`** when the view does not need one. **`<%@ include %>`** is **translation-time** text; **`<jsp:include>`** is **request-time** dispatch. Lifecycle: [[How would you explain the JSP page lifecycle]]. View/controller: [[How would you explain JSP - servlet - JSP]]. Errors: [[How do you handle errors on JSP pages]]. Groups: [[How is JSP configured in the web deployment descriptor]]. Tags: [[How would you explain JSTL the JSP Standard Tag Library]].

## Translation unit, not a CGI script

A JSP **describes a response**. The container **translates** it once into a servlet class, then runs that instance **per request**. Directives (`page`, `taglib`, `include`) are **translation** facts. Scriptlets glue Java into the page; the spec’s **page-author** role is **actions and EL**, not Java.

**Keep Java out of the page.** If EL and existing tags are not enough, write a **tag** or move the work to a **servlet** and pass **request attributes**. `jsp-property-group` **`scripting-invalid`** makes leftover scriptlets a **translation error**.

**`taglib` before use.** A `taglib` directive **after** an action that uses that prefix is a **fatal translation error**. That is why `page` / `taglib` belong at the **top** of the file (and why prelude includes exist), not merely “for readability.”

**Session.** `<%@ page session="false" %>`: the page **does not participate**; the `session` implicit object is **illegal**. Default **`true`** means the page **will** attach to a current or **new** `HttpSession`. That is a **lifecycle** choice, not a CSS tip.

**Two includes.** `<%@ include file="…" %>` inserts **source** (static object: the **text** is parsed into this translation unit). `<jsp:include page="…"/>` **invokes** the resource at **request** time (dynamic object: its **output** is included). A JSP can be included either way; the dump’s “directive = static files only” is **wrong**.

**Comments.** `<%-- … --%>` is **dropped** at translation (does not nest). `<!-- … -->` is **template** and **reaches the client**; EL/actions **inside** it still run.

**Errors.** Uncaught throwables go to **`errorPage`**, or to **`web.xml` `<error-page>`** if the page did not set one. That is the specified path — not “faster than try/catch.”

CSS/JS file layout is **not** a JSP rule. `isThreadSafe` rides deprecated `SingleThreadModel` — do not use it.

```d2
direction: down
src: "JSP: template + actions + EL" {
  width: 260
  height: 40
  style.fill: "#fff8e1"
}
tr: "translate once → servlet class" {
  width: 260
  height: 40
  style.fill: "#e3f2fd"
}
run: "per request: _jspService" {
  width: 260
  height: 40
  style.fill: "#e8f5e9"
}
src -> tr
tr -> run
```

**Fig. 1.** Principles follow the two phases: get translation right, keep request-time code in tags or a servlet.

```jsp
<%@ page session="false" errorPage="/oops.jsp" %>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<%-- translation-time comment; not sent --%>
<jsp:include page="/WEB-INF/fragments/nav.jsp"/>
```

**Listing 1.** No session, taglib **before** tags, JSP comment, **request-time** include. Shared header **source** would be `<%@ include file="…" %>`.

> [!warning] Scriptlets are legal unless you turn them off
> The language still has `<% %>`. “Don’t use them” is the **page-author** model plus **`scripting-invalid`**, not a hidden ban. HTML comments **do not** comment out JSP.

> [!warning] `include` directive is not “static files only”
> It pastes **text** into this page (even another JSP). `jsp:include` runs that resource **now**. Mixing them without knowing which translation unit you are in is the usual bug.

> [!tip] Interview answer
> I treat JSP as the view: EL and tags, no business logic, scriptlets off if I can. Session is on by default so a pure view sets session false. I use the include directive when I want source baked in at translation, and jsp include when I want another resource executed on the request. Errors go to an error page, not a pile of scriptlet catch blocks.
