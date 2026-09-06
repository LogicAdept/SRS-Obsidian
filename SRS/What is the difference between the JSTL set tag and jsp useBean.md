<!--
reps: 0
priority: 0
-->
#Java/JSP/JSTL #Java/JSP/Tags #SRS

# What is the difference between the JSTL set tag and jsp useBean?

> [!abstract] Short answer
> **`<jsp:useBean>` finds or creates a Java object and names it (`id`). `<c:set>` writes a value into a scoped attribute (`var`) or into a property of an existing bean or `Map` (`target`).** `useBean` can **instantiate** (`class` / `beanName`); `c:set` **never** constructs a class. `useBean` is a **standard action**; `c:set` is **JSTL core** (`jakarta.tags.core`). Beans from a request: [[How do you populate a JavaBean or object attributes from a request]]. JSTL: [[How would you explain JSTL the JSP Standard Tag Library]]. Built-in `jsp:`: [[Why are built in JSP tags not configured in web.xml]].

## Locate-or-create vs assign

Jakarta Pages **4.0** §5.1: **`jsp:useBean`** looks up `id` in the given **scope** (default **page**). If found, it binds that instance (cast to `type`) and **ignores the body**. If missing, it **creates** via a public no-arg `class`, or `Beans.instantiate(beanName)`, then **runs the body** (typical: `jsp:setProperty`). `type` without `class`/`beanName` only **aliases** an object that **must already exist** — otherwise `InstantiationException`. `id` must be **unique in the translation unit** and is also a **scripting variable** (in a scriptless page, an **EL name** instead). `jsp:getProperty` / `jsp:setProperty` still need the bean **introduced** this way even if a servlet stored it.

Jakarta Tags **3.0** §4.3: **`c:set`** does **not** look up-or-create a type. Syntax 1–2: `PageContext.setAttribute(var, value, scope)` — **page** if `scope` omitted. Syntax 3–4: `target` must be a **JavaBean with that setter** or a **`Map`** (put/replace key `property`). Syntax 5: deferred `#{…}` into the **VariableMapper** (no `scope`). The type of `var` is **whatever the value evaluates to** (String, bean, `Boolean`, …). JSTL exposes **scoped attributes only** — no scripting variable (`var`, not `id`). Companion: **`c:remove`**.

| | `<jsp:useBean>` | `<c:set>` |
| --- | --- | --- |
| Job | **Find or construct** a named object | **Assign** a value or a property |
| Name | **`id`** (unique per translation unit) | **`var`** (attribute) or **`target`+`property`** |
| Type | `class` / `type` / `beanName` | Type of the **value** (or the bean property after EL coercion) |
| Body | Runs **only if the bean was created** | Alternative to **`value`** (trimmed JSP output) |
| Null `value` | N/A (creation vs lookup) | **Removes** the attribute (or Map key; bean property → `null`) |
| Library | JSP language | **`<%@ taglib uri="jakarta.tags.core" %>`** |

**Together.** A servlet (or `useBean`) puts a bean in request scope; the view uses **EL** or **`c:set target="${cust}" property="city"`** to mutate it. `c:set var="x"` does **not** replace `useBean` when you need a **new** `Customer()`. Scopes: [[What are the implicit EL scope objects in JSP and how do they differ from servlet scoped objects]]. Hub: [[What is PageContext and what are its benefits]]. MVC hop: [[How does JSP servlet JSP interaction work]].

```d2
direction: down
ub: "jsp:useBean id class|type\nfind → else new → maybe body" {
  width: 300
  height: 48
  style.fill: "#fff8e1"
}
cs: "c:set var|target\nsetAttribute or setter / Map.put" {
  width: 300
  height: 48
  style.fill: "#e3f2fd"
}
pc: "PageContext scopes" {
  width: 240
  height: 36
  style.fill: "#e8f5e9"
}
ub -> pc
cs -> pc
```

**Fig. 1.** Both talk to **scopes**. Only **`useBean`** can **new** the object.

```jsp
<%-- Conceptual — create vs assign --%>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<jsp:useBean id="cust" class="example.Customer" scope="request">
  <jsp:setProperty name="cust" property="city" value="Oslo"/>
</jsp:useBean>
<c:set var="label" value="${cust.city}" scope="page"/>
<c:set target="${cust}" property="city" value="${param.city}"/>
```

**Listing 1.** `useBean` **constructs** (body runs only on create). `c:set var` stores a **value**. `c:set target` writes a **property** on the existing bean.

```jsp
<%-- Conceptual — null c:set removes --%>
<c:set var="label" value="${empty param.q ? null : param.q}"/>
```

**Listing 2.** A **null** `value` is **`removeAttribute("label")`**, not an attribute whose value is `null`. `useBean` does not work that way.

> [!warning] `c:set` will not new your bean; `useBean` body is skipped if it already exists
> No `class` on `c:set`. Duplicate **`id`** on `useBean` is a **translation error**. `type` alone when the object is **absent** → **`InstantiationException`**. `target` **null** or not a bean/`Map` → **`JspException`**. **`session`** scope on a `session="false"` page is illegal for `useBean` and fails at runtime for JSTL. `jsp:setProperty name="cust"` still needs **`useBean`** (or equivalent) on **this** page.

> [!tip] Interview answer
> jsp:useBean locates a Java object by id and scope, or constructs one with class or beanName, and introduces it as a scripting or EL name. c:set never instantiates; it assigns a scoped attribute or a property on an existing bean or Map. I use useBean when the page must create or re-bind a typed bean, and c:set when I only need to put a value in scope or update a property. A null c:set value removes the attribute; a useBean body runs only when the bean was just created.
