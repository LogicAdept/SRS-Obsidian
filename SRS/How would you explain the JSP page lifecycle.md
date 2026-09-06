<!--
reps: 0
priority: 0
-->
#Java/JSP #Java/Servlet/Lifecycle #SRS

# How would you explain the JSP page lifecycle?

> [!abstract] Short answer
> **Two phases: translation once, then the servlet lifecycle per instance.** The container turns the JSP into a **page implementation class** (`HttpJspPage` / `JspPage`). **`init`** stores `ServletConfig` and calls **`jspInit`** (before the first request). Each hit is **`service` → `_jspService`**. **`destroy`** calls **`jspDestroy`** when no request is in flight. You may declare **`jspInit` / `jspDestroy`**; you **must not** declare **`_jspService`** or other servlet methods. What JSP is: [[What is Java Server Pages JSP]]. Override points: [[Which JSP lifecycle methods can be overridden]]. Servlet `init`: [[Why override the no argument init method in a servlet]].

## Translate, then `init` / service / `destroy`

Jakarta Pages **4.0**: a JSP container runs **translation** then **execution**. Translation **validates** the page (and tag files), applies directives/actions/taglibs, and produces an implementation class whose **name and package are implementation-dependent**. That can happen at **deploy**, **ahead of time**, or **on the first request**. Execution manages **one or more instances** of that class. After translation, requests follow **Servlet 6.1** rules. What a JSP is: [[What is Java Server Pages JSP]]. Precompile via `jsp-file` / `load-on-startup`: [[How is JSP configured in the web deployment descriptor]].

**HTTP contract (`HttpJspPage`).** Table JSP.11-1:

| Container calls | Author |
| --- | --- |
| `jspInit()` | Optional, in a **declaration**. `getServletConfig` and the rest of `Servlet` are already usable. |
| `_jspService(request, response)` | **Generated.** Invoked **per request**. **Must not** be defined in the page. |
| `jspDestroy()` | Optional declaration. Invoked **before destroy**, when the page is **not** servicing a request. |

Typical generated superclass: **`init(ServletConfig)`** saves config, then **`jspInit()`**; **`service`** casts to HTTP and calls **`_jspService`**; **`destroy`** calls **`jspDestroy()`**. Those three servlet methods are **`final`** on the example superclass so a declaration cannot replace them. A JSP author **may not (re)define servlet methods** in `<%! … %>`. Names `_jsp*` / `_jspx*` (any case) are **reserved**. Declarations: [[Can you declare a class inside a JSP page]].

`<%@ page extends="…" %>` makes **you** responsible for that contract (`service` → `_jspService`, `init` → `jspInit`, `destroy` → `jspDestroy`, `HttpJspPage`, servlet methods **final**). Most containers will **not** check. Avoid it.

```d2
direction: down
src: "*.jsp text" {
  width: 160
  height: 36
  style.fill: "#fff8e1"
}
tr: "translation\nimplementation class" {
  width: 240
  height: 48
  style.fill: "#e8f5e9"
}
ini: "init → jspInit" {
  width: 200
  height: 36
}
svc: "service → _jspService\n(per request)" {
  width: 240
  height: 48
  style.fill: "#e3f2fd"
}
des: "jspDestroy → destroy" {
  width: 220
  height: 36
}
src -> tr
tr -> ini
ini -> svc
svc -> des
```

**Fig. 1.** Lifecycle is **compile to a servlet**, then the usual **init / service / destroy** hooks with JSP names.

```jsp
<%-- Conceptual — Jakarta Pages 4.0 declarations --%>
<%!
  public void jspInit() {
    getServletContext().log("page ready");
  }
  public void jspDestroy() {
    getServletContext().log("page gone");
  }
%>
<p>${pageContext.request.method}</p>
```

**Listing 1.** Optional **`jspInit` / `jspDestroy`**. The body still becomes **`_jspService`**. Do not declare `_jspService` here.

> [!warning] Do not declare `_jspService` or `init` / `service` / `destroy`
> The container **generates** `_jspService`. Redeclaring servlet methods in a declaration is **illegal**. `jspInit` is **not** a constructor: it runs from **`init`**, with **`ServletConfig` already set**. Instance fields you also declare are **shared** across concurrent `_jspService` calls on that instance.

> [!warning] First request can be translation
> On-demand compile makes the **first** client pay **translate + compile**; a broken page is **HTTP 500**, not `jspInit`. `extends` freezes the superclass and blocks container optimizations. The implementation class name is **not** a stable API.

> [!tip] Interview answer
> I split JSP into translation and request. Translation produces a servlet. Then init calls jspInit, each request is _jspService, and destroy calls jspDestroy. I may write jspInit and jspDestroy in a declaration; I never write _jspService.
