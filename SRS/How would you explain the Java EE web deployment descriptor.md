<!--
reps: 0
priority: 0
-->
#Java/Servlet #Java/JavaEE #SRS

# How would you explain the Java EE web deployment descriptor?

> [!abstract] Short answer
> The **web application deployment descriptor** is **`WEB-INF/web.xml`**: XML that carries **how this WAR is assembled and deployed** (servlets, filters, listeners, mappings, context params, session, welcome/error pages, MIME, locale/encoding, security). Root element **`web-app`**, schema **version** on that element (Servlet **6.1** today). It is **optional** if you have **no** servlet/filter/listener components or you declare them with **annotations**. **`metadata-complete="true"`** means **ignore** those annotations (and fragments) for deployment metadata. Layout: [[How do you write a web application in Java]]. Context params: [[How would you explain ServletContext in Java web applications]]. JSP block: [[How is JSP configured in the web deployment descriptor]]. Constraints: [[How do you restrict servlet endpoints to users with a valid session]]. vs Spring XML: [[What is the difference between web.xml and Spring servlet.xml]].

## Portable `web.xml`, not the vendor file

The Servlet spec’s DD is the contract among **developer, assembler, and deployer**. Paths are **URL-decoded**, should start with **`/`**, and are **canonicalized** (`/a/../b` → `/b`). The document **must validate** against the schema. Older `web.xml` versions **must still deploy**. Child elements of `web-app` may appear in **any order**; you still get **at most one** `session-config`, `jsp-config`, and `login-config`.

**What it configures.** Context init parameters; session timeout; servlet / JSP (`jsp-file`) declarations and **url-pattern** mappings; listeners; filters and filter mappings; MIME; welcome files; error pages; locale/encoding; security (`security-constraint`, `login-config`, roles, `run-as`, `deny-uncovered-http-methods`). Also default context path, request/response character encoding.

**Annotations and fragments.** `@WebServlet` / `@WebFilter` / `@WebListener` can replace entries. The DD **overrides** annotation defaults. Libraries under **`WEB-INF/lib`** may add **`META-INF/web-fragment.xml`** (root **`web-fragment`**). `web.xml` **`absolute-ordering`** (or fragment `ordering`) controls merge order. Names must be **unique** across the union.

**Not this file.** **`application.xml`** is the **EAR** application DD (`META-INF` of the **enterprise** archive), not the web module. **`sun-web.xml` / `glassfish-web.xml` / Tomcat `context.xml`** are **runtime-specific**. Portable apps do not need them.

```d2
direction: down
war: "WAR" {
  width: 160
  height: 36
  style.fill: "#fff8e1"
}
xml: "WEB-INF/web.xml" {
  width: 200
  height: 36
  style.fill: "#e3f2fd"
}
fr: "WEB-INF/lib\nMETA-INF/web-fragment.xml" {
  width: 240
  height: 48
  style.fill: "#e3f2fd"
}
ann: "@WebServlet and friends" {
  width: 220
  height: 36
  style.fill: "#e8f5e9"
}
war -> xml
war -> fr
war -> ann
```

**Fig. 1.** Effective config = descriptor + fragments + annotations, unless `metadata-complete` stops the last two.

```xml
<!-- Conceptual — Servlet 6.1 WEB-INF/web.xml -->
<web-app version="6.1">
  <context-param>
    <param-name>adminEmail</param-name>
    <param-value>ops@example.com</param-value>
  </context-param>
  <servlet>
    <servlet-name>catalog</servlet-name>
    <servlet-class>com.example.CatalogServlet</servlet-class>
  </servlet>
  <servlet-mapping>
    <servlet-name>catalog</servlet-name>
    <url-pattern>/catalog/*</url-pattern>
  </servlet-mapping>
</web-app>
```

**Listing 1.** Name uniqueness is per web application. `version` selects the schema generation.

> [!warning] Missing `web.xml` is legal; duplicate `jsp-config` is not
> Static files / JSP-only (or annotation-only components) need **no** `web.xml`. Two `login-config` (or `session-config` / `jsp-config`) elements are an **error**. `metadata-complete="true"` does **not** skip CDI / `HandlesTypes`.

> [!warning] Vendor XML is not the Java EE web DD
> `sun-web.xml` never made an app portable. `application.xml` describes an **EAR**, not this WAR. Enumerated values in `web.xml` are **case-sensitive**.

> [!tip] Interview answer
> The Java EE web deployment descriptor is WEB-INF/web.xml: XML that tells the container how to deploy the WAR, from servlet mappings to security. Since Servlet 3 you can omit it and use annotations, but web.xml still wins when both say the same thing, and metadata-complete true means ignore those annotations. Fragments in library JARs merge in; vendor files like sun-web.xml are extra and not this descriptor.
