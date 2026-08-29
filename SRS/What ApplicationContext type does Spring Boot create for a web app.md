<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Embedded #Java/Spring/Core/IoC #SRS

# What ApplicationContext type does Spring Boot create for a web app?

> [!abstract] Short answer
> `SpringApplication` **deduces** a **`WebApplicationType`** from the classpath, then builds the matching context. **Spring MVC** present → **`AnnotationConfigServletWebServerApplicationContext`** (embedded servlet container). **MVC absent and WebFlux present** → **`AnnotationConfigReactiveWebServerApplicationContext`**. **Neither** → plain **`AnnotationConfigApplicationContext`** (no server). Override with **`setWebApplicationType`** or **`spring.main.web-application-type`**.

## Deduce, then construct

The **Web Environment** algorithm on `SpringApplication` is ordered:

1. **Spring MVC** on the classpath → servlet web context (starts Tomcat/Jetty/Undertow).
2. Else **Spring WebFlux** → reactive web context (Netty by default).
3. Else → **`AnnotationConfigApplicationContext`**.

Boot 4 packages: **`org.springframework.boot.web.server.servlet.context.AnnotationConfigServletWebServerApplicationContext`** (extends **`ServletWebServerApplicationContext`**, a **`WebApplicationContext`**) and **`org.springframework.boot.web.server.reactive.context.AnnotationConfigReactiveWebServerApplicationContext`**. Both accept `@Configuration` / `@Component` like Framework’s **`AnnotationConfigApplicationContext`**.

If **MVC and WebFlux** are both present (classic: `starter-web` plus `WebClient`), deduction still picks **MVC / `SERVLET`**. Force reactive with `WebApplicationType.REACTIVE`. Force no server with **`NONE`** ([[How do you create a non-web Spring Boot application]]). Full replacement: `setApplicationContextFactory(…)`.

```java
SpringApplication app = new SpringApplication(MyApplication.class);
app.setWebApplicationType(WebApplicationType.REACTIVE);
app.run(args);
```

**Listing 1.** Java override. Property form: `spring.main.web-application-type=servlet` | `reactive` | `none` (unset ⇒ auto-detect).

```d2
direction: down
cp: "Classpath" {
  width: 160
  height: 50
  style.fill: "#e3f2fd"
}
mvc: "Spring MVC?" {
  width: 140
  height: 50
  style.fill: "#fff3e0"
}
flux: "WebFlux only?" {
  width: 140
  height: 50
  style.fill: "#fff3e0"
}
servlet: "AnnotationConfigServlet\nWebServerApplicationContext" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
reactive: "AnnotationConfigReactive\nWebServerApplicationContext" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
plain: "AnnotationConfigApplicationContext" {
  width: 260
  height: 50
  style.fill: "#f3e5f5"
}

cp -> mvc
mvc -> servlet: yes
mvc -> flux: no
flux -> reactive: yes
flux -> plain: no
```

**Fig. 1.** Context type **is** the web-server decision. Changing Tomcat to Jetty still leaves the **servlet** context ([[How do you switch the embedded server from Tomcat to Jetty]]; [[Which embedded containers are supported by Spring Boot]]).

`server.port=-1` does **not** switch this type: it still builds a web `ApplicationContext` and only turns HTTP endpoints off.

> [!warning] Leftover `starter-web` still starts a servlet container
> A “batch” or “worker” POM that transitively keeps **`spring-boot-starter-web`** (or Spring MVC) is a **servlet** app: **`AnnotationConfigServletWebServerApplicationContext`** plus embedded Tomcat. `NONE` / `spring.main.web-application-type=none` is the override; excluding one auto-config class is not the documented way to change the context type.

> [!warning] WebFlux on an MVC classpath is still servlet
> Adding **`starter-webflux`** for **`WebClient`** does **not** switch to **`AnnotationConfigReactiveWebServerApplicationContext`**. Call **`setWebApplicationType(REACTIVE)`** (or the property) if the process should be a reactive server. Boot 4’s servlet/reactive context types live under **`web.server.*.context`**, not the older `web.servlet.context` package.

> [!tip] Interview answer
> For a web app Boot creates AnnotationConfigServletWebServerApplicationContext if Spring MVC is on the classpath, or AnnotationConfigReactiveWebServerApplicationContext if only WebFlux is. It picks that by WebApplicationType deduction, which you can override. A leftover starter-web on a worker still gets the servlet context and starts Tomcat.
