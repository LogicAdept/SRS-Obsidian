<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Servlet #SRS

# What is Spring MVC `DispatcherServlet`?

> [!abstract] Short answer
> **`DispatcherServlet` is Spring MVC’s front controller:** one servlet that runs a **fixed dispatch algorithm** and delegates mapping, interceptors, invocation, views, and exceptions to beans in its **`WebApplicationContext`**. It does not contain your business logic. Register it like any servlet (`web.xml`, `WebApplicationInitializer`, or Boot auto-config). Defaults include **`RequestMappingHandlerMapping`** + **`RequestMappingHandlerAdapter`** so `@RequestMapping` works.

## Shared algorithm, pluggable delegates

Spring MVC *DispatcherServlet*: the servlet is declared and URL-mapped per the Servlet spec; Spring config supplies **`HandlerMapping`**, **`HandlerAdapter`**, **`ViewResolver`**, **`HandlerExceptionResolver`**, **`LocaleResolver`**, optional **`MultipartResolver`**, and so on. Beans are detected **by type** (any name). Declaring your own beans of that type **replaces** the servlet’s defaults.

Official processing order:

1. Bind the servlet `WebApplicationContext` on the request (`WEB_APPLICATION_CONTEXT_ATTRIBUTE`).
2. Bind `LocaleResolver` (and wrap the request if a `MultipartResolver` sees a multipart).
3. Ask `HandlerMapping`s **in order** for a `HandlerExecutionChain` (handler + interceptors).
4. Find the first `HandlerAdapter` that **supports** that handler and invoke it.
5. Render a `View` if a model/view name was returned; **annotated controllers may write the body inside the adapter** (`@ResponseBody`).
6. On failure, `HandlerExceptionResolver`s run.

```java
public class MyWebApplicationInitializer implements WebApplicationInitializer {

    @Override
    public void onStartup(ServletContext servletContext) {
        AnnotationConfigWebApplicationContext context = new AnnotationConfigWebApplicationContext();
        context.register(AppConfig.class);
        DispatcherServlet servlet = new DispatcherServlet(context);
        ServletRegistration.Dynamic registration = servletContext.addServlet("app", servlet);
        registration.setLoadOnStartup(1);
        registration.addMapping("/app/*");
    }
}
```

**Listing 1.** Conceptual Framework registration. Mapping is `/app/*`, not automatically `/`. Java vs `web.xml`: [[What is WebApplicationInitializer in Spring MVC]]. Root vs servlet context: [[What is the difference between DispatcherServlet and ContextLoaderListener]]. Pattern: [[What is the Front Controller pattern in Spring MVC]].

```d2
direction: down
http: "HTTP request\nmapped to this servlet" {
  width: 280
  height: 60
  style.fill: "#e3f2fd"
}
ds: "DispatcherServlet" {
  width: 220
  height: 50
  style.fill: "#fff3e0"
}
hm: "HandlerMapping\n+ interceptors" {
  width: 240
  height: 60
  style.fill: "#e8f5e9"
}
ha: "HandlerAdapter\ninvoke handler" {
  width: 240
  height: 60
  style.fill: "#fce4ec"
}
out: "ViewResolver or\nHttpMessageConverter" {
  width: 260
  height: 60
  style.fill: "#f3e5f5"
}

http -> ds -> hm -> ha -> out
```

**Fig. 1.** Mapping: [[What is HandlerMapping in Spring MVC]]. Invocation: [[What is HandlerAdapter in Spring MVC]]. Chain callbacks: [[What is a HandlerInterceptor in Spring MVC]].

Default mappings: **`BeanNameUrlHandlerMapping`** and **`RequestMappingHandlerMapping`**. Default adapters: **`HttpRequestHandlerAdapter`**, **`SimpleControllerHandlerAdapter`**, **`RequestMappingHandlerAdapter`**. Default view resolver if none declared: **`InternalResourceViewResolver`**. Locale default: **`AcceptHeaderLocaleResolver`**.

Spring Boot registers the servlet from **Spring configuration** with the embedded container — not `web.xml`.

> [!warning] Custom `HandlerMapping` can drop `@RequestMapping`
> If you register mappings/adapters yourself, you must still include **`RequestMappingHandlerMapping`** and **`RequestMappingHandlerAdapter`** or `@RequestMapping` methods are ignored.

> [!warning] It is not “every HTTP request”
> Only URLs in **this servlet’s mapping** enter it. Filters (including Security) run **around** the servlet, not inside it. Several `DispatcherServlet`s can coexist, each with its own context namespace (`[servlet-name]-servlet` by default).

> [!warning] No handler is an exception (Spring 6.1+)
> `throwExceptionIfNoHandlerFound` defaults to **`true`** (and is deprecated). A configured **default servlet** still swallows unmatched paths (no MVC 404).

> [!tip] Interview answer
> **`DispatcherServlet` is the front controller: it finds a handler via `HandlerMapping`, runs interceptors, lets a `HandlerAdapter` invoke the controller, then renders a view or writes the body.** You register it as a servlet; Boot does that for you. Your controllers are beans it dispatches to, not subclasses of the servlet.
