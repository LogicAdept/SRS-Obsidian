<!--
reps: 0
priority: 0
-->
#Java/JSP/Scripting #Java/Language/NestedClasses #SRS

# Can you declare a class inside a JSP page?

> [!abstract] Short answer
> **Yes — as a nested type of the generated servlet, not as a standalone `.java` compilation unit.** A **declaration** (`<%! … %>` or `<jsp:declaration>`) is concatenated into the **class body** of the page implementation class, so a `class` there is a **member class** of that servlet. A `class` inside a **scriptlet** (`<% … %>`) is a **local class** of `_jspService`, not a servlet member. `<%@ page extends="…" %>` names a **superclass**; it does not nest a type in the page.

## Where the type actually lives

Jakarta Pages **4.0** translates a page into one **Java class** (`jspXXX`; the name is **implementation-dependent**). **Declarations** fill a **declaration section** at class-body level. **Scriptlets** become a **sequence of statements** inside `_jspService`. The page is legal only when that class (plus container support types) is a legal Java program. Java’s class body may contain **member classes**; a method body may contain **local classes**. That is why both placements compile, and why they are different kinds of nested type.

A declaration must be a **complete** declarative construct in the scripting language. In JSP **4.0** that language is **`java`** only. Declarations emit **no** bytes to `out`. They are initialized when the page is initialized and are visible to later declarations, scriptlets, and expressions on the **same** translation unit. They are **not** a public API other pages can `import`: other JSPs cannot rely on `jspXXX$Helper`.

Prefer a real type in a `.java` file and `<%@ page import="…" %>`, a bean, or EL. Page authors are expected to **avoid scripting**; `web.xml` can set **`scripting-invalid`** so any `<%!` / `<%` / `<%=` is a **translation error**. What JSP is: [[What is Java Server Pages JSP]]. Scriptless style: [[What are practical guidelines for working with JSP]]. Groups: [[How is JSP configured in the web deployment descriptor]].

```d2
direction: down
page: "*.jsp source" {
  width: 200
  height: 40
  style.fill: "#fff8e1"
}
impl: "class jspXXX { … }" {
  width: 280
  height: 40
  style.fill: "#e8f5e9"
}
mem: "<%! class Helper { } %>\nmember class of jspXXX" {
  width: 300
  height: 56
}
loc: "_jspService(request, response)\n<% class Line { } %>\nlocal class of the method" {
  width: 300
  height: 72
  style.fill: "#e3f2fd"
}
page -> impl: "translation"
impl -> mem
impl -> loc
```

**Fig. 1.** Same `class` keyword, two homes: **member** of the servlet versus **local** to `_jspService`.

```jsp
<%-- Conceptual — Jakarta Pages 4.0, language java --%>
<%@ page contentType="text/html;charset=UTF-8" %>
<%!
  static final class Greeting {
    static String of(String name) {
      return "Hello, " + name;
    }
  }
%>
<p><%= Greeting.of("JSP") %></p>
```

**Listing 1.** **Static member class** in a declaration. `Greeting` is a nested type of the generated servlet, visible to scriptlets and expressions on this page.

```jsp
<%-- Conceptual — local class of _jspService --%>
<%
  class Line {
    String wrap(String s) {
      return "[" + s + "]";
    }
  }
  Line line = new Line();
%>
<p><%= line.wrap("ok") %></p>
```

**Listing 2.** A scriptlet **local class**. It is **not** `public`/`protected`/`private`/`static`, is **not** a member of the servlet, and is visible only in `_jspService` after its declaration. It **can** read effectively final implicit objects (`out`, `request`, …) because those are **locals of that method**. A member class in Listing 1 **cannot**.

> [!warning] Implicit objects are `_jspService` locals
> `request`, `response`, `out`, `session`, `pageContext`, and the rest are created in the **initialization section of `_jspService`**, for **scriptlets and expressions**. A **member** nested class does not see them. Pass `JspWriter` / `HttpServletRequest` in, or use servlet methods (`getServletContext()`) from `jspInit`. A **local** class in a scriptlet can capture those variables.

> [!warning] `scripting-invalid` forbids the whole trick
> A `jsp-property-group` with `<scripting-invalid>true</scripting-invalid>` makes declarations and scriptlets a **translation error**. Do not name a nested type `_jsp…` / `_jspx…` (reserved). Do not treat `jspXXX$Helper` as a stable type other pages import. Instance fields you also declare with `<%! %>` are **shared across concurrent requests** on the same servlet instance.

> [!tip] Interview answer
> Yes. A class in `<%! … %>` becomes a nested member of the servlet the container generates; a class in a scriptlet is only a local class of `_jspService`. I still would not put types in the page: they are not a reusable compilation unit, implicit objects are not in scope for a member class, and `scripting-invalid` can ban the syntax. I put helpers in `.java` and keep the JSP as template plus EL.
