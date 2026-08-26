<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Spring/Framework/WebFlux #SRS

# Can you use Spring MVC and WebFlux in the same application?

> [!abstract] Short answer
> **Not as two HTTP stacks at once.** Spring Boot auto-configures **one** web application type. If both `spring-boot-starter-web` and `spring-boot-starter-webflux` are on the classpath, **MVC wins** so you can still use reactive **`WebClient`**. Force WebFlux with `SpringApplication.setWebApplicationType(WebApplicationType.REACTIVE)` or `spring.main.web-application-type=reactive`.

## One server model per Boot app

Spring Boot *Reactive Web Applications*: adding **both** web starters results in **Spring MVC**, not WebFlux. That is intentional — developers often add `spring-boot-starter-webflux` only for `WebClient` inside an MVC app.

`WebApplicationType` detection: servlet MVC context if Spring MVC is present; reactive context if only WebFlux is present. Override with `setWebApplicationType` or the `spring.main.web-application-type` property (also used in tests).

Spring MVC needs the **Servlet** API and blocking I/O (`DispatcherServlet`). WebFlux does **not** require Servlet; Boot’s WebFlux starter **defaults to Netty**. Tomcat and Jetty can host **either** stack, but **differently**: MVC uses blocking Servlet I/O; WebFlux uses non-blocking Servlet I/O behind an adapter — the Servlet API is not for direct use in WebFlux.

```d2
direction: down
cp: "Classpath:\nstarter-web + starter-webflux" {
  width: 320
  height: 70
  style.fill: "#fff3e0"
}
boot: "Boot chooses\nWebApplicationType.SERVLET" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
mvc: "DispatcherServlet\n(MVC)" {
  width: 220
  height: 60
  style.fill: "#e8f5e9"
}
wc: "WebClient still usable\n(HTTP client only)" {
  width: 260
  height: 70
  style.fill: "#fce4ec"
}

cp -> boot -> mvc
boot -> wc
```

**Fig. 1.** Both starters do not start MVC and a Netty WebFlux server together. Client vs server: [[What is the difference between RestTemplate WebClient and RestClient]].

```java
SpringApplication app = new SpringApplication(MyApp.class);
app.setWebApplicationType(WebApplicationType.REACTIVE);
app.run(args);
```

**Listing 1.** Conceptual override from Spring Boot reference when both stacks are on the classpath and you want WebFlux.

Programming-model contrast: [[What is the difference between Spring MVC and Spring WebFlux]]. Threading/virtual threads is a different choice — [[When should you use WebFlux versus Spring MVC versus virtual threads]].

> [!warning] Mixing blocking and non-blocking I/O in one context
> Spring Framework WebFlux overview: do **not** map Servlet filters or drive the Servlet API in a WebFlux app. Mixing blocking and non-blocking I/O in the same context causes runtime issues.

> [!warning] MVC does not run on Netty
> A Servlet `DispatcherServlet` app is not a Netty WebFlux server. “MVC on Netty” is not a supported Boot arrangement.

> [!warning] `@EnableWebFlux` takes over
> If you stay on WebFlux auto-config, add `WebFluxConfigurer` **without** `@EnableWebFlux`. `@EnableWebFlux` means you take complete control of WebFlux setup.

> [!tip] Interview answer
> **Boot picks one web type.** Both starters → MVC so `WebClient` still works. You do not run `DispatcherServlet` and a WebFlux Netty server as dual front controllers. Override `web-application-type` if you really want reactive when MVC is also on the classpath.
