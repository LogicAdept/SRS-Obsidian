<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Servlet #SRS

# What is `WebApplicationInitializer` in Spring MVC?

> [!abstract] Short answer
> **`WebApplicationInitializer` is Spring’s Servlet 3 SPI to configure the `ServletContext` in Java** — register servlets, filters, listeners, and context params **instead of (or together with) `web.xml`**. The container loads **`SpringServletContainerInitializer`** from `spring-web`, finds your implementations, and calls **`onStartup(ServletContext)`**. For MVC, extend **`AbstractAnnotationConfigDispatcherServletInitializer`** rather than wiring `DispatcherServlet` by hand.

## Detected, then `onStartup`

`SpringServletContainerInitializer` is a `ServletContainerInitializer` listed in `META-INF/services`. It is annotated `@HandlesTypes(WebApplicationInitializer.class)`, so the container scans implementations and passes them in. Spring instantiates them (honoring **`@Order` / `Ordered`**), then each `onStartup` runs. No implementations → **no-op** (INFO log). The types live in **`spring-web`** and can register **any** servlet, filter, or listener — not only MVC.

```java
public class MyWebAppInitializer implements WebApplicationInitializer {

    @Override
    public void onStartup(ServletContext container) {
        AnnotationConfigWebApplicationContext rootContext =
                new AnnotationConfigWebApplicationContext();
        rootContext.register(AppConfig.class);
        container.addListener(new ContextLoaderListener(rootContext));

        AnnotationConfigWebApplicationContext dispatcherContext =
                new AnnotationConfigWebApplicationContext();
        dispatcherContext.register(DispatcherConfig.class);

        ServletRegistration.Dynamic dispatcher =
                container.addServlet("dispatcher", new DispatcherServlet(dispatcherContext));
        dispatcher.setLoadOnStartup(1);
        dispatcher.addMapping("/");
    }
}
```

**Listing 1.** Conceptual Framework 7 javadoc example: constructor-injected contexts, no servlet init-params. Servlet itself: [[What is Spring MVC DispatcherServlet]]. Root vs child: [[What is the difference between DispatcherServlet and ContextLoaderListener]].

Usual shortcut since 3.2:

```java
public class AppInitializer extends AbstractAnnotationConfigDispatcherServletInitializer {

    @Override
    protected Class<?>[] getRootConfigClasses() {
        return new Class<?>[] { RootConfig.class };
    }

    @Override
    protected Class<?>[] getServletConfigClasses() {
        return new Class<?>[] { WebConfig.class };
    }

    @Override
    protected String[] getServletMappings() {
        return new String[] { "/" };
    }
}
```

**Listing 2.** Conceptual: root `@Configuration` for `ContextLoaderListener`, servlet `@Configuration` for `DispatcherServlet`. Return **`null`** from `getServletConfigClasses()` if everything lives in the root.

```d2
direction: down
sci: "Servlet container\nSpringServletContainerInitializer" {
  width: 320
  height: 70
  style.fill: "#e3f2fd"
}
wai: "WebApplicationInitializer\nonStartup(ServletContext)" {
  width: 320
  height: 70
  style.fill: "#fff3e0"
}
reg: "addServlet / addFilter / addListener" {
  width: 300
  height: 60
  style.fill: "#e8f5e9"
}

sci -> wai -> reg
```

**Fig. 1.** You do not register this interface in `web.xml`; the container finds it. XML `web.xml` may still exist alongside.

> [!warning] `absolute-ordering` can skip Spring
> `metadata-complete` and `<absolute-ordering>` limit SCI / fragment scanning. To keep this initializer, include the **`spring_web`** fragment name in `<absolute-ordering>`.

> [!warning] Not how Boot starts
> Boot bootstraps the **embedded** container from Spring config and registers `Filter`/`Servlet` beans itself. A `WebApplicationInitializer` in a Boot JAR is the **WAR / external Tomcat** story, not `SpringApplication.run`.

> [!warning] Still Servlet 3+
> `ServletContext.addServlet` is the Servlet 3 programmatic API. A Servlet 2.5-only container will not run this SPI.

> [!tip] Interview answer
> **`WebApplicationInitializer.onStartup` is Java `web.xml`.** `SpringServletContainerInitializer` discovers it on the classpath. For MVC, extend `AbstractAnnotationConfigDispatcherServletInitializer` and return root vs servlet `@Configuration` classes plus URL mappings. Boot does not use this path for an embedded server.
