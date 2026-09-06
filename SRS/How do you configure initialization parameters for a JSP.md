<!--
reps: 0
priority: 0
-->
#Java/JSP #Java/Servlet #SRS

# How do you configure initialization parameters for a JSP?

> [!abstract] Short answer
> Declare the page as a **servlet** in `web.xml` with **`<jsp-file>`** instead of `<servlet-class>`, then add **`<init-param>`** children (name/value pairs). Those values land on that page’s **`ServletConfig`**, the implicit **`config`** object. Read them with `config.getInitParameter("…")`, or in **`jspInit()`** via `getServletConfig()` once the container has stored the config. Do **not** use `${initParam.…}` for this — that map is **context** parameters. `ServletConfig`: [[How would you explain ServletConfig in the servlet API]]. vs context: [[What is the difference between ServletContext and ServletConfig]]. Descriptor: [[How would you explain the Java EE web deployment descriptor]].

## A JSP is a servlet declaration

A JSP compiles to a servlet that implements `JspPage`. The deployment descriptor’s `<servlet>` element describes **both** class-based servlets and JSP pages. For a page you choose **`<jsp-file>`** (not `<servlet-class>`). After that choice, **`<init-param>`** is the same unbounded list of `param-name` / `param-value` pairs used for any servlet.

If `<load-on-startup>` is present with `<jsp-file>`, the JSP **should be precompiled and loaded** at application start (same integer ordering rules as other servlets).

Map the servlet (`<url-pattern>`) or call it by **name** (`getNamedDispatcher`). Init parameters belong to **that declaration**. Hitting the file through a generic `*.jsp` mapping is a **different** servlet and a **different** `ServletConfig`.

Programmatic equivalent (during context startup): `ServletContext.addJspFile(servletName, jspFile)` returns a `ServletRegistration.Dynamic`. Call `setInitParameter` (and mappings) on it **before** the context finishes initializing. `setInitParameter` returns `false` if the name already exists; it throws `IllegalStateException` after the context is initialized.

`jsp-property-group` under `jsp-config` is **not** init parameters. It sets group properties (encoding, EL, scripting, prelude/coda, …).

```d2
direction: down
dd: "web.xml servlet\njsp-file + init-param" {
  width: 260
  height: 50
  style.fill: "#fff8e1"
}
sc: "ServletConfig for that declaration" {
  width: 260
  height: 44
  style.fill: "#e3f2fd"
}
page: "JSP implicit config\nor jspInit + getServletConfig" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
ctx: "context-param\nEL initParam map" {
  width: 260
  height: 50
  style.fill: "#ffebee"
}
dd -> sc
sc -> page
ctx -> page: "not servlet init-param"
```

**Fig. 1.** Page init parameters ride `ServletConfig`. The EL `initParam` map is `ServletContext`.

```xml
<!-- Conceptual — Jakarta Servlet 6.1 web.xml -->
<servlet>
  <servlet-name>report</servlet-name>
  <jsp-file>/report.jsp</jsp-file>
  <init-param>
    <param-name>rows</param-name>
    <param-value>50</param-value>
  </init-param>
  <load-on-startup>1</load-on-startup>
</servlet>
<servlet-mapping>
  <servlet-name>report</servlet-name>
  <url-pattern>/report</url-pattern>
</servlet-mapping>
```

**Listing 1.** `<jsp-file>` replaces `<servlet-class>`. Init parameters are siblings, not children of `jsp-config`.

```jsp
<%-- Conceptual — declaration + scriptlet; config is ServletConfig --%>
<%!
  private String rows;
  public void jspInit() {
    rows = getServletConfig().getInitParameter("rows");
  }
%>
<p>rows=<%= config.getInitParameter("rows") %></p>
```

**Listing 2.** `jspInit` runs after `init(ServletConfig)` has stored the config, so `getServletConfig()` is valid. The implicit `config` object is that same `ServletConfig` (page scope).

> [!warning] `${initParam.rows}` is not a servlet init parameter
> The EL implicit object **`initParam`** is `ServletContext.getInitParameter` — application-wide **`<context-param>`**. Page-specific values are **`config.getInitParameter`**. Mixing the two looks like “init params are null.”

> [!warning] Declare `jspInit`, not `Servlet.init`
> `JspPage.jspInit` is the author hook. The container (or a legal `extends` superclass) must keep `getServletConfig()` working at that point. Overriding `init` fights the generated `init` → `jspInit` chain. `jspInit` is optional and runs before the first request (or at load-on-startup).

> [!warning] The URL must hit **this** servlet declaration
> Init parameters are not magically attached to the `.jsp` file on disk. Request `/report` (or a named dispatcher for `report`). Opening `/report.jsp` through the container's default JSP mapping uses another `ServletConfig` without those `init-param`s.

> [!tip] Interview answer
> A JSP is configured like a servlet: in web.xml use jsp-file instead of servlet-class, then init-param name/value pairs, and map that servlet. Those values show up on the page’s ServletConfig, the implicit config object, and in jspInit through getServletConfig. Do not confuse them with context-param or the EL initParam map, and do not expect jsp-property-group to carry them.
