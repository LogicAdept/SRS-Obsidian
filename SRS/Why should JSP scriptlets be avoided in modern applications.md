<!--
reps: 0
priority: 0
-->
#Java/JSP/Scripting #SRS

# Why should JSP scriptlets be avoided in modern applications?

> [!abstract] Short answer
> **Because the spec’s page-author role is presentation without Java.** Jakarta Pages **4.0** expects authors to use **standard/custom actions and EL**, not `<% %>` / `<%! %>` / `<%= %>`. EL exists so pages can be **scriptless**; **`scripting-invalid`** makes leftover scripting a **translation error**. Put work in a servlet or tag; the JSP renders. Guidelines: [[What are practical guidelines for working with JSP]]. EL: [[What do you know about the JSP Expression Language]].

## The language already replaced them

**Roles.** **Page authors** “will **not** make use of the scripting capabilities” and **need not know Java**. **Advanced** authors who do know Java are still told to **avoid scripting where possible**. Java belongs with **tag-library developers** and **controller** code, not in the template.

**What scriptlets were for.** §1.12: glue around template and actions; **JSP 2.0 added EL as the alternative**. Chapter **2**: EL is how you write **scriptless** pages (EL yes; scriptlets / expressions / declarations **no**). JSTL supplies the control flow those scriptlets used to be (`c:if`, `c:forEach`, `c:out`): [[How would you explain JSTL the JSP Standard Tag Library]]. Custom tags: [[How can you extend JSP functionality]]. MVC hop: [[How does JSP servlet JSP interaction work]].

**Enforce it.** Scripting is **on by default**. A `jsp-property-group` **`<scripting-invalid>true</scripting-invalid>`** (or the matching page setting) makes `<%` / `<%!` / `<%=` a **translation error**. That is **not** `el-ignored`. Groups: [[How is JSP configured in the web deployment descriptor]].

**Why it hurts when you ignore that**

- **Two jobs in one file** — markup plus business rules; designers cannot edit the view; Java is not unit-testable inside `_jspService`.
- **`<%= %>` is not `c:out`** — no XML escaping; user data becomes XSS.
- **Declarations are instance fields** — concurrent `_jspService` calls share them; scriptlet locals do not. Lifecycle: [[How would you explain the JSP page lifecycle]].
- **Modern tag bodies are `scriptless`** — SimpleTag / tag files **cannot** contain scriptlets; a page full of `<%` will not compose with them.

```d2
direction: down
old: "<% Java in the view %>" {
  width: 240
  height: 40
  style.fill: "#ffcdd2"
}
now: "servlet / bean / tag\n+ JSP template + EL + JSTL" {
  width: 300
  height: 48
  style.fill: "#e8f5e9"
}
old -> now: "scripting-invalid"
```

**Fig. 1.** Scriptlets were glue. The replacement is **scriptless** pages plus components.

```jsp
<%-- Conceptual — avoid --%>
<% User u = (User) request.getAttribute("user"); %>
<p><%= u.getName() %></p>
```

**Listing 1.** Scriptlet + unescaped expression. Logic and XSS in the template.

```jsp
<%-- Conceptual — scriptless --%>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<p><c:out value="${requestScope.user.name}"/></p>
```

**Listing 2.** EL for the value, **`c:out`** for escaping. The servlet still **setAttribute** and **forward**.

> [!warning] Scripting is still legal until you ban it
> Default **`scripting-invalid` is off**, so `<%` **compiles**. Turning off **EL** (`isELIgnored`) does **not** turn off scriptlets. `<%! %>` and `<%= %>` count as scripting too. HTML comments do **not** disable them: [[How do you comment code in JSP]].

> [!tip] Interview answer
> I avoid JSP scriptlets because the spec page-author model is template plus actions and EL, not Java in the view. EL and JSTL already cover data access, loops, and output, and scripting-invalid can make leftover scriptlets a translation error. Scriptlets mix concerns, skip escaping, and fight scriptless tag bodies. I keep work in a servlet or a tag and let the JSP render.
