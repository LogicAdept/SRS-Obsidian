<!--
reps: 0
priority: 0
-->
#Java/JSP/EL #SRS

# What do you know about the JSP Expression Language?

> [!abstract] Short answer
> **EL is a small, scriptless language for values (and, when a tag asks, deferred methods).** Jakarta Pages **4.0** evaluates **`${…}` immediately** in template text and in `rtexprvalue` attributes; **`#{…}` is deferred** and legal only on attributes that accept it. Bare names are **scoped attributes**; `.` / `[]` walk beans, maps, lists, arrays. Functions are **public static** methods named in a **TLD**. Turn it off: [[How do you disable Expression Language in JSP]]. Operators: [[What operator types exist in the JSP Expression Language]].

## Language plus JSP wiring

**Jakarta Expression Language 6.0** is the language (literals, operators, coercion, lambdas, collection ops). **Pages 4.0 Chapter 2** is how JSP hosts it: the page can stay **scriptless** (`scripting-invalid`) and still reach request data. Template-text `${…}` is coerced to **`String`** when the response is rendered. A **`tagdependent`** body does **not** run EL. Nested eval-expressions such as `${item[${i}]}` are **illegal**; write `${item[i]}`. Mixing `${}` and `#{}` in one composite expression is **illegal**.

**`${}` vs `#{}`.** The EL engine parses both the same way. JSP (and Faces) treat **`${}` as immediate** and **`#{}` as deferred** (`ValueExpression` / `MethodExpression` handed to the tag, evaluated later). In JSP template text only **`${}`** is allowed; **`#{}` is a translation error** unless deferred syntax is permitted as a literal. Static TLD attributes (`rtexprvalue=false`) cannot take an expression at all.

**Names.** JSP always supplies EL implicits: **`pageContext`**, the four **`*Scope` maps**, **`param` / `paramValues`**, **`header` / `headerValues`**, **`cookie`**, **`initParam`**. There is **no** EL implicit named `request` or `session` — use **`${pageContext.request}`** or the maps. Bare **`${product}`** is **`PageContext.findAttribute`**. Maps vs servlet objects: [[What are the implicit EL scope objects in JSP and how do they differ from servlet scoped objects]]. Method on the request: [[How do you read the HTTP method with JSP EL]].

**Resolution (JSP chain).** `ImplicitObjectELResolver` → application-added resolvers → stream / static field / map / bundle / list / array / **`RecordELResolver`** (read-only) / bean → **`ScopedAttributeELResolver`** → import → **`NotFoundELResolver`**. Unknown identifiers default to **`null`** (masks typos) unless **`errorOnELNotFound` / `error-on-el-not-found`**. EL 6.0 also exposes array **`length`**. Invalid EL syntax is a **translation error**.

**Functions.** `prefix:name(args)` maps to a **public static** method listed in that library’s TLD (`function-class` + `function-signature`). Duplicate function **names** in one TLD fail translation. JSTL `fn:` is one such library: [[How would you explain JSTL the JSP Standard Tag Library]]. Authoring a function: [[How can you extend JSP functionality]].

**Defaults, not warnings.** Missing pieces yield type-correct defaults; real failures throw (JSP error-page machinery). Template output is **not** HTML-escaped; use **`c:out`** (or equivalent) for untrusted text.

```d2
direction: down
tmpl: "template text\n${} → String now\n#{} translation error" {
  width: 280
  height: 48
  style.fill: "#fff8e1"
}
attr: "rtexprvalue attribute\n${} evaluate now\n#{} if TLD deferred" {
  width: 280
  height: 48
  style.fill: "#e3f2fd"
}
res: "CompositeELResolver\nimplicits → bean → findAttribute → null" {
  width: 300
  height: 48
  style.fill: "#e8f5e9"
}
tmpl -> res
attr -> res
```

**Fig. 1.** JSP decides **when** `${}` / `#{}` run; the EL resolver chain decides **what** a name means.

```jsp
<%-- Conceptual — EL on a scriptless page --%>
<p>${pageContext.request.contextPath}</p>
<p>${requestScope.user.name}</p>
<c:if test="${not empty param.q}">
  <c:out value="${param.q}"/>
</c:if>
```

**Listing 1.** Immediate `${}` in template text and a dynamic attribute. `empty` is an EL operator; `c:out` escapes. `${request.user}` would **not** mean the servlet request.

```jsp
<%-- Conceptual — quoting when EL is on --%>
<p>${'${'}not.an.expression}</p>
```

**Listing 2.** Emit the characters `${not.an.expression}` without evaluating. `\$` also quotes when EL is **enabled**; with `isELIgnored` the quote rules do not apply.

> [!warning] Unknown names are `null`; `#{}` is not for template text
> `${missing}` is **not** a translation error by default — **`NotFoundELResolver` returns `null`**. Turn on **`errorOnELNotFound`** if you want a fail. `${request.method}` is a **scoped attribute** named `request`, not `HttpServletRequest`. `#{}` in template text fails translation. Reserved words (`empty`, `eq`, `true`, `null`, `div`, …) are **not** identifiers.

> [!tip] Interview answer
> JSP EL is a scriptless language: ${} runs immediately in template text and in dynamic attributes, while #{} is deferred for tags that accept ValueExpression or MethodExpression. Names resolve through implicits, then beans and maps, then PageContext.findAttribute, and a missing name is null unless I set errorOnELNotFound. I reach the servlet request as pageContext.request, I map functions in a TLD to public static methods, and I escape untrusted output with c:out rather than raw ${}.
