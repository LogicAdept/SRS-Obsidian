<!--
reps: 0
priority: 0
-->
#Java/Servlet #SRS

# What steps are required to create a servlet?

> [!abstract] Short answer
> **(1)** Write a class that **implements `Servlet`**, almost always by **extending `HttpServlet`**. **(2)** Keep a **public zero-arg constructor**. **(3)** Override **`doGet` / `doPost`** (not `service`). **(4)** **Register and map** it: **`@WebServlet`** with at least one URL pattern, **or** `<servlet>` + `<servlet-mapping>` in **`web.xml`**, **or** **`ServletContext.addServlet` at startup**. **(5)** Put the class in a **web application** (`WEB-INF/classes` or a JAR in `WEB-INF/lib`) and **deploy** it to a **servlet container**. The engine then **`new`s, `init`s, and `service`s**. What a servlet is: [[What is a servlet]]. HTTP methods: [[What are the main HttpServlet request handling methods]]. Constructor vs `init`: [[Should you define a constructor for a servlet and how should you initialize it]]. Container: [[What is a servlet container]].

## Class, mapping, WAR, container

Jakarta Servlet **6.1**:

1. **Implement `Servlet`.** Spec §2: usually **`HttpServlet`**. **`@WebServlet` requires `extends HttpServlet`** and **`urlPatterns` or `value`** (not both). Default servlet **name** = FQCN if omitted.
2. **Zero-arg constructor.** **`createServlet` / container `new`** need it. Do **not** put `ServletConfig` work in `new`.
3. **Handle HTTP.** Override **`doGet`/`doPost`/…**. Optional **`init()`** for one-time setup.
4. **Declare the mapping** (pick one):
   - **Annotation (3.0+):** `@WebServlet("/foo")` — `web.xml` may be omitted; it **overrides** annotations. **`metadata-complete="true"`** skips annotation scan.
   - **Descriptor:** `<servlet>` (`servlet-name`, `servlet-class`) and `<servlet-mapping>` (`url-pattern`).
   - **Programmatic:** `addServlet` from a **declared/`@WebListener` `ServletContextListener`** or **`ServletContainerInitializer.onStartup`** only.
5. **Package and deploy.** Classes under **`WEB-INF/classes`** or JARs in **`WEB-INF/lib`**. The **container** loads, instantiates, **`init`s**, then **`service`**. Lifecycle: [[How does a servlet container manage the servlet lifecycle]]. Annotations: [[What features were added in the Servlet 3 specification]].

```d2
direction: down
cls: "HttpServlet + doGet" {
  width: 200
  height: 40
  style.fill: "#e8f5e9"
}
map: "@WebServlet or web.xml or addServlet" {
  width: 280
  height: 40
  style.fill: "#fff8e1"
}
war: "WAR → servlet container" {
  width: 220
  height: 40
}
cls -> map -> war
```

**Fig. 1.** A class on disk is not a servlet until it is **mapped** and **hosted**.

```java
// Conceptual — Jakarta Servlet 6.1
@WebServlet("/hello")
public class HelloServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        resp.setContentType("text/plain;charset=UTF-8");
        resp.getWriter().write("hello");
    }
}
```

**Listing 1.** Minimum **3.0+** servlet: **extend `HttpServlet`**, **one URL pattern**, **`doGet`**. XML registration is the same class without the annotation.

> [!warning] `@WebServlet` is not optional mapping-wise
> An annotated class **without** a URL pattern is **not deployed**. **`value` and `urlPatterns` together** is **illegal**. The same class under a **different name** in `web.xml` is a **second instance**. **`java HelloServlet`** does not start HTTP.

> [!warning] `metadata-complete` hides annotations
> If `web.xml` says **`metadata-complete="true"`**, **`@WebServlet` is ignored**. **`addServlet` from `service`** is too late. A **parameterized-only constructor** cannot be instantiated by the container.

> [!tip] Interview answer
> I create a servlet by extending HttpServlet, overriding doGet or doPost, and mapping a URL with @WebServlet or web.xml. The class needs a public no-arg constructor. Then I package it in a WAR and deploy it; the container constructs it, calls init, and routes requests to service. Without a mapping or a container, it is just a Java class.
