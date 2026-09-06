<!--
reps: 0
priority: 0
-->
#Java/JSP #Java/Servlet/Lifecycle #SRS

# Which JSP lifecycle methods can be overridden?

> [!abstract] Short answer
> **Only `jspInit()` and `jspDestroy()`.** Declare them in `<%! … %>`. They are the JSP hooks on `JspPage` (`HttpJspPage` for HTTP). **`_jspService` is generated** from the page body and **must not** be declared. Do **not** override servlet **`init` / `service` / `destroy`** in the page — the container (or the `extends` superclass) maps those to the JSP trio. Full lifecycle: [[How would you explain the JSP page lifecycle]]. Servlet `init`: [[Why override the no argument init method in a servlet]].

## Two optional hooks, one generated method

Jakarta Pages **4.0** Table **JSP.11-1** and `jakarta.servlet.jsp.JspPage` / `HttpJspPage`:

| Method | Override in the JSP? |
| --- | --- |
| **`jspInit()`** | **Yes** — optional declaration. Runs from servlet **`init`** after **`ServletConfig` is stored**; `getServletConfig()` already works. |
| **`jspDestroy()`** | **Yes** — optional declaration. Runs from servlet **`destroy`** when the instance is **not** servicing a request. |
| **`_jspService(request, response)`** | **No** — “defined automatically… **should never be defined** by the page author.” Throws `ServletException`, `IOException`. HTTP signature uses `HttpServletRequest` / `HttpServletResponse`. |
| **`init` / `service` / `destroy`** | **No** in `<%! %>` — reserved for the implementation class / superclass (often **`final`** in the spec’s example base). |

The page implementation **is** a servlet (`HttpJspPage` extends `JspPage` extends `Servlet`). Translation writes `_jspService` from template, actions, and scriptlets. Declarations become **members** of that class, so `jspInit` / `jspDestroy` **override** empty defaults on the generated superclass. Names starting `_jsp` / `_jspx` (any case) are **reserved**. Nested types in declarations: [[Can you declare a class inside a JSP page]]. What a JSP is: [[What is Java Server Pages JSP]].

**`page extends`.** If you name a superclass, **you** must keep this contract: `init` → `jspInit`, `service` → `_jspService`, `destroy` → `jspDestroy`. That superclass may wrap `service` around `_jspService`; the **page** still must not declare `_jspService`. Most containers **do not** verify. Avoid `extends`.

```d2
direction: down
ok: "author may declare\njspInit · jspDestroy" {
  width: 280
  height: 40
  style.fill: "#e8f5e9"
}
no: "container owns\n_jspService · init · service · destroy" {
  width: 300
  height: 48
  style.fill: "#ffcdd2"
}
ok -> no: "init calls jspInit\ndestroy calls jspDestroy"
```

**Fig. 1.** Override the **JSP** pair. Leave the **servlet** pair and **`_jspService`** alone.

```jsp
<%-- Conceptual — the only legal lifecycle overrides --%>
<%!
  public void jspInit() {
    getServletContext().log("ready");
  }
  public void jspDestroy() {
    getServletContext().log("gone");
  }
%>
```

**Listing 1.** `<%! %>` methods on the implementation class. The rest of the file still becomes **`_jspService`**. Config is already there: [[How is JSP configured in the web deployment descriptor]].

> [!warning] Declaring `_jspService` or `init` is illegal
> The translator **owns** `_jspService`. Redeclaring servlet lifecycle methods in a declaration violates the author contract (and loses to **`final`** on typical superclasses). **`jspInit` is not a constructor** — no implicits (`out`, `request`) yet; those are locals in `_jspService`. Instance fields you declare are **shared** across concurrent requests on that instance.

> [!tip] Interview answer
> I can override jspInit and jspDestroy in a JSP declaration. I cannot override _jspService; the container generates that from the page. I also do not override servlet init, service, or destroy in the page, because those already call the JSP hooks. jspInit runs after ServletConfig is set, and jspDestroy runs when no request is in flight.
