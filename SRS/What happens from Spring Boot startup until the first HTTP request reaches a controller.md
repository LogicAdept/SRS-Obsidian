<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot #Java/Spring/Framework/WebMvc #SRS

# What happens from Spring Boot startup until the first HTTP request reaches a controller?

> [!abstract] Short answer
> **`SpringApplication.run`** builds a **`ServletWebServerApplicationContext`**, loads auto-config, **refreshes** the context (beans + **`RequestMappingHandlerMapping.afterPropertiesSet`** register mappings), and **during that refresh** a **`ServletWebServerFactory`** starts **Tomcat**. **`DispatcherServletAutoConfiguration`** registers **`DispatcherServlet`** on **`/`** via **`DispatcherServletRegistrationBean`**. The port can accept TCP **before** runners finish. **`ApplicationReadyEvent`** (after **`ApplicationRunner` / `CommandLineRunner`**) is when Boot calls the app **ready to service requests**. The first HTTP then is filters → already-initialized **`DispatcherServlet`** → already-registered **`HandlerMethod`**. Embedded Boot **does not run** **`WebApplicationInitializer`**.

## Refresh starts the server; Ready is later

Boot *SpringApplication* event order:

1. **`ApplicationStartingEvent`**
2. **`ApplicationEnvironmentPreparedEvent`**
3. **`ApplicationContextInitializedEvent`** (initializers; no bean defs yet)
4. **`ApplicationPreparedEvent`** (defs loaded; **before** refresh)
5. Refresh: **`ContextRefreshedEvent`**, and **`WebServerInitializedEvent`** once the **`WebServer`** is up (**between** Prepared and Started)
6. **`ApplicationStartedEvent`** (context refreshed; **before** runners) + liveness **`CORRECT`**
7. Runners
8. **`ApplicationReadyEvent`** + readiness **`ACCEPTING_TRAFFIC`**

Web type: MVC on the classpath → **`AnnotationConfigServletWebServerApplicationContext`**. That context looks up one **`ServletWebServerFactory`** (usually Tomcat) and starts it **while the context initializes**. **`ServletContext`** is therefore **not** safe in **`@PostConstruct`**. Listen for **`ApplicationStartedEvent`** (or inject `ApplicationContext` and read `ServletContext` later).

MVC wiring: **`DispatcherServletAutoConfiguration`** (Boot **4**, `org.springframework.boot.webmvc.autoconfigure`) creates the servlet bean mapped to **`/`**. **`AbstractHandlerMethodMapping`**: **`afterPropertiesSet` → `initHandlerMethods`**. Detection uses **`BeanFactory.getType`** so mapping registration **need not instantiate** the controller; default **eager singletons** still create `@RestController` beans **during refresh**, not on first request.

Embedded containers **do not** invoke **`ServletContainerInitializer` / `WebApplicationInitializer`**. Register extra servlets as **`ServletContextInitializer` / `ServletRegistrationBean`**. First request path: [[How does the Spring MVC request lifecycle work]]. Servlet registration: [[How do you register a servlet in Spring]]. Front controller: [[What is Spring MVC DispatcherServlet]]. Missing bean: [[Can a Spring controller be missing from the application context]].

```java
@SpringBootApplication
public class MyApplication {
    public static void main(String[] args) {
        SpringApplication.run(MyApplication.class, args);
    }
}
```

**Listing 1.** Conceptual first-app entry. `@SpringBootApplication` = configuration + **`@EnableAutoConfiguration`** + **`@ComponentScan`**. The webmvc starter makes auto-config pick Tomcat + MVC.

```d2
direction: down
run: "SpringApplication.run" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
refresh: "Context refresh\nbeans + HandlerMapping" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
tomcat: "Tomcat listen :8080\nWebServerInitializedEvent" {
  width: 300
  height: 50
  style.fill: "#ffe0b2"
}
started: "ApplicationStartedEvent\nthen runners" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
ready: "ApplicationReadyEvent" {
  width: 240
  height: 40
  style.fill: "#c8e6c9"
}
http: "First HTTP\nDispatcherServlet → controller" {
  width: 300
  height: 50
  style.fill: "#f3e5f5"
}

run -> refresh -> tomcat -> started -> ready -> http
```

**Fig. 1.** The socket can be open at **`WebServerInitializedEvent`**, **before** Ready. Kubernetes should wait for **readiness**, not only “port 8080 is bound.”

> [!warning] The port is not the same as Ready
> **`WebServerInitializedEvent`** fires **during** refresh. **`CommandLineRunner`** can still be running while Tomcat already accepts connections. **`ApplicationReadyEvent`** is the Boot “ready to service requests” signal. Liveness is **earlier** (context refreshed).

> [!warning] `@PostConstruct` must not assume `ServletContext`
> Server startup is **inside** context initialization. Inject **`ApplicationContext`** and resolve `ServletContext` later, or listen for **`ApplicationStartedEvent`**.

> [!warning] Embedded Boot ignores `WebApplicationInitializer`
> A class that only implements that SPI **never runs** in `java -jar`. Use **`ServletRegistrationBean`** / **`ServletContextInitializer`**, or **`SpringBootServletInitializer`** for a **WAR**. See [[What is WebApplicationInitializer in Spring MVC]].

> [!warning] First request does not scan `@RequestMapping`
> Mappings are registered when **`RequestMappingHandlerMapping`** initializes. A 404 on the first call is a **missing/unscanned bean** or wrong mapping, not “warm-up.” `@Lazy` can delay **instantiation**; it does not wait until the first HTTP to **discover** methods.

> [!tip] Interview answer
> **`SpringApplication.run` refreshes a servlet web context, auto-config registers `DispatcherServlet` on `/`, and Tomcat starts during that refresh.** Handler mappings are built then. **`ApplicationReadyEvent` is after runners.** The first request is ordinary MVC dispatch on already-created (usually singleton) controllers. Embedded Boot does not run `WebApplicationInitializer`.
