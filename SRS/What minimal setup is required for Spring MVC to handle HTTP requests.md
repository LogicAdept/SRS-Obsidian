<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Servlet #SRS

# What minimal setup is required for Spring MVC to handle HTTP requests?

> [!abstract] Short answer
> **Three pieces:** (1) a **`DispatcherServlet` mapped** to a URL pattern, (2) a **`WebApplicationContext`** for that servlet that contains MVC strategy beans (**`HandlerMapping` + `HandlerAdapter`** — the servlet **installs defaults** if you declare none), and (3) at least one **`@Controller` / `@RestController` bean in that context** with a mapping. **`@EnableWebMvc` does not register the servlet.** Boot’s web starter does all three.

## Servlet, context, then a handler bean

Spring MVC *DispatcherServlet*: declare and map the servlet per the Servlet spec (`web.xml` or `WebApplicationInitializer`). It then discovers **`HandlerMapping`**, **`HandlerAdapter`**, **`ViewResolver`**, **`HandlerExceptionResolver`**, … **by type**. If you **do not** declare those types, it uses **framework defaults**, including **`RequestMappingHandlerMapping`** and **`RequestMappingHandlerAdapter`**. Declaring **any** mapping/adapter beans **replaces** those defaults.

`RequestMappingHandlerMapping` only treats **type-level `@Controller`** as a handler, and by default it does **not** scan **ancestor** contexts. Put controllers in the **servlet** `WebApplicationContext` (`@ComponentScan` on the config you pass to `DispatcherServlet`), not only in a `ContextLoaderListener` root.

`@EnableWebMvc` imports mapping/adapter/converters; it is **not** required if you accept servlet defaults, and it is **not** a servlet registration. You still need a scan or `@Bean` for the controller.

```java
public class AppInitializer implements WebApplicationInitializer {
    @Override
    public void onStartup(ServletContext sc) {
        AnnotationConfigWebApplicationContext ctx = new AnnotationConfigWebApplicationContext();
        ctx.register(WebConfig.class);
        ServletRegistration.Dynamic reg = sc.addServlet("app", new DispatcherServlet(ctx));
        reg.setLoadOnStartup(1);
        reg.addMapping("/");
    }
}

@Configuration
@ComponentScan("com.example.web")
class WebConfig { }

@RestController
class HelloController {
    @GetMapping("/hello")
    String hello() { return "ok"; }
}
```

**Listing 1.** Conceptual minimum without Boot: map `/`, scan controllers, let servlet defaults map `@GetMapping`. Registration: [[What is WebApplicationInitializer in Spring MVC]]. Front controller: [[What is Spring MVC DispatcherServlet]]. Java MVC import: [[What is the EnableWebMvc annotation]]. Controllers: [[How do you create a Spring MVC controller]]. Boot shortcut: [[How do you write a Spring Boot RESTful web service]].

```d2
direction: down
map: "URL → DispatcherServlet" {
  width: 260
  height: 40
  style.fill: "#e3f2fd"
}
wac: "WebApplicationContext\nHandlerMapping + Adapter" {
  width: 300
  height: 50
  style.fill: "#fff3e0"
}
c: "@Controller bean" {
  width: 200
  height: 40
  style.fill: "#e8f5e9"
}

map -> wac
wac -> c
```

**Fig. 1.** No mapping → the container never calls Spring. No strategy beans (and no defaults) → no dispatch. No `@Controller` in that context → `NoHandlerFoundException` / 404.

> [!warning] Controllers in the root context only
> Default `RequestMappingHandlerMapping` does **not** detect handlers in parent contexts. A service-only root plus an empty servlet context yields **404** for `@GetMapping`.

> [!warning] Custom `HandlerMapping` beans wipe defaults
> One extra `SimpleUrlHandlerMapping` `@Bean` **replaces** `RequestMappingHandlerMapping`. Keep the annotated mapping bean or you lose `@RequestMapping`.

> [!warning] Boot: skip `@EnableWebMvc`
> `spring-boot-starter-webmvc` already registers the servlet and MVC infrastructure. `@EnableWebMvc` **turns off** Boot’s MVC auto-configuration (including static resources).

> [!tip] Interview answer
> **Map `DispatcherServlet`, give it a `WebApplicationContext`, put a `@Controller` in that context.** Strategy beans default if omitted. Boot: web starter + `@SpringBootApplication` + `@RestController`. `@EnableWebMvc` is infrastructure, not the HTTP entry point.
