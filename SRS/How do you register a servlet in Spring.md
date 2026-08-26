<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Spring/Boot #Java/Servlet #SRS

# How do you register a servlet in Spring?

> [!abstract] Short answer
> **On the `ServletContext`**, not in a Spring XML bean file. Classic MVC: **`web.xml` `<servlet>`** or **`ServletContext.addServlet`** from a **`WebApplicationInitializer`**. Boot (embedded): declare the **`Servlet` as a `@Bean`**, or wrap it in **`ServletRegistrationBean`**. A **single** servlet bean maps to **`/`**; **several** use the **bean name as a path prefix**. **`@WebServlet`** needs **`@ServletComponentScan`** on Boot. Embedded Boot **does not run** `WebApplicationInitializer`.

## Container registration, then Spring beans

Jakarta: servlets are named, mapped, and `load-on-startup`’d by the **container**. Spring’s `DispatcherServlet` is one such servlet.

**WAR / Servlet 3:** `WebApplicationInitializer.onStartup` → `addServlet("app", new DispatcherServlet(ctx)).addMapping("/app/*")`. Shortcut: **`AbstractAnnotationConfigDispatcherServletInitializer`**. `web.xml` still works; the descriptor **overrides** annotations.

**Boot embedded:** `ServletContextInitializer` beans (including **`ServletRegistrationBean`**) run from Spring, **not** from `SpringServletContainerInitializer`. Docs: do **not** rely on `WebApplicationInitializer` in an embedded container — wrap it in a `ServletContextInitializer` bean if you must reuse one.

`ServletRegistrationBean`: set the servlet before startup; `setUrlMappings` default **`/`**; `setLoadOnStartup`; `setMultipartConfig`. Filters: `FilterRegistrationBean`.

```java
@Bean
ServletRegistrationBean<PingServlet> ping() {
    return new ServletRegistrationBean<>(new PingServlet(), "/ping/*");
}

@Configuration
class WebInit implements WebApplicationInitializer {
    @Override
    public void onStartup(ServletContext sc) {
        sc.addServlet("app", new DispatcherServlet(ctx)).addMapping("/");
    }
}
```

**Listing 1.** Conceptual: Boot bean vs classic initializer. Front controller: [[What is Spring MVC DispatcherServlet]]. SPI: [[What is WebApplicationInitializer in Spring MVC]]. Descriptor vs Spring XML: [[What is the difference between web.xml and Spring servlet.xml]]. Minimal MVC: [[What minimal setup is required for Spring MVC to handle HTTP requests]].

```d2
direction: down
sc: "ServletContext" {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
xml: "web.xml" {
  width: 140
  height: 35
  style.fill: "#fff3e0"
}
wai: "WebApplicationInitializer\n(WAR)" {
  width: 240
  height: 45
  style.fill: "#fff3e0"
}
boot: "ServletRegistrationBean\n(Boot embedded)" {
  width: 260
  height: 45
  style.fill: "#e8f5e9"
}

xml -> sc
wai -> sc
boot -> sc
```

**Fig. 1.** All three call `ServletContext`. `*-servlet.xml` is **bean config**, not servlet registration.

> [!warning] Embedded Boot ignores `WebApplicationInitializer`
> Third-party WARs that only ship that interface **never start** their servlets in `java -jar`. Use **`ServletRegistrationBean`** / a **`ServletContextInitializer`** `@Bean`.

> [!warning] `@WebServlet` is not scanned by default
> Add **`@ServletComponentScan`**. It has **no effect** in a **standalone** container (the server’s own scan applies).

> [!warning] Two servlet beans change the map
> One servlet bean → **`/`**. A second servlet bean switches convention to **`/{beanName}`** prefixes. Prefer explicit **`ServletRegistrationBean`** mappings when you add a custom servlet next to `DispatcherServlet`.

> [!tip] Interview answer
> **Register on `ServletContext`:** `web.xml`, `WebApplicationInitializer.addServlet`, or Boot **`ServletRegistrationBean`**. Boot already registers `DispatcherServlet`. Embedded Boot will **not** pick up `WebApplicationInitializer` by itself.
