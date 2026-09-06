<!--
reps: 0
priority: 0
-->
#Java/JSP/JSTL #SRS

# How would you explain JSTL the JSP Standard Tag Library?

> [!abstract] Short answer
> **Jakarta Standard Tag Library (JSTL, Jakarta Tags 3.0) is the portable tag library of common page-author actions and EL functions** — so a JSP can iterate, branch, print, format, and call helpers **without Java scriptlets**. It **extends** JSP; it is **not** the `jsp:` standard actions and **not** one TLD. You import the libraries you need with `<%@ taglib %>`. Five libraries: [[How is the JSTL tag library organized]]. Custom tags in general: [[How can you extend JSP functionality]]. Built-in `jsp:`: [[Why are built in JSP tags not configured in web.xml]].

## Standard behavior for people who write the view

The spec’s goal is to **simplify page authors’ lives**. Many authors are not Java programmers; scripting is a poor fit. JSTL gives **tag-based** control flow (`if`, `choose`, `forEach`) that is more natural than `<% %>`, plus **general-purpose** actions that sit next to EL: show a value (`c:out`), set/remove scoped attributes (`c:set` / `c:remove`), catch nested failures (`c:catch`). It also standardizes **URL** work, **i18n/formatting**, **XML**, **SQL**, and **string EL functions** (`fn:length`, `fn:escapeXml`, …). What a JSP is: [[What is Java Server Pages JSP]]. Scriptless style: [[What are practical guidelines for working with JSP]]. Errors: [[How does JSTL handle errors]].

**Not the JSP language.** `jsp:include` / `jsp:useBean` are **standard actions** the translator already knows. JSTL is a **tag library**: URI + TLD + handlers, typically `jakarta.servlet.jsp.jstl` APIs. Tags **3.0** needs a Pages **3.0** container (EL is its own spec). A Pages **4.0** app still **declares** the libraries.

**Collaboration.** JSTL actions export **scoped attributes** (`var`, default **page** scope), **not** scripting variables. Iterators collaborate with nested tags through a defined interface. `c:out` **escapes** `<`, `>`, `'`, `"`, `&` by default (`escapeXml`) so raw EL in the page is not an XSS hole.

```d2
direction: down
author: "page author\nHTML + EL" {
  width: 220
  height: 40
  style.fill: "#fff8e1"
}
jstl: "JSTL actions + fn:*\n(not scriptlets)" {
  width: 260
  height: 48
  style.fill: "#e8f5e9"
}
jsp: "JSP → servlet" {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
author -> jstl
jstl -> jsp
```

**Fig. 1.** Explain JSTL as the **standard toolbox** on top of JSP, not as a second page language.

```jsp
<%-- Conceptual — Jakarta Tags 3.0 --%>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<%@ taglib prefix="fn" uri="jakarta.tags.functions" %>
<p><c:out value="${user.name}"/></p>
<p>count ${fn:length(items)}</p>
<c:forEach var="item" items="${items}">
  <c:out value="${item}"/>
</c:forEach>
```

**Listing 1.** Core actions plus an **EL function**. `var` on `forEach` is a **page-scoped** attribute, not a Java local.

> [!warning] JSTL is not built into the JSP translator
> Without the library on the classpath and a `taglib` for that **URI**, `<c:out>` is unknown. Do not treat `c:` as a reserved prefix: the **URI** selects the TLD. `jsp:forward` does **not** require JSTL.

> [!warning] `c:out` escaping is a default, not optional hygiene you can forget
> `escapeXml` defaults to **true**. Setting it **false**, or printing with `<%= %>` / raw `${}` in template text, reopens markup injection. JSTL **SQL** tags exist for page-author DB access; they are a **separate** library, not a reason to put JDBC in the view.

> [!tip] Interview answer
> JSTL is the standard tag library for JSP page authors: conditionals, loops, output, formatting, and EL functions so I do not write Java in the page. It is not part of the JSP syntax the way jsp: actions are; I import jakarta.tags URIs. I still keep business work in a servlet and use the page as the view.
