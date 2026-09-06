<!--
reps: 0
priority: 0
-->
#Java/Servlet #Java/JSP #SRS

# How do you populate a JavaBean or object attributes from a request?

> [!abstract] Short answer
> Request data arrives as **parameters** (`getParameter` / `getParameterValues` / `getParameterMap` — query string or form body). Copy them onto a bean by **calling setters**, or in JSP with **`<jsp:useBean>`** then **`<jsp:setProperty>`**. **`property="*"`** walks the current `ServletRequest` parameters and sets each bean property whose **name and setter type** match. A missing parameter or `""` is a **noop** (that property is left alone). Request API: [[How would you explain the ServletRequest interface]]. JSP: [[What is Java Server Pages JSP]].

## Parameters in, properties out

HTTP parameters are **strings** (and string arrays). A JavaBean exposes properties through **introspection** (name, simple vs indexed, getter/setter, optional `PropertyEditor`).

**In a servlet**, read the request then set the bean yourself:

- `getParameter(name)` — one value, or the **first** of many; `null` if absent. Prefer `getParameterValues` when the field can repeat.
- Form POST: `application/x-www-form-urlencoded` or `multipart/form-data` (needs `MultipartConfig`). Reading the body with `getInputStream()` / `getReader()` **before** these methods can **block parameter parsing**.

**In JSP**, `jsp:useBean` finds or **creates** (public no-arg constructor) a bean in page/request/session/application scope. Then `jsp:setProperty`:

| Form | Effect |
| --- | --- |
| `property="*"` | Iterate **request parameters**; match **parameter name** to **property name** and types; set each match. `""` does **not** modify that property. |
| `property="user" param="username"` | One property from a **named** parameter (default: param name = property name). Absent or `""` → **noop**. |
| `property="x" value="…"` | Constant, scriptlet, or EL. **Not** together with `param`. |

From a request **parameter** or a **String `value`**, JSP applies **string conversions**: `PropertyEditor.setAsText`, or `Boolean`/`Integer`/… `valueOf` (empty string → `false` / `0` as in that table), or `new String` for `Object`. Conversion failure is a **translation- or request-time error**. Indexed properties take an **array**. EL `value` uses EL conversion; a **scriptlet** `value` is **not** auto-converted.

The `name` on `setProperty` must already have been **introduced** (`jsp:useBean` or a custom action). An object stuffed in the **session** by another servlet is **not** visible to `jsp:setProperty` until `useBean` (or equivalent) exposes it.

```d2
direction: down
form: "request parameters\nquery / form fields" {
  width: 260
  height: 48
  style.fill: "#fff8e1"
}
star: "jsp:setProperty property=*" {
  width: 260
  height: 44
  style.fill: "#e3f2fd"
}
set: "matching setters\n+ String conversions" {
  width: 260
  height: 48
  style.fill: "#e8f5e9"
}
form -> star
star -> set
```

**Fig. 1.** `property="*"` is name-and-type matching against the current request, not a deep copy of the HTML page.

```jsp
<%-- Conceptual — Jakarta Pages 4.0 --%>
<jsp:useBean id="user" class="com.example.User" scope="request" />
<jsp:setProperty name="user" property="*" />
<jsp:setProperty name="user" property="email" param="mail" />
```

**Listing 1.** Create/find the bean, then bulk-map parameters. `email` comes from the `mail` field.

```java
// Conceptual — servlet equivalent
User user = new User();
user.setName(req.getParameter("name"));
String[] roles = req.getParameterValues("role"); // repeating fields
req.setAttribute("user", user);
```

**Listing 2.** Same idea without JSP: parameters are strings; you call setters (and handle multi-valued fields).

> [!warning] `property="*"` is not “bind the whole form blindly”
> Only **matching names** are set. Extra request parameters are ignored. Empty string skips the property. Conversion errors **fail the request**, they do not skip. HTML control names must match bean property names (or use `param`).

> [!warning] Bean visibility and constructors
> `useBean` with `class` needs a **public no-arg constructor**. `setProperty` will not see a controller-created session object unless the page **introduces** it. Do not put `param` and `value` on the same action.

> [!warning] This is not Spring MVC form tags
> Servlet/JSP mapping is **request parameters → JavaBean setters**. Spring MVC `form:` tags / command objects are a **different** stack. Do not mix that story into `jsp:setProperty`.

> [!tip] Interview answer
> In a servlet I read getParameter or getParameterValues and call setters on a JavaBean. In JSP I jsp:useBean then jsp:setProperty; property star copies each request parameter onto a matching property, with string-to-type conversion, and blank or missing parameters leave the property unchanged. Multi-valued fields need getParameterValues or indexed properties, and I do not read the body as a stream first if I still need parameters.
