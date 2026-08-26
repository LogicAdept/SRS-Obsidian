<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Spring/Boot #SRS

# What is the Spring MVC web layer?

> [!abstract] Short answer
> The **web layer** is the **HTTP / presentation** slice: **`DispatcherServlet`**, its **special beans** (`HandlerMapping`, `HandlerAdapter`, `ViewResolver`, `HandlerExceptionResolver`, locale/multipart/flash), and **`@Controller` / `@RestController` / `@ControllerAdvice`**. It maps requests, binds HTTP input, writes a **`View`** or a **message-converter** body, and should **call** `@Service` / `@Repository` — not contain persistence. Filters are **Servlet** infrastructure **around** that servlet. Boot’s **`@WebMvcTest`** (module **`spring-boot-webmvc-test`**) is the official **slice** of this layer: it does **not** scan regular `@Component` / `@Service` / `@Repository`.

## Front controller plus web-only beans

Spring MVC is a **front controller**: one **`DispatcherServlet`** runs a shared algorithm; **special beans** do mapping, invocation, views, and exceptions. Annotated controllers (`@Controller` since **2.5**, `@RestController` = `@Controller` + `@ResponseBody` since **4.0**) are the usual handlers. They do **not** need a base class.

Classic two-context apps put **services and `DataSource` in the root** `WebApplicationContext` and **controllers + MVC special beans in the servlet child**. Boot often uses **one** context, but the **types** are the same: web beans vs domain/persistence beans. Stereotype extras: [[What is the difference between Repository Component Controller and Service annotations]]. Mapping vs adapter: [[What is HandlerMapping in Spring MVC]], [[What is HandlerAdapter in Spring MVC]]. Pattern: [[What is the Front Controller pattern in Spring MVC]].

Servlet **filters** wrap the servlet (Security lives here). **`HandlerInterceptor`** is **inside** MVC, after the request has a handler. Difference: [[How do servlet filters interceptors and AOP differ in Spring]].

Boot testing: *“focus only on the web layer”* → **`@WebMvcTest`**. It auto-configures MVC + **MockMvc** (no real HTTP server) and scans **`@Controller`**, **`@ControllerAdvice`**, converters, filters, interceptors, **`WebMvcConfigurer`**, argument resolvers, … — **not** ordinary `@Component`. Collaborators: **`@MockitoBean`** or **`@Import`**. Full app + MockMvc: **`@SpringBootTest` + `@AutoConfigureMockMvc`**.

```java
@WebMvcTest(HelloController.class)
class HelloControllerTests {
    // MockMvc / MockMvcTester auto-configured; HelloService is not a bean unless mocked
}
```

**Listing 1.** Conceptual Boot **4** slice (`org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest`). Limit to one controller; mock the service.

```d2
direction: down
http: "HTTP" {
  width: 160
  height: 35
  style.fill: "#e3f2fd"
}
filt: "Servlet filters" {
  width: 200
  height: 40
  style.fill: "#fff3e0"
}
web: "Web layer\nDispatcherServlet +\n@Controller + special beans" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
svc: "@Service / @Repository\nnot the web layer" {
  width: 260
  height: 50
  style.fill: "#fce4ec"
}

http -> filt -> web -> svc
```

**Fig. 1.** The web layer ends at HTTP adapters and controllers. Domain and store types sit behind it. Context split: [[What is a WebApplicationContext in Spring MVC]].

> [!warning] `@GetMapping` on `@Service` is not the web layer
> **`RequestMappingHandlerMapping.isHandler`** requires type-level **`@Controller`**. The service is a bean; the method is **not** mapped. Silent **404**.

> [!warning] `@WebMvcTest` does not load `@Service`
> The controller’s constructor collaborator is **missing** unless you **`@MockitoBean`** / **`@Import`**. A `@Bean` `SecurityFilterChain` in a random `@Configuration` is also **skipped** unless imported. That is the slice working, not a broken test.

> [!warning] Controllers are still singletons
> Web-layer beans default to **one instance** for all requests. Request state does not belong in fields. Persistence in the controller couples HTTP to the store and skips exception translation on `@Repository`.

> [!tip] Interview answer
> **Spring MVC’s web layer is `DispatcherServlet` plus controllers and the MVC special beans that map, invoke, render, and translate exceptions.** Services and repositories sit behind it. Filters wrap the servlet; interceptors run inside MVC. Boot **`@WebMvcTest`** loads that slice and MockMvc, not the database.
