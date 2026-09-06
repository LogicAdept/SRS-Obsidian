<!--
reps: 0
priority: 0
-->
#Java/JSP/ImplicitObjects #SRS

# Which implicit JSP objects are unavailable on a plain JSP page?

> [!abstract] Short answer
> **`exception`.** On a normal page `isErrorPage` defaults to **`false`**, so the implicit **`exception` (`Throwable`) is undefined** — naming it is a **fatal translation error**. It appears only on **`isErrorPage="true"`** (Table JSP.1-7). A JSP page also has **no `jspContext`** (tag files use that instead of `pageContext` / `page`). `session` is missing only if you set **`session="false"`**. Error wiring: [[How do you handle errors on JSP pages]]. Session opt-out: [[Is a session object always created on a JSP page and can it be disabled]].

## What Table JSP.1-6 always gives you

Jakarta Pages **4.0** §1.8.3 — a **JSP page** always has scripting implicits **`request`**, **`response`**, **`pageContext`**, **`application`**, **`out`**, **`config`**, **`page`**, and **`session`** when the page is session-aware (default). Those are **page** / **request** / **session** / **application** scoped as in [[What variable scopes exist in JSP]]. Tag handlers see them through **`PageContext`**: [[What is PageContext and what are its benefits]].

**Unavailable on that plain page**

| Implicit | Where it exists | If you use it on a plain JSP |
| --- | --- | --- |
| **`exception`** | Error page only (`isErrorPage="true"`) | **Translation error** (`isErrorPage` default **`false`**) |
| **`jspContext`** | **Tag files** (Table JSP.8-5) | Not a page implicit — pages have **`pageContext`** and **`page`** |
| **`session`** | Session-aware pages | **Translation error** if **`session="false"`** (not the default) |

§1.4.3: `exception` is `jakarta.servlet.error.exception`, else the old `jakarta.servlet.jsp.jspException`. **`ErrorData`** is initialized for EL (`${pageContext.errorData.statusCode}`) **on the error page**. On a plain page **`getErrorData()` is meaningless**. A **`web.xml` `<error-page>`** dispatch to a JSP does **not** create the scripting variable — the target still needs **`isErrorPage="true"`**. Self-referencing error pages are a translation error.

EL has **no** `exception` implicit name either; you still go through **`pageContext`**. Scripting `exception` vs EL: [[What do you know about the JSP Expression Language]]. Lifecycle of the generated servlet: [[How would you explain the JSP page lifecycle]].

```d2
direction: down
plain: "plain JSP\nisErrorPage false (default)" {
  width: 280
  height: 40
  style.fill: "#fff8e1"
}
ok: "request response pageContext\nsession out config page application" {
  width: 300
  height: 48
  style.fill: "#e8f5e9"
}
no: "no exception\nno jspContext" {
  width: 240
  height: 40
  style.fill: "#ffcdd2"
}
plain -> ok
plain -> no
```

**Fig. 1.** A plain page is Table **JSP.1-6** only. **`exception`** is Table **JSP.1-7**.

```jsp
<%-- Conceptual — illegal on a plain page --%>
<%@ page session="true" %>
<p><%= exception.getMessage() %></p>
```

**Listing 1.** Fatal **translation** error: `isErrorPage` is still **false**.

```jsp
<%-- Conceptual — error page --%>
<%@ page isErrorPage="true" %>
<p><%= exception.getMessage() %></p>
<p>${pageContext.errorData.statusCode}</p>
```

**Listing 2.** Now **`exception`** and **`errorData`** are defined. Authoring: [[What do you know about authoring custom JSP tags]] (tag files: `jspContext`, not `page`).

> [!warning] `web.xml` error-page does not invent `exception`
> Mapping `/oops.jsp` as an `<error-page>` location still leaves **`exception` illegal** until that file sets **`isErrorPage="true"`**. Do not write **`jspContext`** in a `.jsp`. Do not assume **`${pageContext.errorData}`** on a happy-path view. **`session`** is present on a plain page unless you turn it off.

> [!tip] Interview answer
> On a plain JSP the exception implicit is unavailable because isErrorPage defaults to false, and naming it is a translation error. I turn that page into an error page with isErrorPage true so exception is the Throwable. Tag files use jspContext instead of pageContext, and session disappears only if I set session false.
