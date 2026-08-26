<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Spring/Core/IoC #SRS

# Can a Spring controller be missing from the application context?

> [!abstract] Short answer
> **Yes — and then it is not a Spring MVC controller.** `@Controller` / `@RestController` only matter if the class is a **bean** in the **`DispatcherServlet` `WebApplicationContext`**. A class on the classpath with those annotations is **not** enough. Typical misses: **`@ComponentScan` does not cover the package**, controllers live only in the **root** context while mapping beans live in the **child** (`detectHandlerMethodsInAncestorContexts` defaults **false**), or you used **`@Service` instead of `@Controller`**. Result is **404**, not a startup error.

## Stereotype is not registration

`@Controller` is a `@Component` specialization: **scan or an explicit `@Bean`** creates the singleton. MVC *Declaration*: auto-detection needs `@ComponentScan` (or XML component-scan) on the **servlet** context. Boot’s `@SpringBootApplication` scans **that class’s package and below** — a controller in a **sibling** package is invisible.

`AbstractHandlerMethodMapping`: default **`detectHandlerMethodsInAncestorContexts = false`**. Only beans in the **same** context as the `HandlerMapping` (the servlet child) are candidates. Root-only controllers are beans you can inject, but **`RequestMappingHandlerMapping` will not register their methods**. Switch the flag **or** register controllers in servlet config (`getServletConfigClasses()`).

`RequestMappingHandlerMapping.isHandler` requires **type-level `@Controller`**. `@GetMapping` on a `@Component`/`@Service` bean is ignored.

```java
// RootConfig: @ComponentScan("com.example.service")  — no web
// WebConfig:  @ComponentScan("com.example.web")     — controllers here

@RestController
class HelloController {
    @GetMapping("/hello")
    String hello() { return "ok"; }
}
```

**Listing 1.** Conceptual split: scan web types into the servlet context. Creating controllers: [[How do you create a Spring MVC controller]]. Root vs child: [[What is the difference between DispatcherServlet and ContextLoaderListener]]. Setup: [[What minimal setup is required for Spring MVC to handle HTTP requests]]. Stereotype mix-up: [[What is the difference between Repository Component Controller and Service annotations]].

```d2
direction: down
cls: "@Controller class on disk" {
  width: 260
  height: 40
  style.fill: "#fff3e0"
}
scan: "ComponentScan / @Bean" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
wac: "DispatcherServlet WAC" {
  width: 240
  height: 40
  style.fill: "#e8f5e9"
}
map: "RequestMappingHandlerMapping" {
  width: 280
  height: 40
  style.fill: "#fce4ec"
}

cls -> scan
scan -> wac
wac -> map
```

**Fig. 1.** Annotation → bean in the **servlet** context → mapping. Skip a step and HTTP never reaches the method.

> [!warning] 404 is the usual symptom
> Missing handler beans do **not** fail context refresh. `DispatcherServlet` answers **no handler** (`NoHandlerFoundException` / Boot resource 404). Check `/actuator/mappings` (if Actuator is on) or DEBUG `RequestMappingHandlerMapping`.

> [!warning] `new HelloController()` is not MVC
> Instantiating the class yourself bypasses the container. No injection, no mapping registration.

> [!warning] Boot scan base package
> Moving `@SpringBootApplication` to `com.example.boot` while controllers sit in `com.example.api` without `@ComponentScan` / `@SpringBootApplication(scanBasePackages=…)` leaves them out.

> [!tip] Interview answer
> **Yes.** `@Controller` is only a stereotype. If it is not a bean in the **servlet** context, `RequestMappingHandlerMapping` never sees it (parent context is ignored by default). Wrong package scan and `@Service`+`@GetMapping` are the usual causes of a silent 404.
